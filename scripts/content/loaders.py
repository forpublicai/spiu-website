"""Load structured page content from JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONTENT_DIR = Path(__file__).resolve().parent


def load_json(name: str) -> dict[str, Any]:
    path = CONTENT_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


def load_about() -> dict[str, Any]:
    return load_json("about.json")


def load_team() -> dict[str, Any]:
    return load_json("team.json")


def load_news() -> dict[str, Any]:
    return load_json("news.json")


def load_contact() -> dict[str, Any]:
    return load_json("contact.json")


def load_terms() -> dict[str, Any]:
    return load_json("terms.json")


def load_privacy() -> dict[str, Any]:
    return load_json("privacy.json")


def load_fonds() -> dict[str, Any]:
    return load_json("fonds.json")


def load_impressum() -> dict[str, Any]:
    return load_json("impressum.json")


def load_join() -> dict[str, Any]:
    return load_json("join.json")


def load_community_photos() -> dict[str, str]:
    return load_json("community_photos.json")
