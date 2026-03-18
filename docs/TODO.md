# Trail Status — Project TODO

## Current Session
- [ ] Install Flask-SQLAlchemy and set up SQLite database
- [ ] Create `models.py` — Trail database model
- [ ] Create `seed.py` — migrate hardcoded trails into the database
- [ ] Update `app.py` — fetch trails from DB instead of hardcoded list
- [ ] Create `/admin` page — view and add trails without touching code
- [ ] Auto-update `tools.txt` from `requirements.txt` using a script or agent

---

## Phase 1 — Weather & Foundation
- [ ] Add caching to weather API calls (avoid fetching on every page load)
- [ ] Add a trail detail page (`/trail/<id>`) with full weather breakdown
- [ ] Add "last updated" timestamp to homepage
- [ ] Initialize Git repo and push to GitHub ✅
- [ ] Set up SQLite database ← in progress

---

## Phase 2 — User Interaction
- [ ] User registration and login (Flask-Login)
- [ ] Trail condition reports (users can post updates)
- [ ] Comment system on trail reports
- [ ] Upvote/downvote trail reports

---

## Phase 3 — Admin Portal
- [ ] Admin login with protected routes
- [ ] Moderate/delete user reports
- [ ] Add, edit, and remove trails via UI
- [ ] Trail status override (admin can manually set Open/Closed)

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

## General / Resume Polish
- [ ] Mobile-friendly UI improvements
- [ ] Add trail map (leaflet.js or Google Maps embed)
- [ ] Deploy to Render or Railway
- [ ] Custom domain name
- [ ] Add README.md with project description and screenshots
- [ ] Write up project as a portfolio case study
