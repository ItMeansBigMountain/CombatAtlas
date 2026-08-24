from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any


class ImportValidationError(ValueError):
    pass


def _id() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require(obj: dict[str, Any], fields: tuple[str, ...], scope: str) -> None:
    for field in fields:
        if obj.get(field) in (None, ""):
            raise ImportValidationError(f"{scope}.{field} is required")


def _validate(bundle: dict[str, Any]) -> None:
    _require(bundle, ("provider", "schedule", "items", "rules"), "bundle")
    provider = bundle["provider"]
    schedule = bundle["schedule"]
    _require(provider, ("external_id", "name", "source_type", "license_classification"), "provider")
    _require(schedule, ("external_version", "source_url", "effective_from", "retrieved_at", "region", "applicability", "confidence"), "schedule")
    confidence = {"unknown", "low", "medium", "high", "verified"}
    triggers = {"mileage_only", "time_only", "whichever_first", "both"}
    severities = {"normal", "severe", "all", "unknown"}
    recurrences = {"repeating", "one_time"}
    if schedule["confidence"] not in confidence:
        raise ImportValidationError("schedule.confidence is invalid")
    item_ids = set()
    for i, item in enumerate(bundle["items"]):
        _require(item, ("external_id", "name", "category"), f"items[{i}]")
        if item["external_id"] in item_ids:
            raise ImportValidationError("duplicate item external_id")
        item_ids.add(item["external_id"])
    for i, rule in enumerate(bundle["rules"]):
        _require(rule, ("external_id", "service_item_external_id", "trigger_mode", "usage_severity", "applicability", "confidence"), f"rules[{i}]")
        if rule["service_item_external_id"] not in item_ids:
            raise ImportValidationError(f"rules[{i}] references unknown service item")
        if rule["trigger_mode"] not in triggers or rule["usage_severity"] not in severities or rule["confidence"] not in confidence:
            raise ImportValidationError(f"rules[{i}] contains an invalid enum")
        if rule.get("recurrence", "repeating") not in recurrences:
            raise ImportValidationError(f"rules[{i}].recurrence is invalid")
        for tolerance in ("mileage_tolerance", "time_tolerance_days"):
            if not isinstance(rule.get(tolerance, 0), int) or rule.get(tolerance, 0) < 0:
                raise ImportValidationError(f"rules[{i}].{tolerance} must be a non-negative integer")
        has_miles = bool(rule.get("mileage_interval"))
        has_time = bool(rule.get("time_interval_months"))
        required = {"mileage_only": (True, False), "time_only": (False, True), "whichever_first": (True, True), "both": (True, True)}
        if (has_miles, has_time) != required[rule["trigger_mode"]]:
            raise ImportValidationError(f"rules[{i}] trigger values do not match trigger_mode")


def import_schedule_bundle(connection: sqlite3.Connection, bundle: dict[str, Any]) -> dict[str, int]:
    _validate(bundle)
    provider = bundle["provider"]
    schedule = bundle["schedule"]
    canonical = json.dumps(bundle, sort_keys=True, separators=(",", ":"))
    content_hash = hashlib.sha256(canonical.encode()).hexdigest()
    with connection:
        row = connection.execute("SELECT id FROM schedule_providers WHERE external_id=?", (provider["external_id"],)).fetchone()
        provider_id = row[0] if row else _id()
        if not row:
            connection.execute(
                "INSERT INTO schedule_providers(id, external_id, name, source_type, license_classification, terms_uri, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (provider_id, provider["external_id"], provider["name"], provider["source_type"], provider["license_classification"], provider.get("terms_uri"), _now()),
            )
        row = connection.execute(
            "SELECT id, content_hash FROM schedule_versions WHERE provider_id=? AND external_version=?",
            (provider_id, schedule["external_version"]),
        ).fetchone()
        if row and row[1] != content_hash:
            raise ImportValidationError("published schedule version is immutable; use a new external_version")
        version_id = row[0] if row else _id()
        if not row:
            connection.execute(
                "INSERT INTO schedule_versions(id, provider_id, external_version, source_url, effective_from, effective_to, retrieved_at, region, applicability_json, license_classification, confidence, content_hash, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (version_id, provider_id, schedule["external_version"], schedule["source_url"], schedule["effective_from"], schedule.get("effective_to"), schedule["retrieved_at"], schedule["region"], json.dumps(schedule["applicability"], sort_keys=True), provider["license_classification"], schedule["confidence"], content_hash, _now()),
            )
        item_map = {}
        for item in bundle["items"]:
            row = connection.execute("SELECT id FROM service_items WHERE provider_id=? AND external_id=?", (provider_id, item["external_id"])).fetchone()
            item_id = row[0] if row else _id()
            if not row:
                connection.execute(
                    "INSERT INTO service_items(id, provider_id, external_id, name, category, description, canonical_key) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (item_id, provider_id, item["external_id"], item["name"], item["category"], item.get("description"), item.get("canonical_key")),
                )
            item_map[item["external_id"]] = item_id
        for rule in bundle["rules"]:
            exists = connection.execute("SELECT 1 FROM interval_rules WHERE schedule_version_id=? AND external_id=?", (version_id, rule["external_id"])).fetchone()
            if not exists:
                connection.execute(
                    "INSERT INTO interval_rules(id, schedule_version_id, service_item_id, external_id, trigger_mode, mileage_interval, time_interval_months, initial_mileage, initial_months, usage_severity, applicability_json, confidence, source_note, recurrence, mileage_tolerance, time_tolerance_days) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (_id(), version_id, item_map[rule["service_item_external_id"]], rule["external_id"], rule["trigger_mode"], rule.get("mileage_interval"), rule.get("time_interval_months"), rule.get("initial_mileage"), rule.get("initial_months"), rule["usage_severity"], json.dumps(rule["applicability"], sort_keys=True), rule["confidence"], rule.get("source_note"), rule.get("recurrence", "repeating"), rule.get("mileage_tolerance", 0), rule.get("time_tolerance_days", 0)),
                )
    return {"service_items": len(bundle["items"]), "interval_rules": len(bundle["rules"])}
