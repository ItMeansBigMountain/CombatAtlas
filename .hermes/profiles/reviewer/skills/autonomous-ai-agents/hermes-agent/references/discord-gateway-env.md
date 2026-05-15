# Discord gateway env/config verification notes

Use when configuring Hermes Agent Discord gateway and the token is expected to be present.

Observed workflow/pitfalls:

1. Do not print Discord tokens. Detect only env var names or boolean presence.

2. In hosted/profiled Hermes environments, `hermes` may not be on `PATH` even though Hermes is installed. If `hermes config ...` fails with `No such file or directory`, check:

```bash
python3 - <<'PY'
import importlib.util, os, shutil
print('HERMES_HOME=', os.getenv('HERMES_HOME'))
print('hermes_exe=', shutil.which('hermes'))
print('hermes_cli_module=', bool(importlib.util.find_spec('hermes_cli')))
PY
```

If `/opt/hermes/.venv/bin/python` exists, use:

```bash
cd /opt/hermes
/opt/hermes/.venv/bin/python -m hermes_cli.main config check
/opt/hermes/.venv/bin/python -m hermes_cli.main gateway status
/opt/hermes/.venv/bin/python -m hermes_cli.main gateway run
```

If this is the official Docker image and the current user is root, `gateway run` may refuse with:

```text
Refusing to run the Hermes gateway as root inside the official Docker image.
```

Prefer running as the `hermes` user and make sure `$HERMES_HOME` is readable by that user:

```bash
chown -R hermes:hermes /opt/data
chmod 700 /opt/data
chmod 600 /opt/data/.env /opt/data/config.yaml
cd /opt/hermes
runuser -u hermes -- sh -lc 'set -a; . /opt/data/.env; set +a; /opt/hermes/.venv/bin/python -m hermes_cli.main gateway run'
```

If policy blocks `runuser`, do not retry blindly; report that the gateway is configured but must be started by the user/admin, or use the container entrypoint/service mechanism. `HERMES_ALLOW_ROOT_GATEWAY=1` exists but is a last resort because it can create root-owned files in `$HERMES_HOME`.

If the user explicitly wants Discord Hermes to have privileged local control while the gateway still runs as the non-root `hermes` user, configure passwordless sudo rather than running the gateway as root:

```bash
# Debian/Ubuntu official image example, run as root/admin
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y sudo
mkdir -p /etc/sudoers.d
printf '%s\n' 'hermes ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/90-hermes-nopasswd
chmod 0440 /etc/sudoers.d/90-hermes-nopasswd
visudo -cf /etc/sudoers
visudo -cf /etc/sudoers.d/90-hermes-nopasswd
usermod -aG sudo hermes
runuser -u hermes -- sudo -n true
runuser -u hermes -- sudo -n id
```

The sudoers file is the effective grant; adding the `sudo` group is useful for shell/session consistency but not required for the explicit `hermes ALL=(ALL) NOPASSWD:ALL` line. Verify non-interactive `sudo -n` succeeds before telling the user Discord has root-equivalent command capability.

3. `python` may not exist; use `python3` for system probes, or `/opt/hermes/.venv/bin/python` for Hermes commands because it has dependencies such as `yaml` installed.

4. Hermes config/env paths in this hosted layout commonly are:

```text
HERMES_HOME=/opt/data
config: /opt/data/config.yaml
env: /opt/data/.env
source: /opt/hermes
```

5. `hermes config check` lists `DISCORD_BOT_TOKEN` as optional and can pass even when Discord cannot connect. Explicitly source the env file and check boolean token presence:

