# SYGMA-GPT

**SYGMA** is an autonomous, Notion-integrated GPT assistant capable of full CRUD (Create, Read, Update, Delete) operations on pages, blocks, databases, and properties. It prevents content duplication using semantic matching and offers full programmable interaction with a Notion workspace.

---

## 🚀 Features

- Create pages only if they don't semantically exist (no duplication)
- Update existing pages if their title differs
- Fetch and browse your entire Notion workspace
- Ready to extend into full block creation, deletion, transformation, etc.

---

## 📘 API Endpoints

| Method | Endpoint               | Description                      |
|--------|------------------------|----------------------------------|
| `GET`  | `/notion/search`       | Search all content in Notion     |
| `POST` | `/notion/create_page`  | Smart page creation              |
| `PATCH`| `/notion/update_page`  | Safe update to page titles       |

---

## 🧰 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SYGMA-GPT.git
   cd SYGMA-GPT
