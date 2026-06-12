#!/usr/bin/env python3
"""YouTube upload OAuth helper for headless VPS flows.

Usage:
  python3 scripts/youtube_oauth.py preflight
  python3 scripts/youtube_oauth.py auth-url
  python3 scripts/youtube_oauth.py exchange "http://localhost:5000/?code=..."
  python3 scripts/youtube_oauth.py check
"""
from __future__ import annotations

import argparse, json, os, pathlib, sys
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]
SCOPE = " ".join(SCOPES)
DEFAULT_CLIENT = "/opt/data/secrets/faceless-youtube-channel/youtube_client_secret.json"
DEFAULT_TOKEN = "/opt/data/secrets/faceless-youtube-channel/youtube_upload_token.json"
PENDING = "/opt/data/secrets/faceless-youtube-channel/youtube_oauth_pending.json"


def paths(args):
    client = pathlib.Path(args.client_secret or os.getenv("YOUTUBE_UPLOAD_CLIENT_SECRET") or DEFAULT_CLIENT)
    token = pathlib.Path(args.token or os.getenv("YOUTUBE_UPLOAD_TOKEN") or DEFAULT_TOKEN)
    pending = pathlib.Path(args.pending or PENDING)
    token.parent.mkdir(parents=True, exist_ok=True)
    pending.parent.mkdir(parents=True, exist_ok=True)
    return client, token, pending


def client_metadata(path: pathlib.Path):
    data = json.loads(path.read_text())
    obj = data.get("installed") or data.get("web") or {}
    return {
        "exists": path.exists(),
        "type": "installed" if "installed" in data else "web" if "web" in data else "unknown",
        "project_id": obj.get("project_id"),
        "client_id_prefix": (obj.get("client_id") or "")[:12] + "...",
        "redirect_uri": (obj.get("redirect_uris") or ["http://localhost:5000/"])[0],
    }


def make_flow(client: pathlib.Path, redirect_uri: str | None = None):
    meta = client_metadata(client)
    flow = Flow.from_client_secrets_file(str(client), scopes=SCOPES)
    flow.redirect_uri = redirect_uri or meta["redirect_uri"] or "http://localhost:5000/"
    return flow


def load_creds(token: pathlib.Path):
    if not token.exists():
        return None
    return Credentials.from_authorized_user_file(str(token), scopes=SCOPES)


def save_creds(creds, token: pathlib.Path):
    token.write_text(creds.to_json())
    os.chmod(token, 0o600)


def cmd_preflight(args):
    client, token, pending = paths(args)
    meta = client_metadata(client) if client.exists() else {"exists": False}
    print(json.dumps({
        "client_secret": {"path": str(client), **meta},
        "token": {"path": str(token), "exists": token.exists()},
        "pending": {"path": str(pending), "exists": pending.exists()},
        "scope": SCOPE,
    }, indent=2))


def cmd_auth_url(args):
    client, token, pending = paths(args)
    flow = make_flow(client)
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="false",
        prompt="consent",
    )
    pending.write_text(json.dumps({
        "state": state,
        "redirect_uri": flow.redirect_uri,
        "client_secret": str(client),
        "token": str(token),
        # google-auth-oauthlib auto-generates PKCE code_verifier for web clients.
        # Persist it so a headless second process can exchange the returned code.
        "code_verifier": getattr(flow, "code_verifier", None),
    }, indent=2))
    os.chmod(pending, 0o600)
    print(json.dumps({"auth_url": auth_url, "redirect_uri": flow.redirect_uri, "scope": SCOPE}, indent=2))


def cmd_exchange(args):
    client, token, pending = paths(args)
    if pending.exists():
        data = json.loads(pending.read_text())
        client = pathlib.Path(data.get("client_secret") or client)
        token = pathlib.Path(data.get("token") or token)
        redirect_uri = data.get("redirect_uri")
        code_verifier = data.get("code_verifier")
    else:
        redirect_uri = None
        code_verifier = None
    flow = make_flow(client, redirect_uri)
    if code_verifier:
        flow.code_verifier = code_verifier
    flow.fetch_token(authorization_response=args.authorization_response)
    save_creds(flow.credentials, token)
    if pending.exists(): pending.unlink()
    print(json.dumps({"status": "TOKEN_SAVED", "token_path": str(token), "has_refresh_token": bool(flow.credentials.refresh_token)}, indent=2))


def cmd_check(args):
    client, token, pending = paths(args)
    creds = load_creds(token)
    if not creds:
        print(json.dumps({"status":"MISSING_TOKEN", "token_path": str(token)}, indent=2)); return 2
    try:
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            save_creds(creds, token)
        yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
        # youtube.upload scope cannot necessarily read private channel data; this checks service creation + token refresh.
        print(json.dumps({"status":"READY", "valid": bool(creds.valid), "scopes": creds.scopes}, indent=2))
    except Exception as e:
        print(json.dumps({"status":"FAILED", "error_type": type(e).__name__, "error": str(e)[:1000]}, indent=2))
        return 1
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--client-secret")
    p.add_argument("--token")
    p.add_argument("--pending")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("preflight")
    sub.add_parser("auth-url")
    ex = sub.add_parser("exchange"); ex.add_argument("authorization_response")
    sub.add_parser("check")
    args = p.parse_args()
    rc = globals()[f"cmd_{args.cmd.replace('-', '_')}"](args)
    raise SystemExit(rc or 0)
if __name__ == "__main__": main()
