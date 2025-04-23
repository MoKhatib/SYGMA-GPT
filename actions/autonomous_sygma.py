import os
import httpx
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION
}

async def scan_and_suggest(database_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"https://api.notion.com/v1/databases/{database_id}/query", headers=HEADERS)
        entries = res.json().get("results", [])
        texts = [str(page.get("properties")) for page in entries]

    summary_prompt = (
        "You are a Notion workspace assistant. Analyze the following page metadata and suggest any action items, cleanups, "
        "or summaries a user might want to see:

" + "\n\n".join(texts)
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You're an AI Notion assistant."},
                  {"role": "user", "content": summary_prompt}]
    )
    return response['choices'][0]['message']['content']
