from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx

from actions.delete_page import delete_page
from actions.create_block import create_block
from actions.convert_block import convert_block
from db_actions.create_database import create_database
from db_actions.link_database import add_relation_property

load_dotenv()

# ✅ Main FastAPI app instance with documentation enabled
app = FastAPI(
    title="SYGMA GPT",
    description="An AI-powered Notion API assistant for full CRUD operations on pages, blocks, and databases.",
    version="1.0.0"
)

# === DELETE PAGE ===
class PageDeleteRequest(BaseModel):
    page_id: str

@app.delete("/notion/delete_page")
async def delete_page_endpoint(req: PageDeleteRequest):
    return await delete_page(req.page_id)

# === CREATE BLOCK ===
class BlockCreateRequest(BaseModel):
    parent_id: str
    block_type: str
    text: str

@app.post("/notion/create_block")
async def create_block_endpoint(req: BlockCreateRequest):
    return await create_block(req.parent_id, req.block_type, req.text)

# === CONVERT BLOCK ===
class BlockConvertRequest(BaseModel):
    block_id: str
    new_type: str

@app.patch("/notion/convert_block")
async def convert_block_endpoint(req: BlockConvertRequest):
    return await convert_block(req.block_id, req.new_type)

# === CREATE DATABASE ===
class DatabaseCreateRequest(BaseModel):
    parent_page_id: str
    title: str
    properties: dict

@app.post("/notion/create_database")
async def create_database_endpoint(req: DatabaseCreateRequest):
    return await create_database(req.parent_page_id, req.title, req.properties)

# === LINK DATABASES ===
class DatabaseLinkRequest(BaseModel):
    database_id: str
    related_database_id: str
    property_name: str = "Relation"

@app.patch("/notion/link_database")
async def link_database_endpoint(req: DatabaseLinkRequest):
    return await add_relation_property(req.database_id, req.related_database_id, req.property_name)
