from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx

from actions.create_page import create_page_if_unique
from actions.update_page import update_page_if_changed  # NEW IMPORT

load_dotenv()

app = FastAPI()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = os.getenv("NOTION_VERSION")
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

@app.get("/notion/search")
async def search_notion():
    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.notion.com/v1/search", headers=HEADERS, json={})
        return res.json()

# Create Page
class PageCreateRequest(BaseModel):
    title: str
    parent_id: str

@app.post("/notion/create_page")
async def create_page(req: PageCreateRequest):
    return await create_page_if_unique(req.title, req.parent_id)

# Update Page
class PageUpdateRequest(BaseModel):
    page_id: str
    new_title: str

@app.patch("/notion/update_page")
async def update_page(req: PageUpdateRequest):
    return await update_page_if_changed(req.page_id, req.new_title)
