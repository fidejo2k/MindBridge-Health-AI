\# CLI COMMAND REFERENCE FOR HEALTHCARE AI ENGINEERS

\*\*Last Updated:\*\* February 10, 2026  

\*\*Version:\*\* 1.0  

\*\*Platform:\*\* Windows 11 (with notes for Mac/Linux)



---



\## 🖥️ WINDOWS POWERSHELL / COMMAND PROMPT BASICS



\### Opening Terminal

\- \*\*PowerShell:\*\* `Windows Key` → type `powershell` → Enter

\- \*\*Command Prompt:\*\* `Windows Key + R` → type `cmd` → Enter

\- \*\*From Folder:\*\* Shift + Right-click in folder → "Open PowerShell window here"



\### Navigation

```powershell

\# Show current directory

pwd                              # PowerShell

cd                              # Command Prompt



\# List files and folders

dir                             # Windows

ls                              # PowerShell (also works)



\# Change directory

cd "E:\\Mindbridge health care"  # Use quotes if spaces in path

cd scripts                      # Go into subfolder

cd ..                           # Go up one level

cd ..\\..                        # Go up two levels



\# Go to specific drive

E:                              # Switch to E drive

C:                              # Switch to C drive

```



\### File Operations

```powershell

\# Create folder

mkdir reports                   # Make directory

mkdir "New Folder"              # Use quotes for spaces



\# Create empty file

type nul > test.txt             # Command Prompt

New-Item test.txt               # PowerShell



\# Copy files

copy file.txt backup.txt        # Copy file

xcopy scripts backup /E /I      # Copy folder with contents



\# Move files

move file.txt reports\\          # Move file to folder



\# Delete files

del file.txt                    # Delete file

rmdir /S reports                # Delete folder and contents



\# View file contents

type file.txt                   # Display file

more file.txt                   # Display with pagination

```



---



\## 🐍 PYTHON COMMANDS



\### Check Installation

```powershell

\# Check Python version

python --version

\# Output: Python 3.13.11



\# Check where Python is installed

where python                    # Windows

which python                    # Mac/Linux



\# Check pip version

pip --version

```



\### Running Python Scripts

```powershell

\# Run a Python script

python script.py



\# Run with full path

python "E:\\Mindbridge health care\\scripts\\patient\_analyzer.py"



\# Run from different directory

cd "E:\\Mindbridge health care"

python scripts\\patient\_analyzer.py



\# Run Python interactively (REPL)

python

>>> print("Hello")

>>> exit()                      # Exit Python

```



\### Python Package Management (pip)

```powershell

\# Install package

pip install anthropic

pip install pandas

pip install requests



\# Install specific version

pip install anthropic==0.25.0



\# Install from requirements file

pip install -r requirements.txt



\# Upgrade package

pip install --upgrade anthropic

pip install --upgrade pip



\# Uninstall package

pip uninstall anthropic



\# List installed packages

pip list



\# Show package details

pip show anthropic



\# Search for packages

pip search healthcare            # Note: This may not work on all systems



\# Freeze installed packages (for sharing)

pip freeze > requirements.txt

```



\*\*REMEMBER:\*\* Always use `--break-system-packages` flag if needed on some systems:

```powershell

pip install anthropic --break-system-packages

```



---



\## 🔑 ENVIRONMENT VARIABLES (Windows)



\### Viewing Environment Variables

```powershell

\# View all environment variables

set                             # Command Prompt

Get-ChildItem Env:              # PowerShell



\# View specific variable

echo %ANTHROPIC\_API\_KEY%        # Command Prompt

$env:ANTHROPIC\_API\_KEY          # PowerShell

```



\### Setting Environment Variables (Temporary - Current Session Only)

```powershell

\# Command Prompt (current session only)

set ANTHROPIC\_API\_KEY=sk-ant-api...



\# PowerShell (current session only)

$env:ANTHROPIC\_API\_KEY = "sk-ant-api..."

```



\### Setting Environment Variables (Permanent - GUI Method)

1\. Press `Windows Key`

2\. Type: `environment variables`

3\. Click: "Edit the system environment variables"

4\. Click: "Environment Variables..." button

5\. Under "User variables", click "New..."

6\. Variable name: `ANTHROPIC\_API\_KEY`

7\. Variable value: \[your key]

8\. Click OK on all windows

9\. \*\*RESTART YOUR TERMINAL\*\* (important!)



\### Testing Environment Variable

```powershell

\# Command Prompt

echo %ANTHROPIC\_API\_KEY%

\# Should show: sk-ant-api...



\# PowerShell

echo $env:ANTHROPIC\_API\_KEY

\# Should show: sk-ant-api...



\# If shows the variable name literally, it's not set!

```



---



\## 📁 FILE \& FOLDER MANAGEMENT



\### Creating Project Structure

