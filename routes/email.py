import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app


def send_otp_email(email, otp):
    mail_config = current_app.config
    sender = mail_config.get('MAIL_USERNAME', '').strip()
    password = mail_config.get('MAIL_PASSWORD', '')
    server_name = mail_config.get('MAIL_SERVER', '').strip()
    port = int(mail_config.get('MAIL_PORT', 587))

    if not sender or not password:
        raise RuntimeError('Mail credentials are not configured.')

    if not server_name:
        raise RuntimeError('Mail server is not configured.')

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = email
    message['Subject'] = 'ProjectAI Password Reset OTP'
    message.attach(MIMEText(
        f'''Hello,

Your ProjectAI password reset OTP is:

{otp}

This OTP is valid for 10 minutes.

If you did not request this password reset, you can ignore this email.

ProjectAI
Smart Project Monitoring
''',
        'plain',
    ))

    if port == 465:
        smtp_connection = smtplib.SMTP_SSL(server_name, port, timeout=15)
    else:
        smtp_connection = smtplib.SMTP(server_name, port, timeout=15)

    with smtp_connection as server:
        if port != 465:
            server.starttls()
        server.login(sender, password)
        server.send_message(message)