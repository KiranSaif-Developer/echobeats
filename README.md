<div align="center">

# 🎧 EchoBeats

**A full-stack social music streaming platform** — browse songs, build playlists, and listen together.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791?logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?logo=javascript&logoColor=black)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue)

[Live Demo](#) · [Report a Bug](#) · [Request a Feature](#)

</div>

---

## 📸 Preview

<!--
  Add real screenshots or a short GIF walkthrough here before sharing this
  README — this is the single highest-impact thing you can add. A 10-second
  screen recording converted to GIF (using ScreenToGif or similar) of you
  signing up, browsing songs, and playing one works great.
-->

| Landing Page | Song Library | Player |
|---|---|---|
| _screenshot here_ | _screenshot here_ | _screenshot here_ |

---

## 🧩 Overview

EchoBeats is a full-stack music streaming application built to explore how a modern
social-audio product is actually put together — from database design and secure
authentication, to a real-time playback engine and a hand-built design system.

Rather than a UI mockup, every feature shown is fully functional end-to-end: real
accounts, a real PostgreSQL database, and real audio/video playback via the YouTube
IFrame API.

## ✨ Key Features

- 🔐 **Secure authentication** — bcrypt password hashing + JWT-based sessions
- 🎵 **Real playback** — songs play via the YouTube IFrame Player API, fully controlled by a custom UI (no visible embed, no YouTube branding)
- ➕ **Add any song** — paste a YouTube link and it's instantly added to the library
- 📃 **Playlists** — create, view, and manage personal playlists
- ❤️ **Likes** — save favorite tracks to a personal collection
- 🔍 **Live search** — debounced search across song titles and artists
- 🎨 **Custom design system** — a hand-built visual identity (typographic album art, animated equalizer motif, light theme) rather than a UI-kit default

## 🛠️ Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript | No framework overhead for a project this size; forces a real understanding of the DOM and state management |
| Backend | Python, Flask | Lightweight, explicit routing, easy to reason about for a REST API |
| Database | PostgreSQL (hosted on Supabase) | Relational integrity for users/songs/playlists/likes/follows; Supabase gives free managed Postgres + a SQL editor |
| DB Driver | pg8000 | Pure-Python Postgres driver — avoids native-compiler build issues on newer Python versions |
| Auth | PyJWT + bcrypt | Industry-standard token-based auth with salted password hashing |
| Playback | YouTube IFrame Player API | Real audio/video playback without hosting or licensing media files |

## 🏗️ Architecture

```
┌─────────────────────┐
│   Frontend            │
│   HTML / CSS / JS      │   REST (JSON) + JWT Bearer auth
│   YouTube IFrame API   │◄──────────────────────────────┐
└─────────────────────┘                                │
                                                          ▼
                                                ┌──────────────────┐
                                                │   Flask REST API   │
                                                │  auth / songs /     │
                                                │  playlists blueprints│
                                                └─────────┬────────┘
                                                          │ pg8000
                                                          ▼
                                                ┌──────────────────┐
                                                │  PostgreSQL (Supabase) │
                                                │  users, songs,          │
                                                │  playlists, likes,       │
                                                │  follows, comments        │
                                                └──────────────────┘
```

## 🧠 Technical Highlights

A few decisions worth calling out (the parts that tend to come up in interviews):

- **Driver choice under real constraints** — `psycopg2-binary` had no prebuilt wheel for the Python version this was built on, and building it from source needed a heavy compiler toolchain. Swapped to `pg8000`, a pure-Python driver, and wrote a small `fetch_all` / `fetch_one` / `execute` helper layer so the rest of the codebase didn't need to care about the underlying driver's API differences.
- **Stateless auth** — JWT tokens issued on login/signup, verified per-request via a `@login_required` decorator, keeping the API stateless and horizontally scalable in principle.
- **No media hosting required** — rather than storing and streaming audio files (which real licensing and storage costs make impractical for a demo), playback is delegated to the YouTube IFrame API, with the app's own UI fully driving play/pause/seek state.
- **CORS-aware local dev setup** — frontend and backend run on separate local ports during development; `flask-cors` is configured explicitly rather than left wide open.

## 🚀 Getting Started

Full setup instructions (Postgres/Supabase setup, environment variables, running
both servers) are in [`backend/README.md`](./backend/README.md).

Quick version:
```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env   # then fill in your DB credentials
python app.py

# Frontend (separate terminal)
cd frontend
python -m http.server 5500
```
Then open `http://localhost:5500`.

## 📁 Project Structure

```
echobeats/
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── auth_utils.py
│   ├── requirements.txt
│   └── routes/
│       ├── auth.py
│       ├── songs.py
│       └── playlists.py
├── frontend/
│   └── index.html
└── database/
    ├── 02_tables_and_data.sql
    └── 03_add_youtube_support.sql
```

## 🗺️ Roadmap

- [ ] Follow system + activity feed (see who your friends are listening to)
- [ ] Comments on songs
- [ ] Collaborative playlists
- [ ] Recommendation engine

## 👤 Author

**Your Name** — add your LinkedIn, portfolio site, and email here.

## 📄 License

MIT — free to use as a reference or starting point.