```powershell

\# Create project folders

cd "E:\\Mindbridge health care"

mkdir scripts

mkdir reports

mkdir data

mkdir tests



\# Create multiple folders at once

mkdir output\\reports output\\logs output\\temp

```



\### Organizing Files

```powershell

\# Move Python files to scripts folder

move \*.py scripts\\



\# Copy all reports to backup

xcopy reports reports\_backup\\ /E /I



\# Delete all .txt files in current folder

del \*.txt



\# Delete all files in reports folder

del reports\\\*.\*

```



\### Finding Files

```powershell

\# Find files by name

dir /s patient\*.py              # Search subdirectories



\# Find files by extension

dir /s \*.csv



\# Find text in files

findstr "High Risk" \*.txt       # Search text in all .txt files

```



---



\## 🔧 TROUBLESHOOTING COMMANDS



\### Common Issues



\#### "Command not recognized" Error

```powershell

\# Problem: 'python' is not recognized...

\# Solution: Python not in PATH



\# Fix 1: Use full path

"C:\\Users\\TOBBY\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" script.py



\# Fix 2: Add Python to PATH (permanently)

\# Windows Key → "environment variables" → Edit PATH → Add Python folder

```



\#### "Permission Denied" Error

```powershell

\# Problem: Can't write to file

\# Solution: Run as administrator OR change location



\# Run PowerShell as admin:

\# Right-click PowerShell → "Run as administrator"

```



\#### "Module not found" Error

```powershell

\# Problem: ModuleNotFoundError: No module named 'anthropic'

\# Solution: Install the package



pip install anthropic



\# If still fails, check which Python pip is using:

pip --version

python --version



\# Make sure they match!

```



\#### "File not found" Error

```powershell

\# Problem: Can't find file

\# Solution: Check you're in right directory



\# Show current location

cd



\# List files

dir



\# Navigate to correct folder

cd "E:\\Mindbridge health care"

```



---



\## 🚀 RUNNING YOUR HEALTHCARE AI SCRIPTS



\### Script #1: Single Patient Analyzer

```powershell

cd "E:\\Mindbridge health care"

python scripts\\patient\_analyzer.py

```



\### Script #2: Batch Processor

```powershell

cd "E:\\Mindbridge health care"

python scripts\\batch\_processor.py

```



\### Script #3: Report Generator

```powershell

cd "E:\\Mindbridge health care"

python scripts\\report\_generator.py

```



\### Script #4: CSV Patient Analyzer

```powershell

cd "E:\\Mindbridge health care"

python scripts\\csv\_patient\_analyzer.py

```



\### Run with Error Logging

```powershell

\# Save errors to log file

python scripts\\csv\_patient\_analyzer.py 2> error\_log.txt



\# Save both output and errors

python scripts\\csv\_patient\_analyzer.py > output.txt 2>\&1

```



---



\## 📊 WORKING WITH DATA FILES



\### CSV Files

```powershell

\# View CSV in terminal

type patients.csv

more patients.csv               # Paginated view



\# Count lines (patients)

find /c /v "" patients.csv      # Windows



\# Copy CSV for backup

copy patients.csv patients\_backup.csv

```



\### Report Files

```powershell

\# View report

type reports\\daily\_screening\_20260210.txt

more reports\\daily\_screening\_20260210.txt



\# Open in Notepad

notepad reports\\daily\_screening\_20260210.txt



\# Search in report

findstr "HIGH RISK" reports\\daily\_screening\_20260210.txt

```



---



\## 🔄 GIT COMMANDS (Coming Thursday!)



\### Basic Git Workflow

```powershell

\# Initialize repository

git init



\# Check status

git status



\# Add files

git add .                       # Add all files

git add script.py               # Add specific file



\# Commit changes

git commit -m "Initial commit"

git commit -m "Added patient analyzer"



\# View history

git log

git log --oneline               # Compact view



\# Create branch

git branch feature-new-analyzer

git checkout feature-new-analyzer



\# Push to GitHub

git remote add origin https://github.com/username/repo.git

git push -u origin main

```



---



\## ⚡ PRODUCTIVITY SHORTCUTS



\### Terminal Shortcuts

\- \*\*Ctrl + C\*\*: Stop running program

\- \*\*Ctrl + L\*\* or `cls`: Clear screen

\- \*\*Tab\*\*: Auto-complete file/folder names

\- \*\*Up Arrow\*\*: Previous command

\- \*\*Down Arrow\*\*: Next command

\- \*\*Ctrl + R\*\*: Search command history (PowerShell)



\### Command History

```powershell

\# View recent commands

doskey /history                 # Command Prompt

Get-History                     # PowerShell



\# Re-run previous command

!!                              # PowerShell (requires module)



\# Re-run command from history

\#                        # PowerShell

```



\### Aliases (PowerShell)

```powershell

\# Create shortcut commands

Set-Alias analyze "python scripts\\patient\_analyzer.py"



\# Now you can just type:

analyze

```



---



