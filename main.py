import sys
import time

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QDialog, QProgressBar, QLabel, QVBoxLayout

from email_manager import EmailManager
from email_composer import EmailComposer

from send_email import send_email_smtp

from login_dialog import LoginDialog

class MainWindow(QMainWindow):
    def __init__(self, email, password, smtp_host, smtp_port, use_ssl):
        super().__init__()
        self.sender_email = email
        self.app_password = password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.use_ssl = use_ssl

        self.setWindowTitle("Email Sender Version-1.3")
        self.resize(800, 600)

        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        self.email_manager = EmailManager()
        self.setCentralWidget(self.email_manager)
        self.email_manager.next_clicked.connect(self.show_composer)

    def show_composer(self, recipients):
        self.composer = EmailComposer(recipients)
        self.setCentralWidget(self.composer)
        self.composer.send_clicked.connect(self.send_email)
        self.composer.back_clicked.connect(self.show_manager)

    def show_manager(self):
        # Always create a new EmailManager widget
        self.email_manager = EmailManager()
        self.email_manager.next_clicked.connect(self.show_composer)
        self.setCentralWidget(self.email_manager)


    def show_about(self):
        QMessageBox.about(self,
                            "About Email Sender App",
                            "<b>Email Sender App v1.3</b><br>"
                            "Developed by <b>Bowen Zhou</b>.<br><br>"
                            "This app allows you to select multiple recipients and send email to all of them.<br>"
                            "Data will be saved at: <b>C:\\Users\\&lt;YourUsername&gt;\\Documents\\EmailSenderApp</b><br>"
                            "If recipients are more than 100, it will be automatically split into multiple 100 recipients.<br><br>"
                            "If you want to send email to more than 100 recipients at a time <b>INDIVIDUALLY</b>, it is normal for the App to freeze for a second.<br><br>"
                            "<b>EmailSender</b> will automatically split recipients into batches (multiple groups) and send it.<br>"
                            "Each batch = 100 recipients with <b>10s</b> break between each batch.<br>"
                            "App will freeze before all of emails have been sent.<br>"
                            )


    # Safer SMTP server handling
    def send_email(self, subject, body_html, recipients_string, image_paths=None):
        recipients = [email.strip() for email in recipients_string.split(",")]
        batch_size = 100
        delay_seconds = 10

        total_recipients = len(recipients)

        send_individually = self.composer.individual_checkbox.isChecked()

        for i in range(0, len(recipients), batch_size):
            batch = recipients[i:i + batch_size]

            if send_individually:
                for recipient in batch:
                    try:
                        send_email_smtp(
                            self.smtp_host,
                            self.smtp_port,
                            self.use_ssl,
                            self.sender_email,
                            self.app_password,
                            [recipient],
                            subject,
                            body_html,
                            image_paths if image_paths else None
                        )
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to send to {recipient}: \n{e}")
                        return
            else:
                try:
                    send_email_smtp(
                        self.smtp_host,
                        self.smtp_port,
                        self.use_ssl,
                        self.sender_email,
                        self.app_password,
                        batch,
                        subject,
                        body_html,
                        image_paths if image_paths else None
                    )
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to send batch: \n{e}")
                    return
            if i + batch_size < total_recipients:
                time.sleep(delay_seconds)

        QMessageBox.information(self, "Sent", "All emails have been sent.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_dialog = LoginDialog()
    if login_dialog.exec() != QDialog.DialogCode.Accepted:
        sys.exit(0)
    email, password, smtp_host, smtp_port, use_ssl = login_dialog.get_credentials()
    win = MainWindow(email, password, smtp_host, smtp_port, use_ssl)
    win.show()
    sys.exit(app.exec())