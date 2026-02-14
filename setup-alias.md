# Setting Up Aliases for Easy Use

## Windows PowerShell

Add this to your PowerShell profile (`$PROFILE`):

```powershell
# Add alias for claude-multi
function claude-multi { python -m claude_multi.cli $args }
```

Then reload:
```powershell
. $PROFILE
```

Now you can use:
```powershell
claude-multi init
claude-multi start .
claude-multi status
```

## Windows Command Prompt

Create a file `claude-multi.bat` in a directory that's in your PATH (e.g., `C:\Windows\`):

```batch
@echo off
python -m claude_multi.cli %*
```

## Git Bash / WSL

Add to `~/.bashrc` or `~/.bash_profile`:

```bash
alias claude-multi='python -m claude_multi.cli'
```

Then reload:
```bash
source ~/.bashrc
```

## Alternative: Use the Batch File

Simply use the provided `run.bat` from the project directory:

```bash
cd C:\Users\ksups\PROGRAMS\python\claude-multi
.\run.bat start .
.\run.bat status
```

## Or: Add Scripts Directory to PATH

Add this to your system PATH:
```
C:\Users\ksups\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts
```

Steps:
1. Open System Properties → Environment Variables
2. Edit PATH variable
3. Add the directory above
4. Restart terminal
5. Use `claude-multi` directly