```bash
set -a; . /opt/data/.env; set +a
/opt/hermes/.venv/bin/python - <<'PY'
import os, yaml
cfg=yaml.safe_load(open('/opt/data/config.yaml'))
d=cfg.get('discord', {})
print('config_yaml_parse=ok')
print('DISCORD_BOT_TOKEN_visible_to_gateway_env=' + str(bool(os.getenv('DISCORD_BOT_TOKEN'))))
print('GATEWAY_ALLOW_ALL_USERS=' + str(os.getenv('GATEWAY_ALLOW_ALL_USERS')))
print('toolsets=' + ','.join(cfg.get('toolsets', [])))
print('discord.require_mention=' + str(d.get('require_mention')))
print('discord.server_actions=' + repr(d.get('server_actions')))
print('discord.allow_mentions.everyone=' + str(d.get('allow_mentions', {}).get('everyone')))
print('discord.allow_mentions.roles=' + str(d.get('allow_mentions', {}).get('roles')))
PY
```

Expected for private full-control Discord setup:

```text
DISCORD_BOT_TOKEN_visible_to_gateway_env=True
GATEWAY_ALLOW_ALL_USERS=true
toolsets includes discord,discord_admin
discord.require_mention=False
discord.server_actions=''
discord.allow_mentions.everyone=False
discord.allow_mentions.roles=False
```

6. If the user says a token is in environment variables but it is not visible, check all current process env names without values:

```bash
env | cut -d= -f1 | sort | grep -Ei 'discord|bot|hermes|token' || true
```

If no Discord token appears, the token was not injected into this process or not written to the Hermes env file. Ask the user to put it in `/opt/data/.env` as `DISCORD_BOT_TOKEN=...` or restart the launching environment so the gateway process sees it.

7. To answer “what Discord bot options can I configure?”, ground the answer in the live source/config rather than memory. Useful probes:

```bash
# Current configured Discord block and set env var names (hide values)
set -a; . /opt/data/.env; set +a
/opt/hermes/.venv/bin/python - <<'PY'
import os, yaml
cfg=yaml.safe_load(open('/opt/data/config.yaml'))
print('Current discord config.yaml:')
for k, v in cfg.get('discord', {}).items():
    print(f'  {k}: {v!r}')
print('Current Discord env vars set (values hidden):')
for k in sorted(os.environ):
    if 'DISCORD' in k or k.startswith('HERMES_DISCORD') or k == 'GATEWAY_ALLOW_ALL_USERS':
        print(f'  {k}=<set>')
PY

# Discover supported env knobs from the installed Hermes source
/opt/hermes/.venv/bin/python - <<'PY'
from pathlib import Path
import re
files = [
  '/opt/hermes/gateway/platforms/discord.py',
  '/opt/hermes/gateway/config.py',
  '/opt/hermes/gateway/run.py',
  '/opt/hermes/hermes_cli/config.py',
]
vars = set()
for p in files:
    txt = Path(p).read_text(errors='ignore')
    vars.update(re.findall(r'os\\.getenv\\(["\\']([A-Z0-9_]*DISCORD[A-Z0-9_]*)["\\']', txt))
    vars.update(re.findall(r'get_env_value\\(["\\']([A-Z0-9_]*DISCORD[A-Z0-9_]*)["\\']', txt))
    vars.update(re.findall(r'"([A-Z0-9_]*DISCORD[A-Z0-9_]*)"', txt))
print('\n'.join(sorted(vars)))
PY
```

Common Discord config/env knobs found in Hermes:

