# Google Project Permissions and Enabled API Probe

Generated: 2026-05-31T18:13:16.839389Z

Private keys, client secrets, access tokens, and full API keys were not printed or copied.

| Project / credential | Project ID | Principal | Credential path | Mode | IAM roles visible for principal | Enabled APIs visible | API probes | Known purpose |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Workspace / assistant service account | airy-sled-497503-r8 | ai-service@airy-sled-497503-r8.iam.gserviceaccount.com | /opt/data/credentials/google-creds.json | 0o600 | Not visible (api_disabled) | analyticshub.googleapis.com, bigquery.googleapis.com, bigqueryconnection.googleapis.com, bigquerydatapolicy.googleapis.com, bigquerydatatransfer.googleapis.com, bigquerymigration.googleapis.com, bigqueryreservation.googleapis.com, bigquerystorage.googleapis.com, calendar-json.googleapis.com, cloudapis.googleapis.com, cloudtrace.googleapis.com, dataform.googleapis.com, dataplex.googleapis.com, datastore.googleapis.com, docs.googleapis.com, drive.googleapis.com, logging.googleapis.com, monitoring.googleapis.com, people.googleapis.com, servicemanagement.googleapis.com +8 more | Cloud Resource Manager projects.get: API disabled; Service Usage services.list: OK; IAM get project policy: API disabled; Calendar list calendars: OK; Drive about.get: OK; Gmail profile: API disabled; Sheets API discovery-ish spreadsheets.get invalid: API reachable; test resource not found; Docs API invalid doc probe: API reachable; test resource not found; YouTube mostPopular: OK | Workspace-style assistant automation; prior canonical credential |
| Secondary/current env default service account | gen-lang-client-0835809364 | ai-service@gen-lang-client-0835809364.iam.gserviceaccount.com | /opt/data/google_service_account.json | 0o600 | Not visible (api_disabled) | Not visible (api_disabled) | Cloud Resource Manager projects.get: API disabled; Service Usage services.list: API disabled; IAM get project policy: API disabled; Calendar list calendars: OK; Drive about.get: API disabled; Gmail profile: API disabled; Sheets API discovery-ish spreadsheets.get invalid: API disabled; Docs API invalid doc probe: API disabled; YouTube mostPopular: OK | Currently referenced by /opt/data/.env GOOGLE_APPLICATION_CREDENTIALS |
| Legacy tweet/video generator OAuth client | autotweet-357502 | OAuth client ID redacted: 422180951323-ubqn8… | /opt/data/HeRmEz/projects/tweet_video_generator/googleAUTH/cred.json | 0o600 | Cannot inspect with OAuth client JSON alone; needs user OAuth token or Cloud IAM access | Cannot inspect with OAuth client JSON alone | Not run: client secret not used/read; no user OAuth token available | Legacy YouTube/social video OAuth client |

## Raw safe probe results

