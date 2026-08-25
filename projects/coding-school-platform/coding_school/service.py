from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from .models import (
    Account, MasteryLevel, PortfolioProject, Progress, ProjectIteration,
    ReviewStatus, Role, Submission,
)

_PRIVATE_PROFILE_TERMS = ("address", "school", "phone", "email", "token", "secret")


class LearningPlatform:
    """In-memory demo domain service; persistence/UI adapters can wrap this API."""

    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {}
        self._parents: dict[str, set[str]] = {}
        self._assignments: dict[str, set[str]] = {}
        self._submissions: dict[str, Submission] = {}
        self._projects: dict[str, PortfolioProject] = {}

    def add_account(self, account: Account) -> None:
        if account.role is Role.STUDENT and not account.is_demo:
            raise ValueError("student records are limited to demo accounts")
        if account.id in self._accounts:
            raise ValueError("account id already exists")
        self._accounts[account.id] = account

    def update_profile(self, account_id: str, fields: dict[str, str]) -> None:
        self._account(account_id)
        for key in fields:
            if any(term in key.casefold() for term in _PRIVATE_PROFILE_TERMS):
                raise ValueError(f"private field is not accepted: {key}")

    def link_parent(self, parent_id: str, student_id: str) -> None:
        self._require_role(parent_id, Role.PARENT)
        self._require_role(student_id, Role.STUDENT)
        self._parents.setdefault(parent_id, set()).add(student_id)

    def assign_lesson(self, teacher_id: str, student_id: str, lesson_id: str) -> None:
        self._require_role(teacher_id, Role.TEACHER)
        self._require_role(student_id, Role.STUDENT)
        self._assignments.setdefault(teacher_id, set()).add(student_id)

    def submit(self, submission: Submission) -> None:
        self._require_role(submission.student_id, Role.STUDENT)
        if not submission.evidence or not submission.reflection.strip():
            raise ValueError("submission requires evidence and reflection")
        if submission.id in self._submissions:
            raise ValueError("submission id already exists")
        self._submissions[submission.id] = submission

    def review_submission(self, submission_id: str, *, reviewer_id: str, status: ReviewStatus,
                          mastery: MasteryLevel, badge_ids: tuple[str, ...], parent_safe_summary: str) -> None:
        self._require_role(reviewer_id, Role.TEACHER)
        if status is not ReviewStatus.APPROVED and badge_ids:
            raise ValueError("badges require approval")
        if not parent_safe_summary.strip():
            raise ValueError("parent-safe summary is required")
        item = self._submissions[submission_id]
        self._submissions[submission_id] = replace(
            item, review_status=status, mastery=mastery, badge_ids=badge_ids,
            reviewed_by=reviewer_id, parent_safe_summary=parent_safe_summary,
        )

    def student_progress(self, student_id: str) -> Progress:
        self._require_role(student_id, Role.STUDENT)
        items = [item for item in self._submissions.values() if item.student_id == student_id]
        approved = [item for item in items if item.review_status is ReviewStatus.APPROVED]
        badges = tuple(sorted({badge for item in approved for badge in item.badge_ids}))
        summaries = " ".join(item.parent_safe_summary for item in approved if item.parent_safe_summary)
        return Progress(len({item.lesson_id for item in items}), len({item.lesson_id for item in approved}), badges,
                        summaries or "No teacher-reviewed accomplishment yet.")

    def teacher_dashboard(self, teacher_id: str) -> dict[str, object]:
        self._require_role(teacher_id, Role.TEACHER)
        assigned = tuple(sorted(self._assignments.get(teacher_id, set())))
        pending = tuple(sorted(item.id for item in self._submissions.values()
                               if item.student_id in assigned and item.review_status is ReviewStatus.PENDING))
        return {"assigned_students": assigned, "pending_reviews": pending}

    def admin_dashboard(self, admin_id: str) -> dict[str, int]:
        self._require_role(admin_id, Role.ADMIN)
        return {
            "demo_accounts": sum(account.is_demo for account in self._accounts.values()),
            "real_student_records": sum(account.role is Role.STUDENT and not account.is_demo for account in self._accounts.values()),
        }

    def parent_dashboard(self, parent_id: str, student_id: str) -> dict[str, str]:
        self._require_role(parent_id, Role.PARENT)
        student = self._require_role(student_id, Role.STUDENT)
        if student_id not in self._parents.get(parent_id, set()):
            raise PermissionError("parent is not linked to this learner")
        progress = self.student_progress(student_id)
        return {
            "student_name": student.display_name,
            "weekly_win": progress.parent_safe_summary,
            "next_step": "Start Linear Search Treasure Hunt" if not progress.completed_lessons else "Review teacher feedback and try the next variation",
        }

    def create_project(self, project: PortfolioProject) -> None:
        self._require_role(project.student_id, Role.STUDENT)
        self._projects[project.id] = project

    def add_project_iteration(self, project_id: str, *, student_id: str, artifact: str, reflection: str) -> None:
        project = self._projects[project_id]
        if project.student_id != student_id:
            raise PermissionError("only the project learner can add an iteration")
        iteration = ProjectIteration(artifact=artifact, reflection=reflection)
        milestones = project.milestones + (("first-run",) if not project.iterations else ())
        self._projects[project_id] = replace(project, milestones=milestones, iterations=project.iterations + (iteration,))

    def review_project_iteration(self, project_id: str, *, reviewer_id: str, feedback: str,
                                 approved: bool, reviewed_at: datetime) -> None:
        self._require_role(reviewer_id, Role.TEACHER)
        project = self._projects[project_id]
        if not project.iterations:
            raise ValueError("project has no iteration to review")
        reviewed = replace(project.iterations[-1], teacher_feedback=feedback, approved=approved, reviewed_at=reviewed_at)
        self._projects[project_id] = replace(project, iterations=project.iterations[:-1] + (reviewed,))

    def project(self, project_id: str, *, requester_id: str) -> PortfolioProject:
        project = self._projects[project_id]
        account = self._account(requester_id)
        if account.role not in (Role.TEACHER, Role.ADMIN) and requester_id != project.student_id:
            raise PermissionError("project is private")
        return project

    def _account(self, account_id: str) -> Account:
        try:
            return self._accounts[account_id]
        except KeyError as exc:
            raise KeyError(f"unknown account: {account_id}") from exc

    def _require_role(self, account_id: str, role: Role) -> Account:
        account = self._account(account_id)
        if account.role is not role:
            raise PermissionError(f"{role.value} role required")
        return account
