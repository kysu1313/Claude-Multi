"""Memory synchronization and management."""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
import hashlib


class MemoryManager:
    """Manages memory synchronization between sessions."""

    def __init__(self, config):
        self.config = config
        self.shared_memory_dir = config.shared_memory_dir
        self.sessions_dir = config.sessions_dir

    def sync_to_session(self, project_path: Path) -> bool:
        """Sync shared memory to a session's memory directory.

        Args:
            project_path: Path to the Claude Code project directory

        Returns:
            True if sync was successful
        """
        memory_dir = project_path / "memory"
        memory_dir.mkdir(exist_ok=True)

        # Track what we've synced
        synced_files = []

        # Copy all shared memory files to the session
        for shared_file in self.shared_memory_dir.glob("*.md"):
            target_file = memory_dir / shared_file.name

            # If file exists in session, merge it; otherwise copy
            if target_file.exists():
                self._merge_memory_file(shared_file, target_file)
            else:
                shutil.copy2(shared_file, target_file)

            synced_files.append(shared_file.name)

        # Also sync topic directories
        for topic_dir in self.shared_memory_dir.iterdir():
            if topic_dir.is_dir():
                target_dir = memory_dir / topic_dir.name
                target_dir.mkdir(exist_ok=True)

                for topic_file in topic_dir.glob("*.md"):
                    target_file = target_dir / topic_file.name
                    if target_file.exists():
                        self._merge_memory_file(topic_file, target_file)
                    else:
                        shutil.copy2(topic_file, target_file)

        return True

    def sync_from_session(self, project_path: Path, session_name: str) -> bool:
        """Sync session memory back to shared memory.

        Args:
            project_path: Path to the Claude Code project directory
            session_name: Name of the session

        Returns:
            True if sync was successful
        """
        memory_dir = project_path / "memory"

        if not memory_dir.exists():
            return False

        # Create a backup of this session's memory
        session_backup = self.sessions_dir / session_name / datetime.now().strftime("%Y%m%d_%H%M%S")
        session_backup.mkdir(parents=True, exist_ok=True)

        # Sync all memory files from session to shared
        for session_file in memory_dir.glob("*.md"):
            # Backup the session file
            shutil.copy2(session_file, session_backup / session_file.name)

            # Merge into shared memory
            shared_file = self.shared_memory_dir / session_file.name
            if shared_file.exists():
                self._merge_memory_file(session_file, shared_file)
            else:
                shutil.copy2(session_file, shared_file)

        # Also sync topic directories
        for topic_dir in memory_dir.iterdir():
            if topic_dir.is_dir():
                shared_topic_dir = self.shared_memory_dir / topic_dir.name
                shared_topic_dir.mkdir(exist_ok=True)

                for topic_file in topic_dir.glob("*.md"):
                    shutil.copy2(topic_file, session_backup / topic_file.name)

                    shared_file = shared_topic_dir / topic_file.name
                    if shared_file.exists():
                        self._merge_memory_file(topic_file, shared_file)
                    else:
                        shutil.copy2(topic_file, shared_file)

        return True

    def _merge_memory_file(self, source: Path, target: Path):
        """Merge two memory files intelligently.

        Uses a simple strategy:
        1. Read both files
        2. Split into sections by headers
        3. Merge sections, preferring newer content
        4. Deduplicate bullet points
        """
        with open(source, 'r', encoding='utf-8') as f:
            source_content = f.read()

        with open(target, 'r', encoding='utf-8') as f:
            target_content = f.read()

        # Simple merge: combine unique lines, preserving structure
        source_lines = source_content.split('\n')
        target_lines = target_content.split('\n')

        # Create a set of existing lines for deduplication
        existing_lines = set()
        merged_lines = []

        # First add all target lines
        for line in target_lines:
            line_stripped = line.strip()
            if line_stripped:
                # For bullet points and content, deduplicate
                if line_stripped.startswith(('-', '*', '+')):
                    line_key = self._normalize_line(line_stripped)
                    if line_key not in existing_lines:
                        existing_lines.add(line_key)
                        merged_lines.append(line)
                    else:
                        continue
                else:
                    merged_lines.append(line)
            else:
                merged_lines.append(line)

        # Then add new lines from source that don't exist in target
        new_content_started = False
        for line in source_lines:
            line_stripped = line.strip()
            if line_stripped:
                if line_stripped.startswith(('-', '*', '+')):
                    line_key = self._normalize_line(line_stripped)
                    if line_key not in existing_lines:
                        if not new_content_started:
                            merged_lines.append("")
                            merged_lines.append(f"## Updates from {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                            merged_lines.append("")
                            new_content_started = True
                        existing_lines.add(line_key)
                        merged_lines.append(line)
                elif line_stripped.startswith('#'):
                    # Headers - add if not duplicate
                    if line not in merged_lines:
                        merged_lines.append(line)
                else:
                    # Regular content - check for duplicates
                    line_key = self._normalize_line(line_stripped)
                    if line_key not in existing_lines:
                        existing_lines.add(line_key)
                        merged_lines.append(line)

        # Write merged content
        with open(target, 'w', encoding='utf-8') as f:
            f.write('\n'.join(merged_lines))

    def _normalize_line(self, line: str) -> str:
        """Normalize a line for comparison (remove leading markers, extra spaces)."""
        # Remove bullet points and list markers
        normalized = line.lstrip('*-+ ')
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        # Make lowercase for comparison
        return normalized.lower()

    def get_session_history(self, session_name: str) -> List[Path]:
        """Get all backup snapshots for a session."""
        session_dir = self.sessions_dir / session_name
        if not session_dir.exists():
            return []

        return sorted(session_dir.iterdir(), reverse=True)

    def list_sessions(self) -> List[str]:
        """List all tracked sessions."""
        if not self.sessions_dir.exists():
            return []

        return [d.name for d in self.sessions_dir.iterdir() if d.is_dir()]

    def get_shared_memory_summary(self) -> Dict[str, any]:
        """Get summary of shared memory contents."""
        summary = {
            "files": [],
            "total_size": 0,
            "last_updated": None
        }

        for file in self.shared_memory_dir.glob("*.md"):
            stat = file.stat()
            summary["files"].append({
                "name": file.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime)
            })
            summary["total_size"] += stat.st_size

            if summary["last_updated"] is None or stat.st_mtime > summary["last_updated"].timestamp():
                summary["last_updated"] = datetime.fromtimestamp(stat.st_mtime)

        return summary
