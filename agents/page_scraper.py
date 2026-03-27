import requests
from bs4 import BeautifulSoup
import re
from typing import List

def scrape_job_text(url: str) -> List[str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')

    useful = soup.find_all(['p', 'span', 'li', 'h1'])

    cleaned_text = []
    for p in useful:
        text = p.get_text(" ", strip=True)
        text = re.sub(r'\s+', ' ', text)
        if text:
            cleaned_text.append(text)

    return cleaned_text