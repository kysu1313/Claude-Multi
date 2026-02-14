# Claude Multi - Instructions Guide

How to inject CLAUDE.md instructions into every session automatically.

## Overview

Claude Multi can automatically inject instructions into your Claude Code sessions. This is perfect for:
- Common CLI tools you want Claude to use (like `tea` for Gitea)
- Project conventions and coding standards
- Testing requirements
- Environment-specific setup

## How It Works

When you start a session, Claude Multi:
1. Reads shared instructions from `~/.claude-multi/shared/CLAUDE.md`
2. Reads any configured default instruction files
3. Reads any instruction files specified with `--instructions` flag
4. Merges them all into `CLAUDE.md` in your project directory
5. Claude Code automatically reads this file when it starts!

## Quick Start

### 1. Edit Shared Instructions

```powershell
# Edit the shared CLAUDE.md
notepad C:\Users\YourName\.claude-multi\shared\CLAUDE.md
```

Add your common instructions:
```markdown
# Shared Claude Code Instructions

## CLI Tools
- Use the `tea` CLI tool to interact with Gitea
- Use `gh` for GitHub operations

## Coding Standards
- Always run tests before committing
- Follow PEP 8 for Python code
- Use TypeScript for all new JavaScript files

## Testing
- Run `pytest` for Python projects
- Run `npm test` for Node.js projects
```

### 2. Start a Session

```powershell
python -m claude_multi.cli start .
```

The instructions are **automatically injected**!

### 3. Claude Knows Your Preferences

When Claude Code starts, it reads the CLAUDE.md file and follows your instructions automatically.

## Usage Examples

### Example 1: Shared Instructions for All Sessions

**Edit ~/.claude-multi/shared/CLAUDE.md:**
```markdown
# My Development Standards

## Version Control
- Use `tea` CLI for Gitea operations
- Always create feature branches
- Write descriptive commit messages

## Testing
- Run tests before every commit
- Maintain 80% code coverage
```

**Start any session:**
```powershell
python -m claude_multi.cli start .
```

Claude will automatically use `tea` for Git operations!

### Example 2: Project-Specific Instructions

**Create ~/work-instructions.md:**
```markdown
# Work Project Instructions

## Gitea Integration
- Repository: https://gitea.company.com/team/project
- Use `tea` CLI for all operations
- PR template requires: description, tests, docs

## Environment
- Development: `npm run dev`
- Production: `npm run build && npm start`
- Database: PostgreSQL on localhost:5432
```

**Start session with these instructions:**
```powershell
python -m claude_multi.cli start . --instructions ~/work-instructions.md
```

### Example 3: Multiple Instruction Files

```powershell
# Combine multiple instruction files
python -m claude_multi.cli start . `
  --instructions ~/company-standards.md `
  --instructions ~/gitea-setup.md `
  --instructions ~/testing-requirements.md
```

All three files will be merged into the session!

### Example 4: Default Instruction Files

**Add a file to always be included:**
```powershell
python -m claude_multi.cli config --add-instructions ~/work-setup.md
```

**Now every session automatically includes it:**
```powershell
python -m claude_multi.cli start .
# Automatically includes ~/work-setup.md!
```

**Remove it later:**
```powershell
python -m claude_multi.cli config --remove-instructions ~/work-setup.md
```

## Configuration

### View Current Settings

```powershell
python -m claude_multi.cli config
```

Output:
```
=== Configuration ===

  Config directory: C:\Users\Name\.claude-multi
  Shared memory: C:\Users\Name\.claude-multi\shared
  Shared CLAUDE.md: C:\Users\Name\.claude-multi\shared\CLAUDE.md

  Settings:
    auto_sync: True
    sync_on_start: True
    sync_on_end: True
    watch_interval: 30
    inject_instructions: True
    instruction_files:
      - C:\Users\Name\work-instructions.md
      - C:\Users\Name\gitea-setup.md
```

### Enable/Disable Instruction Injection

```powershell
# Disable for all sessions
python -m claude_multi.cli config --key inject_instructions --value false

# Enable again
python -m claude_multi.cli config --key inject_instructions --value true
```

### Manage Default Instruction Files

```powershell
# Add a file to always include
python -m claude_multi.cli config --add-instructions ~/my-standards.md

# Remove a file
python -m claude_multi.cli config --remove-instructions ~/my-standards.md

# View configured files
python -m claude_multi.cli config
```

## Instruction Priority

Instructions are merged in this order:
1. **Shared CLAUDE.md** (~/.claude-multi/shared/CLAUDE.md)
2. **Configured default files** (added with --add-instructions)
3. **Command-line files** (specified with --instructions flag)
4. **Existing project CLAUDE.md** (if it exists)

Later instructions don't override earlier ones - they're all combined!

## Real-World Example: Gitea Workflow

### Problem
Every time you start a new Claude session, you have to tell it:
> "Use the tea CLI tool to interact with Gitea"

### Solution

**Step 1: Create gitea-instructions.md**
```markdown
# Gitea Integration

