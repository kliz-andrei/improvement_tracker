import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Email Configuration
PORT = 587
EMAIL_SERVER = "smtp.gmail.com"
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")

# Load the Google Sheets data
SHEET_ID = "1AYWSFI1ej4mM-RmnA8Je_jR8EtPjZjszQNGYIDqcUcI"
SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    """Load the Google Sheet as a DataFrame."""
    parse_dates = ["Due Date"]
    return pd.read_csv(url, parse_dates=parse_dates)

def generate_custom_message(row):
    """Generate a personalized and aesthetically pleasing message."""
    category = row["Category"]
    name = row["Name"]
    progress = row["Progress"]
    due_date = row["Due Date"].date()
    days_left = (due_date - date.today()).days

    message_template = """
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 15px; border-radius: 8px;">
          <h2 style="text-align: center; color: #4CAF50;">📈 Progress Update</h2>
          <p style="font-size: 18px; color: #333;">
            Hello! Here's an update on your <b style="color: #2196F3;">{category}</b>:
          </p>
          <p style="font-size: 18px; color: #555;">
            <b style="color: #FF5722;">{name}</b> is currently <b>{progress}%</b> complete.
          </p>
          <p style="font-size: 18px; color: #666;">
            You have <b style="color: #9C27B0;">{days_left} days</b> left until the due date: 
            <b style="color: #009688;">{due_date}</b>.
          </p>
          <p style="font-style: italic; color: #607D8B;">
            {custom_message}
          </p>
        </div>
      </body>
    </html>
    """

    # Custom messages based on the category
    if category == "Course":
        custom_message = "Keep up the great work! You're making steady progress 🎓."
    elif category == "Book":
        custom_message = "Dive deeper into your book 📖 and enjoy the journey!"
    elif category == "Project":
        custom_message = "Almost there! Stay motivated to finish your project 🚀."
    elif category == "Assignment":
        custom_message = "You're doing well with this assignment 📝. Complete it on time and shine!"
    else:
        custom_message = "Keep pushing forward. You're doing amazing 💪!"

    # Format the message using the template
    return message_template.format(
        category=category,
        name=name,
        progress=progress,
        days_left=days_left,
        due_date=due_date.strftime("%d %b %Y"),
        custom_message=custom_message,
    )

def send_email(subject, message, receiver_emails):
    """Send an email to multiple recipients."""
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(receiver_emails)  # Join multiple emails with commas
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "html"))

        # Connect to the SMTP server
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
        
        print(f"Email successfully sent to: {receiver_emails}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

def query_data_and_email(df):
    """Check tasks in progress and send emails accordingly."""
    present = date.today()
    email_counter = 0

    for _, row in df.iterrows():
        # Process only tasks that are in progress
        if row["Progress"] < 100 and row["Status"] == "In Progress":
            receiver_emails = [email.strip() for email in row["Email"].split(",")]
            message = generate_custom_message(row)
            send_email(
                subject=f"Progress Update: {row['Name']}",
                message=message,
                receiver_emails=receiver_emails
            )
            email_counter += 1

    return f"Total emails sent: {email_counter}"

# Load the data and execute the query function
df = load_df(URL)
result = query_data_and_email(df)
print(result)
