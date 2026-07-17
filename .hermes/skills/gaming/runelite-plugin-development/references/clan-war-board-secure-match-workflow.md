# Clan War Board secure match workflow

## Domain contract before routes

Implement and test canonical fight terms before adding authenticated HTTP writes or Cosmos war records. Required terms:

- opponent clan ID
- location
- public OSRS world
- timezone-aware ISO-8601 start time
- combat minimum and maximum
- duration in minutes
- rules

Validate OSRS world range, combat levels 3–126 with min <= max, duration bounds, and text lengths. Normalize time to UTC.

Serialize canonical terms with sorted keys and compact separators, then SHA-256 the UTF-8 JSON. Acceptance is always tied to this `termsHash`, never only a mutable war ID.

State behavior:

```text
proposed -> first clan accepts -> proposed
proposed -> second distinct clan accepts same hash -> confirmed
confirmed -> any term changes -> reconfirm_required
reconfirm_required -> both distinct clans accept new hash -> confirmed
proposed/reconfirm_required -> reject -> rejected
creator -> cancel -> cancelled
```

A counteroffer replaces the terms/hash and clears old acceptance except for the countering clan's acceptance of its own proposal.

## Authority boundary

- A persistent installation UUID provides continuity, not identity proof.
- Hash installation IDs before persistence.
- Return/rotate short-lived installation sessions for abuse control.
- Never include the development pretend-leader/member setting in registration or authority payloads.
- A public RuneLite client can be modified; claimed clan rank is evidence, not cryptographic proof.
- High-impact leader capabilities need server-side approval/verification, expiration, revocation, audit records, rate limits, idempotency, and replay protection.
- Do not expose challenge write routes until the capability check exists.

## Telemetry gate

Do not collect global combat telemetry merely because the player is logged in. Telemetry should start only for a confirmed fight, within its time/world/location window, and include war ID, terms hash, installation/session identity, monotonic sequence, and idempotency fingerprint. Failed batches need bounded retry/backoff and must not be silently discarded.

## Privacy

Member public statistics remain opt-in/private by default. Public worlds are a separate product policy. Opponent identifiers need pseudonymization/retention rules even if the local member opts in.
