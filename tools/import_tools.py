import os
import csv
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

async def import_csv_to_database(csv_file: str, database_id: str, column_map: dict):
    entries = []
    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            properties = {
                col: {"title": [{"text": {"content": row[csv_col]}}]} if typ == "title" else
                {"rich_text": [{"text": {"content": row[csv_col]}}]}
                for csv_col, (col, typ) in column_map.items()
            }

            payload = {
                "parent": {"database_id": database_id},
                "properties": properties
            }

            async with httpx.AsyncClient() as client:
                res = await client.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
                entries.append(res.status_code)

    return {"message": f"Imported {len(entries)} rows to Notion", "status_codes": entries}
