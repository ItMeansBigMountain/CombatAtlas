from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from types import MappingProxyType
from typing import Mapping, Sequence


_CONFIDENCE_ORDER = ("unknown", "low", "medium", "high", "verified")


@dataclass(frozen=True)
class ScheduleSource:
    provider_id: str
    provider_name: str
    schedule_version: str
    source_url: str
    source_type: str


@dataclass(frozen=True)
class ScheduleRule:
    rule_id: str
    item_id: str
    item_name: str
    provider_id: str
    provider_name: str
    schedule_version: str
    source_url: str
    source_type: str
    confidence: str
    severity: str
    trigger_mode: str
    applicability: Mapping[str, object]
    mileage_interval: int | None = None
    time_interval_months: int | None = None
    initial_mileage: int | None = None
    initial_months: int | None = None
    recurrence: str = "repeating"
    mileage_tolerance: int = 0
    time_tolerance_days: int = 0

    def __post_init__(self) -> None:
        if self.trigger_mode not in {"mileage_only", "time_only", "whichever_first", "both"}:
            raise ValueError("invalid trigger mode")
        if self.recurrence not in {"repeating", "one_time"}:
            raise ValueError("invalid recurrence")
        if self.confidence not in _CONFIDENCE_ORDER:
            raise ValueError("invalid confidence")
        if self.mileage_interval is not None and self.mileage_interval <= 0:
            raise ValueError("mileage interval must be positive")
        if self.time_interval_months is not None and self.time_interval_months <= 0:
            raise ValueError("time interval must be positive")
        object.__setattr__(self, "applicability", MappingProxyType(dict(self.applicability)))


@dataclass(frozen=True)
class VehicleSnapshot:
    vehicle_id: str
    odometer_miles: int | None
    as_of: date
    in_service_date: date | None
    usage_severity: str
    applicability: Mapping[str, object]

    def __post_init__(self) -> None:
        if self.odometer_miles is not None and self.odometer_miles < 0:
            raise ValueError("odometer cannot be negative")
        object.__setattr__(self, "applicability", MappingProxyType(dict(self.applicability)))


@dataclass(frozen=True)
class ServiceConfirmation:
    record_id: str
    item_id: str
    performed_at: date
    odometer_miles: int | None
    schedule_version: str | None = None


@dataclass(frozen=True)
class TimelineOccurrence:
    ordinal: int
    due_mileage: int | None
    due_date: date | None
    state: str
    confirmation_id: str | None = None


@dataclass(frozen=True)
class TimelineResult:
    vehicle_id: str
    rule_id: str
    item_id: str
    classification: str
    expected_count: int
    confirmed_count: int
    occurrences: tuple[TimelineOccurrence, ...]
    next_due_mileage: int | None
    next_due_date: date | None
    source: ScheduleSource
    assumptions: tuple[str, ...]
    confidence: str
    generic_fallback: bool


