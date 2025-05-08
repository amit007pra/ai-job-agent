# ai-job-agent🤖📩

An AI-powered tool that automates your job application process. It integrates with Gmail to send interview or job-related emails, respond smartly using AI, send personalized job applications (with resume and cover letter), and follow up automatically — all through an easy-to-use interface.

## ✨ Features

- ✅ **Gmail Integration** via OAuth 2.0
- 🤖 **AI-Generated Responses** to recruiter emails
- 📤 **Bulk Job Application Sender** using CSV data set of recuiters information
- 📎 **Resume and Cover Letter Attachment** automation
- 🌐 **User Interface** built using Streamlit

---
## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/amit007pra/ai-job-agent
cd ai-job-application-assistant 

### 2. Install the required packages

pip install -r requirements.txt

### 3. Configure Gmail API Access

Go to Google Cloud Console
Create a new project and enable Gmail API
Create OAuth 2.0 Credentials and download credentials.json

### 4. Export your OpenAI API key

export OPENAI_API_KEY=#your_openAI_API_key

### 5. Start the Application

streamlit run login.py

## Next stage of Development:

- 🔁 **Follow-up Reminders & Automation** after 7 days
- 🔔 **Interview Notification UI**, with visual cues (e.g., green alerts)

## 🛠️ Tech Stack

Python
Gmail API
OpenAI API (or LLM model of your choice)
Streamlit 
Pandas, smtplib, email
OAuth2.0
