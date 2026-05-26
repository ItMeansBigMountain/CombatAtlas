"""Simple launcher for the Pythonista Pocket Toolkit."""

from __future__ import annotations

from toolkit.tools.clipboard_history import main as clipboard_main
from toolkit.tools.location_reminders import main as reminders_main
from toolkit.tools.where_was_i import main as where_was_i_main


def main() -> None:
    actions = {
        "1": ("Where Was I tracker", where_was_i_main),
        "2": ("Clipboard history", clipboard_main),
        "3": ("Location reminders", reminders_main),
    }
    print("Pythonista Pocket Toolkit")
    for key, (label, _) in actions.items():
        print(f"{key}. {label}")
    choice = input("Choose: ").strip()
    action = actions.get(choice)
    if not action:
        print("No action selected.")
        return
    print("\n---", action[0], "---")
    action[1]()


if __name__ == "__main__":
    main()
