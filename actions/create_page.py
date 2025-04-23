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

async def search_existing_pages(title):
    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.notion.com/v1/search", headers=HEADERS, json={"query": title})
        return res.json().get("results", [])

async def create_page_if_unique(title: str, parent_id: str):
    existing_pages = await search_existing_pages(title)

    for page in existing_pages:
        existing_title = page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("text", {}).get("content", "")
        if await similar(title, existing_title) > 0.8:
            return {"status": "duplicate", "reason": f"Similar page already exists: {existing_title}"}

    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": title}}]
            }
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
        return response.json()
