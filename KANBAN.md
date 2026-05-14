# HeRmEz Kanban Board

This workspace has a dedicated Hermes Kanban board for durable multi-step work.

## Board

- Slug: `hermez`
- Name: `HeRmEz Workspace`
- DB path: `/opt/data/kanban/boards/hermez/kanban.db`
- Workspace repo: `/opt/data/HeRmEz`

Because this current chat session was started before the board was switched, shell commands in this session inherit `HERMES_KANBAN_BOARD=default`. To target the HeRmEz board from this session, prefix commands with:

```bash
HERMES_KANBAN_BOARD=hermez hermes kanban ...
```

New Hermes sessions should use the active board file at `/opt/data/kanban/current`, which is set to `hermez`.

## Useful commands

List boards:

```bash
hermes kanban boards list
```

Show current board:

```bash
hermes kanban boards current
```

List tasks on this board:

```bash
HERMES_KANBAN_BOARD=hermez hermes kanban list
```

Create a triage task:

```bash
HERMES_KANBAN_BOARD=hermez hermes kanban create \
  --triage \
  --created-by user \
  "Plan my next project"
```

Create a worker task for the default profile:

```bash
HERMES_KANBAN_BOARD=hermez hermes kanban create \
  --assignee default \
  --workspace dir:/opt/data/HeRmEz \
  --body "Do the requested work in /opt/data/HeRmEz and summarize results." \
  "Example worker task"
```

Watch stats:

```bash
HERMES_KANBAN_BOARD=hermez hermes kanban stats
```

Follow a task:

```bash
HERMES_KANBAN_BOARD=hermez hermes kanban tail <task_id>
```

## Profiles

Current known assignee profiles:

- `default`

More specialist profiles can be added later with `hermes profile create <name>` and then used as Kanban assignees.

## Dispatcher

The Hermes gateway is running and Kanban dispatching is enabled in config:

```yaml
kanban:
  dispatch_in_gateway: true
  dispatch_interval_seconds: 60
```

Ready tasks assigned to a valid profile are picked up by the gateway dispatcher. Triage tasks stay parked until specified/promoted.
