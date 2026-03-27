from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from utils.loader import load_file
from PyPDF2 import PdfReader
from io import BytesIO
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PROMPT_PATH = "agent-skils/cv-extractor.md"


def extract_cv_from_bytes(cv_bytes: BytesIO) -> dict:
    reader = PdfReader(cv_bytes)
    cv_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

    prompt_template = load_file(PROMPT_PATH)

    prompt = f"{prompt_template}\n\nCV:\n{cv_text}"

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a strict CV extraction system. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content