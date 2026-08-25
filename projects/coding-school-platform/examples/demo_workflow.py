"""Run a complete demo learner → teacher review → parent feedback loop."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from coding_school.models import Account, Evidence, MasteryLevel, ReviewStatus, Role, Submission
from coding_school.service import LearningPlatform

platform = LearningPlatform()
for account in (
    Account("teacher-demo", Role.TEACHER, "Coach Rivera", True),
    Account("student-demo", Role.STUDENT, "Learner One", True),
    Account("parent-demo", Role.PARENT, "Family View", True),
):
    platform.add_account(account)
platform.link_parent("parent-demo", "student-demo")
platform.assign_lesson("teacher-demo", "student-demo", "student-linear-search")
platform.submit(Submission(
    "submission-1", "student-demo", "student-linear-search",
    (Evidence("runnable-code", "Linear search returns the target index", "examples/linear_search.py"),),
    "The value is the treasure and the index is its address.",
))
platform.review_submission(
    "submission-1", reviewer_id="teacher-demo", status=ReviewStatus.APPROVED,
    mastery=MasteryLevel.PROFICIENT, badge_ids=("trace-passed", "explanation-approved"),
    parent_safe_summary="Learner One traced a search, fixed an index mistake, and explained the strategy independently.",
)
print(platform.parent_dashboard("parent-demo", "student-demo"))
