"""Encrypted MusicAI token storage.

Supports durable Postgres via MUSICAI_DATABASE_URL/MUSICAI_TOKEN_DB/DATABASE_URL and a local or /tmp
SQLite fallback for development/testing. OAuth tokens are encrypted before storage.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet, InvalidToken


@dataclass(frozen=True)
class StorageStatus:
    backend: str
    durable: bool
    encrypted: bool
    ready: bool
    warning: str = ""


def _db_url() -> str:
    for name in ("MUSICAI_DATABASE_URL", "MUSICAI_TOKEN_DB", "DATABASE_URL", "POSTGRES_URL"):
        value = os.getenv(name, "").strip()
        if value.lower().startswith(("postgres://", "postgresql://")):
            return value
    return ""


def _sqlite_path() -> str:
    explicit = os.getenv("MUSICAI_SQLITE_PATH") or os.getenv("SQLITE_PATH")
    if explicit:
        return explicit
    legacy = os.getenv("MUSICAI_TOKEN_DB", "")
    if legacy and not legacy.lower().startswith(("postgres://", "postgresql://")):
        return legacy
    if os.getenv("VERCEL"):
        return "/tmp/musicai_tokens.db"
    return str(Path(__file__).with_name("musicai_tokens.db"))


def _fernet() -> Fernet:
    secret = (
        os.getenv("MUSICAI_TOKEN_ENCRYPTION_KEY")
        or os.getenv("MUSICAI_TOKEN_SECRET")
        or os.getenv("FLASK_SECRET_KEY")
    )
    if not secret or secret == "something secret":
        raise RuntimeError("Set MUSICAI_TOKEN_ENCRYPTION_KEY or MUSICAI_TOKEN_SECRET before storing OAuth tokens")

    # Accept a real Fernet key if supplied; otherwise derive one from the app secret.
    try:
        return Fernet(secret.encode("utf-8"))
    except Exception:
        digest = hashlib.sha256(secret.encode("utf-8")).digest()
        return Fernet(base64.urlsafe_b64encode(digest))


def _encrypt(payload: Dict[str, Any]) -> str:
    return _fernet().encrypt(json.dumps(payload, separators=(",", ":")).encode("utf-8")).decode("utf-8")


def _decrypt(ciphertext: str) -> Dict[str, Any]:
    try:
        raw = _fernet().decrypt(ciphertext.encode("utf-8"))
        return json.loads(raw.decode("utf-8"))
    except InvalidToken as exc:
        raise RuntimeError("Stored token could not be decrypted with the configured token secret") from exc


def storage_status() -> StorageStatus:
    url = _db_url()
    has_secret = bool(
        os.getenv("MUSICAI_TOKEN_ENCRYPTION_KEY")
        or os.getenv("MUSICAI_TOKEN_SECRET")
        or os.getenv("FLASK_SECRET_KEY")
    )
    if url:
        return StorageStatus("postgres", True, has_secret, has_secret)
    path = _sqlite_path()
    durable = not (os.getenv("VERCEL") or path.startswith("/tmp/"))
    warning = "SQLite token DB is ephemeral on Vercel; configure MUSICAI_DATABASE_URL before real users." if not durable else ""
    return StorageStatus("sqlite", durable, has_secret, has_secret, warning)


def _pg_connect():
    try:
        import psycopg
    except ImportError as exc:
        raise RuntimeError("psycopg is required when MUSICAI_DATABASE_URL/DATABASE_URL is set") from exc
    return psycopg.connect(_db_url())


def _init_sqlite() -> sqlite3.Connection:
    path = Path(_sqlite_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS provider_tokens (
          user_id TEXT NOT NULL,
          provider TEXT NOT NULL,
          provider_account_id TEXT,
          encrypted_payload TEXT NOT NULL,
          scopes TEXT,
          expires_at REAL,
          updated_at REAL NOT NULL,
          PRIMARY KEY (user_id, provider)
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS musicai_accounts (
          user_id TEXT PRIMARY KEY,
          profile_json TEXT,
          created_at REAL NOT NULL,
          last_login_at REAL NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS provider_identities (
          provider TEXT NOT NULL,
          provider_account_id TEXT NOT NULL,
          user_id TEXT NOT NULL,
          profile_json TEXT,
          updated_at REAL NOT NULL,
          PRIMARY KEY (provider, provider_account_id)
        )
        """
    )
    conn.commit()
    return conn


