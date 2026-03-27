from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import json
from utils.loader import load_file
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_PATH = "agent-skils/finalizer.md"

def finalist_summary(cv_json, job_json, matcher_json):
    prompt_template = load_file(PROMPT_PATH)
    prompt = (prompt_template
              .replace("{cv_json}", json.dumps(cv_json, indent=2))
              .replace("{job_json}", json.dumps(job_json, indent=2))
              .replace("{matcher_json}", json.dumps(matcher_json, indent=2)))

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a deterministic Candidate Summary AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content