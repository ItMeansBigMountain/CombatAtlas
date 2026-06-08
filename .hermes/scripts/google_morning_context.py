#!/usr/bin/env python3
"""Collect read-only Google Workspace context for the morning report.

Uses profile-scoped OAuth tokens created by /opt/data/scripts/google_profile_oauth.py.
Prints a compact Markdown brief for the cron agent to summarize.
No write/delete/share/send actions are performed here.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
]

PROFILES = [
    ("hermes-agent", "trapiistan@gmail.com", "Hermes / YouTube / operator account"),
    ("personal-main", "Affan.fareed@gmail.com", "personal main — read-focused; no sends without approval"),
    ("personal-secondary", "fareed320@gmail.com", "personal secondary — read-focused; no sends without approval"),
    ("classicalechos", "classicalechos@gmail.com", "Classical Echos / classy content lane"),
    ("burner", "laflametoast@gmail.com", "burner / low-stakes misc"),
]

CHICAGO = ZoneInfo("America/Chicago")
TOKEN_ROOT = Path("/opt/data/google_profiles")
MAX_SNIPPET = 160
INVISIBLE_CHARS = dict.fromkeys(map(ord, "\u034f\u200b\u200c\u200d\u2060\ufeff\u202a\u202b\u202c\u202d\u202e"), None)
SENSITIVE_NAME_BITS = ("recovery", "password", "secret", "token", "credential", "backup code", "backup-code")


def safe(s: Any, limit: int = 220) -> str:
    text = str(s or "").translate(INVISIBLE_CHARS)
    text = text.replace("\r", " ").replace("\n", " ").strip()
    text = " ".join(text.split())
    return text[:limit] + ("…" if len(text) > limit else "")


def looks_sensitive_name(name: str) -> bool:
    low = (name or "").lower()
    return any(bit in low for bit in SENSITIVE_NAME_BITS)


def load_creds(profile: str) -> Credentials:
    path = TOKEN_ROOT / profile / "google_token.json"
    creds = Credentials.from_authorized_user_file(str(path), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        path.write_text(creds.to_json())
        path.chmod(0o600)
    return creds


def gmail_list_messages(service, query: str, max_results: int = 8) -> list[dict[str, Any]]:
    resp = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
    out = []
    for item in resp.get("messages", [])[:max_results]:
        msg = service.users().messages().get(
            userId="me",
            id=item["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        ).execute()
        headers = {h.get("name", "").lower(): h.get("value", "") for h in msg.get("payload", {}).get("headers", [])}
        out.append(
            {
                "id": item["id"],
                "from": headers.get("from", ""),
                "subject": headers.get("subject", "(no subject)"),
                "date": headers.get("date", ""),
                "snippet": msg.get("snippet", ""),
                "labels": msg.get("labelIds", []),
            }
        )
    return out


def calendar_events(service, days: int = 7, max_results: int = 12) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days)
    resp = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat().replace("+00:00", "Z"),
        timeMax=end.isoformat().replace("+00:00", "Z"),
        singleEvents=True,
        orderBy="startTime",
        maxResults=max_results,
    ).execute()
    events = []
    for ev in resp.get("items", []):
        start = ev.get("start", {}).get("dateTime") or ev.get("start", {}).get("date")
        endt = ev.get("end", {}).get("dateTime") or ev.get("end", {}).get("date")
        events.append(
            {
                "summary": ev.get("summary", "(no title)"),
                "start": start,
                "end": endt,
                "location": ev.get("location", ""),
                "hangoutLink": ev.get("hangoutLink", ""),
            }
        )
    return events


def drive_recent(service, max_results: int = 8) -> list[dict[str, Any]]:
    resp = service.files().list(
        pageSize=max_results,
        orderBy="modifiedTime desc",
        fields="files(id,name,mimeType,modifiedTime,webViewLink,owners(displayName,emailAddress))",
        q="trashed=false",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    return resp.get("files", [])


def profile_block(profile: str, email: str, role: str) -> str:
    token_path = TOKEN_ROOT / profile / "google_token.json"
    if not token_path.exists():
        return f"### {profile} — {email}\n- Auth: missing token at `{token_path}`\n"
    lines = [f"### {profile} — {email}", f"- Role: {role}"]
    try:
        creds = load_creds(profile)
        gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)
        cal = build("calendar", "v3", credentials=creds, cache_discovery=False)
        drive = build("drive", "v3", credentials=creds, cache_discovery=False)

        prof = gmail.users().getProfile(userId="me").execute()
        lines.append(f"- Gmail profile: {prof.get('emailAddress')} | messages: {prof.get('messagesTotal')} | threads: {prof.get('threadsTotal')}")

        unread = gmail_list_messages(gmail, "in:inbox is:unread newer_than:7d", 8)
        important = gmail_list_messages(gmail, "in:inbox (is:starred OR is:important) newer_than:14d", 5)
        recent = gmail_list_messages(gmail, "in:inbox newer_than:2d", 5)
        events = calendar_events(cal)
        files = drive_recent(drive)

        lines.append(f"- Inbox signals: unread={len(unread)} | important/starred={len(important)} | recent={len(recent)}")
        if unread:
            lines.append("- Unread recent:")
            for m in unread[:8]:
                lines.append(f"  - From: {safe(m['from'], 80)} | Subject: {safe(m['subject'], 120)} | Snippet: {safe(m['snippet'], MAX_SNIPPET)}")
        if important:
            lines.append("- Important/starred:")
            seen = set()
            for m in important[:5]:
                key = (m.get("from"), m.get("subject"))
                if key in seen:
                    continue
                seen.add(key)
                lines.append(f"  - From: {safe(m['from'], 80)} | Subject: {safe(m['subject'], 120)} | Snippet: {safe(m['snippet'], MAX_SNIPPET)}")
        if recent:
            lines.append("- Recent inbox sample:")
            for m in recent[:5]:
                lines.append(f"  - From: {safe(m['from'], 70)} | Subject: {safe(m['subject'], 110)}")

        lines.append(f"- Calendar next 7d: {len(events)} event(s)")
        for ev in events[:10]:
            when = safe(ev.get("start"), 40)
            loc = f" | {safe(ev.get('location'), 60)}" if ev.get("location") else ""
            lines.append(f"  - {when} — {safe(ev.get('summary'), 130)}{loc}")

        lines.append("- Recent Drive activity:")
        safe_files = [f for f in files if not looks_sensitive_name(str(f.get("name", "")))]
        skipped_sensitive = len(files) - len(safe_files)
        if safe_files:
            for f in safe_files[:8]:
                owner = ", ".join([o.get("emailAddress") or o.get("displayName", "") for o in f.get("owners", [])])
                lines.append(f"  - {safe(f.get('name'), 130)} | {safe(f.get('modifiedTime'), 30)} | owner: {safe(owner, 80)}")
            if skipped_sensitive:
                lines.append(f"  - {skipped_sensitive} recent Drive item(s) hidden because filename looked credential/recovery-related.")
        else:
            lines.append("  - No recent files returned.")
    except HttpError as e:
        lines.append(f"- ERROR: Google API error: {safe(e, 500)}")
    except Exception as e:
        lines.append(f"- ERROR: {type(e).__name__}: {safe(e, 500)}")
    return "\n".join(lines) + "\n"


def main() -> int:
    now = datetime.now(CHICAGO)
    print(f"# Google Workspace morning context — {now:%A, %Y-%m-%d %I:%M %p %Z}")
    print("Read-only collection across all authorized Google profiles. Summarize high-signal items only; do not send, delete, modify, share, or create anything without explicit user approval.\n")
    for profile, email, role in PROFILES:
        print(profile_block(profile, email, role))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
