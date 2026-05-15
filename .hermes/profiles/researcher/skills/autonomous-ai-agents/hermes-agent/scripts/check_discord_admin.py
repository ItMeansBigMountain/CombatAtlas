#!/usr/bin/env python3
"""Check a Discord bot's effective admin/moderation permissions in a channel.

Required env:
  DISCORD_BOT_TOKEN or DISCORD_TOKEN
Optional env:
  DISCORD_HOME_CHANNEL or DISCORD_HOME_CHANNEL_ID

Usage:
  DISCORD_BOT_TOKEN=... DISCORD_HOME_CHANNEL=... /usr/bin/python3 scripts/check_discord_admin.py
"""
import json
import os
import sys
import urllib.error
import urllib.request


def req(path: str, token: str):
    request = urllib.request.Request(
        "https://discord.com/api/v10" + path,
        headers={"Authorization": "Bot " + token, "User-Agent": "Hermes-permission-check"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as resp:
            data = resp.read().decode()
            return json.loads(data) if data else {}
    except urllib.error.HTTPError as exc:
        return {
            "_http_error": exc.code,
            "body": exc.read().decode(errors="ignore")[:500],
            "path": path,
        }


def main() -> int:
    token = os.getenv("DISCORD_BOT_TOKEN") or os.getenv("DISCORD_TOKEN")
    channel_id = os.getenv("DISCORD_HOME_CHANNEL") or os.getenv("DISCORD_HOME_CHANNEL_ID")
    if not token:
        print(json.dumps({"ok": False, "error": "No DISCORD_BOT_TOKEN/DISCORD_TOKEN found in env"}))
        return 1
    if not channel_id:
        print(json.dumps({"ok": False, "error": "No DISCORD_HOME_CHANNEL/DISCORD_HOME_CHANNEL_ID found in env"}))
        return 1

    me = req("/users/@me", token)
    if "_http_error" in me:
        print(json.dumps({"ok": False, "step": "users/@me", "error": me}, indent=2))
        return 1

    channel = req("/channels/" + str(channel_id), token)
    if "_http_error" in channel:
        print(json.dumps({"ok": False, "step": "channel", "bot": me.get("username"), "error": channel}, indent=2))
        return 1

    guild_id = channel.get("guild_id")
    guild = req("/guilds/" + guild_id, token)
    member = req("/guilds/%s/members/%s" % (guild_id, me["id"]), token)
    roles = req("/guilds/" + guild_id + "/roles", token)
    channels = req("/guilds/" + guild_id + "/channels", token)
    errors = {
        name: value
        for name, value in [("guild", guild), ("member", member), ("roles", roles), ("channels", channels)]
        if isinstance(value, dict) and "_http_error" in value
    }
    if errors:
        print(json.dumps({"ok": False, "bot": me.get("username"), "guild_id": guild_id, "errors": errors}, indent=2))
        return 1

    perms = {
        "kick_members": 1 << 1,
        "ban_members": 1 << 2,
        "administrator": 1 << 3,
        "manage_channels": 1 << 4,
        "manage_guild": 1 << 5,
        "add_reactions": 1 << 6,
        "view_channel": 1 << 10,
        "send_messages": 1 << 11,
        "manage_messages": 1 << 13,
        "embed_links": 1 << 14,
        "attach_files": 1 << 15,
        "read_message_history": 1 << 16,
        "mention_everyone": 1 << 17,
        "manage_roles": 1 << 28,
        "manage_webhooks": 1 << 29,
        "use_application_commands": 1 << 31,
        "manage_threads": 1 << 34,
        "create_public_threads": 1 << 35,
        "create_private_threads": 1 << 36,
        "send_messages_in_threads": 1 << 38,
        "moderate_members": 1 << 40,
    }

    roles_by_id = {r["id"]: r for r in roles}
    perm_bits = int(roles_by_id[guild_id]["permissions"])
    for role_id in member.get("roles", []):
        if role_id in roles_by_id:
            perm_bits |= int(roles_by_id[role_id]["permissions"])

    base_admin = bool(perm_bits & perms["administrator"])
    effective = (1 << 53) - 1 if base_admin else perm_bits
    if not base_admin:
        channel_obj = next((c for c in channels if c["id"] == str(channel_id)), channel)
        chain = []
        if channel_obj.get("parent_id"):
            parent = next((c for c in channels if c["id"] == channel_obj["parent_id"]), None)
            if parent:
                chain.append(parent)
        chain.append(channel_obj)
        for item in chain:
            overwrites = item.get("permission_overwrites", [])
            everyone = next((o for o in overwrites if o.get("id") == guild_id), None)
            if everyone:
                effective &= ~int(everyone.get("deny", "0"))
                effective |= int(everyone.get("allow", "0"))
            allow = deny = 0
            member_roles = set(member.get("roles", []))
            for overwrite in overwrites:
                if overwrite.get("type") == 0 and overwrite.get("id") in member_roles:
                    deny |= int(overwrite.get("deny", "0"))
                    allow |= int(overwrite.get("allow", "0"))
            effective &= ~deny
            effective |= allow
            member_overwrite = next(
                (o for o in overwrites if o.get("type") == 1 and o.get("id") == me["id"]), None
            )
            if member_overwrite:
                effective &= ~int(member_overwrite.get("deny", "0"))
                effective |= int(member_overwrite.get("allow", "0"))

    role_names = [roles_by_id[r]["name"] for r in member.get("roles", []) if r in roles_by_id]
    top_role = max(
        [roles_by_id[r] for r in member.get("roles", []) if r in roles_by_id] + [roles_by_id[guild_id]],
        key=lambda r: int(r.get("position", 0)),
    )
    interesting = [
        "administrator",
        "manage_messages",
        "manage_channels",
        "manage_threads",
        "manage_roles",
        "kick_members",
        "ban_members",
        "moderate_members",
        "manage_guild",
        "manage_webhooks",
        "view_channel",
        "send_messages",
        "read_message_history",
        "create_public_threads",
        "create_private_threads",
        "send_messages_in_threads",
        "add_reactions",
        "attach_files",
        "embed_links",
        "mention_everyone",
        "use_application_commands",
    ]
    print(
        json.dumps(
            {
                "ok": True,
                "bot": me.get("username") + "#" + me.get("discriminator", "0"),
                "bot_id": me["id"],
                "guild": guild.get("name"),
                "guild_id": guild_id,
                "channel": "#" + channel.get("name", ""),
                "channel_id": channel_id,
                "roles": role_names,
                "top_role": top_role.get("name"),
                "base_administrator": base_admin,
                "effective_permissions": {key: bool(effective & perms[key]) for key in interesting},
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
