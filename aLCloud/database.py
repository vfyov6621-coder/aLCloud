"""SQLite database for tokens, settings, file cache."""

import sqlite3
import json
import os
from pathlib import Path

DB_PATH = Path.home() / ".alcloud" / "alcloud.db"


def _ensure_dir():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _conn() -> sqlite3.Connection:
    _ensure_dir()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = _conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            display_name TEXT,
            client_id TEXT DEFAULT '',
            client_secret TEXT DEFAULT '',
            access_token TEXT DEFAULT '',
            refresh_token TEXT DEFAULT '',
            token_expiry TEXT DEFAULT '',
            extra TEXT DEFAULT '{}',
            is_connected INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        CREATE TABLE IF NOT EXISTS file_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_id INTEGER,
            file_id TEXT,
            name TEXT,
            path TEXT,
            size INTEGER DEFAULT 0,
            mime_type TEXT DEFAULT '',
            is_folder INTEGER DEFAULT 0,
            modified_at TEXT,
            cached_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(provider_id) REFERENCES providers(id)
        );
    """)
    conn.commit()
    conn.close()


# ── Providers ──────────────────────────────────────────────

def save_provider(
    provider_type: str,
    display_name: str,
    client_id: str = "",
    client_secret: str = "",
    access_token: str = "",
    refresh_token: str = "",
    token_expiry: str = "",
    extra: dict | None = None,
) -> int:
    conn = _conn()
    cur = conn.execute(
        """INSERT INTO providers
           (type, display_name, client_id, client_secret,
            access_token, refresh_token, token_expiry, extra, is_connected)
           VALUES (?,?,?,?,?,?,?,? ,1)""",
        (provider_type, display_name, client_id, client_secret,
         access_token, refresh_token, token_expiry,
         json.dumps(extra or {})),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def update_provider_tokens(
    provider_id: int,
    access_token: str,
    refresh_token: str = "",
    token_expiry: str = "",
):
    conn = _conn()
    conn.execute(
        """UPDATE providers SET access_token=?, refresh_token=?,
           token_expiry=?, is_connected=1 WHERE id=?""",
        (access_token, refresh_token, token_expiry, provider_id),
    )
    conn.commit()
    conn.close()


def update_provider_creds(provider_id: int, client_id: str, client_secret: str):
    conn = _conn()
    conn.execute(
        "UPDATE providers SET client_id=?, client_secret=? WHERE id=?",
        (client_id, client_secret, provider_id),
    )
    conn.commit()
    conn.close()


def update_provider_extra(provider_id: int, extra: dict):
    conn = _conn()
    conn.execute(
        "UPDATE providers SET extra=? WHERE id=?",
        (json.dumps(extra), provider_id),
    )
    conn.commit()
    conn.close()


def get_providers() -> list[dict]:
    conn = _conn()
    rows = conn.execute(
        "SELECT *, rowid as id FROM providers ORDER BY created_at"
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["extra"] = json.loads(d.get("extra") or "{}")
        d["is_connected"] = bool(d.get("is_connected"))
        result.append(d)
    return result


def get_provider(provider_id: int) -> dict | None:
    conn = _conn()
    row = conn.execute(
        "SELECT *, rowid as id FROM providers WHERE id=?", (provider_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["extra"] = json.loads(d.get("extra") or "{}")
    d["is_connected"] = bool(d.get("is_connected"))
    return d


def delete_provider(provider_id: int):
    conn = _conn()
    conn.execute("DELETE FROM file_cache WHERE provider_id=?", (provider_id,))
    conn.execute("DELETE FROM providers WHERE id=?", (provider_id,))
    conn.commit()
    conn.close()


# ── Settings ───────────────────────────────────────────────

def save_setting(key: str, value: str):
    conn = _conn()
    conn.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
        (key, value),
    )
    conn.commit()
    conn.close()


def get_setting(key: str, default: str = "") -> str:
    conn = _conn()
    row = conn.execute(
        "SELECT value FROM settings WHERE key=?", (key,)
    ).fetchone()
    conn.close()
    return row["value"] if row else default


# ── File cache ─────────────────────────────────────────────

def save_file_cache(provider_id: int, files: list[dict]):
    conn = _conn()
    conn.execute("DELETE FROM file_cache WHERE provider_id=?", (provider_id,))
    for f in files:
        conn.execute(
            """INSERT INTO file_cache
               (provider_id, file_id, name, path, size, mime_type,
                is_folder, modified_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                provider_id,
                f.get("id", ""),
                f.get("name", ""),
                f.get("path", ""),
                f.get("size", 0),
                f.get("mime_type", ""),
                1 if f.get("is_folder") else 0,
                f.get("modified_at", ""),
            ),
        )
    conn.commit()
    conn.close()


def get_cached_files(provider_id: int) -> list[dict]:
    conn = _conn()
    rows = conn.execute(
        "SELECT * FROM file_cache WHERE provider_id=? ORDER BY is_folder DESC, name",
        (provider_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def clear_cache(provider_id: int | None = None):
    conn = _conn()
    if provider_id:
        conn.execute("DELETE FROM file_cache WHERE provider_id=?", (provider_id,))
    else:
        conn.execute("DELETE FROM file_cache")
    conn.commit()
    conn.close()
