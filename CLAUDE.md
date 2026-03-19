# Trail Status — Claude Code Session Guide

## What this project is
A trail condition tracker for mountain bikers in NC. Shows whether trails are Open / Caution / Closed
based on weather data (rainfall, soil moisture, freeze/thaw) and trail drainage characteristics.
Long-term goal: ML-powered predictions + real-time soil moisture sensors at trailheads.

## Session start checklist
1. Read `app.py` and `weather.py` to understand current state
2. Give the user a prioritized daily task list (3–5 tasks)
3. Proactively suggest features or Claude Code workflows relevant to the next phase

## Project phases
- Phase 1 (active): Flask + Open-Meteo weather API
- Phase 2: User accounts + trail reports
- Phase 3: Admin portal
- Phase 4: ML prediction model
- Phase 5: Hardware soil moisture sensors

## Key files
- `app.py` — Flask routes and trail data
- `weather.py` — Open-Meteo API calls and status logic
- `templates/index.html` — Homepage template
- `static/style.css` — Site styles
- `.env` — API keys and config (not committed)

## Working with this user
- Beginner Python developer — explain concepts and patterns as you go
- Keep code clean and well-commented
- Always explain what changed and why after edits
- Suggest next features proactively

## Access control decisions
| Feature | Access |
|---|---|
| View trail status | Anyone |
| View trail reports | Anyone |
| Post a trail report | Anyone (name optional) |
| Edit/delete reports | Admin only |
| Add/remove trails | Admin only (login required) |
| Override trail status | Admin only (login required) |

Login for regular users becomes valuable in Phase 3+ when profiles, saved trails, and report history are added.

## Tech stack
- Python / Flask / Jinja2
- Open-Meteo API (free, no key needed)
- HTML/CSS, eventually JS
- No database yet — trails hardcoded in app.py