def _init_postgres(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS provider_tokens (
              user_id TEXT NOT NULL,
              provider TEXT NOT NULL,
              provider_account_id TEXT,
              encrypted_payload TEXT NOT NULL,
              scopes TEXT,
              expires_at DOUBLE PRECISION,
              updated_at DOUBLE PRECISION NOT NULL,
              PRIMARY KEY (user_id, provider)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS musicai_accounts (
              user_id TEXT PRIMARY KEY,
              profile_json TEXT,
              created_at DOUBLE PRECISION NOT NULL,
              last_login_at DOUBLE PRECISION NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS provider_identities (
              provider TEXT NOT NULL,
              provider_account_id TEXT NOT NULL,
              user_id TEXT NOT NULL,
              profile_json TEXT,
              updated_at DOUBLE PRECISION NOT NULL,
              PRIMARY KEY (provider, provider_account_id)
            )
            """
        )
    conn.commit()


def resolve_account(provider: str, provider_account_id: str, profile: Optional[Dict[str, Any]] = None, preferred_user_id: Optional[str] = None) -> str:
    """Resolve/link one MusicAI account across multiple OAuth providers."""
    if not provider or not provider_account_id:
        raise ValueError("provider and provider_account_id are required")
    now = time.time()
    profile_json = json.dumps(profile or {}, separators=(",", ":"))
    stable_id = f"acct_{hashlib.sha256((provider + ':' + provider_account_id).encode()).hexdigest()[:28]}"
    if _db_url():
        conn = _pg_connect()
        try:
            _init_postgres(conn)
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM provider_identities WHERE provider=%s AND provider_account_id=%s", (provider, provider_account_id))
                row = cur.fetchone()
                user_id = preferred_user_id or (row[0] if row else stable_id)
                cur.execute(
                    "INSERT INTO musicai_accounts (user_id, profile_json, created_at, last_login_at) VALUES (%s,%s,%s,%s) ON CONFLICT (user_id) DO UPDATE SET profile_json=EXCLUDED.profile_json, last_login_at=EXCLUDED.last_login_at",
                    (user_id, profile_json, now, now),
                )
                cur.execute(
                    "INSERT INTO provider_identities (provider, provider_account_id, user_id, profile_json, updated_at) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (provider, provider_account_id) DO UPDATE SET user_id=EXCLUDED.user_id, profile_json=EXCLUDED.profile_json, updated_at=EXCLUDED.updated_at",
                    (provider, provider_account_id, user_id, profile_json, now),
                )
            conn.commit()
            return user_id
        finally:
            conn.close()

    conn = _init_sqlite()
    try:
        row = conn.execute("SELECT user_id FROM provider_identities WHERE provider=? AND provider_account_id=?", (provider, provider_account_id)).fetchone()
        user_id = preferred_user_id or (row[0] if row else stable_id)
        conn.execute(
            "INSERT INTO musicai_accounts (user_id, profile_json, created_at, last_login_at) VALUES (?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET profile_json=excluded.profile_json, last_login_at=excluded.last_login_at",
            (user_id, profile_json, now, now),
        )
        conn.execute(
            "INSERT INTO provider_identities (provider, provider_account_id, user_id, profile_json, updated_at) VALUES (?,?,?,?,?) ON CONFLICT(provider, provider_account_id) DO UPDATE SET user_id=excluded.user_id, profile_json=excluded.profile_json, updated_at=excluded.updated_at",
            (provider, provider_account_id, user_id, profile_json, now),
        )
        conn.commit()
        return user_id
    finally:
        conn.close()


def connected_providers(user_id: str) -> Dict[str, Dict[str, Any]]:
    if not user_id:
        return {}
    if _db_url():
        conn = _pg_connect()
        try:
            _init_postgres(conn)
            with conn.cursor() as cur:
                cur.execute("SELECT provider, provider_account_id, profile_json, updated_at FROM provider_identities WHERE user_id=%s", (user_id,))
                rows = cur.fetchall()
        finally:
            conn.close()
    else:
        conn = _init_sqlite()
        try:
            rows = conn.execute("SELECT provider, provider_account_id, profile_json, updated_at FROM provider_identities WHERE user_id=?", (user_id,)).fetchall()
        finally:
            conn.close()
    return {
        provider: {
            "provider_account_id": account_id,
            "profile": json.loads(profile_json or "{}"),
            "updated_at": updated_at,
        }
        for provider, account_id, profile_json, updated_at in rows
    }


def save_provider_token(
    user_id: str,
    provider: str,
    payload: Dict[str, Any],
    provider_account_id: Optional[str] = None,
    scopes: Optional[str] = None,
    expires_at: Optional[float] = None,
) -> None:
    if not user_id or not provider:
        raise ValueError("user_id and provider are required")
    encrypted = _encrypt(payload)
    now = time.time()
    if _db_url():
        conn = _pg_connect()
        try:
            _init_postgres(conn)
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO provider_tokens (user_id, provider, provider_account_id, encrypted_payload, scopes, expires_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (user_id, provider) DO UPDATE SET
                      provider_account_id = EXCLUDED.provider_account_id,
                      encrypted_payload = EXCLUDED.encrypted_payload,
                      scopes = EXCLUDED.scopes,
                      expires_at = EXCLUDED.expires_at,
                      updated_at = EXCLUDED.updated_at
                    """,
                    (user_id, provider, provider_account_id, encrypted, scopes, expires_at, now),
                )
            conn.commit()
        finally:
            conn.close()
        return

    conn = _init_sqlite()
    try:
        conn.execute(
            """
            INSERT INTO provider_tokens (user_id, provider, provider_account_id, encrypted_payload, scopes, expires_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, provider) DO UPDATE SET
              provider_account_id=excluded.provider_account_id,
              encrypted_payload=excluded.encrypted_payload,
              scopes=excluded.scopes,
              expires_at=excluded.expires_at,
              updated_at=excluded.updated_at
            """,
            (user_id, provider, provider_account_id, encrypted, scopes, expires_at, now),
        )
        conn.commit()
    finally:
        conn.close()


def load_provider_token(user_id: str, provider: str) -> Dict[str, Any]:
    if _db_url():
        conn = _pg_connect()
        try:
            _init_postgres(conn)
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT encrypted_payload FROM provider_tokens WHERE user_id=%s AND provider=%s",
                    (user_id, provider),
                )
                row = cur.fetchone()
        finally:
            conn.close()
        return _decrypt(row[0]) if row else {}

    conn = _init_sqlite()
    try:
        row = conn.execute(
            "SELECT encrypted_payload FROM provider_tokens WHERE user_id=? AND provider=?",
            (user_id, provider),
        ).fetchone()
        return _decrypt(row[0]) if row else {}
    finally:
        conn.close()


def delete_provider_token(user_id: str, provider: str) -> None:
    if _db_url():
        conn = _pg_connect()
        try:
            _init_postgres(conn)
            with conn.cursor() as cur:
                cur.execute("DELETE FROM provider_tokens WHERE user_id=%s AND provider=%s", (user_id, provider))
            conn.commit()
        finally:
            conn.close()
        return
    conn = _init_sqlite()
    try:
        conn.execute("DELETE FROM provider_tokens WHERE user_id=? AND provider=?", (user_id, provider))
        conn.commit()
    finally:
        conn.close()
