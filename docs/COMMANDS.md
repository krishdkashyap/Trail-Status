# Trail Status — Command Reference

## Every Day (Start of Session)
```bash
cd ~/trail-status
source venv/bin/activate
python3 app.py
```
Then open http://127.0.0.1:5000 in your browser.
Stop the server with CTRL+C when done.

---

## Git — Save Your Work
```bash
git add .
git commit -m "describe what you changed"
git push
```
Do this after every meaningful change.

---

## Database
```bash
# First time only — loads trails into the database
python3 seed.py

# Open the database in the terminal
sqlite3 instance/trails.db
SELECT * FROM trail;   # view all trails
.quit                  # exit
```

---

## Install a New Package
```bash
pip install <package-name>
pip freeze > requirements.txt
python3 update_tools.py
```

---

## Update tools.txt
```bash
python3 update_tools.py
```

---

## Open Project in VS Code
```bash
code ~/trail-status
```

---

## Virtual Environment
```bash
# Activate (do this every session)
source venv/bin/activate

# Deactivate (when done)
deactivate
```

---

## VS Code Shortcuts
| Shortcut      | What it does                        |
|---------------|-------------------------------------|
| Ctrl+`        | Open/close integrated terminal      |
| ⌘⇧P           | Command Palette (search any action) |
| ⌘⇧X           | Extensions panel                    |
| ⌘⇧E           | File explorer                       |
| ⌘⇧G           | Git / Source Control panel          |
| ⌘P            | Quick open any file by name         |
| ⌘/            | Comment/uncomment a line of code    |