- Connection/delivery: `DISCORD_BOT_TOKEN`, `DISCORD_PROXY`, `DISCORD_HOME_CHANNEL`, `DISCORD_HOME_CHANNEL_NAME`, `DISCORD_HOME_CHANNEL_THREAD_ID`.
- Access control: `GATEWAY_ALLOW_ALL_USERS`, `DISCORD_ALLOW_ALL_USERS`, `DISCORD_ALLOWED_USERS`, `DISCORD_ALLOWED_ROLES`, `DISCORD_ALLOW_BOTS`; `discord.dm_role_auth_guild` in YAML extends role auth to DMs for one trusted guild.
- Response routing: `discord.require_mention`/`DISCORD_REQUIRE_MENTION`, `discord.free_response_channels`/`DISCORD_FREE_RESPONSE_CHANNELS`, `discord.allowed_channels`/`DISCORD_ALLOWED_CHANNELS`, `discord.ignored_channels`/`DISCORD_IGNORED_CHANNELS`, `discord.no_thread_channels`/`DISCORD_NO_THREAD_CHANNELS`, `DISCORD_IGNORE_NO_MENTION`.
- Thread/reply behavior: `discord.auto_thread`/`DISCORD_AUTO_THREAD`, `discord.reply_to_mode` or `DISCORD_REPLY_TO_MODE=off|first|all`. For natural back-and-forth channel chat (the user's preferred Discord UX), set `discord.auto_thread: false`, keep `discord.require_mention: false` if they want free-response, and set `discord.reply_to_mode: off` so replies appear as normal channel messages instead of Discord reply-chain messages; restart the gateway and verify reconnect.
- Processing reactions: `discord.reactions`/`DISCORD_REACTIONS`.
- Mention safety: `discord.allow_mentions.everyone|roles|users|replied_user` mapping to `DISCORD_ALLOW_MENTION_EVERYONE|ROLES|USERS|REPLIED_USER`; keep everyone/roles false unless explicitly requested.
- Channel prompts: `discord.channel_prompts` keyed by channel ID; forum parents apply to child threads.
- Discord admin tool scope: `discord.server_actions`; empty string means all actions. Known actions include `list_guilds`, `server_info`, `list_channels`, `channel_info`, `list_roles`, `member_info`, `search_members`, `fetch_messages`, `list_pins`, `pin_message`, `unpin_message`, `create_thread`, `add_role`, `remove_role`.
- Slash commands: `DISCORD_COMMAND_SYNC_POLICY=safe|bulk|off`, `DISCORD_HIDE_SLASH_COMMANDS=true|false`.
- Text batching: `HERMES_DISCORD_TEXT_BATCH_DELAY_SECONDS`, `HERMES_DISCORD_TEXT_BATCH_SPLIT_DELAY_SECONDS`.

8. To verify whether Hermes-side admin access is unrestricted versus Discord-side permissions are actually granted, check both layers. Hermes-side `discord.server_actions: ''` means the agent exposes all Discord admin tool actions, but it does not grant Discord guild permissions. Use the bot token only through the Discord API and never print it:

```bash
set -a; . /opt/data/.env; set +a
/opt/hermes/.venv/bin/python - <<'PY'
import os, urllib.request, json
TOKEN=os.environ['DISCORD_BOT_TOKEN']
def get(path):
    req=urllib.request.Request('https://discord.com/api/v10'+path, headers={'Authorization':'Bot '+TOKEN})
    with urllib.request.urlopen(req) as r:
        return json.load(r)
me=get('/users/@me')
print('bot=' + me['username'] + '#' + me.get('discriminator','0'))
print('client_id=' + me['id'])
print('invite_admin_url=https://discord.com/oauth2/authorize?client_id=%s&permissions=8&scope=bot+applications.commands' % me['id'])
print('guilds=' + ','.join(g['name'] + ':' + g['id'] for g in get('/users/@me/guilds')))
PY
```

For an exact channel-level permission answer, fetch the guild/member/channel and compute overwrites with Discord permission bit constants. Key bits: `administrator=1<<3`, `manage_channels=1<<4`, `manage_roles=1<<28`, `manage_messages=1<<13`, `manage_threads=1<<34`, `kick_members=1<<1`, `ban_members=1<<2`, plus communication bits such as `view_channel=1<<10`, `send_messages=1<<11`, `read_message_history=1<<16`, `create_public_threads=1<<35`, `create_private_threads=1<<36`, `send_messages_in_threads=1<<38`. If the bot's top role is only `@everyone` and these admin bits are false, it cannot escalate itself; the user must update the invite/role in Discord. Administrator invite URL format: `https://discord.com/oauth2/authorize?client_id=<bot_id>&permissions=8&scope=bot+applications.commands`.

When summarizing capabilities, be explicit about both boundaries: Discord permissions are determined by Discord guild roles/channel overwrites, while local machine permissions are those of the gateway process user. If passwordless sudo was configured for `hermes`, Discord commands can escalate locally with `sudo`; otherwise they cannot silently do root-only operations.
