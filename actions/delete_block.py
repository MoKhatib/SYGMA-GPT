import os
import httpx
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION
}

async def delete_block(block_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.delete(f"https://api.notion.com/v1/blocks/{block_id}", headers=HEADERS)
        return {"status": res.status_code, "message": "Block deleted" if res.status_code == 200 else res.text}
