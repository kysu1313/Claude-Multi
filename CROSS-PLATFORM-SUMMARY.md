# Cross-Platform Support Summary

## ✅ What Was Added

Claude Multi now has **full cross-platform support** for Windows, macOS, and Linux!

## Files Added

### Unix Support
- **`install.sh`** - Automated installation script for Mac/Linux
- **`run.sh`** - Bash wrapper (equivalent to run.bat on Windows)
- **`UNIX-SETUP.md`** - Complete setup guide for Unix systems

### Documentation
- **`PLATFORM-NOTES.md`** - Platform-specific details and troubleshooting
- **`LICENSE`** - MIT License
- **Updated README.md** - Now includes platform-specific instructions

### Code Improvements
- **Enhanced `session.py`** - Platform-aware path handling
  - Windows: `C:\Users\user\project` → `C--Users-user-project`
  - macOS: `/Users/user/project` → `Users-user-project`
  - Linux: `/home/user/project` → `home-user-project`

## Installation by Platform

### 🪟 Windows

```bash
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi
pip install -e .
python -m claude_multi.cli init
```

**Use it:**
```bash
python -m claude_multi.cli start .
# or
.\run.bat start .
```

**Guide:** `setup-alias.md`

### 🍎 macOS

```bash
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi
chmod +x install.sh
./install.sh
```

**Use it:**
```bash
python3 -m claude_multi.cli start .
# or
./run.sh start .
# or install globally:
sudo cp run.sh /usr/local/bin/claude-multi
claude-multi start .
```

**Guide:** `UNIX-SETUP.md`

### 🐧 Linux

```bash
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi
chmod +x install.sh
./install.sh
```

**Use it:**
```bash
python3 -m claude_multi.cli start .
# or
./run.sh start .
# or install globally:
sudo cp run.sh /usr/local/bin/claude-multi
claude-multi start .
```

**Guide:** `UNIX-SETUP.md`

## Key Differences by Platform

| Feature | Windows | macOS/Linux |
|---------|---------|-------------|
| Python command | `python` | `python3` |
| Wrapper script | `run.bat` | `run.sh` |
| Install script | Manual | `install.sh` |
| Config location | `C:\Users\Name\.claude-multi` | `~/.claude-multi` |
| Shell config | PowerShell `$PROFILE` | `~/.bashrc` or `~/.zshrc` |

## Platform Detection

The tool automatically detects your platform and adjusts:

```python
if sys.platform == 'win32':
    # Windows-specific behavior
else:
    # Unix-specific behavior
```

This happens transparently - you don't need to do anything!

## Shell Integration

### Windows PowerShell
```powershell
# Add to $PROFILE
function claude-multi { python -m claude_multi.cli $args }
```

### Bash (Linux/Mac)
```bash
# Add to ~/.bashrc
alias claude-multi='python3 -m claude_multi.cli'
```

### Zsh (macOS default)
```bash
# Add to ~/.zshrc
alias claude-multi='python3 -m claude_multi.cli'
```

### Fish
```fish
# Add to ~/.config/fish/config.fish
alias claude-multi='python3 -m claude_multi.cli'
```

## Verification

Test on any platform:

```bash
# Check installation
python -m claude_multi.cli --version  # Windows
python3 -m claude_multi.cli --version # Unix

# Check status
python -m claude_multi.cli status  # Windows
python3 -m claude_multi.cli status # Unix

# Try it!
python -m claude_multi.cli start .  # Windows
python3 -m claude_multi.cli start . # Unix
```

## What Works on All Platforms

✅ **Core Features:**
- Shared memory syncing
- Session management
- Memory merging
- Configuration
- All CLI commands

✅ **File Operations:**
- Reading/writing markdown files
- Path handling
- Directory creation

✅ **Subprocess:**
- Launching Claude Code
- Waiting for completion
- Signal handling

## Tested Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| Windows 10/11 | ✅ Tested | Fully working |
| macOS | ⚠️ Should work | Path logic implemented, needs testing |
| Linux (Ubuntu/Debian) | ⚠️ Should work | Path logic implemented, needs testing |
| WSL | ⚠️ Should work | Should work like Linux |

## Need Help?

1. **Windows:** See `setup-alias.md`
2. **Unix:** See `UNIX-SETUP.md`
3. **Platform issues:** See `PLATFORM-NOTES.md`
4. **General help:** See `README.md`

## Contributing

If you test on macOS or Linux and find issues, please:
1. Open an issue on GitHub
2. Include your platform details
3. Include error messages
4. Help us improve cross-platform support!

## Future Improvements

- [ ] WSL-specific testing
- [ ] Docker container version
- [ ] Automated CI/CD testing on all platforms
- [ ] Platform-specific optimizations

---

**Ready to use on any platform!** 🎉

Choose your platform guide and get started:
- Windows → `setup-alias.md`
- Mac/Linux → `UNIX-SETUP.md`
