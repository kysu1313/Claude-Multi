# Claude Multi v0.1.0 - Initial Release

**Multi-session memory sharing for Claude Code**

Run multiple Claude Code sessions and let them share what they learn!

---

## 🎉 Features

### Core Functionality
- ✅ **Shared Memory Pool** - All sessions contribute to a central knowledge base
- ✅ **Automatic Syncing** - Memory syncs before and after each session
- ✅ **Smart Merging** - Deduplicates content automatically
- ✅ **Session Tracking** - Timestamped backups of every session
- ✅ **Easy CLI** - Simple commands to manage everything

### Instruction Injection (NEW!)
- ✅ **CLAUDE.md Auto-Injection** - Set instructions once, use everywhere
- ✅ **Multiple Instruction Sources** - Shared, configured, and per-session
- ✅ **Perfect for CLI Tools** - Tell Claude once: "use tea for Gitea"
- ✅ **Smart Merging** - Combines multiple instruction files intelligently

### Cross-Platform Support
- ✅ **Windows** - Full support with batch wrapper
- ✅ **macOS** - Automated installer and bash wrapper
- ✅ **Linux** - Automated installer and bash wrapper
- ✅ **Platform Detection** - Automatically adapts to your OS

---

## 🚀 Quick Start

### Installation

**Windows:**
```bash
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi
pip install -e .
python -m claude_multi.cli init
```

**macOS/Linux:**
```bash
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi
chmod +x install.sh
./install.sh
```

### Basic Usage

```bash
# Start a session
python -m claude_multi.cli start .

# With instructions
python -m claude_multi.cli start . --instructions ~/my-setup.md

# View shared memory
python -m claude_multi.cli status

# List sessions
python -m claude_multi.cli sessions
```

---

## 📚 Use Cases

### 1. Never Repeat Yourself
Set up instructions once in `~/.claude-multi/shared/CLAUDE.md`:
```markdown
- Use the `tea` CLI tool for Gitea
```
Every session automatically knows this!

### 2. Parallel Development
Work on multiple features simultaneously:
```bash
# Terminal 1: Feature A
python -m claude_multi.cli start . --name feature-a

# Terminal 2: Feature B
python -m claude_multi.cli start . --name feature-b
```
Both sessions share learnings!

### 3. Build Knowledge Over Time
Each session adds to the collective knowledge base. Later sessions benefit from earlier learnings.

---

## 📖 Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - Getting started guide
- **EXAMPLES.md** - Real-world use cases
- **INSTRUCTIONS-GUIDE.md** - How to use instruction injection
- **QUICK-REFERENCE.md** - Command cheat sheet
- **UNIX-SETUP.md** - Mac/Linux installation
- **PLATFORM-NOTES.md** - Platform-specific details

---

## 🔧 Commands

### Session Management
```bash
start [PATH]              # Start a session
  --name, -n              # Session name
  --instructions, -i      # Instruction files to inject
```

### Memory Management
```bash
status                    # View shared memory status
sessions                  # List all sessions
sync [PATH]               # Manual sync
  --direction, -d         # Sync direction (to/from/both)
```

### Configuration
```bash
config                    # View configuration
  --key, -k               # Config key to view/set
  --value, -v             # Value to set
  --add-instructions, -a  # Add default instruction file
  --remove-instructions   # Remove instruction file
```

---

## 📁 File Locations

| Item | Location |
|------|----------|
| Configuration | `~/.claude-multi/config.json` |
| Shared Memory | `~/.claude-multi/shared/MEMORY.md` |
| Shared Instructions | `~/.claude-multi/shared/CLAUDE.md` |
| Session Backups | `~/.claude-multi/sessions/` |

---

## 🎯 What's New in v0.1.0

### Initial Release
- Complete multi-session memory sharing system
- Automatic memory syncing and merging
- Session tracking with timestamped backups

### Instruction Injection
- CLAUDE.md auto-injection
- Shared instruction file support
- Per-session instruction files
- Configured default instruction files

### Cross-Platform Support
- Windows support with run.bat
- macOS/Linux support with install.sh and run.sh
- Platform-aware path handling
- Platform-specific documentation

### Comprehensive Documentation
- 8 documentation files covering all aspects
- Quick reference guide
- Real-world examples
- Platform-specific setup guides

---

## 🐛 Known Issues

None currently reported. Please open an issue if you find any!

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

Built with:
- Python 3.8+
- Click CLI framework
- Love for automation ❤️

Co-Authored-By: Claude Opus 4.6

---

## 📦 Installation Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Claude Code CLI (`claude` command)

---

## 🔗 Links

- **Repository:** https://github.com/kysu1313/Claude-Multi
- **Issues:** https://github.com/kysu1313/Claude-Multi/issues
- **Documentation:** See repository files

---

**Ready to supercharge your Claude Code workflow?** Clone and install today! 🚀
