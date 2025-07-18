from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QMessageBox, QLineEdit, QFileDialog, QCheckBox
)
from PyQt6.QtCore import pyqtSignal
import os

class EmailComposer(QWidget):
    send_clicked = pyqtSignal(str, str, str, list)
    back_clicked = pyqtSignal()

    def __init__(self, recipients):
        super().__init__()
        self.setWindowTitle("Compose Email")
        self.recipients = recipients
        self.image_paths = []

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Recipients Lable
        self.recipient_label = QLabel("To: " + ", ".join(recipients))
        layout.addWidget(self.recipient_label)

        # Subject Edit
        self.subject_edit = QLineEdit(self)
        self.subject_edit.setPlaceholderText("Subject")
        layout.addWidget(self.subject_edit)

        # Body Text
        self.body_edit = QTextEdit()
        self.body_edit.setPlaceholderText("Compose your email...")
        layout.addWidget(self.body_edit)

        # Image
        img_btn_layout = QHBoxLayout()
        self.insert_img_btn = QPushButton("Insert Image")
        self.insert_img_btn.clicked.connect(self.insert_image)
        img_btn_layout.addWidget(self.insert_img_btn)
        layout.addLayout(img_btn_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_email)
        btn_layout.addWidget(self.send_btn)
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.back_clicked)
        btn_layout.addWidget(self.back_btn)
        layout.addLayout(btn_layout)

        self.individual_checkbox = QCheckBox("Send Individually")
        self.individual_checkbox.setChecked(False)
        layout.addWidget(self.individual_checkbox)

    def send_email(self):
        subject = self.subject_edit.text().strip()
        body_html = self.body_edit.toHtml().strip()
        if not subject or not body_html:
            QMessageBox.critical(self, "Error", "Please enter both subject and body.")
            return

        self.send_clicked.emit(subject, body_html, ", ".join(self.recipients), self.image_paths)

    def insert_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp)")
        if not file_path or not os.path.isfile(file_path):
            QMessageBox.warning(self, "Error", "Invalid image file selected.")
            return
        self.image_paths.append(file_path)
        img_cid = f"img{len(self.image_paths) - 1}"
        # Insert HTML with cid
        self.body_edit.insertHtml(f'<img src="cid:{img_cid}"><br>')


'''
    def handle_back(self):
        print("DEBUG: Back button clicked")
        self.back_clicked.emit()
'''