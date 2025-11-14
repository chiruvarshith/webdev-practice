#!/usr/bin/env python3
"""
SafeKey manager prototype
Features:
- provision <mountpoint>
- assign <path>  (assign file or folder to first detected USB token)
- reveal <token> (reveal files for given token or detected USB)
- hide <token>   (hide/restores back to vault)
- poll           (runs poller to detect USB insert/remove and prompts reveal)
"""

import os, sys, json, time, uuid, secrets, shutil, tempfile
from pathlib import Path
import base64, getpass
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

def detect_mounted_tokens():
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

def secure_delete_file(path: Path):
    try:
        if not path.exists() or not path.is_file():
            return
        size = path.stat().st_size
        with open(path, "ba+", buffering=0) as f:
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
    tfile = p / ".safekey_token"
    tfile.write_bytes(token)
    meta = read_meta()
    meta[token.decode()] = {"salt": base64.b64encode(secrets.token_bytes(16)).decode(), "items": []}
    write_meta(meta)
    print("Provisioned USB at", mountpoint, "token:", token.decode())

def _save_vault_item(token_str: str, original_path: str, ciphertext: bytes):
    vault_name = secrets.token_hex(20)
    (VAULT_DIR / vault_name).write_bytes(ciphertext)
    meta = read_meta()
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
                rel = str(fpath.relative_to(p.parent))  # relative to parent, to restore exact path
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
        # if a directory with same name exists and is non-empty, avoid overwriting silently
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
        print("Usage: provision <mount> | assign <path> | reveal <token?> | hide <token?> | poll")
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
        if tokens and len(tokens)==1 and len(sys.argv)==2:
            tok,_ = next(iter(tokens.items()))
            pwd = getpass.getpass("Enter master password: ")
            reveal_for_token(tok, pwd)
        elif len(sys.argv)>=3:
            pwd = getpass.getpass("Enter master password: ")
            reveal_for_token(sys.argv[2], pwd)
        else:
            print("No token specified and no single USB detected.")
    elif cmd == "hide":
        tokens = detect_mounted_tokens()
        if tokens and len(tokens)==1 and len(sys.argv)==2:
            tok,_ = next(iter(tokens.items()))
            pwd = getpass.getpass("Enter master password: ")
            hide_for_token(tok, pwd)
        elif len(sys.argv)>=3:
            pwd = getpass.getpass("Enter master password: ")
            hide_for_token(sys.argv[2], pwd)
        else:
            print("No token specified and no single USB detected.")
    elif cmd == "poll":
        poll_loop()
    else:
        print("Unknown command")
