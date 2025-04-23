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

async def convert_block(block_id: str, new_type: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.notion.com/v1/blocks/{block_id}", headers=HEADERS)
        old_block = res.json()

        text = ""
        if "paragraph" in old_block:
            text = old_block["paragraph"]["rich_text"][0]["text"]["content"]
        elif "to_do" in old_block:
            text = old_block["to_do"]["rich_text"][0]["text"]["content"]

        if not text:
            return {"error": "No transferable content found"}

        block_map = {
            "to_do": {"to_do": {"rich_text": [{"text": {"content": text}}]}},
            "heading_1": {"heading_1": {"rich_text": [{"text": {"content": text}}]}}
        }

        if new_type not in block_map:
            return {"error": f"Conversion to '{new_type}' is not supported."}

        # Create new block
        new_block_payload = block_map[new_type]
        creation_res = await client.patch(f"https://api.notion.com/v1/blocks/{block_id}/children", headers=HEADERS, json={"children": [new_block_payload]})

        # Delete original block
        await client.delete(f"https://api.notion.com/v1/blocks/{block_id}", headers=HEADERS)

        return {"message": "Block converted", "new_block": creation_res.json()}
