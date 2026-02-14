"""Session management for Claude Code instances."""

import subprocess
import os
from pathlib import Path
from typing import Optional
import time


class SessionManager:
    """Manages Claude Code sessions."""

    def __init__(self, config, memory_manager):
        self.config = config
        self.memory = memory_manager

    def _get_project_memory_path(self, project_path: Path) -> Path:
        r"""Get the Claude Code project memory path for a given project directory.

        Claude Code creates project directories based on the working directory path.
        For example: C:\Users\user\PROGRAMS -> C--Users-user-PROGRAMS
        """
        # Normalize the path
        abs_path = project_path.resolve()

        # Convert path to Claude's format (replace : and \ with -)
        # Windows: C:\Users\user\PROGRAMS -> C--Users-user-PROGRAMS
        # Unix: /home/user/projects -> -home-user-projects
        path_str = str(abs_path)

        # Replace drive letter colon
        if ':' in path_str:
            path_str = path_str.replace(':', '-')

        # Replace path separators with dashes
        path_str = path_str.replace('\\', '-').replace('/', '-')

        # Remove leading dash if present
        path_str = path_str.lstrip('-')

        return self.config.claude_projects_dir / path_str

    def start_session(self, project_path: Path, session_name: Optional[str] = None) -> bool:
        """Start a Claude Code session with shared memory.

        Args:
            project_path: Path to the project directory to work in
            session_name: Optional name for this session (defaults to project name)

        Returns:
            True if session started successfully
        """
        project_path = Path(project_path).resolve()

        if not project_path.exists():
            print(f"Error: Project path does not exist: {project_path}")
            return False

        session_name = session_name or project_path.name

        # Get the Claude Code project memory path
        claude_project_path = self._get_project_memory_path(project_path)

        print(f"Session: {session_name}")
        print(f"Project: {project_path}")
        print(f"Claude Code project path: {claude_project_path}")

        # Sync shared memory to session before starting
        if self.config.get("sync_on_start", True):
            print("\n[>>] Syncing shared memory to session...")
            claude_project_path.mkdir(parents=True, exist_ok=True)
            self.memory.sync_to_session(claude_project_path)
            print("[OK] Memory synced to session")

        # Start Claude Code in the project directory
        print(f"\n[*] Starting Claude Code session...")
        print(f"Working directory: {project_path}")
        print("\n" + "="*60)
        print("Claude Code is running. When you exit, memory will be synced back.")
        print("="*60 + "\n")

        try:
            # Run Claude Code interactively
            result = subprocess.run(
                ["claude"],
                cwd=str(project_path),
                shell=True
            )

            print("\n" + "="*60)
            print("Claude Code session ended")
            print("="*60)

            # Sync memory back after session ends
            if self.config.get("sync_on_end", True):
                print("\n[<<] Syncing session memory back to shared pool...")
                self.memory.sync_from_session(claude_project_path, session_name)
                print("[OK] Memory synced from session")

            return True

        except KeyboardInterrupt:
            print("\n\n[!] Session interrupted by user")

            # Still try to sync memory
            if self.config.get("sync_on_end", True):
                print("\n[<<] Syncing session memory back to shared pool...")
                self.memory.sync_from_session(claude_project_path, session_name)
                print("[OK] Memory synced from session")

            return False
        except Exception as e:
            print(f"\n[ERROR] Error running Claude Code: {e}")
            return False

    def manual_sync(self, project_path: Path, direction: str = "both") -> bool:
        """Manually sync memory for a project.

        Args:
            project_path: Path to the project directory
            direction: "to" (shared -> session), "from" (session -> shared), or "both"

        Returns:
            True if sync was successful
        """
        project_path = Path(project_path).resolve()
        claude_project_path = self._get_project_memory_path(project_path)
        session_name = project_path.name

        if direction in ("to", "both"):
            print("[>>] Syncing shared memory to session...")
            claude_project_path.mkdir(parents=True, exist_ok=True)
            self.memory.sync_to_session(claude_project_path)
            print("[OK] Synced to session")

        if direction in ("from", "both"):
            print("[<<] Syncing session memory to shared pool...")
            self.memory.sync_from_session(claude_project_path, session_name)
            print("[OK] Synced from session")

        return True
