"""
update_tools.py — Regenerate tools.txt from this registry + requirements.txt

Run after adding any new tool or after pip install:
    python3 update_tools.py

To add a new tool: find the right category below and add an entry.
Libraries are pulled automatically from requirements.txt.
"""

# ================================================================
#  TOOL REGISTRY — add new tools here
# ================================================================

LANGUAGES = [
    ("Python",   "https://www.python.org"),
    ("HTML/CSS", "(built into browsers)"),
]

APIS = [
    {
        "name": "Open-Meteo",
        "desc": "Free weather + soil moisture API (no key needed)",
        "url":  "https://open-meteo.com",
        "notes": [
            "Docs: https://open-meteo.com/en/docs",
            "Data used: precipitation, soil moisture, temperature (freeze/thaw)",
        ],
    },
]

VERSION_CONTROL = [
    ("Git",    "Local version control",  "https://git-scm.com"),
    ("GitHub", "Remote repo hosting",    "https://github.com"),
    ("Repo",   "",                       "https://github.com/krishdkashyap/Trail-Status"),
]

DEV_ENVIRONMENT = [
    ("Python venv",  "Isolated Python environment (built into Python)", ""),
    ("pip",          "Python package installer (built into Python)",     ""),
    ("VS Code",      "Code editor",                                      "https://code.visualstudio.com"),
    ("Claude Code",  "AI coding assistant (VS Code extension + CLI)",    "https://claude.ai/code"),
]

VS_CODE_EXTENSIONS = [
    ("Python",        "Syntax highlighting and error detection",  "Microsoft"),
    ("Pylance",       "Smarter Python autocomplete",              "Microsoft"),
    ("GitLens",       "Inline git history and blame",             "GitKraken"),
    ("SQLite Viewer", "Browse SQLite databases inside VS Code",   "Florian Klampfer"),
]

PLANNED_TOOLS = [
    ("SQLite",        "Local database (Phase 1)",              "Built into Python"),
    ("PostgreSQL",    "Production database (Phase 2+)",        "https://www.postgresql.org"),
    ("Flask-Login",   "User authentication (Phase 2)",         "https://flask-login.readthedocs.io"),
    ("Render",        "Cloud hosting/deployment",              "https://render.com"),
    ("scikit-learn",  "Machine learning library (Phase 4)",    "https://scikit-learn.org"),
    ("pandas",        "Data analysis (Phase 4)",               "https://pandas.pydata.org"),
]

# ================================================================
#  Packages to hide from the libraries section (low-level deps)
# ================================================================
SKIP_PACKAGES = {
    "blinker", "certifi", "charset-normalizer", "idna", "urllib3",
    "MarkupSafe", "itsdangerous", "click", "Werkzeug", "typing-extensions",
}

# Known descriptions for packages in requirements.txt
KNOWN_PACKAGES = {
    "Flask":            ("Web framework",                             "https://flask.palletsprojects.com"),
    "Flask-SQLAlchemy": ("Database ORM",                              "https://flask-sqlalchemy.palletsprojects.com"),
    "SQLAlchemy":       ("Database toolkit (used by Flask-SQLAlchemy)", "https://www.sqlalchemy.org"),
    "Jinja2":           ("HTML templating (comes with Flask)",        "https://jinja.palletsprojects.com"),
    "requests":         ("HTTP library for API calls",                "https://requests.readthedocs.io"),
    "python-dotenv":    ("Loads .env variables",                      "https://pypi.org/project/python-dotenv"),
    "Flask-Login":      ("User authentication",                       "https://flask-login.readthedocs.io"),
    "Flask-WTF":        ("Form handling and validation",              "https://flask-wtf.readthedocs.io"),
    "pandas":           ("Data analysis library",                     "https://pandas.pydata.org"),
    "scikit-learn":     ("Machine learning library",                  "https://scikit-learn.org"),
}


# ================================================================
#  Script — reads requirements.txt and builds tools.txt
# ================================================================

def read_requirements():
    packages = []
    try:
        with open("requirements.txt") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                name, _, version = line.partition("==")
                name = name.strip()
                if name not in SKIP_PACKAGES:
                    packages.append((name, version.strip()))
    except FileNotFoundError:
        print("Warning: requirements.txt not found")
    return packages


def divider():
    return "=" * 64


def section(title, lines):
    out = [title, "-" * len(title)]
    out.extend(lines)
    return "\n".join(out)


def build_tools_file():
    from datetime import date

    blocks = []
    blocks.append(divider())
    blocks.append("  TRAIL STATUS — Tools, Libraries & Resources")
    blocks.append(divider())

    # Languages
    lang_lines = [f"{name:<20}{url}" for name, url in LANGUAGES]
    blocks.append(section("LANGUAGES", lang_lines))

    # Libraries (from requirements.txt)
    packages = read_requirements()
    lib_lines = []
    for name, version in packages:
        desc, url = KNOWN_PACKAGES.get(name, ("", f"https://pypi.org/project/{name}"))
        if desc:
            lib_lines.append(f"{name:<20}{desc} — {url}")
        else:
            lib_lines.append(f"{name:<20}{url}")
    blocks.append(section("FRAMEWORKS & LIBRARIES", lib_lines))

    # APIs
    api_lines = []
    for api in APIS:
        api_lines.append(f"{api['name']:<20}{api['desc']}")
        api_lines.append(f"{'':20}{api['url']}")
        for note in api.get("notes", []):
            api_lines.append(f"{'':20}{note}")
    blocks.append(section("APIS & DATA SOURCES", api_lines))

    # Version control
    vc_lines = []
    for name, desc, url in VERSION_CONTROL:
        if desc:
            vc_lines.append(f"{name:<20}{desc} — {url}")
        else:
            vc_lines.append(f"{name:<20}{url}")
    blocks.append(section("VERSION CONTROL & HOSTING", vc_lines))

    # Dev environment
    dev_lines = []
    for name, desc, url in DEV_ENVIRONMENT:
        entry = f"{name:<20}{desc}"
        if url:
            entry += f" — {url}"
        dev_lines.append(entry)
    blocks.append(section("DEVELOPMENT ENVIRONMENT", dev_lines))

    # VS Code extensions
    ext_lines = [f"{name:<20}{desc} ({publisher})" for name, desc, publisher in VS_CODE_EXTENSIONS]
    blocks.append(section("VS CODE EXTENSIONS", ext_lines))

    # Planned tools
    planned_lines = []
    for name, desc, url in PLANNED_TOOLS:
        entry = f"{name:<20}{desc}"
        if url:
            entry += f" — {url}"
        planned_lines.append(entry)
    blocks.append(section("PLANNED / FUTURE TOOLS", planned_lines))

    blocks.append(divider())
    blocks.append(f"  Last updated: {date.today()}")
    blocks.append(divider())

    return "\n\n\n".join(blocks) + "\n"


if __name__ == "__main__":
    content = build_tools_file()
    with open("docs/tools.txt", "w") as f:
        f.write(content)
    print("tools.txt updated successfully.")
