# Coding School Platform Direction

Codology becomes the learning engine inside the broader school platform.

## Product goal

A parent/student/teacher learning portal where students practice coding, parents track progress, and teachers record lesson notes/test outcomes.

## Core roles

- Students: lessons, examples, practice, quizzes, streaks, confidence checks.
- Parents: child progress, strengths, gaps, upcoming lessons, teacher notes.
- Teachers: lesson notes, test results, attendance, assignments, progress updates.

## Codology integration

- Import `algos` examples from all branches as lessons and code exercises.
- Convert each algorithm into explanation, runnable example, practice task, and assessment rubric.
- Store progress by concept, language, difficulty, and mastery state.

## Coding-school CRM direction

Build functional parity with the useful parts of a coding-school customer/teacher portal:

- Teacher login and schedule view.
- Students already assigned to teachers.
- After-class check-in from each scheduled student session.
- Teacher notes, attendance, homework, concepts, blockers, and confidence ratings.
- AI parser for pasted Zoom after-meeting notes, gated to entitled accounts/quotas to save API tokens.
- Non-AI tag parser for accounts without AI access: one tag per line, comma-separated, space-separated, and local keyword extraction.
- Human-reviewed AI/local tags for languages, concepts, skills, projects, blockers, and mastery evidence.
- Parent dashboard with weekly notes and plain-English progress.
- Student dashboard with accomplishments, learning journey, projects, and Codology practice.
- Progress graph powered by tags and evidence over time.

Research and implementation plan: `CODERSCHOOL_CRM_RESEARCH_AND_PLAN.md` and `docs/plans/2026-05-26-coding-school-crm.md`.
