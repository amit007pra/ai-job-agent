from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64
import pandas as pd
from pathlib import Path
from utils.ai_writer import generate_email

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
        email_body =  f"""Hello {row['recruiter_name']} \n I hope you're doing well.

I'm writing to express my keen interest in the DevOps position. With four years of experience in Linux, containerization (Docker, Kubernetes), cloud platforms (Azure, AWS), and CI/CD automation, I believe my background aligns strongly with the role’s requirements.

I am passionate about continuous learning and actively upskill myself in areas like cloud infrastructure, automation, and scripting. I enjoy applying creative solutions to technical challenges, and I’m excited about opportunities where I can contribute and grow.

Please let me know if I may share my resume for your consideration. Thank you for your time, and I look forward to the opportunity to speak further. 

This email is sent via an AI-JOB-AGENT tool which i have hosted on my Github profile: https://github.com/amit007pra/ai-job-agent."""
        # Currently OpenAI API is not working due to no Credit, so testing the app without the AI prompt. 
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

