# GitHub Copilot Workspace Instructions

## Python Environment Setup

This project uses a Python virtual environment located at `.venv/`. Before running any Python commands, scripts, or applications, always activate the virtual environment first.

### Activation Command
```bash
source .venv/bin/activate
```

### When to Activate
- Before running `python app.py` or any Python script
- Before installing packages with `pip`
- Before running tests or any Python-related commands
- When using tools that execute Python code

### Example Usage
Instead of:
```bash
python app.py
```

Use:
```bash
source .venv/bin/activate
python app.py
```

### Important Notes
- The virtual environment should already be created and contain the required dependencies from `requirements.txt`
- If `.venv` doesn't exist, create it with `python -m venv .venv` and then `source .venv/bin/activate && pip install -r requirements.txt`
- Always ensure the venv is activated in the current terminal session before executing Python commands