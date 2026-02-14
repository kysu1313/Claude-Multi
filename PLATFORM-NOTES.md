# Platform-Specific Notes

## Cross-Platform Compatibility

Claude Multi is designed to work on **Windows, macOS, and Linux**.

## Installation by Platform

### Windows

```bash
cd C:\Users\YourName\path\to\Claude-Multi
pip install -e .
python -m claude_multi.cli init
```

Use the batch wrapper:
```bash
.\run.bat start .
```

Or add to PATH and use directly:
```bash
claude-multi start .
```

See `setup-alias.md` for details.

### macOS / Linux

```bash
cd ~/path/to/Claude-Multi

# Quick install
chmod +x install.sh
./install.sh

# Or manual install
pip3 install -e .
python3 -m claude_multi.cli init
```

Use the shell wrapper:
```bash
./run.sh start .
```

Or install globally:
```bash
sudo cp run.sh /usr/local/bin/claude-multi
claude-multi start .
```

See `UNIX-SETUP.md` for details.

## Platform Differences

### File Paths

The tool automatically handles platform-specific path formats:

**Windows:**
- Project: `C:\Users\user\PROGRAMS\myproject`
- Claude dir: `C--Users-user-PROGRAMS-myproject`

**macOS:**
- Project: `/Users/user/projects/myapp`
- Claude dir: `Users-user-projects-myapp`

**Linux:**
- Project: `/home/user/projects/myapp`
- Claude dir: `home-user-projects-myapp`

### Configuration Location

**Windows:**
```
C:\Users\YourName\.claude-multi\
```

**macOS/Linux:**
```
~/.claude-multi/
```

### Python Command

**Windows:**
```bash
python -m claude_multi.cli
```

**macOS/Linux:**
```bash
python3 -m claude_multi.cli
```

### Running Scripts

**Windows:**
- `.bat` files work natively
- Use `.\run.bat`

**macOS/Linux:**
- `.sh` files need execute permission
- Use `chmod +x run.sh` then `./run.sh`

## Shell Integration

### Windows PowerShell

Add to `$PROFILE`:
```powershell
function claude-multi { python -m claude_multi.cli $args }
```

### Bash (Linux / macOS / Git Bash)

Add to `~/.bashrc`:
```bash
alias claude-multi='python3 -m claude_multi.cli'
```

### Zsh (macOS default)

Add to `~/.zshrc`:
```bash
alias claude-multi='python3 -m claude_multi.cli'
```

### Fish

Add to `~/.config/fish/config.fish`:
```fish
alias claude-multi='python3 -m claude_multi.cli'
```

## Common Issues by Platform

### Windows

**Issue:** Command not found after pip install
```bash
# Solution: Use full python -m command
python -m claude_multi.cli start .
```

**Issue:** Permission denied
```bash
# Solution: Run as administrator or use user install
pip install --user -e .
```

### macOS

**Issue:** `python` not found, only `python3`
```bash
# Solution: Always use python3
python3 -m claude_multi.cli start .

# Or create alias
alias python=python3
```

**Issue:** Permission denied on `/usr/local/bin`
```bash
# Solution: Install to ~/bin instead
mkdir -p ~/bin
cp run.sh ~/bin/claude-multi
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
```

### Linux

**Issue:** Python not installed
```bash
# Debian/Ubuntu
sudo apt-get install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

**Issue:** Permission denied on scripts
```bash
# Solution: Make executable
chmod +x run.sh install.sh
```

## Testing Cross-Platform Compatibility

To test if everything works on your platform:

```bash
# 1. Check Python
python3 --version  # or python --version on Windows

# 2. Check installation
python3 -m claude_multi.cli --version

# 3. Check initialization
python3 -m claude_multi.cli status

# 4. Test in current directory
python3 -m claude_multi.cli start .
```

## Claude Code Compatibility

Claude Code works the same way on all platforms:
- Config location: `~/.claude/` (Windows: `C:\Users\YourName\.claude\`)
- Project directories: `~/.claude/projects/`
- Memory structure: Same across all platforms

## Development Setup

All platforms:
```bash
# Clone repository
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi

# Install in development mode
pip install -e .  # or pip3 on macOS/Linux

# Initialize
python -m claude_multi.cli init  # or python3
```

## Performance Notes

- **Windows**: File operations may be slightly slower due to antivirus scanning
- **macOS**: Fast file operations, may need to approve terminal access
- **Linux**: Generally fastest file operations

## Future Platform Support

Planned:
- [ ] WSL (Windows Subsystem for Linux) - should work now but untested
- [ ] Docker container version
- [ ] Automated platform detection in installer

## Getting Help

If you encounter platform-specific issues:

1. Check this guide
2. Check platform-specific setup guide:
   - Windows: `setup-alias.md`
   - Unix: `UNIX-SETUP.md`
3. Open an issue on GitHub with your platform details

---

**All platforms are fully supported!** Choose your setup guide and get started.
