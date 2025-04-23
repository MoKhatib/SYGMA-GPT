import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def suggest_tags_for_text(text: str):
    prompt = f"Suggest 5 useful tags for the following Notion content:
{text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a Notion tagging expert."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']
