#!/usr/bin/env python3
"""Unified Google/YouTube reauth workflow for Hermes.

Keeps Workspace profile OAuth and YouTube channel OAuth isolated, generates fresh
PKCE auth URLs, exchanges localhost callbacks, and verifies harmless live probes.
No secrets are printed; only paths, status, emails/channel IDs, and scopes.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

REGISTRY = Path("/opt/data/HeRmEz/projects/_ops/google-email-profiles.json")
WORKSPACE_HELPER = Path("/opt/data/scripts/google_profile_oauth.py")
YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]
YOUTUBE_BASE = Path("/opt/data/secrets")


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def yt_paths(profile: str) -> tuple[dict, Path, Path, Path]:
    reg = load_registry()
    meta = (reg.get("youtube_profiles") or {}).get(profile)
    if not meta:
        raise SystemExit(f"Unknown YouTube profile {profile}. Known: {', '.join((reg.get('youtube_profiles') or {}).keys())}")
    token = Path(meta["token_path"])
    # Default client secret lives next to token; fall back to faceless shared client.
    client = token.parent / "youtube_client_secret.json"
    if not client.exists():
        client = Path("/opt/data/secrets/faceless-youtube-channel/youtube_client_secret.json")
    pending = token.parent / "youtube_oauth_pending.json"
    token.parent.mkdir(parents=True, exist_ok=True)
    return meta, client, token, pending


def make_yt_flow(client: Path, redirect_uri: str | None = None, scopes: list[str] | None = None) -> Flow:
    data = json.loads(client.read_text(encoding="utf-8"))
    obj = data.get("installed") or data.get("web") or {}
    redirect = redirect_uri or (obj.get("redirect_uris") or ["http://localhost:5000/"])[0]
    flow = Flow.from_client_secrets_file(str(client), scopes=scopes or YOUTUBE_SCOPES)
    flow.redirect_uri = redirect
    return flow


def cmd_inventory(args) -> int:
    reg = load_registry()
    out = {"workspace": [], "youtube": []}
    for name, meta in (reg.get("workspace_profiles") or {}).items():
        token = Path(meta["token_path"])
        pending = token.parent / "pending.json"
        out["workspace"].append({"profile": name, "email": meta.get("email"), "token_path": str(token), "has_token": token.exists(), "has_pending": pending.exists(), "access": meta.get("access")})
    for name, meta in (reg.get("youtube_profiles") or {}).items():
        token = Path(meta["token_path"])
        pending = token.parent / "youtube_oauth_pending.json"
        out["youtube"].append({"profile": name, "expected_email": meta.get("email"), "expected_channel_title": meta.get("channel_title"), "expected_channel_id": meta.get("channel_id"), "token_path": str(token), "has_token": token.exists(), "has_pending": pending.exists()})
    print(json.dumps(out, indent=2))
    return 0


def cmd_workspace_auth_url(args) -> int:
    profiles = list((load_registry().get("workspace_profiles") or {}).keys()) if args.all else args.profiles
    if not profiles:
        raise SystemExit("Pass one or more profiles, or --all")
    result = {}
    for profile in profiles:
        proc = subprocess.run([sys.executable, str(WORKSPACE_HELPER), "auth-url", profile], text=True, capture_output=True, check=False)
        if proc.returncode != 0:
            result[profile] = {"status": "failed", "error": proc.stderr.strip() or proc.stdout.strip()}
        else:
            result[profile] = {"status": "pending", "auth_url": proc.stdout.strip(), "callback_format": f"workspace:{profile}: <full localhost URL>"}
    print(json.dumps(result, indent=2))
    return 0


def cmd_workspace_exchange(args) -> int:
    proc = subprocess.run([sys.executable, str(WORKSPACE_HELPER), "auth-code", args.profile, args.callback], text=True, capture_output=True, check=False)
    sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    if proc.returncode == 0 and args.verify:
        return verify_workspace(args.profile)
    return proc.returncode


def cmd_youtube_auth_url(args) -> int:
    profiles = list((load_registry().get("youtube_profiles") or {}).keys()) if args.all else args.profiles
    if not profiles:
        raise SystemExit("Pass one or more profiles, or --all")
    out = {}
    for profile in profiles:
        meta, client, token, pending = yt_paths(profile)
        flow = make_yt_flow(client)
        auth_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="false", prompt="consent", login_hint=meta.get("email"))
        pending.write_text(json.dumps({"profile": profile, "state": state, "redirect_uri": flow.redirect_uri, "client_secret": str(client), "token": str(token), "scopes": YOUTUBE_SCOPES, "code_verifier": getattr(flow, "code_verifier", None)}, indent=2), encoding="utf-8")
        os.chmod(pending, 0o600)
        out[profile] = {"status": "pending", "expected_channel_title": meta.get("channel_title"), "expected_email": meta.get("email"), "token_path": str(token), "auth_url": auth_url, "callback_format": f"youtube:{profile}: <full localhost URL>"}
    print(json.dumps(out, indent=2))
    return 0


def cmd_youtube_exchange(args) -> int:
    meta, client, token, pending = yt_paths(args.profile)
    if not pending.exists():
        raise SystemExit(f"No pending YouTube OAuth for {args.profile}; run youtube-auth-url first")
    data = json.loads(pending.read_text(encoding="utf-8"))
    flow = make_yt_flow(Path(data.get("client_secret") or client), data.get("redirect_uri"), data.get("scopes") or YOUTUBE_SCOPES)
    if data.get("code_verifier"):
        flow.code_verifier = data["code_verifier"]
    os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")
    flow.fetch_token(authorization_response=args.callback)
    token.write_text(flow.credentials.to_json(), encoding="utf-8")
    os.chmod(token, 0o600)
    pending.unlink(missing_ok=True)
    print(json.dumps({"status": "TOKEN_SAVED", "profile": args.profile, "token_path": str(token), "has_refresh_token": bool(flow.credentials.refresh_token)}, indent=2))
    if args.verify:
        return verify_youtube(args.profile)
    return 0


def token_scopes(token: Path, fallback: list[str] | None = None) -> list[str]:
    try:
        data = json.loads(token.read_text(encoding="utf-8"))
        return data.get("scopes") or data.get("scope", "").split() or fallback or []
    except Exception:
        return fallback or []


def verify_workspace(profile: str) -> int:
    reg = load_registry().get("workspace_profiles") or {}
    meta = reg[profile]
    token = Path(meta["token_path"])
    scopes = token_scopes(token)
    creds = Credentials.from_authorized_user_file(str(token), scopes=scopes or None)
    refresh_error = None
    if not creds.valid and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            token.write_text(creds.to_json(), encoding="utf-8")
            os.chmod(token, 0o600)
        except Exception as e:
            refresh_error = f"{type(e).__name__}: {str(e)[:500]}"
    result = {"profile": profile, "expected_email": meta.get("email"), "token_path": str(token), "valid": bool(creds.valid), "probes": {}}
    if refresh_error:
        result["refresh_error"] = refresh_error
        result["next_step"] = f"Run: python3 /opt/data/scripts/google_reauth_workflow.py workspace-auth-url {profile}"
        print(json.dumps(result, indent=2))
        return 1
    try:
        gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)
        prof = gmail.users().getProfile(userId="me").execute()
        result["probes"]["gmail_profile"] = {"emailAddress": prof.get("emailAddress"), "ok": True}
        gmail.users().labels().list(userId="me").execute()
        result["probes"]["gmail_labels"] = {"ok": True}
    except Exception as e:
        result["probes"]["gmail"] = {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}
    for service, version, call in [
        ("calendar", "v3", lambda svc: svc.calendarList().list(maxResults=1).execute()),
        ("drive", "v3", lambda svc: svc.files().list(pageSize=1, fields="files(id,name)").execute()),
    ]:
        try:
            call(build(service, version, credentials=creds, cache_discovery=False))
            result["probes"][service] = {"ok": True}
        except Exception as e:
            result["probes"][service] = {"ok": False, "error": f"{type(e).__name__}: {str(e)[:300]}"}
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


def verify_youtube(profile: str) -> int:
    meta, client, token, pending = yt_paths(profile)
    creds = Credentials.from_authorized_user_file(str(token), scopes=YOUTUBE_SCOPES)
    refresh_error = None
    if not creds.valid and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            token.write_text(creds.to_json(), encoding="utf-8")
            os.chmod(token, 0o600)
        except Exception as e:
            refresh_error = f"{type(e).__name__}: {str(e)[:500]}"
    result = {"profile": profile, "expected_channel_title": meta.get("channel_title"), "expected_channel_id": meta.get("channel_id"), "token_path": str(token), "valid": bool(creds.valid), "scopes": creds.scopes}
    if refresh_error:
        result["refresh_error"] = refresh_error
        result["next_step"] = f"Run: python3 /opt/data/scripts/google_reauth_workflow.py youtube-auth-url {profile}"
        print(json.dumps(result, indent=2))
        return 1
    try:
        yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
        resp = yt.channels().list(part="id,snippet", mine=True).execute()
        items = resp.get("items", [])
        result["channels"] = [{"id": i.get("id"), "title": (i.get("snippet") or {}).get("title")} for i in items]
        expected_id = meta.get("channel_id")
        if str(expected_id or '').startswith('PENDING_') and items:
            chosen = items[0]
            channel_id = chosen.get('id')
            channel_title = (chosen.get('snippet') or {}).get('title')
            reg = load_registry()
            reg.setdefault('youtube_profiles', {}).setdefault(profile, {}).update({
                'channel_id': channel_id,
                'channel_title': channel_title,
            })
            REGISTRY.write_text(json.dumps(reg, indent=2) + '\n', encoding='utf-8')
            meta['channel_id'] = channel_id
            meta['channel_title'] = channel_title
            result['expected_channel_id'] = channel_id
            result['expected_channel_title'] = channel_title
            result['auto_registered_channel'] = True
        result["channel_match"] = any(i.get("id") == meta.get("channel_id") for i in items)
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)[:500]}"
        result["channel_match"] = False
    print(json.dumps(result, indent=2))
    return 0 if result.get("valid") and result.get("channel_match") else 1


def cmd_verify(args) -> int:
    if args.kind == "workspace":
        return verify_workspace(args.profile)
    return verify_youtube(args.profile)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("inventory")
    sp = sub.add_parser("workspace-auth-url"); sp.add_argument("profiles", nargs="*"); sp.add_argument("--all", action="store_true")
    sp = sub.add_parser("workspace-exchange"); sp.add_argument("profile"); sp.add_argument("callback"); sp.add_argument("--no-verify", dest="verify", action="store_false", default=True)
    sp = sub.add_parser("youtube-auth-url"); sp.add_argument("profiles", nargs="*"); sp.add_argument("--all", action="store_true")
    sp = sub.add_parser("youtube-exchange"); sp.add_argument("profile"); sp.add_argument("callback"); sp.add_argument("--no-verify", dest="verify", action="store_false", default=True)
    sp = sub.add_parser("verify"); sp.add_argument("kind", choices=["workspace", "youtube"]); sp.add_argument("profile")
    args = p.parse_args()
    return globals()[f"cmd_{args.cmd.replace('-', '_')}"](args)

if __name__ == "__main__":
    raise SystemExit(main())
