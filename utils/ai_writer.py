import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_email(company, recruiter, role, skills):
    prompt = f"""
    Write a short, professional email to {recruiter} from {company}. 
    I am interested in the {role} position. Mention my interest and alignment with skills like {skills}. 
    Make it enthusiastic and polite. Close with a thank you and willingness to share resume.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful job applicant assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error generating email: {e}"