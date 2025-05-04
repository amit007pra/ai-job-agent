# utils/email_sender.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64
import pandas as pd
from pathlib import Path

RESUME_PATH = Path("data/Resume.pdf") 
DATA_PATH = Path("data/recruiters.csv")

def send_message(service, user_id, message):
    #Send an email message using the Gmail API.
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        return f"✅ Message sent! Message ID: {sent_message['id']}"
    except Exception as error:
        return f"❌ An error occurred: {error}"

def create_message(sender, to, subject, message_text, attachment_path=None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Add the email body
    msg = MIMEText(message_text)
    message.attach(msg)

    # Add the resume attachment if provided
    if attachment_path and Path(attachment_path).exists():
        with open(attachment_path, 'rb') as f:
            resume = MIMEApplication(f.read(), _subtype='pdf')
            resume.add_header('Content-Disposition', 'attachment', filename='resume.pdf')
            message.attach(resume)

    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw_message.decode()}

def send_bulk_emails(service):
    df = pd.read_csv(DATA_PATH)
    for idx, row in df.iterrows():
        if row.get('sent_flag', False):
            continue  # Skip already sent

        # Generate email using AI
        """email_body = generate_email(
            company=row['company_name'],
            recruiter=row['recruiter_name'],
            role=row['role'],
            skills=row['skills_required']
        )""" #
        email_body = " This is an AI_Genertaed Email. You can check out my GitHub: https://github.com/amit007pra"
        # Currently OpenAI API is not working due to no Credit, so testing the app with out the AI prompt. 
        message = create_message(
            sender="me",
            to=row['recruiter_email'],
            subject=f"Application for {row['role']} Role",
            message_text=email_body,
            attachment_path=RESUME_PATH
        )

        result = send_message(service, "me", message)
        print(result)

        # Update flag on recruter.csv
        df.at[idx, 'sent_flag'] = True

    df.to_csv(DATA_PATH, index=False)
    return "✅ All emails processed!"