def _add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    month_lengths = (31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return date(year, month, min(value.day, month_lengths[month - 1]))


def _elapsed(value: int | None, first: int | None, interval: int | None, repeating: bool) -> int | None:
    if value is None or first is None:
        return None
    if value < first:
        return 0
    if not repeating:
        return 1
    assert interval is not None
    return (value - first) // interval + 1


def _due_value(first: int | None, interval: int | None, ordinal: int, repeating: bool) -> int | None:
    if first is None:
        return None
    return first if not repeating else first + (ordinal - 1) * (interval or 0)


def _lower_confidence(confidence: str) -> str:
    return _CONFIDENCE_ORDER[max(0, _CONFIDENCE_ORDER.index(confidence) - 1)]


def evaluate_rule(
    vehicle: VehicleSnapshot,
    rule: ScheduleRule,
    confirmations: Sequence[ServiceConfirmation],
) -> TimelineResult:
    source = ScheduleSource(rule.provider_id, rule.provider_name, rule.schedule_version, rule.source_url, rule.source_type)
    assumptions: list[str] = []
    generic = rule.source_type == "generic_fallback"
    confidence = rule.confidence
    if generic:
        assumptions.append("generic fallback")
        confidence = _lower_confidence(confidence)

    severity_matches = rule.severity in {"all", vehicle.usage_severity}
    exact_matches = all(vehicle.applicability.get(key) == value for key, value in rule.applicability.items())
    if not severity_matches or not exact_matches:
        reason = "usage severity does not match exact rule" if not severity_matches else "vehicle configuration does not match exact rule"
        assumptions.append(reason)
        return TimelineResult(vehicle.vehicle_id, rule.rule_id, rule.item_id, "not_applicable", 0, 0, (), None, None, source, tuple(assumptions), confidence, generic)

    repeating = rule.recurrence == "repeating"
    first_miles = rule.initial_mileage if rule.initial_mileage is not None else rule.mileage_interval
    first_months = rule.initial_months if rule.initial_months is not None else rule.time_interval_months
    mileage_count = _elapsed(vehicle.odometer_miles, first_miles, rule.mileage_interval, repeating)
    age_months = None
    if vehicle.in_service_date is not None:
        age_months = (vehicle.as_of.year - vehicle.in_service_date.year) * 12 + vehicle.as_of.month - vehicle.in_service_date.month
        if vehicle.as_of.day < vehicle.in_service_date.day:
            age_months -= 1
    time_count = _elapsed(age_months, first_months, rule.time_interval_months, repeating)
    if vehicle.odometer_miles is None and rule.mileage_interval is not None:
        assumptions.append("current mileage unavailable")
    if vehicle.in_service_date is None and rule.time_interval_months is not None:
        assumptions.append("in-service date unavailable")

    if rule.trigger_mode == "mileage_only":
        count = mileage_count or 0
    elif rule.trigger_mode == "time_only":
        count = time_count or 0
    elif rule.trigger_mode == "whichever_first":
        count = max(mileage_count or 0, time_count or 0)
    else:
        count = min(mileage_count or 0, time_count or 0)

    applicable_confirmations = sorted(
        (entry for entry in confirmations if entry.item_id == rule.item_id and entry.schedule_version in {None, rule.schedule_version}),
        key=lambda entry: (entry.performed_at, entry.odometer_miles if entry.odometer_miles is not None else -1, entry.record_id),
    )
    occurrences: list[TimelineOccurrence] = []
    for ordinal in range(1, count + 1):
        due_mileage = _due_value(first_miles, rule.mileage_interval, ordinal, repeating)
        due_months = _due_value(first_months, rule.time_interval_months, ordinal, repeating)
        due_date = _add_months(vehicle.in_service_date, due_months) if vehicle.in_service_date is not None and due_months is not None else None
        confirmation = applicable_confirmations[ordinal - 1] if ordinal <= len(applicable_confirmations) else None
        if confirmation:
            state = "confirmed"
        else:
            mileage_overdue = due_mileage is not None and vehicle.odometer_miles is not None and vehicle.odometer_miles > due_mileage + rule.mileage_tolerance
            time_overdue = due_date is not None and vehicle.as_of > due_date + timedelta(days=rule.time_tolerance_days)
            if rule.trigger_mode == "mileage_only":
                overdue = mileage_overdue
            elif rule.trigger_mode == "time_only":
                overdue = time_overdue
            elif rule.trigger_mode == "whichever_first":
                overdue = mileage_overdue or time_overdue
            else:
                overdue = mileage_overdue and time_overdue
            state = "overdue" if overdue else "unknown"
        occurrences.append(TimelineOccurrence(ordinal, due_mileage, due_date, state, confirmation.record_id if confirmation else None))

    confirmed_count = sum(item.state == "confirmed" for item in occurrences)
    if any(item.state == "overdue" for item in occurrences):
        classification = "overdue"
    elif any(item.state == "unknown" for item in occurrences):
        classification = "unknown"
    elif occurrences:
        classification = "confirmed"
    else:
        classification = "expected"

    next_ordinal = count + 1
    has_next = repeating or count == 0
    next_mileage = _due_value(first_miles, rule.mileage_interval, next_ordinal, repeating) if has_next else None
    next_months = _due_value(first_months, rule.time_interval_months, next_ordinal, repeating) if has_next else None
    next_date = _add_months(vehicle.in_service_date, next_months) if vehicle.in_service_date is not None and next_months is not None else None
    return TimelineResult(vehicle.vehicle_id, rule.rule_id, rule.item_id, classification, count, confirmed_count, tuple(occurrences), next_mileage, next_date, source, tuple(assumptions), confidence, generic)
