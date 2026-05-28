from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os
from datetime import datetime

app = FastAPI(title="SupportDesk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "support.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL REFERENCES tickets(ticket_id),
            note_text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def next_ticket_id(conn) -> str:
    row = conn.execute("SELECT COUNT(*) as cnt FROM tickets").fetchone()
    num = row["cnt"] + 1
    return f"TKT-{num:04d}"


class CreateTicket(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str


class UpdateTicket(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None


@app.post("/api/tickets")
def create_ticket(body: CreateTicket):
    conn = get_db()
    now = datetime.utcnow().isoformat()
    tid = next_ticket_id(conn)
    conn.execute(
        "INSERT INTO tickets (ticket_id,customer_name,customer_email,subject,description,status,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
        (tid, body.customer_name, body.customer_email, body.subject, body.description, "Open", now, now),
    )
    conn.commit()
    conn.close()
    return {"ticket_id": tid, "created_at": now}


@app.get("/api/tickets")
def list_tickets(
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
):
    conn = get_db()
    sql = "SELECT ticket_id,customer_name,customer_email,subject,status,created_at FROM tickets WHERE 1=1"
    params: list = []
    if status:
        sql += " AND status=?"
        params.append(status)
    if search:
        like = f"%{search}%"
        sql += " AND (customer_name LIKE ? OR customer_email LIKE ? OR ticket_id LIKE ? OR subject LIKE ? OR description LIKE ?)"
        params += [like, like, like, like, like]
    sql += " ORDER BY created_at DESC"

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket = dict(row)
    notes = conn.execute(
        "SELECT id, note_text, created_at FROM notes WHERE ticket_id=? ORDER BY created_at ASC",
        (ticket_id,),
    ).fetchall()
    ticket["notes"] = [dict(n) for n in notes]
    conn.close()
    return ticket


@app.put("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: str, body: UpdateTicket):
    conn = get_db()
    row = conn.execute("SELECT id FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Ticket not found")
    now = datetime.utcnow().isoformat()
    if body.status:
        conn.execute(
            "UPDATE tickets SET status=?, updated_at=? WHERE ticket_id=?",
            (body.status, now, ticket_id),
        )
    if body.note and body.note.strip():
        conn.execute(
            "INSERT INTO notes (ticket_id, note_text, created_at) VALUES (?,?,?)",
            (ticket_id, body.note.strip(), now),
        )
    conn.commit()
    conn.close()
    return {"success": True, "updated_at": now}


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_db()
    row = conn.execute("SELECT ticket_id FROM notes WHERE id=?", (note_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return {"success": True, "ticket_id": row["ticket_id"]}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/{full_path:path}", response_class=HTMLResponse)
def serve_spa(full_path: str):
    with open("static/index.html") as f:
        return f.read()

init_db()
