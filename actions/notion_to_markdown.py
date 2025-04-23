import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer " + NOTION_API_KEY,
    "Notion-Version": NOTION_VERSION
}

def block_to_md(block):
    b_type = block.get("type")
    text_obj = block.get(b_type, {}).get("rich_text", [{}])[0].get("text", {})
    text = text_obj.get("content", "")
    if b_type == "heading_1":
        return f"# {text}"
    elif b_type == "heading_2":
        return f"## {text}"
    elif b_type == "heading_3":
        return f"### {text}"
    elif b_type == "to_do":
        checked = "x" if block["to_do"].get("checked") else " "
        return f"- [{checked}] {text}"
    elif b_type == "bulleted_list_item":
        return f"- {text}"
    elif b_type == "numbered_list_item":
        return f"1. {text}"
    elif b_type == "quote":
        return f"> {text}"
    else:
        return text

async def notion_to_markdown(page_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=HEADERS)
        blocks = res.json().get("results", [])
        markdown = "\n".join(block_to_md(block) for block in blocks)
        return markdown
