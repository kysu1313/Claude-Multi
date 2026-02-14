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
def start(project_path, name):
    """Start a Claude Code session with shared memory.

    PROJECT_PATH: Path to the project directory (defaults to current directory)

    Example:
        claude-multi start /path/to/project
        claude-multi start . --name my-session
    """
    config = Config()
    memory = MemoryManager(config)
    session = SessionManager(config, memory)

    project_path = Path(project_path).resolve()
    session.start_session(project_path, name)


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
def config(key, value):
    """View or modify configuration settings.

    Example:
        claude-multi config
        claude-multi config --key auto_sync --value false
    """
    cfg = Config()

    if key and value:
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
        click.echo("\n  Settings:")

        for k, v in cfg.settings.items():
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
