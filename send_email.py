import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

def send_email_smtp(smtp_host, smtp_port, use_ssl, sender, password, recipients, subject, body_html, image_paths=None):
    msg_root = MIMEMultipart('related')
    msg_root['From'] = sender
    msg_root['To'] = ', '.join(recipients)
    msg_root['Subject'] = subject

    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)
    msg_alternative.attach(MIMEText(body_html, 'html'))

    # Attach images as inline
    if image_paths:
        for idx, img_path in enumerate(image_paths):
            if not os.path.isfile(img_path):
                continue
            with open(img_path, 'rb') as f:
                mime_img = MIMEImage(f.read())
                img_cid = f"img{idx}"
                mime_img.add_header('Content-ID', f'<{img_cid}>')
                mime_img.add_header('Content-Disposition', 'inline', filename=os.path.basename(img_path))
                msg_root.attach(mime_img)

    if use_ssl:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, msg_root.as_string())
    else:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipients, msg_root.as_string())
