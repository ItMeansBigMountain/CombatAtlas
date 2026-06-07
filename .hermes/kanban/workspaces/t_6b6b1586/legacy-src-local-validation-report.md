# legacy-src local validation report

Task: t_6b6b1586
Project: /opt/data/HeRmEz/projects/legacy-src
Validation log: /opt/data/kanban/workspaces/t_6b6b1586/validation.log

## Scope and safety

Parent inspection classified legacy-src as a script/archive aggregate, not a single cohesive app. I did not run a root install/build. I validated the most concrete package-manager candidates from the parent handoff:

- 3D-React-Web CRA frontend
- stockNews/stock-news-frontend Angular frontend
- ticVoter_REST.api Django API
- RTS-JS-ChatRooms Flask app
- MusicAI Flask app

I avoided printing .env/token/credential contents. I did not run migrations, deploys, Terraform, cloud commands, or destructive git commands.

Environment:

- node v22.22.3
- npm 10.9.8
- Python 3.13.5 available globally
- Python 3.11.15 used for validation virtualenvs
- uv 0.11.6 available

## Results

### 3D-React-Web

Working directory: /opt/data/HeRmEz/projects/legacy-src/3D-React-Web

Commands and statuses:

- `npm ci --ignore-scripts` -> exit 0
- `npm run build` -> exit 0
- `npm test -- --watchAll=false --passWithNoTests` -> exit 0

Important output:

- Install succeeded with peer/deprecation warnings and reported 64 vulnerabilities: 14 low, 20 moderate, 28 high, 2 critical.
- Build succeeded with warnings:
  - `@babel/plugin-proposal-private-property-in-object` is imported by `babel-preset-react-app` but not declared.
  - `Failed to parse source map ... @mediapipe/tasks-vision/vision_bundle_mjs.js.map: ENOENT`.
  - Bundle size warning: `628.4 kB build/static/js/main.01d23e6f.js`.
- Tests: `No tests found, exiting with code 0`.

Status: local install/build/test pass, with dependency/audit warnings and no actual tests present.

### stockNews/stock-news-frontend

Working directory: /opt/data/HeRmEz/projects/legacy-src/stockNews/stock-news-frontend

Commands and statuses:

- `npm ci --ignore-scripts` -> exit 0
- `npm run build` -> exit 0
- `npm test -- --watch=false --browsers=ChromeHeadless` -> exit 1

Important output:

- Install succeeded and reported 86 vulnerabilities: 8 low, 22 moderate, 56 high.
- Build succeeded with warning: `Module 'rfdc' used by ... @swimlane/ngx-charts ... is not ESM`.
- Test bundle generation succeeded, but Karma could not launch ChromeHeadless:
  - `ERROR [launcher]: No binary for ChromeHeadless browser on your platform.`
  - `Please, set "CHROME_BIN" env variable.`

Status: local install/build pass. Test is environment-blocked by missing Chrome/CHROME_BIN, not by an observed app test failure.

Next action: install/provide a Chrome/Chromium binary and set CHROME_BIN, then rerun `npm test -- --watch=false --browsers=ChromeHeadless`.

### ticVoter_REST.api

Working directory: /opt/data/HeRmEz/projects/legacy-src/ticVoter_REST.api

Commands and statuses:

- `python3.11 -m venv .venv-validation` -> exit 0
- `.venv-validation/bin/python -m pip install -r requirements.txt` -> exit 1
- `.venv-validation/bin/python manage.py check` -> exit 1

Important output:

- Requirements install failed while building `PyYAML==5.4.1` on Python 3.11 with current build tooling:
  - `AttributeError: 'build_ext' object has no attribute 'cython_sources'`
- Because install failed before Django installed, `manage.py check` failed with:
  - `ModuleNotFoundError: No module named 'django'`
  - `ImportError: Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?`

Status: blocked at dependency install.

Next action: update/pin the Python packaging path for this legacy API, likely by testing a compatibility constraint for PyYAML/Cython/setuptools or updating `PyYAML==5.4.1` to a modern compatible version, then rerun install and `python manage.py check`.

### RTS-JS-ChatRooms

Working directory: /opt/data/HeRmEz/projects/legacy-src/RTS-JS-ChatRooms

Commands and statuses:

