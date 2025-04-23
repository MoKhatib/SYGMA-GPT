import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION
}

async def export_database_to_json(database_id: str, output_file: str = "notion_export.json"):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"https://api.notion.com/v1/databases/{database_id}/query", headers=HEADERS)
        data = res.json()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {"message": f"Exported to {output_file}", "entries": len(data.get('results', []))}
