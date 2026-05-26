# Coding School CRM — Research + Feature Parity Plan

## Public research source notes

Research performed 2026-05-26 against publicly accessible pages:

- North Shore location page: `https://www.thecoderschool.com/locations/northshore/`
- Client login destination found on that page: `https://tcs-northshore.pike13.com/welcome`
- Code Coaching page: `https://www.thecoderschool.com/code-coaching/`
- After-school coding classes page: `https://www.thecoderschool.com/after-school-coding-classes/`
- Pike13 public product page: `https://www.pike13.com/`

## What The Coder School publicly boasts

The public site emphasizes these customer-visible capabilities and learning concepts:

- Code Coaching as the core philosophy.
- Customized lessons per child instead of one fixed curriculum.
- Small 2:1 coach-to-student style mentoring.
- Weekly notes summarizing the student’s previous session and emailed to parents.
- Custom progress tracking using Coder Points.
- Coder Story roadmap: a student’s long-term coding journey and accomplishments.
- Personalized Student Portal listing student accomplishments.
- Regular skill assessments through App Reviews and app uploads.
- Coder Fair showcase events.
- CoderGames national coding competition.
- Congressional App Challenge support.
- Rounds of Code quizzes.
- AppStream coding video library.
- Wide language/project coverage: Scratch, Python, Java, JavaScript, HTML/CSS, Swift, Android, React, Robotics, Unity, Roblox, AI apps, 3D, image recognition, APIs, etc.
- Parents can check progress with Notes+ tracking languages, concepts, homework, and session information.

## Portal/software capabilities visible from public systems

The North Shore site links to Pike13 for client login. Pike13 publicly describes features around:

- Scheduling classes and appointments.
- Attendance tracking.
- Reducing no-shows.
- Automated billing and recurring payments.
- Mobile access for staff and clients.
- Client-facing pages.
- Client communication, reminders, updates, and follow-ups.
- Financial, client, and staff performance reports.
- Education workflows: student enrollment, attendance, billing, parent communication, and progress tracking.

## User-provided operational knowledge

You used to work for them and described the inside workflow:

- Teacher logs in.
- Teacher sees scheduled students already assigned to them.
- Teacher clicks a student from today’s schedule after class.
- Teacher performs an after-class check-in.
- Teacher uses keywords and tags to record what happened.
- Those tags power a graph showing student progress.
- The graph shows what the student is getting good at and what they learned.
- With AI, a teacher should be able to paste/upload Zoom after-meeting notes.
- AI extracts tags, concepts, skills, progress signals, homework, and assessment notes automatically.

## Product positioning

Build our own coding-school CRM and learning-progress system. Do not copy branding, content, or proprietary implementation. Replicate the useful functional pattern:

> Schedule → teacher check-in → AI/tag extraction → progress graph → parent/student/teacher visibility.

Codology becomes the learning/practice engine. The CRM becomes the operational layer.

## Core roles

### Admin / owner

- Manage teachers, students, parents, schedules, programs, lesson types, and billing placeholders.
- Assign students to teachers.
- View school-wide progress and retention health.

### Teacher / coach

- Login.
- See today’s schedule.
- Open a student/class session.
- Add after-class check-in notes.
- Paste Zoom after-meeting notes.
- Review AI-suggested tags before saving.
- Mark attendance, homework, concepts learned, blockers, confidence, and next steps.
- See student progress history and graph.

### Parent

- Login.
- See child’s progress summary.
- Read weekly notes.
- View concepts learned, strengths, homework, projects, and upcoming schedule.
- Avoid overwhelming technical detail.

### Student

- See accomplishments, projects, points/badges, learning path, and next practice tasks.
- Launch Codology lessons/practice.

## Feature parity checklist

- [ ] Client/parent/student/teacher login.
- [ ] Schedule view by teacher and student.
- [ ] Student profile with parent relationship.
- [ ] Assigned teacher relationship.
- [ ] Session detail page.
- [ ] Attendance and after-class check-in.
- [ ] Weekly notes to parent.
- [ ] AI paste/upload Zoom notes parser.
- [ ] AI-note account entitlements so only approved/paid/internal accounts can spend AI tokens.
- [ ] Non-AI tag parser supporting one-tag-per-line, comma-separated tags, space-separated tags, and local keyword extraction from notes.
- [ ] Human-review queue for AI-extracted or locally parsed tags.
- [ ] Tags for languages, concepts, projects, soft skills, blockers, homework, and mastery.
- [ ] Progress graph by tags/concepts over time.
- [ ] Points/badges/accomplishments system inspired by Coder Points.
- [ ] Student roadmap/story inspired by Coder Story.
- [ ] Project/app upload or link tracking.
- [ ] App review/assessment records.
- [ ] Quiz/test result records.
- [ ] Parent-friendly dashboard.
- [ ] Teacher dashboard.
- [ ] Admin dashboard.
- [ ] Exportable progress report.

## AI note extraction and account gating

To save AI/API tokens, not every account should get full AI note extraction.

### Entitlement levels

- `ai_notes_enabled=true`: account can use AI-assisted Zoom/meeting-note parsing.
- `ai_notes_enabled=false`: account gets deterministic/local tag extraction only.
- Future: quota fields like `ai_notes_monthly_limit`, `ai_notes_used_this_month`, and `preferred_ai_provider`.

### Non-AI fallback

Every teacher should still be able to add tags quickly without AI:

- One tag per line.
- Comma-separated tags.
- Space-separated tags.
- Mixed input should be normalized into clean lowercase tags.
- Freeform notes can still run through a local keyword/tag parser.

Example inputs:

```text
python, loops, conditionals
```

```text
python
loops
conditionals
problem solving
```

```text
python loops conditionals debugging
```

Expected normalized tags:

```json
["python", "loops", "conditionals", "debugging", "problem-solving"]
```

Input examples for AI-enabled accounts:

- Pasted Zoom after-meeting notes.
- Teacher freeform note.
- Transcript excerpt.
- Lesson summary.

AI extraction output:

```json
{
  "summary": "Student practiced loops in Python using a guessing game.",
  "conceptTags": ["python", "loops", "conditionals", "random numbers"],
  "skillTags": ["debugging", "problem decomposition"],
  "projectTags": ["number guessing game"],
  "strengths": ["understands while loops with guidance"],
  "blockers": ["needs more practice with variable naming"],
  "homework": ["finish adding score tracking"],
  "confidence": 3,
  "masterySignals": [
    { "concept": "loops", "level": "developing", "evidence": "built repeated guessing flow" }
  ],
  "parentNote": "Today we worked on Python loops through a guessing game project."
}
```

## Progress graph model

Each saved check-in creates evidence points:

- `concept`
- `skill`
- `language`
- `project`
- `masteryLevel`
- `confidenceScore`
- `teacherRating`
- `evidenceText`
- `sessionDate`

Graphs should show:

- Concepts learned over time.
- Strengths getting stronger.
- Skills needing reinforcement.
- Languages/projects touched.
- Teacher assessment trend.
- Parent-friendly “what changed this month?” summary.

## MVP build order

1. Data model for users, students, parents, teachers, sessions, notes, tags, assessments.
2. Seed demo schedule and student assignments.
3. Teacher login/demo role switch.
4. Teacher today schedule.
5. Student session check-in page.
6. Manual tags and notes.
7. AI note extraction mock/service interface.
8. Progress graph from tags.
9. Parent dashboard.
10. Codology lesson linkage.

## Non-goals for first sprint

- Real billing.
- Full Pike13 replacement.
- Legal/medical claims.
- Copying proprietary UI/branding.
- Automated emails until notes flow is stable.
