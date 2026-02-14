# Claude Multi

Multi-session memory sharing for Claude Code. Run multiple Claude Code sessions and let them share what they learn!

## Features

- 🔄 **Automatic Memory Sync** - Sessions share learnings automatically
- 📚 **Shared Knowledge Pool** - Central memory repository for all sessions
- 🔍 **Session History** - Track what each session learned over time
- ⚙️ **Configurable** - Control when and how syncing happens
- 🚀 **Easy to Use** - Simple CLI interface

## Installation

```bash
# Navigate to the project directory
cd C:\Users\ksups\PROGRAMS\python\claude-multi

# Install in development mode
pip install -e .
```

## Quick Start

```bash
# Initialize Claude Multi
claude-multi init

# Start a session (from any project directory)
claude-multi start /path/to/your/project

# Or start from current directory
cd /path/to/your/project
claude-multi start .

# View shared memory status
claude-multi status

# List all sessions
claude-multi sessions
```

## How It Works

### Architecture

```
┌─────────────────────────────────┐
│   Shared Memory Hub             │
│   ~/.claude-multi/shared/       │
│   - MEMORY.md (aggregated)      │
│   - topic/*.md files            │
└──────────────┬──────────────────┘
               │
       ┌───────┴───────┐
       │               │
   ┌───▼────┐      ┌───▼────┐
   │Session1│      │Session2│
   │memory/ │      │memory/ │
   └────────┘      └────────┘
```

### Workflow

1. **Pre-session sync**: Before starting Claude Code, shared knowledge is synced to the session
2. **Work normally**: Use Claude Code as usual - it learns and saves to its memory
3. **Post-session sync**: When you exit, new learnings are merged back into shared pool
4. **Smart merging**: Duplicate content is automatically deduplicated

## Commands

### `claude-multi start [PROJECT_PATH]`

Start a Claude Code session with shared memory.

```bash
# Start in specific project
claude-multi start /path/to/project

# Start in current directory
claude-multi start .

# Start with custom session name
claude-multi start . --name my-feature-work
```

### `claude-multi sync [PROJECT_PATH]`

Manually sync memory for a project.

```bash
# Sync both directions
claude-multi sync /path/to/project

# Only sync TO session (shared -> session)
claude-multi sync . --direction to

# Only sync FROM session (session -> shared)
claude-multi sync . --direction from
```

### `claude-multi status`

Show status of shared memory pool.

```bash
claude-multi status
```

### `claude-multi sessions`

List all tracked sessions and their history.

```bash
claude-multi sessions
```

### `claude-multi config`

View or modify configuration.

```bash
# View all settings
claude-multi config

# View specific setting
claude-multi config --key auto_sync

# Change a setting
claude-multi config --key sync_on_start --value false
```

## Configuration

Configuration is stored at `~/.claude-multi/config.json`

Default settings:
```json
{
  "auto_sync": true,
  "sync_on_start": true,
  "sync_on_end": true,
  "watch_interval": 30
}
```

- `auto_sync`: Enable automatic syncing
- `sync_on_start`: Sync shared memory to session before starting
- `sync_on_end`: Sync session memory back after ending
- `watch_interval`: How often to check for changes (seconds)

## Directory Structure

```
~/.claude-multi/
├── config.json              # Configuration
├── shared/                  # Shared memory pool
│   ├── MEMORY.md           # Main shared memory
│   └── topic/*.md          # Topic-specific memories
└── sessions/               # Session history
    ├── session-1/
    │   └── 20240214_143022/ # Timestamped snapshots
    └── session-2/
```

## Use Cases

### Parallel Development

Work on multiple features simultaneously:

```bash
# Terminal 1: Feature A
cd ~/projects/myapp
claude-multi start . --name feature-a

# Terminal 2: Feature B
cd ~/projects/myapp
claude-multi start . --name feature-b

# Both sessions share learnings about the codebase!
```

### Team Knowledge Base

Each team member's sessions contribute to shared knowledge:

```bash
# Share the ~/.claude-multi/shared/ directory with your team
# Everyone's Claude sessions contribute to collective learning
```

### Project Onboarding

Build up project knowledge over time:

```bash
# Session 1: Learn about architecture
claude-multi start ~/myproject

# Session 2: Learn about testing
claude-multi start ~/myproject

# All learnings are preserved and shared
```

## Advanced Usage

### Manual Memory Management

```bash
# Export current session memory to shared pool
claude-multi sync . --direction from

# Import shared pool to current session
claude-multi sync . --direction to

# Force full sync both ways
claude-multi sync . --direction both
```

### Session History

Every sync creates a timestamped backup:

```bash
# View session history
claude-multi sessions

# Backups are stored at:
# ~/.claude-multi/sessions/<session-name>/<timestamp>/
```

## Troubleshooting

### Sessions not syncing

1. Check config: `claude-multi config`
2. Ensure `sync_on_start` and `sync_on_end` are true
3. Manually sync: `claude-multi sync .`

### Memory conflicts

The tool uses smart merging to avoid duplicates, but if you see issues:

1. Check `~/.claude-multi/shared/MEMORY.md` manually
2. Edit to resolve conflicts
3. Force sync: `claude-multi sync . --direction to`

### Finding Claude Code project path

Claude Code creates project directories in `~/.claude/projects/` based on your working directory path.

If you're unsure where your project's memory is:

```bash
# The tool automatically finds the right path
# Just run from your project directory
cd /your/project
claude-multi start .
```

## Contributing

This is a personal tool but feel free to modify and extend it!

## License

MIT License - See LICENSE file for details
