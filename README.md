# 📧 Email Notification System for Progress Tracking

## Overview

This project is designed to send automated email notifications based on the progress of various tasks tracked in a Google Sheet. The system retrieves data from the Google Sheet, checks the status of tasks, and sends aesthetically pleasing email updates to multiple recipients for tasks that are still in progress.

## Features

- **Automated Email Notifications:** Sends email updates for tasks with progress less than **100%** and marked as **"In Progress."** 🎯
- **Customizable Messages:** Generates personalized messages for different categories (Courses, Books, Projects, Assignments). 📚
- **Multiple Recipients:** Allows sending emails to multiple recipients for each task. 📬
- **Aesthetic Email Format:** Creates visually appealing email layouts using HTML and inline CSS. ✨

## Requirements

- Python 3.x 🐍
- `pandas` library 📊
- `python-dotenv` library 🔐
- Access to Google Sheets (shared with appropriate permissions) 📄
- SMTP email server (e.g., Gmail) 📧

## Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies:**
   ```bash
   pip install pandas python-dotenv
   ```

3. **Environment Variables:**
   Create a `.env` file in the root of your project directory with the following content:
   ```plaintext
   EMAIL=your_email@gmail.com
   PASSWORD=your_email_password
   ```

4. **Google Sheets Setup:**
   Ensure your Google Sheet is publicly accessible or shared with the email used in the `.env` file. The sheet should contain the following columns:
   - **Name**: Name of the task
   - **Category**: Category of the task (Course, Book, Project, Assignment)
   - **Progress**: Progress percentage (0 to 100)
   - **Due Date**: Due date of the task
   - **Email**: Comma-separated list of recipient emails
   - **Status**: Task status (In Progress, Completed)

5. **Run the Script:**
   Execute the script to send email notifications:
   ```bash
   python your_script_name.py
   ```

## Code Structure

- **load_df(url)**: Loads the Google Sheet data as a DataFrame. 📈
- **generate_custom_message(row)**: Generates a personalized HTML message based on the task's category. 💬
- **send_email(subject, message, receiver_emails)**: Sends an email to the specified recipients. ✉️
- **query_data_and_email(df)**: Checks tasks in progress and triggers email notifications accordingly. 🔍

## Customization

You can customize the email styles and messages in the `generate_custom_message` function. Modify the HTML template to adjust colors, fonts, and layouts according to your preferences. 🌈

## Troubleshooting

- Ensure that your email account allows less secure apps to send emails if using Gmail. 🚫
- Check your Google Sheet's sharing settings to make sure the script has access to read the data. 🛠️

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information. 📜

## Acknowledgments

- Thanks to [pandas](https://pandas.pydata.org/) for data manipulation. 🙏
- Thanks to [python-dotenv](https://pypi.org/project/python-dotenv/) for managing environment variables. 🔑
