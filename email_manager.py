from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QHBoxLayout, QLineEdit, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
import os
import json

from add_dialog import AddDialog

save_dir = os.path.join(os.path.expanduser("~"), "Documents", "EmailSenderApp")
os.makedirs(save_dir, exist_ok=True)
EMAILS_FILE = os.path.join(save_dir, "emails.json")

#EMAILS_FILE = "emails.json"

class EmailManager(QWidget):
    next_clicked = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Emails")
        #self.emails = ["jingliu309@gmail.com", "yongzhou2022@gmail.com", "owenzh516@gmail.com", "mannarabella16@gmail.com"]

        # Load with names and emails
        self.emails = self.load_emails()

        # Layout
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Select", "Name", "Email Address"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Add initial emails
        self.refresh_table()

        # Controls
        hlayout = QHBoxLayout()

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_email)
        hlayout.addWidget(self.add_btn)

        self.del_btn = QPushButton("Delete Selected")
        self.del_btn.clicked.connect(self.delete_selected)
        hlayout.addWidget(self.del_btn)

        self.check_all_btn = QPushButton("Check All")
        self.check_all_btn.clicked.connect(self.check_all)
        hlayout.addWidget(self.check_all_btn)

        self.uncheck_all_btn = QPushButton("Uncheck All")
        self.uncheck_all_btn.clicked.connect(self.uncheck_all)
        hlayout.addWidget(self.uncheck_all_btn)
        layout.addLayout(hlayout)

        # Next Button
        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.on_next)
        layout.addWidget(self.next_btn)

    def refresh_table(self):
        self.table.setRowCount(0)
        for email_data in self.emails:
            row = self.table.rowCount()
            self.table.insertRow(row)

            item = QTableWidgetItem()
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row, 0, item)
            self.table.setItem(row, 1, QTableWidgetItem(email_data["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(email_data["email"]))

    def add_email(self):
        dialog = AddDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, email = dialog.get_input_data()
            if name and email:
                if any(email == e["email"] for e in self.emails):
                    QMessageBox.warning(self, "Duplicate", "Email Already Exists")
                    return
                self.emails.append({"name": name, "email": email})
                self.save_emails()
                self.refresh_table()
            else:
                QMessageBox.warning(self, "Error", "Fill out both name and email")


    def delete_selected(self):
        rows_to_delete = []
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item.checkState() == Qt.CheckState.Checked:
                rows_to_delete.append(i)

        for i in reversed(rows_to_delete):
            del self.emails[i]
        self.save_emails()
        self.refresh_table()

    def check_all(self):
        for i in range(self.table.rowCount()):
            self.table.item(i, 0).setCheckState(Qt.CheckState.Checked)

    def on_next(self):
        selected = []
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(self.emails[i]["email"])

        if not selected:
            QMessageBox.warning(self, "No Recipients", "Select at least one recipient.")
            return
        self.next_clicked.emit(selected)

    def uncheck_all(self):
        for i in range(self.table.rowCount()):
            self.table.item(i, 0).setCheckState(Qt.CheckState.Unchecked)


    def load_emails(self):
        if os.path.exists(EMAILS_FILE):
            try:
                with open(EMAILS_FILE, "r") as f:
                    data = json.load(f)
                    return [{"name": email["name"], "email": email["email"]} for email in data]
            except Exception as e:
                print(f"Can't load emails file: {e}")
                return []
        return []

    def save_emails(self):
        try:
            with open(EMAILS_FILE, "w") as f:
                json.dump(self.emails, f)
        except Exception as e:
            print(f"Can't save emails file: {e}")