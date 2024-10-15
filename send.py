import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")

def send_email(subject, receiver_mail, name, due_date, invoice_no, amount):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Keep moving forward - Kliz", sender_email))
    msg["To"] = receiver_mail

    msg.set_content(
        f"""
        Hi {name},
        I hope you are well.
        This is a reminder that {amount} PHP is due for Invoice {invoice_no} on {due_date}.
        Please confirm if everything is on track for payment.

        Best Regards,
        Kliz
        """
    )

    msg.add_alternative(
        f"""
    <html>
        <body>
            <p>Hi {name},</p>
            <p>I hope you are well.</p>
            <p>This is a reminder that <strong>{amount} PHP</strong> is due for Invoice {invoice_no} on <strong>{due_date}</strong>.</p>
            <p>Please confirm if everything is on track for payment.</p>
            <p>Best Regards,<br>Kliz</p>
        </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        try:
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_mail, msg.as_string())
            print("Email sent successfully!")
        except smtplib.SMTPAuthenticationError as e:
            print(f"Authentication failed: {e}")

if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="John Doe",
        receiver_mail="johnmillares12@gmail.com",
        due_date="11, October 2024",
        invoice_no="12345",
        amount="7",
    )