## CLI Tool
- ALWAYS use the `tea` CLI tool for Gitea operations
- Do NOT use `gh` - that's for GitHub
- Tea is already installed and configured

## Common Commands
- List PRs: `tea pr list`
- Create PR: `tea pr create`
- View issue: `tea issue <number>`
- Clone repo: `tea repo clone <name>`

## Repository Info
- Base URL: https://gitea.company.com
- Organization: myteam
- Authentication: Already configured via tea login
```

**Step 2: Add to default instructions**
```powershell
python -m claude_multi.cli config --add-instructions ~/gitea-instructions.md
```

**Step 3: Start any session**
```powershell
cd ~/myproject
python -m claude_multi.cli start .
```

**Result:** Claude automatically knows to use `tea` for Gitea!

## Tips & Best Practices

### 1. Keep Shared Instructions General
Put company-wide or tool-specific instructions in the shared CLAUDE.md:
- CLI tool preferences
- General coding standards
- Common patterns

### 2. Use Separate Files for Specific Contexts
Create separate instruction files for:
- Work vs. personal projects
- Different clients
- Different tech stacks

### 3. Project-Specific CLAUDE.md
For unique project requirements, create a CLAUDE.md in the project itself.
Claude Multi won't overwrite it - it will be included in the merge.

### 4. Test Your Instructions
Start a session and ask Claude:
> "What instructions do you have about Gitea?"

It should reference your instructions!

### 5. Update Regularly
As your workflow evolves, update your instruction files:
```powershell
notepad C:\Users\YourName\.claude-multi\shared\CLAUDE.md
```

## Troubleshooting

### Instructions Not Being Injected?

**Check if injection is enabled:**
```powershell
python -m claude_multi.cli config --key inject_instructions
```

**Enable it:**
```powershell
python -m claude_multi.cli config --key inject_instructions --value true
```

### Instruction File Not Found?

**Check the path:**
```powershell
python -m claude_multi.cli config
```

Look at the `instruction_files` list - paths should be absolute.

**Fix it:**
```powershell
# Remove bad path
python -m claude_multi.cli config --remove-instructions ~/wrong-path.md

# Add correct path
python -m claude_multi.cli config --add-instructions C:\correct\path\to\file.md
```

### Claude Not Following Instructions?

**Verify the CLAUDE.md was created:**
```powershell
# After starting a session, check:
type CLAUDE.md
```

If it exists, Claude Code should read it automatically.

### Want to See What Gets Injected?

**Start a session, then immediately check:**
```powershell
# In another terminal
type path\to\your\project\CLAUDE.md
```

You'll see the merged instructions!

## Advanced Usage

### Conditional Instructions by Project

**Create different instruction sets:**
- `~/work-projects.md` - For work
- `~/personal-projects.md` - For personal projects
- `~/client-a.md` - For client A
- `~/client-b.md` - For client B

**Use the right one:**
```powershell
# Work project
python -m claude_multi.cli start ~/work/project --instructions ~/work-projects.md

# Personal project
python -m claude_multi.cli start ~/personal/project --instructions ~/personal-projects.md
```

### Template Instructions

**Create templates for common scenarios:**

**web-app-template.md:**
```markdown
# Web Application Development

## Stack
- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL
- Testing: Jest + Supertest

## Commands
- Dev: `npm run dev`
- Test: `npm test`
- Build: `npm run build`
```

**Use when starting new projects:**
```powershell
python -m claude_multi.cli start . --instructions ~/templates/web-app-template.md
```

## Summary

**Three ways to provide instructions:**

1. **Shared (always active):** Edit `~/.claude-multi/shared/CLAUDE.md`
2. **Default (configurable):** Use `--add-instructions` in config
3. **Per-session (flexible):** Use `--instructions` flag when starting

**All three are merged together** to give Claude complete context!

## Next Steps

1. **Edit shared instructions:**
   ```powershell
   notepad C:\Users\YourName\.claude-multi\shared\CLAUDE.md
   ```

2. **Add your Gitea setup:**
   ```markdown
   - Use the `tea` CLI tool to interact with Gitea
   ```

3. **Start a session:**
   ```powershell
   python -m claude_multi.cli start .
   ```

4. **Test it - ask Claude:**
   > "What tool should you use for Gitea?"

It should mention `tea`!

---

**Never repeat yourself again!** Set up instructions once, use them everywhere. 🚀
