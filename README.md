# Luminara — AI Powered Cyber Threat Detection & Awareness Platform

> **"See the threat before it sees you."**

Luminara is a mobile-first AI cybersecurity assistant that helps everyday users detect phishing messages, deepfake media — while building cybersecurity awareness through daily learning streaks.

---

## Project Structure

```
luminara/
├── backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── api/v1/endpoints/     # Route handlers per module
│   │   ├── core/                 # Config, security, logging
│   │   ├── db/                   # Models + repositories (PostgreSQL)
│   │   ├── schemas/              # Pydantic request/response models
│   │   ├── services/             # Business logic per module
│   │   │   ├── ai_agent/         # Input classifier + router
│   │   │   ├── phishing/         # BERT phishing detection
│   │   │   ├── deepfake/         # AASIST audio + GenConViT video
│   │   │   └── awareness/        # Lessons + quiz engine
│   │   ├── middleware/           # Auth, rate limiting, CORS
│   │   └── utils/                # Shared helpers
│   ├── alembic/                  # DB migrations
│   └── tests/                    # Unit + integration tests
│
├── mobile/           # react native mobile app (iOS + Android)
│   ├── lib/
│   │   ├── core/                 # Theme, constants, network, utils
│   │   ├── features/             # One folder per app feature
│   │   └── shared/               # Reusable widgets, models, providers
│   └── assets/                   # Images, fonts, animations
│
├── ai_models/        # Model weights, training scripts, utilities
│   ├── phishing/                 # BERT fine-tuned model
│   ├── deepfake/                 # AASIST (audio) + GenConViT (video)
│   └── agent/                   # Input classifier + router logic
│
├── docs/             # Architecture, API docs, deployment guides
├── scripts/          # Setup, seed, deploy scripts
└── tests/            # End-to-end tests
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Mobile | react native |
| Backend | Python 3.11 + FastAPI |
| Database | PostgreSQL via Supabase |
| Auth | JWT (RS256) + Supabase Auth |
| Phishing AI | BERT (`ealvaradob/bert-finetuned-phishing`) + RoBERTa URL layer |
| Audio Deepfake | AASIST (`clovaai/aasist`) |
| Video Deepfake | GenConViT ensemble + CLIP frame features |
| QR + URL Threat | VirusTotal API + Google Safe Browsing API |
| AI Orchestration | Custom AI Security Agent (rule-based + NLP classifier) |
| Containerisation | Docker + Docker Compose |

---

## Development Phases

| Phase | Description | Status |
|---|---|---|
| 1 | System architecture & folder structure | ✅ Current |
| 2 | Backend API setup (FastAPI + Auth + DB) | ⏳ Next |
| 3 | AI Security Agent | ⏳ |
| 4 | Phishing Detection Module | ⏳ |
| 5 | Deepfake Detection Module | ⏳ |
| 6 | Cybersecurity Awareness Learning | ⏳ |
| 7 | Daily Streak Gamification | ⏳ |
| 8 | Mobile UI Integration | ⏳ |

---

## Quick Start

```bash
# 1. Clone and enter project
git clone <repo-url> && cd luminara

# 2. Backend setup
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
alembic upgrade head
uvicorn app.main:app --reload

# 3. Mobile setup (separate terminal)
cd ../mobile
React Native
Download Expo Go from Playstore
npm install

```

---

## Environment Variables

See `backend/.env.example` for all required variables.
Never commit `.env` files — they are gitignored.

---

## Naming

**Luminara** (Latin: *lumen* = light) — illuminating threats before they reach you.
Tagline: *"See the threat before it sees you."*
