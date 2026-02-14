# Examples & Use Cases

## Example 1: Building a Full-Stack App

You're building a full-stack application and want separate Claude sessions for frontend and backend.

### Setup

```bash
# Terminal 1: Frontend work
cd ~/projects/myapp/frontend
python -m claude_multi.cli start . --name frontend-dev

# Terminal 2: Backend work
cd ~/projects/myapp/backend
python -m claude_multi.cli start . --name backend-dev
```

### What Happens

1. **Session 1 (Frontend)** learns:
   - React component patterns
   - State management approach
   - API endpoint URLs
   - Design system conventions

2. **Session 2 (Backend)** learns:
   - Database schema
   - API routes and handlers
   - Authentication flow
   - Error handling patterns

3. **Both sessions share**:
   - Overall architecture decisions
   - Common pitfalls encountered
   - Debugging techniques
   - Code style preferences

## Example 2: Debugging Across Multiple Services

You have a microservices architecture and need to debug an issue.

```bash
# Session 1: API Gateway
cd ~/services/api-gateway
python -m claude_multi.cli start . --name debug-gateway

# Work on gateway, discover the issue is in auth service
# Exit and start new session

# Session 2: Auth Service
cd ~/services/auth-service
python -m claude_multi.cli start . --name debug-auth
```

**Benefit**: Session 2 already knows:
- What you learned about the issue in Session 1
- API contracts between services
- Authentication flow
- Previous debugging attempts

## Example 3: Learning a New Codebase

You're onboarding to a large codebase and want to explore different parts.

```bash
# Day 1: Explore the core module
cd ~/work/bigproject
python -m claude_multi.cli start . --name explore-core

# Day 2: Explore the API layer
python -m claude_multi.cli start . --name explore-api

# Day 3: Explore the data layer
python -m claude_multi.cli start . --name explore-data
```

After 3 days, check what you've learned:

```bash
python -m claude_multi.cli status
cat ~/.claude-multi/shared/MEMORY.md
```

You'll have a comprehensive knowledge base about the entire codebase!

## Example 4: Parallel Feature Development

Multiple team members working on different features.

**Developer A:**
```bash
cd ~/project
python -m claude_multi.cli start . --name feature-auth
```

**Developer B:**
```bash
cd ~/project
python -m claude_multi.cli start . --name feature-payments
```

Both developers can share the `~/.claude-multi/shared/` directory via Git or shared drive.

## Example 5: Experimentation vs Production

Keep experiments separate but share learnings.

```bash
# Main work
cd ~/myproject
python -m claude_multi.cli start . --name main

# Experimental branch
cd ~/myproject-experimental
python -m claude_multi.cli start . --name experiment

# If experiment works, learnings are already in shared memory!
# If it doesn't, you still learned what doesn't work
```

## Example 6: Documentation Writing

Use sessions to build comprehensive docs.

```bash
# Session 1: Write API docs
cd ~/myproject
python -m claude_multi.cli start . --name docs-api

# Session 2: Write user guide
python -m claude_multi.cli start . --name docs-user

# Session 3: Write architecture docs
python -m claude_multi.cli start . --name docs-arch
```

Each session contributes to shared understanding of the project.

## Example 7: Bug Hunt Marathon

Tackle multiple bugs in one day.

```bash
# Bug #123
cd ~/project
python -m claude_multi.cli start . --name bug-123
# Fix it, exit

# Bug #124
python -m claude_multi.cli start . --name bug-124
# Fix it - Claude already knows patterns from bug-123!

# Bug #125
python -m claude_multi.cli start . --name bug-125
# Even faster now with accumulated knowledge
```

## Example 8: Reviewing Shared Memory

Check what all sessions have learned:

```bash
# View summary
python -m claude_multi.cli status

# List all sessions
python -m claude_multi.cli sessions

# Read the shared memory
cat ~/.claude-multi/shared/MEMORY.md

# Edit shared memory manually
code ~/.claude-multi/shared/MEMORY.md
```

## Example 9: Syncing Before Important Work

Get all the latest knowledge before starting critical work:

```bash
cd ~/important-project
python -m claude_multi.cli sync . --direction to
python -m claude_multi.cli start .
```

## Example 10: Backup and Restore

Session backups are automatic, but you can explore them:

```bash
# List sessions
python -m claude_multi.cli sessions

# Explore a session's history
ls ~/.claude-multi/sessions/my-session-name/

# Each timestamp is a snapshot of that session's memory
cat ~/.claude-multi/sessions/my-session-name/20240214_143022/MEMORY.md
```

## Advanced: Sharing Across Team

### Option 1: Git Repository

```bash
cd ~/.claude-multi/shared
git init
git add .
git commit -m "Initial shared memory"
git remote add origin <repo-url>
git push
```

Team members clone and keep it updated:
```bash
cd ~/.claude-multi/shared
git pull  # Before starting session
git add .
git commit -m "Update from session"
git push  # After ending session
```

### Option 2: Shared Network Drive

Point all team members to the same shared directory:

```bash
python -m claude_multi.cli config --key shared_memory_dir --value "\\\\server\\share\\claude-multi"
```

## Tips for Maximum Benefit

1. **Use descriptive session names** - Makes history easier to understand
2. **Review shared memory periodically** - Clean up outdated info
3. **Exit sessions properly** - Ensures sync happens
4. **Sync before critical work** - Get latest knowledge
5. **Create topic-specific memory files** - Organize by area (api.md, database.md, etc.)

## What Gets Shared?

- Code patterns and conventions
- Architectural decisions
- Common pitfalls and solutions
- File locations and structure
- API contracts and schemas
- Debugging techniques
- Project-specific knowledge
- Dependencies and tools
- Build and deployment processes

## What Doesn't Get Shared?

- Actual code changes (use git for that)
- Session-specific temporary state
- Tool outputs and logs
- File contents (only knowledge about them)
