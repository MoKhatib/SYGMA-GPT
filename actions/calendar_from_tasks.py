import os
import httpx
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

def format_date_string(date_str):
    try:
        date = datetime.fromisoformat(date_str)
        return date.strftime("%A, %B %d")
    except Exception:
        return "No Date"

async def calendar_from_tasks(database_id: str, date_property: str = "Date", title_property: str = "Name"):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"https://api.notion.com/v1/databases/{database_id}/query", headers=HEADERS)
        tasks = res.json().get("results", [])

    calendar = defaultdict(list)

    for task in tasks:
        props = task.get("properties", {})
        title_data = props.get(title_property, {}).get("title", [])
        date_data = props.get(date_property, {}).get("date", {})

        title = title_data[0]["text"]["content"] if title_data else "Untitled"
        start_date = date_data.get("start") if date_data else None
        day_key = format_date_string(start_date) if start_date else "No Date"

        calendar[day_key].append(title)

    return dict(calendar)
