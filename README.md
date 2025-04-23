# SYGMA-GPT

**SYGMA** is an autonomous, Notion-integrated GPT assistant capable of full CRUD (Create, Read, Update, Delete) operations on pages, blocks, databases, and properties. It prevents content duplication using semantic matching and offers full programmable interaction with a Notion workspace.

---

## 🚀 Features

- No-duplication creation and update logic
- Supports full block and database manipulation
- Smart dashboards, semantic querying
- Integrated export to Markdown and CSV

---

## 📘 API Endpoints

| Method | Endpoint                     | Description                            |
|--------|------------------------------|----------------------------------------|
| `GET`  | `/notion/search`             | Search all content in Notion           |
| `POST` | `/notion/create_page`        | Smart page creation                    |
| `PATCH`| `/notion/update_page`        | Safe update to page titles             |
| `DELETE`| `/notion/delete_page`       | Delete any page                        |
| `POST` | `/notion/create_block`       | Create supported block types           |
| `PATCH`| `/notion/convert_block`      | Convert one block type to another      |
| `PATCH`| `/notion/update_block`       | Update content of existing block       |
| `POST` | `/notion/create_database`    | Create new Notion database             |
| `PATCH`| `/notion/link_database`      | Link two databases using relation      |
| `GET`  | `/notion/get_database`       | Fetch structure of a Notion database   |
| `GET`  | `/notion/export_database`    | Export a database to CSV               |
| `GET`  | `/notion/calendar_from_tasks`| Generate calendar view from tasks      |

---

## 🧰 Setup Instructions

```bash
git clone https://github.com/MoKhatib/SYGMA-GPT.git
cd SYGMA-GPT
python -m venv venv
source venv/bin/activate  # on Windows use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🔐 Environment Variables

```dotenv
NOTION_API_KEY=your_secret_key
NOTION_VERSION=2022-06-28
```

---

## 🔎 Supported Block Types

`paragraph`, `heading_1`, `heading_2`, `heading_3`, `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`, `callout`, `quote`, `divider`, `code`, `table`, `table_row`, `image`, `bookmark`, `embed`, `link_to_page`, `synced_block`, `breadcrumb`, `table_of_contents`, `template`, `unsupported`

---

## 🧠 Powered by:
- OpenAI GPT
- Notion API
