#!/usr/bin/env python3
"""
SafeKey / Cloak manager prototype (modified)
- Provides old detect_mounted_tokens() for backward compat
- Adds list_all_usb_drives() to list all connected removable drives, with token info
Other core behaviors unchanged (provision, assign, reveal, hide, poll)
"""

import os
import sys
import json
import time
import uuid
import secrets
import shutil
import tempfile
import platform
from pathlib import Path
import base64
import getpass
import psutil
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

APP_DIR = Path.home() / ".safekey"
VAULT_DIR = APP_DIR / "vault"
META_FILE = APP_DIR / "meta.json"

# --- util ---
def ensure_dirs():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    if not META_FILE.exists():
        META_FILE.write_text(json.dumps({}))

def read_meta():
    ensure_dirs()
    return json.loads(META_FILE.read_text())

def write_meta(m):
    META_FILE.write_text(json.dumps(m, indent=2))

def derive_key(password: str, token_bytes: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=200_000)
    return kdf.derive(password.encode() + token_bytes)

def encrypt_blob(key: bytes, plaintext: bytes) -> bytes:
    aes = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ct = aes.encrypt(nonce, plaintext, None)
    return nonce + ct

def decrypt_blob(key: bytes, blob: bytes) -> bytes:
    aes = AESGCM(key)
    nonce = blob[:12]
    ct = blob[12:]
    return aes.decrypt(nonce, ct, None)

# --- USB detection helpers ---
def detect_mounted_tokens():
    """
    Backward compatible: returns dict {token: mount}
    (same behavior as older code)
    """
    tokens = {}
    for part in psutil.disk_partitions(all=False):
        try:
            p = Path(part.mountpoint)
            tfile = p / ".safekey_token"
            if tfile.exists():
                tok = tfile.read_bytes().strip()
                tokens[tok.decode()] = str(p)
        except Exception:
            continue
    return tokens

def list_all_usb_drives():
    """
    Return list of tuples: (mountpoint, friendly_label, token_or_None)
    - Scans partitions and heuristically includes removable/USB-like mounts.
    - On mac/linux also scans /Volumes and /media to catch mounts psutil might miss.
    """
    drives = []
    sysname = platform.system()

    # Use psutil to enumerate partitions first
    for part in psutil.disk_partitions(all=False):
        try:
            mount = Path(part.mountpoint)
            # Heuristics for USB-like mounts
            is_usb_like = False
            if sysname == "Windows":
                # Exclude system drive (typically C:\). Accept other drives.
                system_drive = os.environ.get("SystemDrive", "C:\\")
                if not str(mount).lower().startswith(system_drive.lower()):
                    is_usb_like = True
            else:
                # macOS/linux: typical external mounts are under /Volumes or /media
                if str(mount).startswith("/Volumes") or str(mount).startswith("/media"):
                    is_usb_like = True
                # also accept mounts that look like removable (fallback)
                # skip root and common system mounts
                if str(mount) in ("/", "/home", "/boot", "/mnt"):
                    is_usb_like = is_usb_like and False

            # friendly label
            label = mount.name if mount.name else str(mount)

            # token presence
            token = None
            try:
                token_path = mount / ".safekey_token"
                if token_path.exists():
                    token = token_path.read_bytes().strip().decode()
            except Exception:
                token = None

            if is_usb_like:
                drives.append((str(mount), label, token))
        except Exception:
            continue

    # Fallback: on POSIX systems, ensure /Volumes and /media entries are included
    if sysname != "Windows":
        for base in ("/Volumes", "/media"):
            try:
                if not os.path.isdir(base):
                    continue
                for name in sorted(os.listdir(base)):
                    mp = Path(base) / name
                    if not mp.exists():
                        continue
                    # avoid duplicates
                    if any(Path(d[0]).samefile(mp) for d in drives if Path(d[0]).exists()):
                        continue
                    token = None
                    try:
                        tf = mp / ".safekey_token"
                        if tf.exists():
                            token = tf.read_bytes().strip().decode()
                    except Exception:
                        token = None
                    drives.append((str(mp), mp.name, token))
            except Exception:
                pass

    # Deduplicate by mountpoint, keep first occurrence
    seen = set()
    out = []
    for mount, label, token in drives:
        if mount not in seen:
            out.append((mount, label, token))
            seen.add(mount)
    return out

