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

async def query_database(database_id: str, filter: dict = None, sorts: list = None):
    payload = {}
    if filter:
        payload["filter"] = filter
    if sorts:
        payload["sorts"] = sorts

    async with httpx.AsyncClient() as client:
        res = await client.post(f"https://api.notion.com/v1/databases/{database_id}/query", headers=HEADERS, json=payload)
        return res.json()
