import os
import httpx
import csv
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer " + NOTION_API_KEY,
    "Notion-Version": NOTION_VERSION
}

async def export_database_to_csv(database_id: str, output_file: str = "notion_export.csv"):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"https://api.notion.com/v1/databases/{database_id}/query", headers=HEADERS)
        data = res.json().get("results", [])

    if not data:
        return {"error": "No data found or query failed"}

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        first_row = data[0]["properties"]
        headers = list(first_row.keys())
        writer.writerow(headers)
        for item in data:
            row = []
            for key in headers:
                prop = item["properties"].get(key, {})
                val = prop.get("title") or prop.get("rich_text") or prop.get("select") or prop.get("multi_select")
                if isinstance(val, list) and val and isinstance(val[0], dict):
                    text = val[0].get("text", {}).get("content", "") if "text" in val[0] else val[0].get("name", "")
                    row.append(text)
                elif isinstance(val, dict):
                    row.append(val.get("name", ""))
                else:
                    row.append("")
            writer.writerow(row)

    return {"message": f"Exported {len(data)} rows to {output_file}"}
