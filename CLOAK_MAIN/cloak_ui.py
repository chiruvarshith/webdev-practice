# cloak_ui.py (fixed: QLineEdit echo + QSize)
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QLabel, QMessageBox, QInputDialog, QLineEdit
)
from PySide6.QtCore import Qt, QTimer, QSize
import sys
from pathlib import Path
import os
import cloak_manager as sk

class SafeKeyUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cloak — Assign files to USB key")
        self.setMinimumSize(1000, 520)
        layout = QHBoxLayout()

        # Left: USB drives
        left = QVBoxLayout()
        left.addWidget(QLabel("<b>Connected USB Drives</b>"))
        self.usb_list = QListWidget()
        self.usb_list.setSelectionMode(QListWidget.SingleSelection)
        self.usb_list.itemSelectionChanged.connect(self.on_usb_selection_changed)
        left.addWidget(self.usb_list)
        btn_refresh = QPushButton("Refresh USBs")
        btn_refresh.clicked.connect(self.refresh_tokens)
        left.addWidget(btn_refresh)
        btn_provision = QPushButton("Provision Selected USB")
        btn_provision.clicked.connect(self.provision_usb_dialog)
        left.addWidget(btn_provision)
        # Selected drive display
        self.selected_label = QLabel("Selected: None")
        left.addWidget(self.selected_label)
        layout.addLayout(left, 1)

        # Center: items to assign
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

        # Right: actions
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

    # --- drive listing / selection helpers ---
    def refresh_tokens(self):
        """
        Populate usb_list with all removable drives.
        Each QListWidgetItem holds (token_or_None, mount) in Qt.UserRole.
        """
        self.usb_list.clear()
        try:
            drives = sk.list_all_usb_drives()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to list drives:\n{e}")
            return

        for mount, label, token in drives:
            if token:
                title = f"[PROVISIONED] {token}"
            else:
                title = f"[UNPROVISIONED] {label}"
            display = f"{title}\n{mount}"
            item = QListWidgetItem(display)
            item.setData(Qt.UserRole, (token, mount))
            # make item slightly taller so long paths wrap better
            item.setSizeHint(item.sizeHint() + QSize(0, 10))
            self.usb_list.addItem(item)

        self.selected_label.setText("Selected: None")

    def provision_usb_dialog(self):
        it = self.usb_list.currentItem()
        if not it:
            QMessageBox.warning(self, "No USB selected", "Select a USB drive from the left list to provision.")
            return
        token, mount = it.data(Qt.UserRole)
        if mount is None:
            QMessageBox.critical(self, "Error", "Selected item has no mount info.")
            return
        try:
            new_token = sk.provision(mount)
            QMessageBox.information(self, "Provisioned", f"USB provisioned at:\n{mount}\n\nToken: {new_token}")
            self.refresh_tokens()
        except Exception as e:
            QMessageBox.critical(self, "Provision failed", str(e))

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Choose files to assign")
        for f in files:
            self.items_list.addItem(f)

    def add_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Choose folder to assign")
        if d:
            self.items_list.addItem(d)

    def remove_selected_item(self):
        for it in list(self.items_list.selectedItems()):
            self.items_list.takeItem(self.items_list.row(it))

    def on_usb_selection_changed(self):
        it = self.usb_list.currentItem()
        if not it:
            self.selected_label.setText("Selected: None")
            return
        token, mount = it.data(Qt.UserRole)
        if token:
            self.selected_label.setText(f"Selected: {mount}  (provisioned)")
        else:
            self.selected_label.setText(f"Selected: {mount}  (not provisioned)")

    def ask_password(self, prompt="Enter Cloak master password"):
        # Use QLineEdit.EchoMode.Password to avoid AttributeError
        pwd, ok = QInputDialog.getText(self, "Master password", prompt, QLineEdit.EchoMode.Password)
        if not ok or pwd == "":
            return None
        return pwd

    # --- assign / reveal ---
    def assign_selected_to_usb(self):
        it = self.usb_list.currentItem()
        if not it:
            QMessageBox.warning(self, "No USB selected", "Select a USB drive from the left list first.")
            return
        token, mount = it.data(Qt.UserRole)
        if mount is None:
            QMessageBox.warning(self, "No USB mount", "Selected list item has no mountpoint.")
            return
        if self.items_list.count() == 0:
            QMessageBox.warning(self, "No items", "Add files/folders to assign.")
            return

        # If drive not provisioned, ask to provision now
        if token is None:
            res = QMessageBox.question(
                self, "USB not provisioned",
                f"The selected USB ({mount}) is not provisioned. Do you want to provision it now?",
                QMessageBox.Yes | QMessageBox.No
            )
            if res == QMessageBox.Yes:
                try:
                    token = sk.provision(mount)
                    self.refresh_tokens()
                    for i in range(self.usb_list.count()):
                        it2 = self.usb_list.item(i)
                        t2, m2 = it2.data(Qt.UserRole)
                        if m2 == mount:
                            self.usb_list.setCurrentItem(it2)
                            break
                except Exception as e:
                    QMessageBox.critical(self, "Provision failed", str(e))
                    return
            else:
                return

        pwd = self.ask_password()
        if pwd is None:
            return

        meta = sk.read_meta()
        if token not in meta:
            QMessageBox.critical(self, "Unknown token", "Token not found in local meta. Provision may have failed.")
            return
        try:
            salt = sk.base64.b64decode(meta[token]["salt"])
            key = sk.derive_key(pwd, token.encode(), salt)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to derive key: {e}")
            return

        failed = []
        succeeded = 0
        paths = [self.items_list.item(i).text() for i in range(self.items_list.count())]
        for path in paths:
            p = Path(path)
            if p.is_file():
                try:
                    data = p.read_bytes()
                    ct = sk.encrypt_blob(key, data)
                    sk._save_vault_item(token, str(p), ct)
                    sk.secure_delete_file(p)
                    succeeded += 1
                except Exception as e:
                    failed.append(f"{path}: {e}")
            elif p.is_dir():
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

        try:
            sk.write_meta(sk.read_meta())
        except Exception:
            pass

        msg = f"Assigned {succeeded} items to USB."
        if failed:
            msg += "\n\nSome errors:\n" + "\n".join(failed[:8])
        QMessageBox.information(self, "Done", msg)
        self.items_list.clear()
        self.refresh_tokens()

    def reveal_for_chosen_usb(self):
        it = self.usb_list.currentItem()
        if not it:
            QMessageBox.warning(self, "No USB selected", "Select a USB drive from the left list first.")
            return
        token, mount = it.data(Qt.UserRole)
        if token is None:
            QMessageBox.information(self, "Not provisioned", "This USB is not provisioned. Provision it first to reveal files.")
            return
        pwd = self.ask_password("Enter master password for reveal")
        if pwd is None:
            return
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
   