#!/usr/bin/env python3
"""Profile-scoped Google OAuth helper for Hermes.

Stores each account's pending PKCE state and token separately:
  /opt/data/google_profiles/<profile>/pending.json
  /opt/data/google_profiles/<profile>/google_token.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

CLIENT_SECRET_PATH = Path("/opt/data/google_client_secret.json")
PROFILES_PATH = Path("/opt/data/HeRmEz/projects/_ops/google-email-profiles.json")
BASE_DIR = Path("/opt/data/google_profiles")
REDIRECT_URI = "http://localhost:1"
FULL_WORKSPACE_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
]

GMAIL_READ_ONLY_WORKSPACE_ADMIN_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
]

READ_ONLY_WORKSPACE_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
]


def scopes_for_profile(profile: str, meta: dict) -> list[str]:
    access = meta.get("access", "")
    if access == "gmail_read_only_workspace_admin":
        return GMAIL_READ_ONLY_WORKSPACE_ADMIN_SCOPES
    if profile == "personal-main" or access == "read_only_workspace":
        return READ_ONLY_WORKSPACE_SCOPES
    return FULL_WORKSPACE_SCOPES


def profile_dir(profile: str) -> Path:
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", profile):
        raise SystemExit("Profile must be alphanumeric plus -/_ only")
    d = BASE_DIR / profile
    d.mkdir(parents=True, exist_ok=True)
    os.chmod(d, 0o700)
    return d


def load_profiles() -> dict:
    if not PROFILES_PATH.exists():
        raise SystemExit(f"Missing profile registry: {PROFILES_PATH}")
    data = json.loads(PROFILES_PATH.read_text())
    return data.get("profiles") or data.get("workspace_profiles") or {}


def normalize_token(payload: dict) -> dict:
    payload = dict(payload)
    payload.setdefault("type", "authorized_user")
    return payload


def extract_code_and_state(code_or_url: str) -> tuple[str, str | None, list[str] | None]:
    if not code_or_url.startswith("http"):
        return code_or_url, None, None
    parsed = urlparse(code_or_url)
    params = parse_qs(parsed.query)
    if "code" not in params:
        raise SystemExit("No code= parameter found in redirect URL")
    granted = None
    scope_val = (params.get("scope") or [""])[0].strip()
    if scope_val:
        granted = scope_val.split()
    return params["code"][0], params.get("state", [None])[0], granted


def auth_url(profile: str) -> None:
    if not CLIENT_SECRET_PATH.exists():
        raise SystemExit(f"Missing client secret: {CLIENT_SECRET_PATH}")
    profiles = load_profiles()
    if profile not in profiles:
        raise SystemExit(f"Unknown profile {profile}. Known: {', '.join(profiles)}")
    email = profiles[profile]["email"]
    scopes = scopes_for_profile(profile, profiles[profile])

    from google_auth_oauthlib.flow import Flow

    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRET_PATH),
        scopes=scopes,
        redirect_uri=REDIRECT_URI,
        autogenerate_code_verifier=True,
    )
    url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        login_hint=email,
    )
    d = profile_dir(profile)
    pending = {
        "profile": profile,
        "email": email,
        "state": state,
        "code_verifier": flow.code_verifier,
        "redirect_uri": REDIRECT_URI,
        "scopes": scopes,
    }
    pending_path = d / "pending.json"
    pending_path.write_text(json.dumps(pending, indent=2))
    os.chmod(pending_path, 0o600)
    print(url)


def auth_code(profile: str, callback: str) -> None:
    d = profile_dir(profile)
    pending_path = d / "pending.json"
    if not pending_path.exists():
        raise SystemExit(f"No pending OAuth for {profile}; run auth-url first")
    pending = json.loads(pending_path.read_text())
    code, returned_state, granted = extract_code_and_state(callback)
    if returned_state and returned_state != pending["state"]:
        raise SystemExit("OAuth state mismatch; generate a fresh URL for this profile")

    from google_auth_oauthlib.flow import Flow

    scopes = granted or pending.get("scopes") or []
    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRET_PATH),
        scopes=scopes,
        redirect_uri=pending.get("redirect_uri", REDIRECT_URI),
        state=pending["state"],
        code_verifier=pending["code_verifier"],
    )
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    flow.fetch_token(code=code)
    token_payload = normalize_token(json.loads(flow.credentials.to_json()))
    token_payload["hermes_profile"] = profile
    token_payload["expected_email"] = pending.get("email")
    if getattr(flow.credentials, "granted_scopes", None):
        token_payload["scopes"] = list(flow.credentials.granted_scopes)
    elif granted:
        token_payload["scopes"] = granted
    token_path = d / "google_token.json"
    token_path.write_text(json.dumps(token_payload, indent=2))
    os.chmod(token_path, 0o600)
    pending_path.unlink(missing_ok=True)
    print(json.dumps({"status": "authenticated", "profile": profile, "expected_email": pending.get("email"), "token_path": str(token_path)}, indent=2))


def list_profiles() -> None:
    profiles = load_profiles()
    out = []
    for name, meta in profiles.items():
        d = profile_dir(name)
        out.append({
            "profile": name,
            "email": meta["email"],
            "has_token": (d / "google_token.json").exists(),
            "has_pending": (d / "pending.json").exists(),
            "token_path": str(d / "google_token.json"),
        })
    print(json.dumps(out, indent=2))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("auth-url")
    p.add_argument("profile")
    p = sub.add_parser("auth-code")
    p.add_argument("profile")
    p.add_argument("callback")
    sub.add_parser("list")
    args = ap.parse_args()
    if args.cmd == "auth-url":
        auth_url(args.profile)
    elif args.cmd == "auth-code":
        auth_code(args.profile, args.callback)
    elif args.cmd == "list":
        list_profiles()


if __name__ == "__main__":
    main()