- `python3.11 -m venv .venv-validation` -> exit 0
- `.venv-validation/bin/python -m pip install -r requirements.txt` -> exit 1
- `.venv-validation/bin/python -m py_compile app/main.py` -> exit 0

Important output:

- Requirements install failed while building `MarkupSafe==1.0` on Python 3.11/current setuptools:
  - `ImportError: cannot import name 'Feature' from 'setuptools'`
- Syntax compilation of `app/main.py` passed.

Status: source parses, but dependency install is blocked by old pinned Flask/Jinja/MarkupSafe stack.

Next action: modernize the Flask dependency pins or validate in an older Python/container image that supports the archived stack.

### MusicAI

Working directory: /opt/data/HeRmEz/projects/legacy-src/MusicAI

Commands and statuses:

- `python3.11 -m venv .venv-validation` -> exit 0
- `.venv-validation/bin/python -m pip install -r requirements.txt` -> exit 0
- `.venv-validation/bin/python test_app.py` before patch -> timed out after 600s because importing `musicAI` started the Flask dev server on port 8080.
- `.venv-validation/bin/python test_app.py` after patch -> exit 0

Important output after patch:

- `✓ All required modules imported successfully`
- `.env file not found - app will use system environment variables`
- `✓ Flask app created successfully`
- `Meme generation credentials not found (optional feature)`
- `Results: 4/4 tests passed`

Minimal source fix applied:

- File: /opt/data/HeRmEz/projects/legacy-src/MusicAI/musicAI.py
- Change: wrapped the bottom-level Flask server start in `if __name__ == "__main__":` so importing `musicAI` no longer starts a long-running server during tests.
- Focused result now at lines 2169-2170:
  - `if __name__ == "__main__":`
  - `    application.run(host='0.0.0.0', port=8080)`

Status: install and local app smoke test pass after minimal import-safety patch.

## Skipped candidates

- Root legacy-src: skipped; no single root runtime/package and parent classified it as an archive aggregate.
- Expo apps (`ticVoter`, `muscleMadness`, `Codology/codology`): package scripts are interactive Expo start/android/ios/web commands, with no documented non-interactive build/test command in package.json. These should be validated only after choosing a specific app target and desired platform.
- `Codology/SERVER`: package.json has dependencies but no scripts; no least-destructive documented build/test/start command was available.
- Django/manage.py candidates without requirements.txt at their own roots (`muscleMadness_API`, `stockNews/stock_news_backend`, `tweetBetweenTheLines/tweetDeleter`, `CombatAtlas/...`): skipped to avoid guessing dependency environments.
- Terraform/Azure/cloud templates: skipped by safety rule; credential/privileged operations require explicit approval.

## Artifacts and local changes

Artifacts:

- Full validation log: /opt/data/kanban/workspaces/t_6b6b1586/validation.log
- This report: /opt/data/kanban/workspaces/t_6b6b1586/legacy-src-local-validation-report.md

Local artifacts created in project folders by validation:

- node_modules/build outputs under validated npm projects from `npm ci`/build
- `.venv-validation` virtualenvs under validated Python projects

Source file changed:

- /opt/data/HeRmEz/projects/legacy-src/MusicAI/musicAI.py

Git state note:

- `/opt/data/HeRmEz/projects/legacy-src` is ignored by /opt/data/HeRmEz/.gitignore, so `git status --short --ignored -- projects/legacy-src` reports `!! projects/legacy-src/` rather than tracked diffs.

## Remaining blockers / recommended PBIs

No child PBIs were created during this run. Recommended follow-ups:

1. `stockNews frontend: provide ChromeHeadless test runtime and rerun Angular tests`
   - Exact blocker: `No binary for ChromeHeadless browser on your platform. Please, set "CHROME_BIN" env variable.`
2. `ticVoter_REST.api: modernize/constraint legacy Python requirements for Python 3.11+`
   - Exact blocker: `PyYAML==5.4.1` build fails with `AttributeError: 'build_ext' object has no attribute 'cython_sources'`.
3. `RTS-JS-ChatRooms: modernize or containerize old Flask dependency stack`
   - Exact blocker: `MarkupSafe==1.0` build fails with `ImportError: cannot import name 'Feature' from 'setuptools'`.
4. `Review MusicAI import-safety patch`
   - Change is minimal and validated by `test_app.py`, but should receive human/code review before being considered final.
