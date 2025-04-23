import os
import httpx
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer " + NOTION_API_KEY,
    "Notion-Version": NOTION_VERSION
}

async def get_database(database_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.notion.com/v1/databases/{database_id}", headers=HEADERS)
        return res.json()
