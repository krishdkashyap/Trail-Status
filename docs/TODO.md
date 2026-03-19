# Trail Status — Project TODO

---

## Up Next (Session 3)
- [ ] Add caching to weather API calls (Flask-Caching)
- [ ] Phase 3 planning — role-based admin accounts
- [ ] "Last updated" timestamp on homepage

---

## Phase 1 — Weather & Foundation
- [x] Initialize Git repo and push to GitHub
- [x] Set up SQLite database (Flask-SQLAlchemy)
- [x] Live weather integration (Open-Meteo)
- [x] Trail status logic (precipitation, soil moisture, freeze/thaw, drainage)
- [x] Trail detail pages with full weather breakdown
- [ ] Add caching to weather API calls
- [ ] Add "last updated" timestamp to homepage

---

## Phase 2 — User Interaction
- [x] Admin login with protected routes (Flask-Login)
- [x] CSRF protection on all forms (Flask-WTF)
- [x] Trail condition reports — anyone can post
- [x] Admin can delete reports
- [x] Trail status override (admin manually sets Open/Caution/Closed)
- [ ] Upvote/downvote trail reports
- [ ] Comment system on trail reports

---

## Phase 3 — Admin Portal
- [x] Add, edit, and remove trails via UI
- [x] Access control design (documented in CLAUDE.md)
- [ ] Role-based admin accounts (superadmin vs trail_admin)
- [ ] Per-trail permissions — trail admins can only edit their assigned trail
- [ ] User management page (create/assign/remove admin accounts)

---

## Phase 4 — Machine Learning
- [ ] Store historical weather + status data in database
- [ ] Build training dataset from historical conditions
- [ ] Train ML model (precipitation, soil moisture, freeze/thaw, drainage)
- [ ] Replace rule-based status logic with model predictions
- [ ] Display prediction confidence score on trail cards

---

## Phase 5 — Hardware
- [ ] Research soil moisture sensor options (Arduino / Raspberry Pi)
- [ ] Build sensor data ingestion endpoint
- [ ] Replace estimated soil moisture with real sensor readings
- [ ] Trailhead weather station integration

---

## Automation & Tooling
- [ ] Auto-update tools.txt when new tools are added (script or agent)
- [ ] Scheduled end-of-session report (auto-appends to PROGRESS.md)

---

## General / Resume Polish
- [ ] Mobile-friendly UI improvements
- [ ] Add trail map (Leaflet.js or Google Maps embed)
- [ ] Deploy to Render or Railway
- [ ] Custom domain name
- [ ] Add README.md with project description and screenshots
- [ ] Write up project as a portfolio case study
