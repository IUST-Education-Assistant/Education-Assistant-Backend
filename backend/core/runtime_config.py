from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


def load_runtime_config() -> Dict[str, Any]:
    """
    Loads runtime configuration.

    Priority:
    1) Environment variables (recommended for Docker)
    2) backend/config.json (kept for backwards compatibility)
    """
    config: Dict[str, Any] = {}

    config_path = Path(__file__).resolve().parent.parent / "config.json"
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            config = {}

    # Drop obvious placeholder values from config.json
    for key, val in list(config.items()):
        if isinstance(val, str) and val.strip() in {"", key}:
            config.pop(key, None)

    # Env overrides
    for key in ["OPENAI_API_KEY", "GROQ_API_KEY", "OPENAI_LLM_MODEL", "GROQ_LLM_MODEL"]:
        val = os.getenv(key)
        if val:
            config[key] = val

    return config

