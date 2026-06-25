#!/usr/bin/env python3
"""Hermes email sorting agent.

Sorts known newsletter/source emails into Gmail labels so Inbox stays clean while
source emails remain available for morning reports and video generation.

Default is dry-run. Use --apply to create labels and move matching source
newsletter / priority-account emails out of INBOX into Hermes/* labels.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from email.utils import parseaddr
from pathlib import Path
from typing import Any

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
TOKEN_ROOT = Path("/opt/data/google_profiles")
# Default sorting only targets profiles where Hermes is allowed to modify Gmail.
# personal-main/affan is intentionally read-only; hermes-agent is not a user inbox lane.
PROFILES = [
    ("personal-secondary", "fareed320@gmail.com"),
    ("classicalechos", "classicalechos@gmail.com"),
    ("burner", "laflametoast@gmail.com"),
]

SOURCE_LABELS = {
    "tldr": "Hermes/Source/TLDR",
    "daily_stoic": "Hermes/Source/Daily Stoic",
    "kino_body": "Hermes/Source/Kino Body",
    "robinhood_snacks": "Hermes/Source/Robinhood Snacks",
    "newsletter_queue": "Hermes/Source/Newsletter Queue",
}
REVIEW_LABELS = {
    "important": "Hermes/Review/Important",
    "needs_human": "Hermes/Review/Needs Human",
    "robinhood": "Hermes/Finance/Robinhood",
    "known_junk": "Hermes/Junk/Known",
}

@dataclass(frozen=True)
class RuleResult:
    key: str
    label: str
    reason: str
    remove_inbox: bool = True


def safe(text: Any, limit: int = 220) -> str:
    s = str(text or "").replace("\r", " ").replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s[:limit] + ("…" if len(s) > limit else "")


def sender_addr(from_header: str) -> str:
    _name, addr = parseaddr(from_header or "")
    return (addr or from_header or "").lower()


def load_creds(profile: str) -> Credentials:
    path = TOKEN_ROOT / profile / "google_token.json"
    creds = Credentials.from_authorized_user_file(str(path), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        path.write_text(creds.to_json())
        path.chmod(0o600)
    return creds


def gmail(profile: str):
    return build("gmail", "v1", credentials=load_creds(profile), cache_discovery=False)


def headers_from_msg(msg: dict[str, Any]) -> dict[str, str]:
    hs = msg.get("payload", {}).get("headers", [])
    return {h.get("name", "").lower(): h.get("value", "") for h in hs}


def classify(account_email: str, msg: dict[str, Any]) -> RuleResult | None:
    h = headers_from_msg(msg)
    sender = sender_addr(h.get("from", ""))
    raw = f"{h.get('from','')} {sender} {h.get('subject','')} {msg.get('snippet','')}".lower()
    account = account_email.lower()

    if sender == "dan@tldrnewsletter.com" and account == "fareed320@gmail.com":
        return RuleResult("tldr", SOURCE_LABELS["tldr"], "preferred TLDR source on personal-secondary")
    if sender == "dan@tldrnewsletter.com":
        return RuleResult("newsletter_queue", SOURCE_LABELS["newsletter_queue"], "duplicate/non-preferred TLDR source")
    if "daily stoic" in raw or "dailystoic" in raw or "dailystoic.com" in raw:
        return RuleResult("daily_stoic", SOURCE_LABELS["daily_stoic"], "Daily Stoic source email")
    if "kinobody" in raw or "kino body" in raw or "greg o'gallagher" in raw or "greg ogallagher" in raw:
        return RuleResult("kino_body", SOURCE_LABELS["kino_body"], "Kino Body source email")
    if sender == "hello@snacks.robinhood.com" or "snacks.robinhood.com" in sender:
        return RuleResult("robinhood_snacks", SOURCE_LABELS["robinhood_snacks"], "Robinhood Snacks financial markets newsletter")
    if "robinhood" in raw or "robinhood.com" in sender:
        return RuleResult("robinhood", REVIEW_LABELS["robinhood"], "Robinhood financial/account email")
    return None


def ensure_label(service, label_name: str, *, apply: bool) -> str | None:
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for label in labels:
        if label.get("name") == label_name:
            return label.get("id")
    if not apply:
        return None
    body = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
    }
    created = service.users().labels().create(userId="me", body=body).execute()
    return created["id"]


def list_inbox_messages(service, max_results: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    page = None
    while len(out) < max_results:
        resp = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=min(100, max_results - len(out)),
            pageToken=page,
        ).execute()
        ids = resp.get("messages", [])
        for item in ids:
            msg = service.users().messages().get(
                userId="me",
                id=item["id"],
                format="metadata",
                metadataHeaders=["From", "Subject", "Date"],
            ).execute()
            out.append(msg)
        page = resp.get("nextPageToken")
        if not page or not ids:
            break
    return out


def process_profile(profile: str, account_email: str, *, apply: bool, max_results: int) -> dict[str, Any]:
    token = TOKEN_ROOT / profile / "google_token.json"
    if not token.exists():
        return {"profile": profile, "email": account_email, "ok": False, "error": f"missing token {token}"}
    try:
        service = gmail(profile)
        label_cache: dict[str, str | None] = {}
        matches = []
        for msg in list_inbox_messages(service, max_results):
            rule = classify(account_email, msg)
            if not rule:
                continue
            if rule.label not in label_cache:
                label_cache[rule.label] = ensure_label(service, rule.label, apply=apply)
            label_id = label_cache[rule.label]
            h = headers_from_msg(msg)
            action = {
                "id": msg["id"],
                "from": safe(h.get("from"), 100),
                "subject": safe(h.get("subject"), 140),
                "label": rule.label,
                "reason": rule.reason,
                "applied": False,
            }
            if apply and label_id:
                service.users().messages().modify(
                    userId="me",
                    id=msg["id"],
                    body={"addLabelIds": [label_id], "removeLabelIds": ["INBOX"] if rule.remove_inbox else []},
                ).execute()
                action["applied"] = True
            matches.append(action)
        return {"profile": profile, "email": account_email, "ok": True, "apply": apply, "matches": matches, "match_count": len(matches)}
    except RefreshError as exc:
        return {"profile": profile, "email": account_email, "ok": False, "blocked": "auth", "error": safe(exc, 500)}
    except HttpError as exc:
        status = getattr(getattr(exc, "resp", None), "status", None)
        blocked = "permission" if status in {401, 403} else "api"
        return {"profile": profile, "email": account_email, "ok": False, "blocked": blocked, "status": status, "error": safe(exc, 500)}
    except Exception as exc:
        return {"profile": profile, "email": account_email, "ok": False, "blocked": "runtime", "error": safe(exc, 500)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Create labels and move matched source newsletters out of INBOX")
    ap.add_argument("--max-results", type=int, default=250, help="Max Inbox messages to inspect per profile")
    ap.add_argument("--profile", action="append", help="Limit to one or more profile names")
    args = ap.parse_args()

    selected = [(p, e) for p, e in PROFILES if not args.profile or p in set(args.profile)]
    results = [process_profile(p, e, apply=args.apply, max_results=args.max_results) for p, e in selected]
    print(json.dumps({"apply": args.apply, "profiles": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
