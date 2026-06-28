# Google OAuth reauth URLs — generated 2026-06-27 09:06:21Z

> Non-secret operational handoff. URLs contain one-time pending OAuth state; if one fails or gets stale, regenerate with the workflow below. Do not paste tokens or credential JSON into chat/docs.

## Durability / expiration notes checked against Google docs

- Generated URLs use `access_type=offline` and `prompt=consent` so Google can issue refresh tokens for long-term automated use.
- Google docs say to save refresh tokens in secure long-term storage and use them while valid; refresh tokens can still expire/revoke due to user revocation, security events, testing-mode limits, inactivity, password changes with Gmail scopes, or Google's token policies. So the correct goal is **long-lived + monitored**, not literally impossible to expire.
- Keep OAuth app published/production where possible, keep tokens active with scheduled health checks, and regenerate through this workflow if revoked.

## Return format

After approving each link, browser localhost failure is expected. Copy the entire address-bar URL containing `code=` and send it back with the shown prefix, e.g. `workspace:trapiistan: http://localhost:1/?code=...`.

## Workspace URLs

### personal-secondary — fareed320@gmail.com
Callback prefix: `workspace:personal-secondary:`

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=984335329962-jmsnmsu79o45n751hdguq832dqool860.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A1&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.send+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.modify+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.settings.basic+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdocuments&state=Ujilm2TczPuhWf4DldVIIJArzNMeQb&code_challenge=zRTKDo3_2gUFa6OqzT-hdBt_iCVIHdr6bkmUjTpdgzU&code_challenge_method=S256&access_type=offline&prompt=consent&login_hint=fareed320%40gmail.com

### trapiistan — trapiistan@gmail.com
Callback prefix: `workspace:trapiistan:`

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=984335329962-jmsnmsu79o45n751hdguq832dqool860.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A1&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.send+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.modify+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.settings.basic+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdocuments&state=ik3GeVGmaFMMbGz0lgfJnL5LqRxAhc&code_challenge=pBSGAWY3A8U-I4BN08athxgLv0g6udOan3lhual5oxo&code_challenge_method=S256&access_type=offline&prompt=consent&login_hint=trapiistan%40gmail.com

### classicalechos — classicalechos@gmail.com
Callback prefix: `workspace:classicalechos:`

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=984335329962-jmsnmsu79o45n751hdguq832dqool860.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A1&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.send+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.modify+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.settings.basic+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdocuments&state=uih937KHVkGYPGP1NSEPMWQBv3ANk2&code_challenge=ca5qSQO--r_QyzbWdCMn1IVsgie-r14TdMcvroZ5bAY&code_challenge_method=S256&access_type=offline&prompt=consent&login_hint=classicalechos%40gmail.com

### burner — laflametoast@gmail.com
Callback prefix: `workspace:burner:`

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=984335329962-jmsnmsu79o45n751hdguq832dqool860.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A1&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.send+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.modify+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.settings.basic+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdocuments&state=mQLdF5kaaBeG8geCGaB5kXdLVhEwuR&code_challenge=_YgsambTeZD8aAhbVRJTV3ak7OA0bP-tYAMdnWEzCYM&code_challenge_method=S256&access_type=offline&prompt=consent&login_hint=laflametoast%40gmail.com

### personal-main — affan.fareed@gmail.com
Callback prefix: `workspace:personal-main:`

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=984335329962-jmsnmsu79o45n751hdguq832dqool860.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A1&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.send+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.modify+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.settings.basic+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcontacts+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdocuments&state=qoIX1E98OwUkooFmIFAnznD46t0A8R&code_challenge=d28g5DFcADYqelktVzN4hLOAjRZXufmpwEEELLj-i5U&code_challenge_method=S256&access_type=offline&prompt=consent&login_hint=affan.fareed%40gmail.com

## YouTube URLs

### trapiistan — expected channel: Sosai Oyama (trapiistan@gmail.com)
Token path: `/opt/data/secrets/youtube-trapiistan/youtube_upload_token.json`
Callback prefix: `youtube:trapiistan:`

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=471944085234-kgi6lv4ib5lvfcdiarv2olg6gratiduj.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyt-analytics.readonly&state=UYX3cDJLsjhxjrZLK1JcNyTDARB3L0&code_challenge=poptvzrp9CStzW-ihDMnGQErhsX53QWfVjBYvQNwI08&code_challenge_method=S256&access_type=offline&include_granted_scopes=false&prompt=consent&login_hint=trapiistan%40gmail.com

### classicalechos — expected channel: Classical Echos (classicalechos@gmail.com)
Token path: `/opt/data/secrets/youtube-classicalechos/youtube_upload_token.json`
Callback prefix: `youtube:classicalechos:`

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=471944085234-kgi6lv4ib5lvfcdiarv2olg6gratiduj.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.force-ssl+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyt-analytics.readonly&state=e3oWL322Od4oKt1JPUL07GJfqFCrzZ&code_challenge=mLLHPXJYNGXG4e13V4AqRyjx_WGyJOsDis9d347bWy8&code_challenge_method=S256&access_type=offline&include_granted_scopes=false&prompt=consent&login_hint=classicalechos%40gmail.com

## Workflow to find/regenerate/exchange/verify

Persistent file path:

```text
/opt/data/HeRmEz/projects/_ops/google-oauth-reauth-current.md
```

Find it later:

```bash
cd /opt/data/HeRmEz
python3 /opt/data/scripts/google_reauth_workflow.py inventory
sed -n '1,220p' projects/_ops/google-oauth-reauth-current.md
```

Regenerate a stale link:

```bash
python3 /opt/data/scripts/google_reauth_workflow.py workspace-auth-url <profile>
python3 /opt/data/scripts/google_reauth_workflow.py youtube-auth-url <profile>
```

Exchange callbacks:

```bash
python3 /opt/data/scripts/google_reauth_workflow.py workspace-exchange <profile> '<full localhost URL>'
python3 /opt/data/scripts/google_reauth_workflow.py youtube-exchange <profile> '<full localhost URL>'
```

Verify after exchange:

```bash
python3 /opt/data/scripts/google_reauth_workflow.py verify workspace <profile>
python3 /opt/data/scripts/google_reauth_workflow.py verify youtube <profile>
```
