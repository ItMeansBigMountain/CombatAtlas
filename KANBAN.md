# HeRmEz Kanban Board

This workspace uses the canonical Hermes `default` Kanban board for durable multi-step work.

## Board

- Slug: `default`
- Name: `Default`
- DB path: `/opt/data/kanban.db`
- Workspace repo: `/opt/data/HeRmEz`

All older project/demo boards were consolidated or removed on 2026-05-29:

- `hermez` was copied into `default`, then deleted.
- `nous-kanban-demo` was deleted.
- Pre-consolidation backup: `/opt/data/HeRmEz/projects/_backups/kanban-consolidation-20260529T053711Z`

## Useful commands

List boards:

```bash
hermes kanban boards list
```

Show current board:

```bash
hermes kanban boards current
```

List tasks:

```bash
hermes kanban list
```

Create a triage task:

```bash
hermes kanban create \
  --triage \
  --created-by user \
  "Plan my next project"
```

Create a worker task for the default profile:

```bash
hermes kanban create \
  --assignee default \
  --workspace dir:/opt/data/HeRmEz \
  --body "Do the requested work in /opt/data/HeRmEz and summarize results." \
  "Example worker task"
```

Watch stats:

```bash
hermes kanban stats
```

Follow a task:

```bash
hermes kanban tail <task_id>
```

## Profiles

Current known assignee profiles:

- `default` — general operator / implementation
- `researcher` — discovery, docs, market/source research
- `reviewer` — code/work review and validation
- `designer` — UI/UX, visual direction, product polish
- `editor` — writing/editing/polish
- `director` — planning, decomposition, orchestration
- `animator` — animation/video/visual motion tasks
- `redteam` — adversarial testing/security-style review

Use only assignee names that appear in `hermes profile list` / `hermes kanban assignees`; invented names will not be picked up by the dispatcher.

## Dispatcher

The Hermes gateway is running and Kanban dispatching is enabled in config:

```yaml
kanban:
  dispatch_in_gateway: true
  dispatch_interval_seconds: 60
```

Ready tasks assigned to a valid profile are picked up by the gateway dispatcher. Triage tasks stay parked until specified/promoted.
