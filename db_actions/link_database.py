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

async def add_relation_property(database_id: str, related_database_id: str, property_name: str = "Relation"):
    payload = {
        "properties": {
            property_name: {
                "type": "relation",
                "relation": {
                    "database_id": related_database_id
                }
            }
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.patch(f"https://api.notion.com/v1/databases/{database_id}", headers=HEADERS, json=payload)
        return res.json()
