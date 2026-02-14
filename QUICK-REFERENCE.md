# Claude Multi - Quick Reference

## Installation

```powershell
python -m claude_multi.cli init
```

## Common Commands

### Start a Session
```powershell
# Basic
python -m claude_multi.cli start .

# With session name
python -m claude_multi.cli start . --name my-session

# With instructions
python -m claude_multi.cli start . --instructions ~/my-setup.md

# With multiple instruction files
python -m claude_multi.cli start . -i ~/gitea.md -i ~/standards.md
```

### Manage Instructions

```powershell
# Edit shared instructions (applies to ALL sessions)
notepad C:\Users\YourName\.claude-multi\shared\CLAUDE.md

# Add a default instruction file
python -m claude_multi.cli config --add-instructions ~/work-setup.md

# Remove a default instruction file
python -m claude_multi.cli config --remove-instructions ~/work-setup.md

# View configuration
python -m claude_multi.cli config
```

### Memory Management

```powershell
# View shared memory status
python -m claude_multi.cli status

# List all sessions
python -m claude_multi.cli sessions

# Manual sync
python -m claude_multi.cli sync .

# Sync only TO session (get latest)
python -m claude_multi.cli sync . --direction to

# Sync only FROM session (push learnings)
python -m claude_multi.cli sync . --direction from
```

### Configuration

```powershell
# View all settings
python -m claude_multi.cli config

# Change a setting
python -m claude_multi.cli config --key auto_sync --value false

# Enable/disable instruction injection
python -m claude_multi.cli config --key inject_instructions --value true
```

## Solving Your Gitea Problem

### The Problem
Every session, you have to tell Claude:
> "Use the tea CLI tool for Gitea"

### The Solution

**Option 1: Add to shared instructions (easiest)**

```powershell
# Edit the shared CLAUDE.md
notepad C:\Users\ksups\.claude-multi\shared\CLAUDE.md
```

Add this:
```markdown
## CLI Tools
- Use the `tea` CLI tool to interact with Gitea
- Do NOT use `gh` - that's for GitHub
```

Save and close. **Done!** Every session will know this now.

**Option 2: Create a dedicated instruction file**

Create `~/gitea-setup.md`:
```markdown
# Gitea Setup

## CLI Tool
- ALWAYS use the `tea` CLI tool for Gitea operations
- Tea is installed and configured

## Common Commands
- List PRs: `tea pr list`
- Create PR: `tea pr create`
```

Add it to defaults:
```powershell
python -m claude_multi.cli config --add-instructions ~/gitea-setup.md
```

**Done!** Every session will include this file.

## File Locations

| Item | Location |
|------|----------|
| Configuration | `~/.claude-multi/config.json` |
| Shared Memory | `~/.claude-multi/shared/MEMORY.md` |
| Shared Instructions | `~/.claude-multi/shared/CLAUDE.md` |
| Session Backups | `~/.claude-multi/sessions/` |

## How Instructions Work

When you start a session:

1. Reads `~/.claude-multi/shared/CLAUDE.md`
2. Reads any configured default instruction files
3. Reads any `--instructions` files you specify
4. Merges them all into `CLAUDE.md` in your project
5. Claude Code reads this file automatically!

## Tips

### Multiple Sessions
```powershell
# Terminal 1: Backend
cd ~/project/backend
python -m claude_multi.cli start . --name backend

# Terminal 2: Frontend
cd ~/project/frontend
python -m claude_multi.cli start . --name frontend
```

Both sessions share learnings + instructions!

### Check What Was Injected
```powershell
# After starting a session, check:
type CLAUDE.md
```

### Different Instructions for Different Projects
```powershell
# Work project
python -m claude_multi.cli start ~/work/project --instructions ~/work-setup.md

# Personal project
python -m claude_multi.cli start ~/personal/project --instructions ~/personal-setup.md
```

## Troubleshooting

### Instructions not working?
```powershell
# Check if injection is enabled
python -m claude_multi.cli config --key inject_instructions

# Enable it
python -m claude_multi.cli config --key inject_instructions --value true
```

### Can't find instruction file?
```powershell
# Use absolute paths
python -m claude_multi.cli config --add-instructions C:\full\path\to\file.md
```

### Want to test?
```powershell
# Start a session
python -m claude_multi.cli start .

# Ask Claude: "What instructions do you have?"
# It should mention your instructions!
```

## Full Workflow Example

```powershell
# 1. Setup (one time)
python -m claude_multi.cli init

# 2. Add Gitea instructions (one time)
notepad C:\Users\ksups\.claude-multi\shared\CLAUDE.md
# Add: "Use tea CLI for Gitea"

# 3. Start working on project A
cd ~/project-a
python -m claude_multi.cli start .
# Claude automatically knows to use tea!

# 4. Later, start working on project B
cd ~/project-b
python -m claude_multi.cli start .
# Claude still knows to use tea!
# Plus it knows what it learned from project A!
```

## Documentation

- **Full Guide:** `README.md`
- **Instructions:** `INSTRUCTIONS-GUIDE.md`
- **Examples:** `EXAMPLES.md`
- **Unix Setup:** `UNIX-SETUP.md`
- **Platform Notes:** `PLATFORM-NOTES.md`

## Getting Help

```powershell
# Command help
python -m claude_multi.cli --help
python -m claude_multi.cli start --help

# View configuration
python -m claude_multi.cli config

# Check status
python -m claude_multi.cli status
```

---

**Quick answer to your question:**

Edit `~/.claude-multi/shared/CLAUDE.md` and add:
```markdown
- Use the `tea` CLI tool for Gitea
```

Then every session will automatically know this! 🚀
