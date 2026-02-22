import os
import secrets
import smtplib
from email.mime.text import MIMEText

def generate_otp(length=6):
    return "".join(str(secrets.randbelow(10)) for _ in range(length))

def otp_sender(receiver_email: str) -> str:
    sender_email = os.getenv("SMTP_USER") or os.getenv("SMTP_FROM")
    sender_password = os.getenv("SMTP_PASSWORD")
    if not sender_email or not sender_password:
        raise RuntimeError("SMTP_USER/SMTP_FROM and SMTP_PASSWORD must be set to send OTP emails")

    otp_code = generate_otp()
    smtp_server = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    message = MIMEText(f"Your OTP code is: {otp_code}")
    message["Subject"] = "OTP Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        if os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes", "y"}:
            server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
    return otp_code