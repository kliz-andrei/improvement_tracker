from datetime import date
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
from send import send_email  # Ensure send_email function exists in send.py

# Load environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Credentials from .env
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")

# Google Sheets Configuration
SHEET_ID = "1AYWSFI1ej4mM-RmnA8Je_jR8EtPjZjszQNGYIDqcUcI"
SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    """Load data from Google Sheets into a DataFrame."""
    parse_dates = ["Due Date"]
    df = pd.read_csv(url, parse_dates=parse_dates)
    return df

def generate_custom_message(row):
    """Generate a personalized and aesthetically pleasing message based on the task category."""
    category = row["Category"]
    name = row["Name"]
    progress = row["Progress"]
    due_date = row["Due Date"].date()  # Convert to `datetime.date`
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


def send_progress_summary(df):
    """Send progress emails for tasks marked 'In Progress'."""
    today = date.today()
    in_progress_items = df[df["Status"] == "In Progress"]

    if in_progress_items.empty:
        print("No tasks in progress to send emails for.")
        return

    email_counter = 0
    for _, row in in_progress_items.iterrows():
        receiver_email = row.get("Email") or sender_email  # Use recipient email or default to sender

        custom_message = generate_custom_message(row)
        message = f"Hi,\n\n{custom_message}\n\nBest regards,\nKliz Millares"

        send_email(
            subject=f"Progress Update: {row['Name']}",
            sender_email=sender_email,
            password=password_email,
            receiver_mail=receiver_email,
            message=message
        )
        email_counter += 1

    print(f"Total emails sent: {email_counter}")

# Main script execution
if __name__ == "__main__":
    try:
        df = load_df(URL)
        send_progress_summary(df)
    except Exception as e:
        print(f"An error occurred: {e}")
