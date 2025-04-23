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

async def create_block(parent_id: str, block_type: str, text: str = "", url: str = ""):
    block_map = {
        "paragraph": {"paragraph": {"rich_text": [{"text": {"content": text}}]}},
        "heading_1": {"heading_1": {"rich_text": [{"text": {"content": text}}]}},
        "heading_2": {"heading_2": {"rich_text": [{"text": {"content": text}}]}},
        "heading_3": {"heading_3": {"rich_text": [{"text": {"content": text}}]}},
        "bulleted_list_item": {"bulleted_list_item": {"rich_text": [{"text": {"content": text}}]}},
        "numbered_list_item": {"numbered_list_item": {"rich_text": [{"text": {"content": text}}]}},
        "to_do": {"to_do": {"rich_text": [{"text": {"content": text}}]}},
        "toggle": {"toggle": {"rich_text": [{"text": {"content": text}}]}},
        "code": {"code": {"rich_text": [{"text": {"content": text}}], "language": "python"}},
        "quote": {"quote": {"rich_text": [{"text": {"content": text}}]}},
        "callout": {"callout": {"rich_text": [{"text": {"content": text}}], "icon": {"emoji": "💡"}}},
        "divider": {"divider": {}},
        "table_of_contents": {"table_of_contents": {}},
        "breadcrumb": {"breadcrumb": {}},
        "child_page": {"child_page": {"title": text}},
        "child_database": {"child_database": {"title": text}},
        "link_to_page": {"link_to_page": {"page_id": text}},  # 'text' should be page_id here
        "equation": {"equation": {"expression": text}},
        "bookmark": {"bookmark": {"url": url}},
        "embed": {"embed": {"url": url}},
        "video": {"video": {"external": {"url": url}}},
        "image": {"image": {"external": {"url": url}}},
        "audio": {"audio": {"external": {"url": url}}},
        "pdf": {"pdf": {"external": {"url": url}}},
        "file": {"file": {"external": {"url": url}}},
        "link_preview": {"link_preview": {"url": url}},
        "unsupported": {"unsupported": {}}
    }

    if block_type not in block_map:
        return {"error": f"Block type '{block_type}' is not supported."}

    block = block_map[block_type]
    payload = {"children": [block]}

    async with httpx.AsyncClient() as client:
        res = await client.patch(f"https://api.notion.com/v1/blocks/{parent_id}/children", headers=HEADERS, json=payload)
        return res.json()
