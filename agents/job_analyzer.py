from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from utils.loader import load_file
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PROMPT_PATH = "agent-skils/job-analyzer.md"

def analyze_job_description(job_text: str) -> dict:
    prompt_template = load_file(PROMPT_PATH)
    prompt = f"{prompt_template}\n\nJob Description:\n{job_text}"
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a professional job analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    
    return response.choices[0].message.content