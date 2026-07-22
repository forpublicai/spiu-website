#!/usr/bin/env python3
"""Merge home page translations into locale i18n files."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOME_I18N = json.loads(
    (ROOT / "content" / "home_i18n.json").read_text(encoding="utf-8")
)


def main() -> None:
    for locale in ("en", "de", "fr", "it", "rm"):
        path = ROOT / f"i18n_{locale}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for key, translations in HOME_I18N.items():
            data[key] = translations[locale]
        path.write_text(
            json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Merged home i18n into i18n_{locale}.json")


if __name__ == "__main__":
    main()
