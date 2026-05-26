"""Private clipboard history for Pythonista.

Use this from the Pythonista app, Share Sheet, or a Shortcuts automation that
periodically opens Pythonista. iOS privacy rules prevent silent always-on
clipboard polling by third-party apps; this captures when invoked.
"""

from __future__ import annotations

from typing import Any

from toolkit.lib.ios_runtime import get_clipboard_text, get_share_text, local_now_label, notify, utc_now_iso
from toolkit.lib.storage import JsonStore, default_data_dir


class ClipboardHistory:
    def __init__(self, store: JsonStore | None = None, limit: int = 100):
        self.store = store or JsonStore(default_data_dir() / "clipboard_history.json", [])
        self.limit = limit

    def capture(self, text: str | None = None, source: str = "clipboard") -> dict[str, Any] | None:
        text = (text if text is not None else get_clipboard_text()).strip()
        if not text:
            return None
        entries = [item for item in self.store.read() if item.get("text") != text]
        entry = {
            "timestamp": utc_now_iso(),
            "local_time": local_now_label(),
            "source": source,
            "kind": classify_text(text),
            "text": text,
            "preview": text[:160],
        }
        entries.insert(0, entry)
        self.store.write(entries[: self.limit])
        return entry

    def entries(self) -> list[dict[str, Any]]:
        return self.store.read()

    def search(self, query: str) -> list[dict[str, Any]]:
        q = query.lower().strip()
        return [item for item in self.entries() if q in item.get("text", "").lower()]


def classify_text(text: str) -> str:
    lowered = text.lower().strip()
    if lowered.startswith(("http://", "https://")):
        return "url"
    if "@" in text and "." in text.split("@")[-1]:
        return "email_or_text"
    if lowered.startswith(("{", "[")):
        return "json_like"
    if len("".join(ch for ch in text if ch.isdigit())) >= 10:
        return "number_or_tracking"
    return "text"


def main() -> None:
    history = ClipboardHistory()
    print("Clipboard History\n1. Capture clipboard/share input\n2. Search\n3. Show latest")
    choice = input("Choose: ").strip()
    if choice == "1":
        text = get_share_text()
        entry = history.capture(text, source="share_or_clipboard")
        if entry:
            notify("Clipboard History", f"Saved {entry['kind']}: {entry['preview'][:45]}")
            print("Saved", entry["preview"])
        else:
            print("Nothing to save.")
    elif choice == "2":
        query = input("Search: ")
        for item in history.search(query)[:20]:
            print(f"{item['local_time']} [{item['kind']}] {item['preview']}")
    else:
        for item in history.entries()[:20]:
            print(f"{item['local_time']} [{item['kind']}] {item['preview']}")


if __name__ == "__main__":
    main()
