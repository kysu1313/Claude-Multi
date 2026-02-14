"""Command-line interface for Claude Multi."""

import click
from pathlib import Path
from .config import Config
from .memory import MemoryManager
from .session import SessionManager


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Claude Multi - Multi-session memory sharing for Claude Code.

    Manage multiple Claude Code sessions with shared learning across all sessions.
    """
    pass


@cli.command()
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('--name', '-n', help='Session name (defaults to project directory name)')
@click.option('--instructions', '-i', multiple=True, help='Additional CLAUDE.md files to inject (can specify multiple)')
def start(project_path, name, instructions):
    """Start a Claude Code session with shared memory.

    PROJECT_PATH: Path to the project directory (defaults to current directory)

    Example:
        claude-multi start /path/to/project
        claude-multi start . --name my-session
        claude-multi start . --instructions ~/work-instructions.md
        claude-multi start . -i ~/common.md -i ~/gitea.md
    """
    config = Config()
    memory = MemoryManager(config)
    session = SessionManager(config, memory)

    project_path = Path(project_path).resolve()
    instruction_list = list(instructions) if instructions else None
    session.start_session(project_path, name, instruction_list)


@cli.command()
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('--direction', '-d',
              type=click.Choice(['to', 'from', 'both']),
              default='both',
              help='Sync direction: to (shared->session), from (session->shared), both')
def sync(project_path, direction):
    """Manually sync memory for a project.

    PROJECT_PATH: Path to the project directory (defaults to current directory)

    Example:
        claude-multi sync /path/to/project
        claude-multi sync . --direction from
    """
    config = Config()
    memory = MemoryManager(config)
    session = SessionManager(config, memory)

    project_path = Path(project_path).resolve()
    session.manual_sync(project_path, direction)

    click.echo("\n[OK] Sync complete!")


@cli.command()
def sessions():
    """List all tracked sessions and their history."""
    config = Config()
    memory = MemoryManager(config)

    session_list = memory.list_sessions()

    if not session_list:
        click.echo("No sessions tracked yet.")
        return

    click.echo("\n=== Tracked Sessions ===\n")

    for session_name in session_list:
        snapshots = memory.get_session_history(session_name)
        click.echo(f"  • {session_name}")
        click.echo(f"    Snapshots: {len(snapshots)}")

        if snapshots:
            latest = snapshots[0]
            click.echo(f"    Latest: {latest.name}")

        click.echo()


@cli.command()
def status():
    """Show status of shared memory pool."""
    config = Config()
    memory = MemoryManager(config)

    summary = memory.get_shared_memory_summary()

    click.echo("\n=== Shared Memory Status ===\n")
    click.echo(f"  Location: {config.shared_memory_dir}")
    click.echo(f"  Total files: {len(summary['files'])}")
    click.echo(f"  Total size: {summary['total_size']} bytes")

    if summary['last_updated']:
        click.echo(f"  Last updated: {summary['last_updated']}")

    if summary['files']:
        click.echo("\n  Files:")
        for file_info in summary['files']:
            click.echo(f"    • {file_info['name']}")
            click.echo(f"      Size: {file_info['size']} bytes")
            click.echo(f"      Modified: {file_info['modified']}")
    else:
        click.echo("\n  No memory files yet.")

    click.echo()


@cli.command()
@click.option('--key', '-k', help='Configuration key to view/set')
@click.option('--value', '-v', help='Value to set (if key is provided)')
@click.option('--add-instructions', '-a', help='Add a CLAUDE.md file to default instruction files')
@click.option('--remove-instructions', '-r', help='Remove a CLAUDE.md file from default instruction files')
def config(key, value, add_instructions, remove_instructions):
    """View or modify configuration settings.

    Example:
        claude-multi config
        claude-multi config --key auto_sync --value false
        claude-multi config --add-instructions ~/my-instructions.md
        claude-multi config --remove-instructions ~/my-instructions.md
    """
    cfg = Config()

    if add_instructions:
        # Add instruction file to config
        instruction_files = cfg.get("instruction_files", [])
        abs_path = str(Path(add_instructions).expanduser().resolve())
        if abs_path not in instruction_files:
            instruction_files.append(abs_path)
            cfg.set("instruction_files", instruction_files)
            click.echo(f"[OK] Added instruction file: {abs_path}")
        else:
            click.echo(f"[!] Instruction file already in list: {abs_path}")

    elif remove_instructions:
        # Remove instruction file from config
        instruction_files = cfg.get("instruction_files", [])
        abs_path = str(Path(remove_instructions).expanduser().resolve())
        if abs_path in instruction_files:
            instruction_files.remove(abs_path)
            cfg.set("instruction_files", instruction_files)
            click.echo(f"[OK] Removed instruction file: {abs_path}")
        else:
            click.echo(f"[!] Instruction file not in list: {abs_path}")

    elif key and value:
        # Set configuration
        # Convert string boolean values
        if value.lower() in ('true', 'false'):
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)

        cfg.set(key, value)
        click.echo(f"[OK] Set {key} = {value}")

    elif key:
        # Get specific configuration
        val = cfg.get(key)
        click.echo(f"{key} = {val}")

    else:
        # Show all configuration
        click.echo("\n=== Configuration ===\n")
        click.echo(f"  Config directory: {cfg.config_dir}")
        click.echo(f"  Shared memory: {cfg.shared_memory_dir}")
        click.echo(f"  Shared CLAUDE.md: {cfg.shared_claude_md}")
        click.echo("\n  Settings:")

        for k, v in cfg.settings.items():
            if k == "instruction_files" and isinstance(v, list):
                click.echo(f"    {k}:")
                if v:
                    for file_path in v:
                        click.echo(f"      - {file_path}")
                else:
                    click.echo(f"      (none)")
            else:
                click.echo(f"    {k}: {v}")

        click.echo()


@cli.command()
def init():
    """Initialize Claude Multi configuration and directories."""
    config = Config()

    click.echo("\n>>> Initializing Claude Multi...\n")
    click.echo(f"  Config directory: {config.config_dir}")
    click.echo(f"  Shared memory: {config.shared_memory_dir}")
    click.echo(f"  Sessions directory: {config.sessions_dir}")

    # Create a default MEMORY.md in shared memory if it doesn't exist
    shared_memory_file = config.shared_memory_dir / "MEMORY.md"
    if not shared_memory_file.exists():
        with open(shared_memory_file, 'w', encoding='utf-8') as f:
            f.write("# Shared Memory Across Claude Code Sessions\n\n")
            f.write("This file contains learnings shared across all Claude Code sessions.\n\n")
            f.write("## Getting Started\n\n")
            f.write("- Use `claude-multi start <project>` to start a session\n")
            f.write("- All sessions will automatically sync learnings here\n")
            f.write("- Organize knowledge by topic in separate .md files\n\n")

        click.echo(f"\n[OK] Created default MEMORY.md")

    # Create a default CLAUDE.md with instructions
    shared_claude_file = config.shared_claude_md
    if not shared_claude_file.exists():
        with open(shared_claude_file, 'w', encoding='utf-8') as f:
            f.write("# Shared Claude Code Instructions\n\n")
            f.write("These instructions are automatically injected into every session.\n\n")
            f.write("## Example Instructions\n\n")
            f.write("Add your common instructions here. For example:\n\n")
            f.write("- Use the `tea` CLI tool to interact with Gitea\n")
            f.write("- Always run tests before committing\n")
            f.write("- Follow the project's code style guide\n\n")
            f.write("## Tips\n\n")
            f.write("- Edit this file at: ~/.claude-multi/shared/CLAUDE.md\n")
            f.write("- Add project-specific CLAUDE.md files with --instructions flag\n")
            f.write("- Configure default instruction files with: claude-multi config --add-instructions <file>\n\n")

        click.echo(f"[OK] Created default CLAUDE.md")

    click.echo("\n[OK] Claude Multi initialized successfully!")
    click.echo("\nNext steps:")
    click.echo("  1. Run 'claude-multi start <project-path>' to start a session")
    click.echo("  2. Work normally in Claude Code")
    click.echo("  3. When you exit, learnings will be synced automatically")
    click.echo()


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