# --- secure delete ---
def secure_delete_file(path: Path):
    try:
        if not path.exists() or not path.is_file():
            return
        size = path.stat().st_size
        # overwrite once with zeros
        with open(path, "br+") as f:
            f.seek(0)
            f.write(b'\x00' * size)
            f.flush()
            os.fsync(f.fileno())
        path.unlink()
    except Exception:
        # fallback: normal delete
        try:
            path.unlink()
        except Exception:
            pass

# --- core operations ---
def provision(mountpoint: str):
    ensure_dirs()
    token = uuid.uuid4().hex.encode()
    p = Path(mountpoint)
    if not p.exists():
        raise FileNotFoundError(f"Mountpoint not found: {mountpoint}")
    tfile = p / ".safekey_token"
    tfile.write_bytes(token)
    meta = read_meta()
    meta[token.decode()] = {"salt": base64.b64encode(secrets.token_bytes(16)).decode(), "items": []}
    write_meta(meta)
    print("Provisioned USB at", mountpoint, "token:", token.decode())
    return token.decode()

def _save_vault_item(token_str: str, original_path: str, ciphertext: bytes):
    vault_name = secrets.token_hex(20)
    (VAULT_DIR / vault_name).write_bytes(ciphertext)
    meta = read_meta()
    if token_str not in meta:
        meta[token_str] = {"salt": base64.b64encode(secrets.token_bytes(16)).decode(), "items": []}
    meta[token_str]["items"].append({"vault": vault_name, "orig": original_path})
    write_meta(meta)

def assign_path(path_str: str, password: str):
    ensure_dirs()
    tokens = detect_mounted_tokens()
    if not tokens:
        print("No provisioned USB mounted. Insert a provisioned USB and try.")
        return
    # choose first token (can improve to ask user)
    token_str, mount = next(iter(tokens.items()))
    token_bytes = token_str.encode()
    meta = read_meta()
    if token_str not in meta:
        print("Token not registered in meta. Re-provision.")
        return
    salt = base64.b64decode(meta[token_str]["salt"])
    key = derive_key(password, token_bytes, salt)

    p = Path(path_str)
    if not p.exists():
        print("Path does not exist:", path_str); return

    if p.is_file():
        data = p.read_bytes()
        ct = encrypt_blob(key, data)
        _save_vault_item(token_str, str(p), ct)
        secure_delete_file(p)
        print("Assigned file to USB key and hidden:", p)
    else:
        # folder: recursively encrypt files inside, keep directory structure metadata
        for root, dirs, files in os.walk(p):
            for fname in files:
                fpath = Path(root) / fname
                data = fpath.read_bytes()
                ct = encrypt_blob(key, data)
                _save_vault_item(token_str, str(fpath), ct)
                secure_delete_file(fpath)
        print("Assigned folder (contents encrypted) to USB key:", p)

def reveal_for_token(token_str: str, password: str):
    ensure_dirs()
    meta = read_meta()
    if token_str not in meta:
        print("Unknown token")
        return
    salt = base64.b64decode(meta[token_str]["salt"])
    key = derive_key(password, token_str.encode(), salt)
    restored = []
    for item in list(meta[token_str]["items"]):
        vault_file = VAULT_DIR / item["vault"]
        if not vault_file.exists():
            print("Missing vault blob:", item["vault"]); continue
        try:
            plaintext = decrypt_blob(key, vault_file.read_bytes())
        except Exception:
            print("Decryption failed for item, maybe wrong password or token mismatch:", item["orig"])
            continue
        orig_path = Path(item["orig"])
        orig_path.parent.mkdir(parents=True, exist_ok=True)
        if orig_path.exists():
            print("Warning: original path exists already. Overwriting:", orig_path)
        orig_path.write_bytes(plaintext)
        restored.append(str(orig_path))
    print("Revealed {} items for token {}".format(len(restored), token_str))
    return restored

