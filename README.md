# 🎫 SupportDesk

A lightweight, modern **customer support ticket management system** built with **FastAPI** and a clean **light-themed single-page frontend**. Create, track, and manage support tickets — all from a single self-contained app with zero external database dependencies.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Ticket Management** | Create, view, and update support tickets with status tracking |
| **Status Workflow** | Move tickets through `Open` → `In Progress` → `Closed` lifecycle |
| **Notes & Comments** | Add and delete internal notes on any ticket |
| **Search & Filter** | Full-text search across customer name, email, ticket ID, subject, and description |
| **Status Filtering** | Filter the ticket list by status (Open / In Progress / Closed) |
| **Live Dashboard** | At-a-glance stats showing Total, Open, In Progress, and Closed counts |
| **Light Theme UI** | Clean, professional light interface with smooth animations, toast notifications, and responsive design |
| **Zero Config DB** | Uses SQLite — the database is created automatically on first run |

---

## 🛠 Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Server:** [Uvicorn](https://www.uvicorn.org/) (ASGI)
- **Database:** SQLite (file-based, no setup required)
- **Frontend:** Vanilla HTML/CSS/JS with [Tailwind CSS](https://tailwindcss.com/) (CDN)
- **Typography:** [DM Sans](https://fonts.google.com/specimen/DM+Sans) + [DM Mono](https://fonts.google.com/specimen/DM+Mono)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- `pip` available in your terminal

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/support-desk.git
cd support-desk
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

Activate it:

- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (Command Prompt):**
  ```bash
  venv\Scripts\activate.bat
  ```
- **Windows (PowerShell):**
  ```bash
  venv\Scripts\Activate.ps1
  ```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start the server**

```bash
uvicorn main:app --reload --port 8000
```

**5. Open the app**

Visit **[http://localhost:8000](http://localhost:8000)** in your browser.

> **Note:** The SQLite database (`support.db`) is created automatically on first run. No database setup is required.

---

## 📡 API Reference

All endpoints are prefixed with `/api`. The interactive API docs are available at `/docs` (Swagger UI) when the server is running.

### Tickets

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/tickets` | Create a new ticket |
| `GET` | `/api/tickets` | List all tickets (with optional `?status=` and `?search=` query params) |
| `GET` | `/api/tickets/{ticket_id}` | Get ticket details (including notes) |
| `PUT` | `/api/tickets/{ticket_id}` | Update ticket status and/or add a note |

### Notes

| Method | Endpoint | Description |
|---|---|---|
| `DELETE` | `/api/notes/{note_id}` | Delete a specific note |

### Example: Create a ticket

```bash
curl -X POST http://localhost:8000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "subject": "Cannot reset password",
    "description": "I have tried resetting my password multiple times but the email never arrives."
  }'
```

**Response:**

```json
{
  "ticket_id": "TKT-0001",
  "created_at": "2026-05-30T00:00:00.000000"
}
```

---

## 📁 Project Structure

```
support-desk/
├── main.py              # FastAPI application (routes, models, DB init)
├── static/
│   └── index.html       # Single-page frontend (HTML + CSS + JS)
├── requirements.txt     # Python dependencies
├── Procfile             # Process file for deployment (Render, Heroku)
├── render.yaml          # Render deployment configuration
├── .gitignore           # Git ignore rules
└── support.db           # SQLite database (auto-generated at runtime)
```

---

## ☁️ Deployment (Render)

### Prerequisites

- A free account at [render.com](https://render.com)
- Your project pushed to a GitHub or GitLab repository

### Steps

1. **Push to GitHub**

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/support-desk.git
   git push -u origin main
   ```

2. **Create a Web Service on Render**

   Log in to [render.com](https://render.com) → **New → Web Service** → Connect your repo.

   | Setting | Value |
   |---|---|
   | **Name** | `support-desk` |
   | **Branch** | `main` |
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

3. **Wait for the build** (~1–2 minutes) and click the live URL.

> **⚠️ SQLite on Render:** The free tier uses an ephemeral filesystem — the database resets on each deploy/restart. For production, connect a **PostgreSQL** database via Render's managed DB service and update `DB_PATH` in `main.py`.

---

## 📋 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | 0.111.0 | Web framework |
| `uvicorn[standard]` | 0.29.0 | ASGI server |
| `pydantic` | 2.7.1 | Data validation |

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute as needed.
