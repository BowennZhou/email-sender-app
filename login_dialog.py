from operator import truediv

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QCheckBox, QBoxLayout
)

import os
import json
import smtplib

save_dir = os.path.join(os.path.expanduser("~"), "Documents", "EmailSenderApp")
os.makedirs(save_dir, exist_ok=True)
CREDENTIAL_FILE = os.path.join(save_dir, "login.json")

#CREDENTIAL_FILE = "login.json"

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login to Mail Server")
        self.setMinimumSize(400, 300)
        layout = (QVBoxLayout(self))

        layout.addWidget(QLabel("Email Address:"))
        self.email_edit = QLineEdit()
        layout.addWidget(self.email_edit)

        layout.addWidget(QLabel("Password:"))
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.pwd_edit)

        layout.addWidget(QLabel("SMTP Server:"))
        self.smtp_edit = QLineEdit()
        self.smtp_edit.setPlaceholderText("e.g. smtp.gmail.com")
        layout.addWidget(self.smtp_edit)

        layout.addWidget(QLabel("Port:"))
        self.port_edit = QLineEdit()
        self.port_edit.setPlaceholderText("465(SSL) or 587(TSL)")
        layout.addWidget(self.port_edit)

        self.ssl_checkbox = QCheckBox("Use SSL (Uncheck for TLS/STARTTLS)")
        self.ssl_checkbox.setChecked(True)
        layout.addWidget(self.ssl_checkbox)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.try_accept)
        btn_layout.addWidget(self.login_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_credentials)
        btn_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.load_credentials()


    def load_credentials(self):
        if os.path.exists(CREDENTIAL_FILE):
            try:
                with open(CREDENTIAL_FILE, "r") as f:
                    data = json.load(f)
                self.email_edit.setText(data.get("email", ""))
                self.pwd_edit.setText(data.get("password", ""))
                self.smtp_edit.setText(data.get("smtp", ""))
                self.port_edit.setText(str(data.get("port", "")))
                self.ssl_checkbox.setChecked(data.get("ssl", True))
            except Exception as e:
                QMessageBox.warning(self, "Error", "Could not load local credentials: \n{e}")

    def save_credentials(self):
        data = {
            "email": self.email_edit.text().strip(),
            "password": self.pwd_edit.text().strip(),
            "smtp": self.smtp_edit.text().strip(),
            "port": int(self.port_edit.text().strip()),
            "ssl": self.ssl_checkbox.isChecked(),
        }
        try:
            with open(CREDENTIAL_FILE, "w") as f:
                json.dump(data, f)
            QMessageBox.information(self, "Success", "Credentials saved")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save credentials: \n{e}")


    def try_accept(self):
        email = self.email_edit.text().strip()
        password = self.pwd_edit.text().strip()
        smtp = self.smtp_edit.text().strip()
        port = self.port_edit.text().strip()
        use_ssl = self.ssl_checkbox.isChecked()
        if not email or not password or not smtp or not port:
            QMessageBox.warning(self, "Error", "fill all fields")
            return
        try:
            port = int(port)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid port")
            return

        if not self.test_smtp_credentials(email, password, smtp, port, use_ssl):
            QMessageBox.warning(self, "Login Failed", "Invalid credentials")
            return

        QMessageBox.information(self, "Success", "Credentials are valid")
        self.accept()

    def get_credentials(self):
        return (
            self.email_edit.text().strip(),
            self.pwd_edit.text().strip(),
            self.smtp_edit.text().strip(),
            int(self.port_edit.text().strip()),
            self.ssl_checkbox.isChecked(),
        )

    def test_smtp_credentials(self, email, password, smtp_host, port, use_ssl):
        try:
            if use_ssl:
                with smtplib.SMTP_SSL(smtp_host, port, timeout = 10) as server:
                    server.login(email, password)
            else:
                with smtplib.SMTP(smtp_host, port, timeout = 10) as server:
                    server.ehlo()
                    server.starttls()
                    server.login(email, password)
            return True
        except Exception as e:
            print("SMTP Login Failed:", e)
            return False
