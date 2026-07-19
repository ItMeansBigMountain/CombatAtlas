# Google OAuth project-scope audit — 2026-07-19

## Audited roots

- `/opt/data/scripts`
- `/opt/data/HeRmEz/projects`
- Google profile registry and active cron helper scripts

Generated/backups/vendor documentation were treated as historical evidence, not active scope requirements.

## Workspace user OAuth scope set

Applied to all five configured Workspace profiles because registry policy is `full_workspace`:

- `https://www.googleapis.com/auth/gmail.readonly`
- `https://www.googleapis.com/auth/gmail.send`
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.settings.basic`
- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/contacts`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/documents`

Coverage: Gmail reporting/sorting/sending/labeling/deleting processed source mail/settings; Calendar CRUD; Drive CRUD; Docs/Sheets CRUD; Contacts CRUD.

## YouTube user OAuth scope set

Applied to the three configured YouTube channel profiles (`trapiistan`, `classicalechos`, `fareed320`):

- `https://www.googleapis.com/auth/youtube`
- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube.force-ssl`
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

Coverage: channel/video management, uploads, metadata/privacy/comments/captions operations, discovery/read probes, and analytics. The broad `youtube` scope was added after the audit found maintained metadata-management code explicitly requesting it.

## Separate credentials (not merged into user URLs)

- `https://www.googleapis.com/auth/cloud-platform` is used with Google service-account credentials for TTS/cloud workloads. It must remain a service-account authorization and is not requested in personal user OAuth consent URLs.
- YouTube source-download cookies are browser session credentials, not OAuth scopes.

## Account-feature map

- `personal-main` (`affan.fareed@gmail.com`): full Workspace.
- `personal-secondary` (`fareed320@gmail.com`): full Workspace plus YouTube channel `A F` through separate YouTube token.
- `trapiistan` (`trapiistan@gmail.com`): full Workspace plus YouTube channel `Sosai Oyama` through separate YouTube token.
- `classicalechos` (`classicalechos@gmail.com`): full Workspace plus YouTube channel `Classical Echos` through separate YouTube token.
- `burner` (`laflametoast@gmail.com`): full Workspace.

## Authorization design

Workspace and YouTube tokens stay separated by token path and are exchanged/verified independently. This prevents a Workspace callback from silently replacing the wrong YouTube channel token and preserves channel-ID verification before token installation.
