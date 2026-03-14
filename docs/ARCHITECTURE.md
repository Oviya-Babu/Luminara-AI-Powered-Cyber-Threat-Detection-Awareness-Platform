# Luminara — System Architecture (Phase 1)

## Overview

Luminara is a mobile-first AI cybersecurity platform built with a clean,
layered architecture. Each layer has a single responsibility and communicates
only with adjacent layers.

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│          Flutter Mobile App (iOS + Android)              │
│  Features: Auth · Dashboard · Scan · Learn · Streak      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTPS / REST
┌────────────────────────▼────────────────────────────────┐
│              FastAPI Backend (Python 3.11)                │
│  Middleware: JWT Auth · Rate Limiting · CORS · Logging    │
│  Services:   AI Agent · Phishing · Deepfake · QR · Learn │
└──────────┬────────────────────────────┬─────────────────┘
           │                            │
┌──────────▼──────────┐   ┌────────────▼───────────────┐
│   AI/ML Pipeline    │   │   External Security APIs    │
│  BERT (phishing)    │   │   VirusTotal               │
│  AASIST (audio df)  │   │   Google Safe Browsing     │
│  GenConViT (video)  │   │   Firebase FCM             │
└──────────┬──────────┘   └────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────┐
│           PostgreSQL via Supabase                        │
│  Tables: users · scan_results · lessons · streaks        │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow — Phishing Analysis Request

```
User pastes message (Flutter)
    → POST /api/v1/agent/analyze
    → AI Security Agent classifies input type
    → Routes to PhishingService
    → BERT model inference
    → RoBERTa URL layer (if URL present)
    → Result aggregated + risk score computed
    → ScanResult saved to PostgreSQL
    → Response returned to Flutter
    → UI shows risk level + explanation
```

---

## Security Architecture

| Concern             | Implementation                                    |
|---------------------|---------------------------------------------------|
| Authentication      | JWT (HS256), short-lived access + refresh tokens  |
| Password storage    | bcrypt (cost factor 12)                           |
| Transport security  | HTTPS enforced; HTTP redirect in production       |
| Input validation    | Pydantic schemas on every endpoint                |
| File uploads        | MIME type check + size limit (50MB)               |
| Rate limiting       | 30 req/min general, 10 req/min for AI endpoints   |
| SQL injection       | SQLAlchemy ORM — no raw queries                   |
| CORS                | Strict allowlist — no wildcard origins            |
| Secrets             | Environment variables — never hardcoded           |
| API keys            | Server-side only — never sent to mobile client    |

---

## Database Schema Summary

| Table             | Purpose                                          |
|-------------------|--------------------------------------------------|
| users             | User accounts, language, knowledge level         |
| scan_results      | All detection results (phishing/deepfake/QR)     |
| lessons           | Multilingual cybersecurity lesson content        |
| lesson_progress   | Per-user lesson completion tracking              |
| quizzes           | Quiz questions with multilingual options         |
| quiz_attempts     | Per-user quiz answer history                     |
| user_streaks      | Daily streak, badges, awareness score            |

---

## Module Responsibilities

| Module             | Backend Service          | Phase |
|--------------------|--------------------------|-------|
| AI Security Agent  | services/ai_agent/       | 3     |
| Phishing Detection | services/phishing/       | 4     |
| Deepfake Detection | services/deepfake/       | 5     |
| QR Threat Scanner  | services/qr_scanner/     | 6     |
| Notification Mon.  | services/notification/   | 7     |
| Awareness Learning | services/awareness/      | 8     |
| Daily Streak       | (streak logic in awareness) | 9  |

---

## AI Model Details

### Phishing Detection (Phase 4)
- **Primary**: `ealvaradob/bert-finetuned-phishing` — 96% accuracy on emails/SMS
- **URL layer**: `pirocheto/phishing-url-detection` — URL-specific RoBERTa
- **Heuristics**: urgency keywords, impersonation patterns, link shorteners

### Audio Deepfake (Phase 5)
- **Model**: AASIST (`clovaai/aasist`) — 84% accuracy, 0.91 AUC
- **Preprocessing**: librosa MFCC + spectral features
- **Fallback**: RawNet2 if AASIST inference times out

### Video Deepfake (Phase 5)
- **Model**: GenConViT ensemble + CLIP frame features
- **Strategy**: Sample 16 frames → per-frame score → aggregate
- **Honesty**: 75% real-world accuracy disclosed to user via confidence band

### Input Classification (Phase 3)
- Rule-based MIME type detection (files)
- URL regex detection (text with links)
- NLP intent classifier for ambiguous text inputs