def hide_for_token(token_str: str, password: str):
    """
    Re-scan meta for items and re-encrypt anything that currently exists on disk at orig path.
    (useful on USB removal to re-hide any revealed files)
    """
    ensure_dirs()
    meta = read_meta()
    if token_str not in meta:
        print("Unknown token"); return
    salt = base64.b64decode(meta[token_str]["salt"])
    key = derive_key(password, token_str.encode(), salt)
    for item in list(meta[token_str]["items"]):
        orig_path = Path(item["orig"])
        if orig_path.exists() and orig_path.is_file():
            data = orig_path.read_bytes()
            ct = encrypt_blob(key, data)
            (VAULT_DIR / item["vault"]).write_bytes(ct)
            secure_delete_file(orig_path)
            print("Re-hidden:", orig_path)
    print("Hide complete for token", token_str)

# --- poller (simple) ---
def poll_loop():
    ensure_dirs()
    print("SafeKey poller started. Press Ctrl-C to quit.")
    known = set()
    password = getpass.getpass("Enter SafeKey master password (same as used when assigning): ")
    while True:
        tokens = detect_mounted_tokens()  # returns {token: mountpoint}
        # new inserted tokens
        for tok, mount in tokens.items():
            if tok not in known:
                print(f"\n[USB inserted] token={tok} mount={mount}")
                # prompt user (simple)
                ans = input("Reveal hidden files for this USB? (y/n): ").strip().lower()
                if ans == "y":
                    reveal_for_token(tok, password)
                known.add(tok)
        # removed tokens -> hide
        removed = [k for k in list(known) if k not in tokens]
        for k in removed:
            print(f"\n[USB removed] token={k}")
            # attempt to re-hide any restored files
            hide_for_token(k, password)
            known.remove(k)
        time.sleep(2)

# --- CLI entry ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: provision <mount> | assign <path> | reveal <token?> | hide <token?> | poll | listdrives")
        sys.exit(1)
    cmd = sys.argv[1]
    ensure_dirs()
    if cmd == "provision":
        if len(sys.argv) < 3:
            print("usage: provision /path/to/mount"); sys.exit(1)
        provision(sys.argv[2])
    elif cmd == "assign":
        if len(sys.argv) < 3:
            print("usage: assign /path/to/file_or_folder"); sys.exit(1)
        pwd = getpass.getpass("Enter master password: ")
        assign_path(sys.argv[2], pwd)
    elif cmd == "reveal":
        tokens = detect_mounted_tokens()
        if tokens and len(tokens) == 1 and len(sys.argv) == 2:
            tok, _ = next(iter(tokens.items()))
            pwd = getpass.getpass("Enter master password: ")
            reveal_for_token(tok, pwd)
        elif len(sys.argv) >= 3:
            pwd = getpass.getpass("Enter master password: ")
            reveal_for_token(sys.argv[2], pwd)
        else:
            print("No token specified and no single USB detected.")
    elif cmd == "hide":
        tokens = detect_mounted_tokens()
        if tokens and len(tokens) == 1 and len(sys.argv) == 2:
            tok, _ = next(iter(tokens.items()))
            pwd = getpass.getpass("Enter master password: ")
            hide_for_token(tok, pwd)
        elif len(sys.argv) >= 3:
            pwd = getpass.getpass("Enter master password: ")
            hide_for_token(sys.argv[2], pwd)
        else:
            print("No token specified and no single USB detected.")
    elif cmd == "poll":
        poll_loop()
    elif cmd == "listdrives":
        # debug helper to print drives
        print("All removable drives found:")
        for mount, label, token in list_all_usb_drives():
            print(f"{mount}  (label={label})  token={'YES' if token else 'NO'}")
    else:
        print("Unknown command")
