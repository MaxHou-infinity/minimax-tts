"""Configuration management for MiniMax TTS CLI."""
import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".minimax-tts"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "api_key": "",
    "model": "speech-2.8-hd",
    "voice_id": "female-shaonv",
    "speed": 1.0,
    "vol": 1.0,
    "pitch": 0,
    "format": "mp3",
    "sample_rate": 32000,
    "bitrate": 128000,
    "output_dir": str(Path.home() / ".minimax-tts" / "audio"),
}


def load_config() -> dict:
    """Load config from file, merging with defaults."""
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            config.update(saved)
        except (json.JSONDecodeError, OSError):
            pass
    # Environment variable override
    env_key = os.getenv("MINIMAX_API_KEY")
    if env_key:
        config["api_key"] = env_key
    return config


def save_config(config: dict):
    """Save config to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_api_key() -> str:
    """Get API key from config or env, raise if missing."""
    config = load_config()
    key = config.get("api_key", "")
    if not key:
        raise ValueError(
            "API Key 未配置！请运行 minimax-tts config 设置，"
            "或设置环境变量 MINIMAX_API_KEY"
        )
    return key
