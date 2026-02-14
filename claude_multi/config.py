"""Configuration management for Claude Multi."""

import os
from pathlib import Path
from typing import Optional
import json


class Config:
    """Manages configuration for Claude Multi."""

    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".claude-multi"
        self.shared_memory_dir = self.config_dir / "shared"
        self.sessions_dir = self.config_dir / "sessions"
        self.config_file = self.config_dir / "config.json"
        self.shared_claude_md = self.shared_memory_dir / "CLAUDE.md"

        self.claude_dir = Path.home() / ".claude"
        self.claude_projects_dir = self.claude_dir / "projects"

        self._ensure_directories()
        self._load_config()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.config_dir.mkdir(exist_ok=True)
        self.shared_memory_dir.mkdir(exist_ok=True)
        self.sessions_dir.mkdir(exist_ok=True)

    def _load_config(self):
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                "auto_sync": True,
                "sync_on_start": True,
                "sync_on_end": True,
                "watch_interval": 30,  # seconds
                "inject_instructions": True,  # Inject CLAUDE.md before sessions
                "instruction_files": []  # Additional CLAUDE.md files to include
            }
            self._save_config()

    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, indent=2, fp=f)

    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.settings.get(key, default)

    def set(self, key: str, value):
        """Set configuration value."""
        self.settings[key] = value
        self._save_config()
