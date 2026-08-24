from __future__ import annotations

import argparse
import json
from pathlib import Path

from .db import Database
from .imports import import_schedule_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="BurnoutBoyz backend administration")
    parser.add_argument("--database", default="burnoutboyz.db")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("migrate")
    importer = sub.add_parser("import-schedule")
    importer.add_argument("bundle")
    sub.add_parser("schema-status")
    args = parser.parse_args(argv)

    db = Database(args.database)
    try:
        db.migrate()
        if args.command == "migrate":
            payload = {"database": str(Path(args.database)), "migrated": True}
        elif args.command == "import-schedule":
            bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
            payload = import_schedule_bundle(db.connection, bundle)
        else:
            versions = [r[0] for r in db.connection.execute("SELECT version FROM schema_migrations ORDER BY version")]
            table_count = db.connection.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchone()[0]
            payload = {"database": str(Path(args.database)), "migration_versions": versions, "table_count": table_count}
        print(json.dumps(payload, sort_keys=True))
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