\## 🎯 DAILY WORKFLOW COMMANDS



\### Morning Setup

```powershell

\# 1. Navigate to project

cd "E:\\Mindbridge health care"



\# 2. Check for new patient data

dir data\\\*.csv



\# 3. Run daily screening

python scripts\\csv\_patient\_analyzer.py



\# 4. Check reports folder

dir reports\\

```



\### Testing New Script

```powershell

\# 1. Edit script in Notepad

notepad scripts\\new\_script.py



\# 2. Save and run

python scripts\\new\_script.py



\# 3. If error, check error message

\# 4. Fix and re-run

python scripts\\new\_script.py



\# 5. When working, move to production folder

```



---



\## 📦 VIRTUAL ENVIRONMENTS (Advanced - Optional)



\### Why Use Virtual Environments?

\- Isolate project dependencies

\- Avoid package conflicts

\- Easier deployment



\### Creating Virtual Environment

```powershell

\# Create virtual environment

python -m venv venv



\# Activate it

venv\\Scripts\\activate           # Windows



\# Install packages (only in this environment)

pip install anthropic pandas



\# Deactivate when done

deactivate

```



---



\## 🔍 USEFUL UTILITIES



\### System Information

```powershell

\# Check system info

systeminfo



\# Check disk space

wmic logicaldisk get size,freespace,caption



\# Check memory

wmic memorychip get capacity



\# Check Python packages disk usage

pip list --format=freeze

```



\### Network Commands

```powershell

\# Test internet connection

ping google.com



\# Test API endpoint

curl https://api.anthropic.com/v1/messages

```



---



\## 🚨 EMERGENCY FIXES



\### Python Script Won't Run

```powershell

\# Step 1: Verify Python installed

python --version



\# Step 2: Verify you're in correct folder

cd

dir



\# Step 3: Check file exists

dir scripts\\script\_name.py



\# Step 4: Try running with full path

python "E:\\Mindbridge health care\\scripts\\script\_name.py"



\# Step 5: Check for syntax errors

python -m py\_compile scripts\\script\_name.py

```



\### Pip Won't Install Package

```powershell

\# Step 1: Upgrade pip

python -m pip install --upgrade pip



\# Step 2: Clear cache

pip cache purge



\# Step 3: Try again

pip install anthropic



\# Step 4: If still fails, check internet

ping pypi.org

```



\### Environment Variable Not Working

```powershell

\# Step 1: Close and reopen terminal

\# Step 2: Check it's set

echo %ANTHROPIC\_API\_KEY%



\# Step 3: Set temporarily to test

set ANTHROPIC\_API\_KEY=sk-ant-api...



\# Step 4: Run script

python scripts\\test.py



\# Step 5: If works, problem was permanent setting - redo GUI method

```



---



\## 📚 QUICK REFERENCE CHEAT SHEET

```powershell

\# NAVIGATION

cd folder                       # Change directory

cd ..                           # Go up one level

dir                            # List files

pwd                            # Show current location



\# FILES

mkdir folder                    # Create folder

type file.txt                   # View file

copy file.txt backup.txt        # Copy file

move file.txt folder\\           # Move file

del file.txt                    # Delete file



\# PYTHON

python script.py                # Run script

python --version                # Check version

pip install package             # Install package

pip list                        # List packages



\# ENVIRONMENT

echo %VAR%                      # View variable (cmd)

echo $env:VAR                   # View variable (PowerShell)

set VAR=value                   # Set variable (cmd, temporary)



\# GIT (coming soon!)

git status                      # Check status

git add .                       # Stage all files

git commit -m "message"         # Commit

git push                        # Push to remote



\# TROUBLESHOOTING

cls                            # Clear screen

Ctrl + C                       # Stop program

python -m pip install --upgrade pip  # Upgrade pip

```



---



\## 💡 PRO TIPS



1\. \*\*Use Tab completion\*\* - Start typing filename and press Tab

2\. \*\*Use Up Arrow\*\* - Quickly re-run previous commands

3\. \*\*Keep terminal open\*\* - Don't close and reopen constantly

4\. \*\*Use quotes for spaces\*\* - `cd "folder name"` not `cd folder name`

5\. \*\*Always check you're in right folder\*\* - Use `cd` to verify

6\. \*\*Use UTF-8 encoding\*\* - Prevents weird character errors

7\. \*\*Restart terminal after env variable changes\*\* - Required for changes to take effect

8\. \*\*Save long commands as scripts\*\* - Create `.bat` or `.ps1` files



---



\## 🎯 WHAT'S COMING NEXT WEEK



\### Git \& GitHub Commands

\- Repository management

\- Version control

\- Collaboration workflows

\- Deployment scripts



\### Advanced Automation

\- Batch files (.bat)

\- PowerShell scripts (.ps1)

\- Scheduled tasks

\- Error handling



---



\*\*KEEP THIS HANDY!\*\* Reference it whenever you need CLI help! 💻



