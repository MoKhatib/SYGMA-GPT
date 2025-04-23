import os
import httpx
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

async def create_database(parent_page_id: str, title: str, properties: dict):
    payload = {
        "parent": {"page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties
    }

    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.notion.com/v1/databases", headers=HEADERS, json=payload)
        return res.json()
