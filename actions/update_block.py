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

async def update_block(block_id: str, block_type: str, content: str):
    block_update_map = {
        "paragraph": {"paragraph": {"rich_text": [{"text": {"content": content}}]}},
        "to_do": {"to_do": {"rich_text": [{"text": {"content": content}}]}},
        "heading_1": {"heading_1": {"rich_text": [{"text": {"content": content}}]}},
        "heading_2": {"heading_2": {"rich_text": [{"text": {"content": content}}]}},
        "heading_3": {"heading_3": {"rich_text": [{"text": {"content": content}}]}},
        "quote": {"quote": {"rich_text": [{"text": {"content": content}}]}},
        "callout": {"callout": {"rich_text": [{"text": {"content": content}}], "icon": {"emoji": "💡"}}},
        "toggle": {"toggle": {"rich_text": [{"text": {"content": content}}]}},
        "code": {"code": {"rich_text": [{"text": {"content": content}}], "language": "python"}}
    }

    if block_type not in block_update_map:
        return {"error": f"Block type '{block_type}' not supported for updates."}

    payload = block_update_map[block_type]

    async with httpx.AsyncClient() as client:
        res = await client.patch(f"https://api.notion.com/v1/blocks/{block_id}", headers=HEADERS, json=payload)
        return res.json()
