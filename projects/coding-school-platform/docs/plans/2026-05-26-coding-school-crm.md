# Coding School CRM Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a coding-school CRM that gives teachers schedules and after-class check-ins, parents progress visibility, students accomplishments/practice, and AI-extracted tags from lesson/Zoom notes.

**Curriculum source of truth:** `../../CURRICULUM_SOURCE_OF_TRUTH.md` now defines the teacher mastery track, Basic 13 progression, Algorithm Academy scope, accomplishment loop, and child-safe AI/portfolio requirements. Implement curriculum/progress work from that file first.

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

### Task 4: Add AI entitlement and local tag parser

**Objective:** Save API tokens by allowing only entitled accounts to use AI note extraction, while every teacher still gets fast local tag entry/parsing.

**Files:**
- Create: `src/lib/tagParser.js`
- Create: `src/lib/aiEntitlements.js`
- Test: `tests/tag-parser.test.js`
- Test: `tests/ai-entitlements.test.js`

**Tag parser requirements:**

- Accept tags one per line.
- Accept comma-separated tags.
- Accept space-separated tags.
- Accept mixed comma/newline/space input.
- Normalize to lowercase.
- Trim whitespace.
- Deduplicate.
- Preserve useful multi-word tags when entered on their own line or comma-separated, e.g. `problem solving` → `problem-solving`.

**Example:**

```js
parseTags(`python, loops\nconditionals debugging\nproblem solving`)
// ["python", "loops", "conditionals", "debugging", "problem-solving"]
```

**Entitlement requirements:**

- `canUseAiNotes(account)` returns true only when the account has `ai_notes_enabled === true` and quota remains.
- Non-entitled accounts route to local tag extraction.
- AI output must always be human-reviewed before saving.

**Acceptance criteria:**

- Tests prove non-AI tag parsing handles commas, spaces, and lines.
- Tests prove non-entitled account cannot call AI extraction path.
- UI can display: “AI notes unavailable for this account; use tags/keyword extraction instead.”

---

### Task 5: Add AI notes parser interface

**Objective:** Teacher can paste Zoom after-meeting notes and receive suggested tags/summary only when account entitlements allow it.

**Files:**
- Create: `src/lib/aiNoteParser.js`
- Test: `tests/ai-note-parser.test.js`

**Implementation:**

Start deterministic/local, no API key required. Use keyword extraction and simple rules first. Later replace with LLM provider.

**Provider strategy:**

- Default path: local parser, free.
- AI path: OpenRouter-compatible interface.
- Prefer free OpenRouter models for low-value note parsing.
- Track model failures and fall back to local parsing rather than blocking teacher check-in.

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

### Task 6: Build student progress graph

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

### Task 7: Build parent dashboard

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

### Task 8: Link Codology lessons into the CRM

**Objective:** The CRM can recommend Codology practice based on tags and progress gaps.

**Inputs:**

- `Codology/ALGOS_IMPORT_PLAN.json`
- Student progress tags.
- Teacher-selected next topics.

**Acceptance criteria:**

- A student weak on loops gets loop/iteration practice suggestions.
- Teacher can attach a Codology lesson to next session/homework.

---

### Task 9: Add admin queue and reports

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
2. Teacher sees teacher mastery modules before learner modules.
3. Teacher today schedule.
4. Click student.
5. Select Basic 13 or Linear Search curriculum item.
6. Paste Zoom note or enter tags line-by-line/comma/space separated.
7. If entitled, AI suggests tags; otherwise local parser extracts tags.
8. Teacher reviews and saves note/evidence.
9. Student accomplishment/progress graph updates.
10. Parent dashboard shows a clean weekly summary.

## Verification checklist

- Local tests pass.
- Browser smoke test covers teacher schedule → check-in → progress graph.
- No proprietary branding copied.
- No real student data committed.
- Demo data only.
- AI extraction is gated by account entitlement and quota.
- Non-entitled accounts can still parse manual/freeform tags without external API keys.
- AI extraction failures fall back to local tag extraction.
