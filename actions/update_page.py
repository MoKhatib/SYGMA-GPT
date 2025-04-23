import os
import httpx
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

async def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

async def fetch_page_title(page_id):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.notion.com/v1/pages/{page_id}", headers=HEADERS)
        data = res.json()
        return data.get("properties", {}).get("title", {}).get("title", [{}])[0].get("text", {}).get("content", ""), data

async def update_page_if_changed(page_id: str, new_title: str):
    current_title, _ = await fetch_page_title(page_id)

    if await similar(current_title, new_title) > 0.9:
        return {"status": "skipped", "reason": "Title already similar enough, no update applied."}

    payload = {
        "properties": {
            "title": {
                "title": [{"text": {"content": new_title}}]
            }
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.patch(f"https://api.notion.com/v1/pages/{page_id}", headers=HEADERS, json=payload)
        return res.json()
