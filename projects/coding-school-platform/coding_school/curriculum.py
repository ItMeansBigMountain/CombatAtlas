from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CurriculumItem:
    id: str
    track: str
    stage: str
    module: str
    lesson: str
    concept_tags: tuple[str, ...]
    skill_tags: tuple[str, ...]
    prerequisites: tuple[str, ...]
    rubric: tuple[str, ...]
    badges: tuple[str, ...]
    starter_code: str = ""


_BASIC = (
    "Print 1-255", "Print odd numbers 1-255", "Sum 1-255", "Print list values",
    "Find maximum", "Find average", "Collect odd numbers", "Square values",
    "Count above threshold", "Convert matches to zero", "Min, max, average",
    "Shift list values", "Replace negatives",
)


def curriculum_catalog() -> tuple[CurriculumItem, ...]:
    teacher = tuple(
        CurriculumItem(
            id=f"teacher-t{level}", track="teacher", stage=f"T{level}",
            module=("Safety onboarding", "Basic 13 coaching", "Algorithm coaching")[level],
            lesson=("Child-safe platform use", "Teach loops and lists", "Teach search strategies")[level],
            concept_tags=(("safe-AI-use",), ("loops", "lists"), ("search", "indexing"))[level],
            skill_tags=("explaining-code", "teacher-observation"), prerequisites=(() if level == 0 else (f"teacher-t{level-1}",)),
            rubric=("Submit evidence", "Receive reviewer approval"), badges=(f"teacher-t{level}-ready",),
        ) for level in range(3)
    )
    basic = tuple(
        CurriculumItem(
            id=f"student-basic-{number:02d}", track="student", stage="2", module="Basic 13",
            lesson=title, concept_tags=("loops", "lists"),
            skill_tags=("reading-code", "predicting-output", "debugging"),
            prerequisites=(() if number == 1 else (f"student-basic-{number-1:02d}",)),
            rubric=("Read", "Predict", "Run", "Fix", "Challenge", "Reflect"),
            badges=("basic-13-builder",),
        ) for number, title in enumerate(_BASIC, 1)
    )
    linear = CurriculumItem(
        id="student-linear-search", track="student", stage="3", module="Algorithm Academy",
        lesson="Linear Search Treasure Hunt", concept_tags=("search", "indexing", "loops"),
        skill_tags=("tracing", "debugging", "explaining-code"),
        prerequisites=("student-basic-13",),
        rubric=("Trace target", "Return index", "Handle not found", "Explain index vs value"),
        badges=("trace-passed", "bug-fixed", "explanation-approved"),
        starter_code="def linear_search(nums, target):\n    for index, value in enumerate(nums):\n        if value == target:\n            return index\n    return -1\n",
    )
    return teacher + basic + (linear,)
