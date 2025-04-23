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

async def create_block(parent_id: str, block_type: str, text: str):
    block_map = {
        "paragraph": {"paragraph": {"rich_text": [{"text": {"content": text}}]}},
        "to_do": {"to_do": {"rich_text": [{"text": {"content": text}}]}},
        "heading_1": {"heading_1": {"rich_text": [{"text": {"content": text}}]}},
        "heading_2": {"heading_2": {"rich_text": [{"text": {"content": text}}]}},
        "heading_3": {"heading_3": {"rich_text": [{"text": {"content": text}}]}}
    }

    if block_type not in block_map:
        return {"error": f"Block type '{block_type}' not supported in Phase 1."}

    block = block_map[block_type]
    payload = {
        "children": [block]
    }

    async with httpx.AsyncClient() as client:
        res = await client.patch(f"https://api.notion.com/v1/blocks/{parent_id}/children", headers=HEADERS, json=payload)
        return res.json()
