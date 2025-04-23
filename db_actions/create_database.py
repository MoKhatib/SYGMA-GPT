async def create_database(parent_page_id: str, title: str, properties: dict = None):
    # Fallback: Inject a default property if none provided
    if not properties:
        properties = {
            "Title": {
                "title": {}
            }
        }

    payload = {
        "parent": {"page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties
    }

    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.notion.com/v1/databases", headers=HEADERS, json=payload)
        return res.json()
