from datetime import date
import pandas as pd
from send import send_email

# Google Sheets URL
SHEET_ID = "16H9-qMS8dMvkUDRWEZZqOIE45w2Pd6b_zICAMU4WPDE"
SHEET_NAME = "Sheet1"  # Adjust this based on the actual sheet name
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    parse_dates = ["due_date", "reminder_date"]
    try:
        df = pd.read_csv(url, parse_dates=parse_dates)
        print("Data loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

def query_data_and_email(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        if (present >= row["reminder_date"].date()) and (row["has_paid"].lower() == "no"):
            send_email(
                subject=f"[Kliz Millares] Invoice: {row['invoice_no']}",
                receiver_mail=row['email'],
                name=row["name"],
                due_date=row["due_date"].strftime("%d, %b %Y"),
                invoice_no=row["invoice_no"],
                amount=row["amount"],
            )
            email_counter += 1
    return f"Total emails sent: {email_counter}"

# Load DataFrame and send emails
df = load_df(URL)
result = query_data_and_email(df)
print(result)
