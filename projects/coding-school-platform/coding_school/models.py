from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import StrEnum


class Role(StrEnum):
    STUDENT = "student"
    TEACHER = "teacher"
    PARENT = "parent"
    ADMIN = "admin"


class ReviewStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    NEEDS_REVISION = "needs-revision"


class MasteryLevel(StrEnum):
    INTRODUCED = "introduced"
    PRACTICING = "practicing"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    MENTOR_READY = "mentor-ready"


@dataclass(frozen=True)
class Account:
    id: str
    role: Role
    display_name: str
    is_demo: bool


@dataclass(frozen=True)
class Evidence:
    evidence_type: str
    description: str
    artifact: str | None = None


@dataclass(frozen=True)
class Submission:
    id: str
    student_id: str
    lesson_id: str
    evidence: tuple[Evidence, ...]
    reflection: str
    review_status: ReviewStatus = ReviewStatus.PENDING
    mastery: MasteryLevel | None = None
    badge_ids: tuple[str, ...] = ()
    reviewed_by: str | None = None
    parent_safe_summary: str = ""


@dataclass(frozen=True)
class ProjectIteration:
    artifact: str
    reflection: str
    teacher_feedback: str = ""
    approved: bool = False
    reviewed_at: datetime | None = None


@dataclass(frozen=True)
class PortfolioProject:
    id: str
    student_id: str
    title: str
    description: str
    milestones: tuple[str, ...] = ("idea-scoped",)
    iterations: tuple[ProjectIteration, ...] = ()


@dataclass(frozen=True)
class Progress:
    completed_lessons: int
    mastered_lessons: int
    badges: tuple[str, ...]
    parent_safe_summary: str