```json
[
  {
    "credential": {
      "Project / credential": "Workspace / assistant service account",
      "Project ID": "airy-sled-497503-r8",
      "Principal": "ai-service@airy-sled-497503-r8.iam.gserviceaccount.com",
      "Credential path": "/opt/data/credentials/google-creds.json",
      "Mode": "0o600",
      "IAM roles visible for principal": "Not visible (api_disabled)",
      "Enabled APIs visible": "analyticshub.googleapis.com, bigquery.googleapis.com, bigqueryconnection.googleapis.com, bigquerydatapolicy.googleapis.com, bigquerydatatransfer.googleapis.com, bigquerymigration.googleapis.com, bigqueryreservation.googleapis.com, bigquerystorage.googleapis.com, calendar-json.googleapis.com, cloudapis.googleapis.com, cloudtrace.googleapis.com, dataform.googleapis.com, dataplex.googleapis.com, datastore.googleapis.com, docs.googleapis.com, drive.googleapis.com, logging.googleapis.com, monitoring.googleapis.com, people.googleapis.com, servicemanagement.googleapis.com +8 more",
      "API probes": "Cloud Resource Manager projects.get: API disabled; Service Usage services.list: OK; IAM get project policy: API disabled; Calendar list calendars: OK; Drive about.get: OK; Gmail profile: API disabled; Sheets API discovery-ish spreadsheets.get invalid: API reachable; test resource not found; Docs API invalid doc probe: API reachable; test resource not found; YouTube mostPopular: OK",
      "Known purpose": "Workspace-style assistant automation; prior canonical credential"
    },
    "enabled_api_count": 28,
    "enabled_apis": [
      "analyticshub.googleapis.com",
      "bigquery.googleapis.com",
      "bigqueryconnection.googleapis.com",
      "bigquerydatapolicy.googleapis.com",
      "bigquerydatatransfer.googleapis.com",
      "bigquerymigration.googleapis.com",
      "bigqueryreservation.googleapis.com",
      "bigquerystorage.googleapis.com",
      "calendar-json.googleapis.com",
      "cloudapis.googleapis.com",
      "cloudtrace.googleapis.com",
      "dataform.googleapis.com",
      "dataplex.googleapis.com",
      "datastore.googleapis.com",
      "docs.googleapis.com",
      "drive.googleapis.com",
      "logging.googleapis.com",
      "monitoring.googleapis.com",
      "people.googleapis.com",
      "servicemanagement.googleapis.com",
      "serviceusage.googleapis.com",
      "sheets.googleapis.com",
      "sql-component.googleapis.com",
      "storage-api.googleapis.com",
      "storage-component.googleapis.com",
      "storage.googleapis.com",
      "telemetry.googleapis.com",
      "youtube.googleapis.com"
    ],
    "tests": {
      "Cloud Resource Manager projects.get": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "Service Usage services.list": {
        "ok": true,
        "status": 200,
        "reason": null
      },
      "IAM get project policy": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "Calendar list calendars": {
        "ok": true,
        "status": 200,
        "reason": null
      },
      "Drive about.get": {
        "ok": true,
        "status": 200,
        "reason": null
      },
      "Gmail profile": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "Sheets API discovery-ish spreadsheets.get invalid": {
        "ok": false,
        "status": 404,
        "reason": "not_found"
      },
      "Docs API invalid doc probe": {
        "ok": false,
        "status": 404,
        "reason": "not_found"
      },
      "YouTube mostPopular": {
        "ok": true,
        "status": 200,
        "reason": null
      }
    }
  },
  {
    "credential": {
      "Project / credential": "Secondary/current env default service account",
      "Project ID": "gen-lang-client-0835809364",
      "Principal": "ai-service@gen-lang-client-0835809364.iam.gserviceaccount.com",
      "Credential path": "/opt/data/google_service_account.json",
      "Mode": "0o600",
      "IAM roles visible for principal": "Not visible (api_disabled)",
      "Enabled APIs visible": "Not visible (api_disabled)",
      "API probes": "Cloud Resource Manager projects.get: API disabled; Service Usage services.list: API disabled; IAM get project policy: API disabled; Calendar list calendars: OK; Drive about.get: API disabled; Gmail profile: API disabled; Sheets API discovery-ish spreadsheets.get invalid: API disabled; Docs API invalid doc probe: API disabled; YouTube mostPopular: OK",
      "Known purpose": "Currently referenced by /opt/data/.env GOOGLE_APPLICATION_CREDENTIALS"
    },
    "enabled_api_count": 0,
    "enabled_apis": [],
    "tests": {
      "Cloud Resource Manager projects.get": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "Service Usage services.list": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "IAM get project policy": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "Calendar list calendars": {
        "ok": true,
        "status": 200,
        "reason": null
      },
      "Drive about.get": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "Gmail profile": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "Sheets API discovery-ish spreadsheets.get invalid": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "Docs API invalid doc probe": {
        "ok": false,
        "status": 403,
        "reason": "api_disabled"
      },
      "YouTube mostPopular": {
        "ok": true,
        "status": 200,
        "reason": null
      }
    }
  }
]
```
