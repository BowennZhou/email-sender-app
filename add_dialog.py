from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFormLayout, QMessageBox
)

class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Client")
        self.setMinimumSize(400, 200)

        layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()

        self.form_layout.addRow("Name: ", self.name_input)
        self.form_layout.addRow("Email Address: ", self.email_input)

        layout.addLayout(self.form_layout)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.add_button)
        layout.addWidget(self.cancel_button)

    def get_input_data(self):
        # Need to use .text() because strip() would crash
        name = self.name_input.text()
        email = self.email_input.text()

        if not name or not email:
            QMessageBox.warning(self, "Fill out both NAME and EMAIL")
            return None, None

        return name, email