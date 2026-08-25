# Coding School Platform

Coding school operations and product suite: teacher hiring plan, student progress app, coding community, worksheets, Scratch/Python material, and interactive story learning app.

## Curriculum source of truth

The canonical teacher-first curriculum and Algorithm Academy scope is `CURRICULUM_SOURCE_OF_TRUTH.md`. Use it before implementing learner, teacher, progress, AI-coding, or portfolio workflows.

## Implemented domain slice

The dependency-free `coding_school` package now provides the first teacher-first Algorithm Academy workflows:

- Structured teacher T0-T2, Basic 13, and Linear Search curriculum data.
- Demo-only child accounts and role-scoped teacher, parent, and admin views.
- Evidence submissions that distinguish completion from teacher-reviewed mastery.
- Badges, plain-language parent feedback, and iterative portfolio projects.

Run the verified examples and test suite from this directory:

```bash
python3 examples/linear_search.py
python3 examples/demo_workflow.py
python3 -m unittest discover -s tests -v
```

This is a local domain/API implementation. The universal web/iOS/Android learner and teacher interface is tracked separately and is not represented as shipped by this package.

## Universal learner and teacher app

`app/` is an Expo SDK 57 universal application for web, iOS, and Android. It includes:

- Mobile-first learner modules, editable coding drafts, rubrics, reflection, progress, and accomplishment counts.
- A teacher review queue where mastery approval remains separate from completion.
- Offline persistence for lesson evidence and review state using AsyncStorage.
- A hint-only safe AI coach that never completes the exercise for the learner.
- A script-free sandboxed web preview (`CodeRunner.web.tsx`) and native-friendly teacher-approved runner guidance (`CodeRunner.native.tsx`).
- A demo admin release console for operational gates, missing check-ins, and no-real-student-data verification.
- Demo-only learner data and no private profile fields.

Run and verify it:

```bash
cd app
npm run typecheck
npm run build:web
npm run smoke:web
npm run build:android
npm run build:ios
npm run web
```

Static web output is written to `app/dist/`. Native exports verify Metro bundles for both platforms; signed store builds still require the corresponding Apple and Google developer credentials.

Release verification, browser smoke coverage, rollout blockers, and rollback notes are documented in `RELEASE_VERIFICATION.md`.

## Environment

Local configuration should come from `.env`. Do not commit real secrets. Keep committed examples in `.env.example`.
