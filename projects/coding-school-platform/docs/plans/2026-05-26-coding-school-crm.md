# Coding School CRM Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a coding-school CRM that gives teachers schedules and after-class check-ins, parents progress visibility, students accomplishments/practice, and AI-extracted tags from lesson/Zoom notes.

**Architecture:** Start as a web app inside `coding-school-platform` with a role-based demo data model and UI. Codology remains the practice/lesson engine and links into the CRM through lessons, exercises, tags, and progress evidence.

**Tech Stack:** Current project is mostly static/legacy source, so first sprint should use a simple React/Vite or Next.js app with local JSON/demo data before adding hosted database/auth.

---

## Public reference features to match functionally

From public The Coder School and Pike13 pages, build functional equivalents for:

- Teacher/parent/student/client login.
- Teacher schedule.
- Student assignment to teacher.
- Attendance/session check-in.
- Weekly parent notes.
- Progress tracking using points/tags.
- Student accomplishment portal.
- App/project uploads or links.
- Skill assessments and quizzes.
- Parent communication and progress reports.
- Mobile-friendly staff/client experience.

Do not copy branding, proprietary names, or UI. Use original naming:

- Coder Points → `Progress Points`
- Coder Story → `Learning Journey`
- Notes+ → `Lesson Notes`
- App Reviews → `Project Reviews`

---

### Task 1: Create CRM domain model fixtures

**Objective:** Add demo data for teachers, students, parents, schedules, sessions, tags, and progress events.

**Files:**
- Create: `src/data/crmDemoData.js`
- Test: `tests/crm-data.test.js`

**Required entities:**

- `users`
- `students`
- `parents`
- `teachers`
- `scheduledSessions`
- `lessonNotes`
- `skillTags`
- `progressEvents`
- `codologyLessons`

**Verification:**

Run: `npm test`

Expected: data integrity tests prove each scheduled session links to a valid teacher and student.

---

### Task 2: Build teacher schedule dashboard

**Objective:** Teachers can login/demo-switch and see their schedule for today/upcoming sessions.

**Files:**
- Create/modify UI entry files depending chosen framework.
- Test: add UI text assertions for teacher dashboard.

**Acceptance criteria:**

- Teacher sees assigned students only.
- Each schedule card shows time, student name, lesson type, and check-in button.
- Clicking student opens session check-in page.

---

### Task 3: Build after-class check-in form

**Objective:** Teacher records attendance, notes, concepts, homework, blocker, confidence, and rating.

**Fields:**

- Attendance: present/late/missed.
- Freeform notes.
- Concepts covered.
- Project worked on.
- Strengths.
- Blockers.
- Homework.
- Confidence 1-5.
- Teacher mastery rating 1-5.

**Acceptance criteria:**

- Saving creates a lesson note.
- Saving creates progress events for selected tags.
- Parent-safe summary can be generated from the teacher note.

---

### Task 4: Add AI notes parser interface

**Objective:** Teacher can paste Zoom after-meeting notes and receive suggested tags/summary.

**Files:**
- Create: `src/lib/aiNoteParser.js`
- Test: `tests/ai-note-parser.test.js`

**Implementation:**

Start deterministic/local, no API key required. Use keyword extraction and simple rules first. Later replace with LLM provider.

**Output schema:**

```js
{
  summary: string,
  conceptTags: string[],
  skillTags: string[],
  projectTags: string[],
  strengths: string[],
  blockers: string[],
  homework: string[],
  confidence: number,
  masterySignals: [{ concept: string, level: string, evidence: string }],
  parentNote: string
}
```

**Acceptance criteria:**

- Teacher can review/edit suggestions before saving.
- AI output never silently overwrites teacher-entered fields.

---

### Task 5: Build student progress graph

**Objective:** Show progress by concept/tag over time.

**Graph views:**

- Concepts learned over time.
- Strengths growing.
- Needs reinforcement.
- Languages practiced.
- Projects built.
- Confidence trend.

**Acceptance criteria:**

- Graph uses progress events, not hardcoded values.
- Parent view uses plain-English labels.
- Teacher view can drill into evidence notes.

---

### Task 6: Build parent dashboard

**Objective:** Parents can see their child’s weekly notes and progress without overwhelming technical detail.

**Cards:**

- This week’s win.
- Concepts learned.
- Current project.
- Homework/next step.
- Confidence trend.
- Teacher note.
- Upcoming session.

---

### Task 7: Link Codology lessons into the CRM

**Objective:** The CRM can recommend Codology practice based on tags and progress gaps.

**Inputs:**

- `Codology/ALGOS_IMPORT_PLAN.json`
- Student progress tags.
- Teacher-selected next topics.

**Acceptance criteria:**

- A student weak on loops gets loop/iteration practice suggestions.
- Teacher can attach a Codology lesson to next session/homework.

---

### Task 8: Add admin queue and reports

**Objective:** Admin can review missing check-ins, inactive students, and progress/report health.

**Views:**

- Missing notes after completed sessions.
- Students without recent progress events.
- Teachers with pending check-ins.
- Parent update readiness.

---

## First vertical slice

The first shippable vertical slice should be:

1. Demo teacher login.
2. Teacher today schedule.
3. Click student.
4. Paste Zoom note.
5. AI suggests tags.
6. Teacher saves note.
7. Student progress graph updates.
8. Parent dashboard shows a clean weekly summary.

## Verification checklist

- Local tests pass.
- Browser smoke test covers teacher schedule → check-in → progress graph.
- No proprietary branding copied.
- No real student data committed.
- Demo data only.
- AI extraction works without external API keys.
