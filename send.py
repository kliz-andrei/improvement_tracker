import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, sender_email, password, receiver_mail, message):
    """Send an HTML email."""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_mail
    msg['Subject'] = subject

    # Attach the HTML message
    msg.attach(MIMEText(message, 'html'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"Email sent to {receiver_mail}")
    except Exception as e:
        print(f"An error occurred: {e}")
