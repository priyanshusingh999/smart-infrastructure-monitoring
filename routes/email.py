import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from config import Config

def send_otp_email(email, otp):
    sender = Config.MAIL_USERNAME
    password = Config.MAIL_PASSWORD
    port = Config.MAIL_PORT

    message = MIMEMultipart()

    message["From"] = sender
    message["To"] = email
    message["Subject"] = "ProjectAI Password Reset OTP"

    body = f"""
Hello,

Your ProjectAI password reset OTP is:

{otp}

This OTP is valid for 10 minutes.

If you did not request a password reset,
you can ignore this email.

ProjectAI
Smart Project Monitoring
"""

    message.attach(
        MIMEText(body, "plain")
    )

    with smtplib.SMTP(
        Config.MAIL_SERVER,
        Config.MAIL_PORT
    ) as server:

        server.starttls()

        server.login(
            sender,
            password
        )

        server.send_message(message)