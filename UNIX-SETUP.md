# Unix Setup Guide (Mac/Linux)

Complete installation and setup guide for Mac and Linux systems.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- git (for cloning the repository)

Check your Python version:
```bash
python3 --version
```

## Quick Installation

### Option 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi

# Run the install script
chmod +x install.sh
./install.sh
```

This will:
1. Install the package
2. Make scripts executable
3. Initialize configuration
4. Show you how to use it

### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi

# Install the package
pip3 install -e .

# Make the runner script executable
chmod +x run.sh

# Initialize
python3 -m claude_multi.cli init
```

## Usage

### Method 1: Using the Wrapper Script

```bash
# From the Claude-Multi directory
./run.sh start /path/to/project
./run.sh status
./run.sh sessions
```

### Method 2: Using Python Directly

```bash
python3 -m claude_multi.cli start /path/to/project
python3 -m claude_multi.cli status
python3 -m claude_multi.cli sessions
```

### Method 3: Install Globally (Recommended)

Copy the wrapper to your PATH:

```bash
# Option A: System-wide (requires sudo)
sudo cp run.sh /usr/local/bin/claude-multi
sudo chmod +x /usr/local/bin/claude-multi

# Option B: User-only (no sudo required)
mkdir -p ~/bin
cp run.sh ~/bin/claude-multi
chmod +x ~/bin/claude-multi

# Add ~/bin to PATH if not already there
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
source ~/.bashrc  # or source ~/.zshrc
```

Now you can use it from anywhere:
```bash
claude-multi start /path/to/project
claude-multi status
```

### Method 4: Shell Alias

Add to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
alias claude-multi='python3 -m claude_multi.cli'
```

Reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc
```

Now use it anywhere:
```bash
claude-multi start .
claude-multi status
```

## Platform-Specific Notes

### macOS

1. **Python**: macOS may have `python3` but not `python`. Use `python3` explicitly or create an alias.

2. **Shell**: macOS Catalina+ uses `zsh` by default. Add aliases to `~/.zshrc` instead of `~/.bashrc`.

3. **Permissions**: You may need to allow terminal access in System Preferences → Security & Privacy.

### Linux

1. **Python**: Most Linux distributions include Python 3. If not:
   ```bash
   # Debian/Ubuntu
   sudo apt-get update
   sudo apt-get install python3 python3-pip

   # Fedora/RHEL
   sudo dnf install python3 python3-pip

   # Arch
   sudo pacman -S python python-pip
   ```

2. **Shell**: Most Linux systems use `bash`. Add aliases to `~/.bashrc`.

## Verifying Installation

```bash
# Check if installed
python3 -m claude_multi.cli --version

# View help
python3 -m claude_multi.cli --help

# Check status
python3 -m claude_multi.cli status
```

## Directory Structure

After initialization, you'll have:

```
~/.claude-multi/
├── config.json           # Configuration
├── shared/              # Shared memory pool
│   └── MEMORY.md       # Shared knowledge
└── sessions/           # Session backups
```

## Quick Start Example

```bash
# Navigate to a project
cd ~/projects/my-app

# Start a Claude Code session with shared memory
python3 -m claude_multi.cli start .

# Or if you installed globally/added alias:
claude-multi start .
```

## Common Issues

### Permission Denied

If you get "Permission denied" when running scripts:
```bash
chmod +x run.sh
chmod +x install.sh
```

### Python Not Found

Make sure Python 3 is installed:
```bash
python3 --version
```

If not installed, install it:
- **macOS**: `brew install python3` (requires Homebrew)
- **Linux**: See platform-specific notes above

### Module Not Found

If you get "No module named claude_multi":
```bash
pip3 install -e .
```

Make sure you're in the Claude-Multi directory.

### Command Not Found (after global install)

Make sure the directory is in your PATH:
```bash
# Check PATH
echo $PATH

# If /usr/local/bin or ~/bin is not in PATH, add it:
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Updating

To update to the latest version:

```bash
cd Claude-Multi
git pull origin main
pip3 install -e . --upgrade
```

## Uninstalling

```bash
# Remove the package
pip3 uninstall claude-multi

# Remove configuration (optional)
rm -rf ~/.claude-multi

# Remove global command (if installed)
sudo rm /usr/local/bin/claude-multi
# or
rm ~/bin/claude-multi
```

## Next Steps

- Read `QUICKSTART.md` for usage guide
- Read `EXAMPLES.md` for real-world use cases
- Read `README.md` for full documentation

## Getting Help

If you encounter issues:

1. Check this guide
2. Read the main README.md
3. Check the issue tracker on GitHub
4. Create a new issue with details about your platform and error

## Advanced: Development Setup

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/kysu1313/Claude-Multi.git
cd Claude-Multi

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install in development mode with dev dependencies
pip3 install -e ".[dev]"

# Run tests (when available)
pytest

# Format code
black claude_multi/

# Lint
flake8 claude_multi/
```

## Shell Integration Examples

### Bash (~/.bashrc)

```bash
# Claude Multi alias
alias cm='python3 -m claude_multi.cli'
alias cm-start='python3 -m claude_multi.cli start .'
alias cm-status='python3 -m claude_multi.cli status'
alias cm-sync='python3 -m claude_multi.cli sync .'
```

### Zsh (~/.zshrc)

```bash
# Claude Multi aliases
alias cm='python3 -m claude_multi.cli'
alias cm-start='python3 -m claude_multi.cli start .'
alias cm-status='python3 -m claude_multi.cli status'
alias cm-sync='python3 -m claude_multi.cli sync .'
```

### Fish (~/.config/fish/config.fish)

```fish
# Claude Multi aliases
alias cm='python3 -m claude_multi.cli'
alias cm-start='python3 -m claude_multi.cli start .'
alias cm-status='python3 -m claude_multi.cli status'
alias cm-sync='python3 -m claude_multi.cli sync .'
```

Now you can use shortcuts:
```bash
cm start .           # Start session
cm-status            # Check status
cm-sync              # Sync memory
```

---

**Ready to use!** Run `./run.sh start .` or `claude-multi start .` to begin.
