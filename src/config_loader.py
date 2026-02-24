"""Configuration helpers for the Release Manager crew."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PACKAGE_ROOT / "config.yaml"

REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "NOTION_API_KEY",
    "NOTION_RELEASE_DATABASE_ID",
    "SLACK_BOT_TOKEN",
    "SLACK_SIGNING_SECRET",
    "SLACK_ANNOUNCE_CHANNEL",
    "JIRA_API_TOKEN",
    "JIRA_BASE_URL",
    "JIRA_PROJECT_KEY",
    "JIRA_EMAIL",
]


def load_config() -> dict:
    """Load the YAML configuration file."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Missing config.yaml at {CONFIG_PATH}")
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def ensure_env_vars(vars_to_check: Iterable[str] | None = None) -> None:
    """Ensure environment variables are set before running the crew."""
    missing = [var for var in (vars_to_check or REQUIRED_ENV_VARS) if not os.getenv(var)]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(sorted(missing))
        )


def load_tool_config(config: dict) -> dict:
    notion_cfg = config.get("tools", {}).get("notion_release", {})
    env_var = notion_cfg.get("database_id_env", "NOTION_RELEASE_DATABASE_ID")
    database_id = os.getenv(env_var)
    if not database_id:
        raise RuntimeError(f"Environment variable {env_var} must be set for Notion access")
    return {
        "release_doc_url": notion_cfg.get("release_doc_url", "https://www.notion.so"),
        "database_id": database_id,
    }
