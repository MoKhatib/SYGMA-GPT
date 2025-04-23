import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def summarize_page_content(text: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a professional summarizer."},
            {"role": "user", "content": f"Summarize this Notion content:
{text}"}
        ]
    )
    return response['choices'][0]['message']['content']
