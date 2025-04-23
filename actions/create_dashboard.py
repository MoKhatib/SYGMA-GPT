import os
import httpx
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer " + NOTION_API_KEY,
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

async def create_dashboard(parent_id: str, title: str, summary: str = "", callout: str = "📌 Dashboard Overview"):
    blocks = [
        {"callout": {"rich_text": [{"text": {"content": callout}}], "icon": {"emoji": "📣"}}},
        {"paragraph": {"rich_text": [{"text": {"content": summary}}]}}
    ]
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]}
        },
        "children": blocks
    }
    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
        return res.json()
