# safekey_ui.py
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QFileDialog, QLabel, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt, QTimer
import sys
import os
from pathlib import Path
import cloak_manager as sk  # your existing script in same folder

class SafeKeyUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SafeKey — Assign files to USB key")
        self.setMinimumSize(800, 420)
        layout = QHBoxLayout()
        left = QVBoxLayout()
        left.addWidget(QLabel("<b>Detected USB Keys</b>"))
        self.usb_list = QListWidget()
        left.addWidget(self.usb_list)
        btn_refresh = QPushButton("Refresh USBs")
        btn_refresh.clicked.connect(self.refresh_tokens)
        left.addWidget(btn_refresh)
        btn_provision = QPushButton("Provision USB (write token)")
        btn_provision.clicked.connect(self.provision_usb_dialog)
        left.addWidget(btn_provision)
        layout.addLayout(left, 1)

        center = QVBoxLayout()
        center.addWidget(QLabel("<b>Selected items to assign</b>"))
        self.items_list = QListWidget()
        center.addWidget(self.items_list)
        h = QHBoxLayout()
        btn_add_files = QPushButton("Add Files")
        btn_add_files.clicked.connect(self.add_files)
        btn_add_folder = QPushButton("Add Folder")
        btn_add_folder.clicked.connect(self.add_folder)
        h.addWidget(btn_add_files); h.addWidget(btn_add_folder)
        center.addLayout(h)
        btn_remove = QPushButton("Remove Selected Item")
        btn_remove.clicked.connect(self.remove_selected_item)
        center.addWidget(btn_remove)
        layout.addLayout(center, 2)

        right = QVBoxLayout()
        right.addWidget(QLabel("<b>Actions</b>"))
        btn_assign = QPushButton("Assign selected → chosen USB")
        btn_assign.clicked.connect(self.assign_selected_to_usb)
        right.addWidget(btn_assign)
        right.addSpacing(10)
        btn_reveal = QPushButton("Reveal files for chosen USB")
        btn_reveal.clicked.connect(self.reveal_for_chosen_usb)
        right.addWidget(btn_reveal)
        right.addStretch(1)
        layout.addLayout(right, 1)

        self.setLayout(layout)
        self.refresh_tokens()
        # refresh tokens periodically (in case user plugs/unplugs)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_tokens)
        self.timer.start(2500)

    def refresh_tokens(self):
        self.usb_list.clear()
        tokens = sk.detect_mounted_tokens()  # {token: mount}
        for tok, mount in tokens.items():
            display = f"{tok}  —  {mount}"
            self.usb_list.addItem(display)

    def provision_usb_dialog(self):
        d = QFileDialog.getExistingDirectory(self, "Select USB mountpoint to provision")
        if not d:
            return
        try:
            sk.provision(d)
            QMessageBox.information(self, "Provisioned", f"USB provisioned at:\n{d}")
            self.refresh_tokens()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Provision failed:\n{e}")

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Choose files to assign")
        for f in files:
            self.items_list.addItem(f)

    def add_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Choose folder to assign")
        if d:
            self.items_list.addItem(d)

    def remove_selected_item(self):
        for it in self.items_list.selectedItems():
            self.items_list.takeItem(self.items_list.row(it))

    def selected_token(self):
        it = self.usb_list.currentItem()
        if not it:
            return None
        text = it.text()
        tok = text.split("  —  ")[0].strip()
        return tok

    def ask_password(self, prompt="Enter SafeKey master password"):
        pwd, ok = QInputDialog.getText(self, "Master password", prompt, echo=QInputDialog.EchoMode.Password)
        if not ok or pwd == "":
            return None
        return pwd

    def assign_selected_to_usb(self):
        token = self.selected_token()
        if not token:
            QMessageBox.warning(self, "No USB selected", "Select a USB key from the left list first.")
            return
        if self.items_list.count() == 0:
            QMessageBox.warning(self, "No items", "Add files/folders to assign.")
            return
        pwd = self.ask_password()
        if pwd is None:
            return

        # perform assignment — reuse logic from safekey_manager but use chosen token
        meta = sk.read_meta()
        if token not in meta:
            QMessageBox.critical(self, "Unknown token", "Token not found in local meta. Re-provision the USB.")
            return
        salt = sk.base64.b64decode(meta[token]["salt"])
        key = sk.derive_key(pwd, token.encode(), salt)

        failed = []
        succeeded = 0
        for i in range(self.items_list.count()):
            path = self.items_list.item(i).text()
            p = Path(path)
            if p.is_file():
                try:
                    data = p.read_bytes()
                    ct = sk.encrypt_blob(key, data)
                    sk._save_vault_item(token, str(p), ct)  # reuse helper from safekey_manager
                    sk.secure_delete_file(p)
                    succeeded += 1
                except Exception as e:
                    failed.append(f"{path}: {e}")
            elif p.is_dir():
                # walk directory
                for root, dirs, files in os.walk(p):
                    for fname in files:
                        fpath = Path(root) / fname
                        try:
                            data = fpath.read_bytes()
                            ct = sk.encrypt_blob(key, data)
                            sk._save_vault_item(token, str(fpath), ct)
                            sk.secure_delete_file(fpath)
                            succeeded += 1
                        except Exception as e:
                            failed.append(f"{fpath}: {e}")
            else:
                failed.append(f"{path}: not found")

        sk.write_meta(meta)  # save any metadata changes
        msg = f"Assigned {succeeded} items to USB."
        if failed:
            msg += "\n\nSome errors:\n" + "\n".join(failed[:8])
        QMessageBox.information(self, "Done", msg)
        self.items_list.clear()

    def reveal_for_chosen_usb(self):
        token = self.selected_token()
        if not token:
            QMessageBox.warning(self, "No USB selected", "Select a USB key from the left list first.")
            return
        pwd = self.ask_password("Enter master password for reveal")
        if pwd is None:
            return
        # call safekey_manager reveal_for_token
        try:
            restored = sk.reveal_for_token(token, pwd)
            if restored:
                QMessageBox.information(self, "Reveal finished", f"Revealed {len(restored)} items (restored to original paths).")
            else:
                QMessageBox.information(self, "Reveal", "No items restored (maybe already present or decryption failed).")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Reveal failed:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SafeKeyUI()
    w.show()
    sys.exit(app.exec())
