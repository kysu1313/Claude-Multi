# Quick Start Guide

## Installation Complete!

Claude Multi is now installed and ready to use.

## Running Commands

Since the tool may not be in your PATH, you have two options:

### Option 1: Use the batch wrapper (Windows)

```bash
# From the claude-multi directory
.\run.bat init
.\run.bat start .
.\run.bat status
```

### Option 2: Use python -m

```bash
python -m claude_multi.cli init
python -m claude_multi.cli start .
python -m claude_multi.cli status
```

### Option 3: Add to PATH (Recommended)

Add this directory to your PATH:
```
C:\Users\ksups\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts
```

Then you can use:
```bash
claude-multi init
claude-multi start .
```

## Example Workflow

### 1. Initialize (already done!)

```bash
python -m claude_multi.cli init
```

### 2. Start a session in your project

```bash
cd C:\Users\ksups\PROGRAMS\your-project
python -m claude_multi.cli start .
```

This will:
- Load shared knowledge into your session
- Start Claude Code in your project
- When you exit, sync learnings back to the shared pool

### 3. Work in multiple sessions

**Terminal 1:**
```bash
cd C:\Users\ksups\PROGRAMS\project-a
python -m claude_multi.cli start . --name project-a
```

**Terminal 2:**
```bash
cd C:\Users\ksups\PROGRAMS\project-b
python -m claude_multi.cli start . --name project-b
```

Both sessions will share learnings!

### 4. Check what's been learned

```bash
python -m claude_multi.cli status
python -m claude_multi.cli sessions
```

### 5. Manual sync (if needed)

```bash
# In your project directory
python -m claude_multi.cli sync .

# Sync only TO session (get latest shared knowledge)
python -m claude_multi.cli sync . --direction to

# Sync only FROM session (push learnings to shared pool)
python -m claude_multi.cli sync . --direction from
```

## Testing It Out

Let's test it with the current project:

```bash
# Start a session right here in claude-multi project
python -m claude_multi.cli start .
```

This will:
1. Sync the shared MEMORY.md to this project's memory
2. Start Claude Code
3. When you exit, sync any learnings back

## Where Things Are Stored

- **Shared Memory**: `C:\Users\ksups\.claude-multi\shared/`
- **Session Backups**: `C:\Users\ksups\.claude-multi\sessions/`
- **Configuration**: `C:\Users\ksups\.claude-multi\config.json`

## Tips

1. **Always exit Claude Code normally** (not Ctrl+C) for best sync results
2. **Check status regularly** to see what's being learned
3. **Edit shared memory directly** at `~/.claude-multi/shared/MEMORY.md` if needed
4. **Session backups** are timestamped so you can see what each session learned

## Troubleshooting

### Sessions not syncing?
```bash
python -m claude_multi.cli config --key sync_on_end --value true
```

### Want to see all settings?
```bash
python -m claude_multi.cli config
```

### Manual sync not working?
Make sure you're in a project directory that has been used with Claude Code before.

## Next Steps

Try starting a session in one of your existing projects:

```bash
cd C:\Users\ksups\PROGRAMS\python\your-project
python -m claude_multi.cli start .
```

Work for a while, exit, then start another session in a different project. You'll notice the second session has knowledge from the first!
