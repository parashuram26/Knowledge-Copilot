# SD-01 · L0 Self-Serve KB Chatbot

> **AI Prototype Challenge** — Service Desk Use Case SD-01  
> RAG-powered support chatbot with citations and confidence-based escalation

---

## 🏗️ Architecture

```
User Query
    │
    ▼
Frontend (index.html)
    │  Sends question + KB context
    ▼
Anthropic Claude API (RAG layer)
    │  Retrieves from embedded KB articles
    │  Scores confidence (0.0–1.0)
    ▼
Response Engine
    ├── High Confidence (≥0.75) → Answer + Citations
    ├── Medium Confidence (0.55–0.74) → Answer + Warning
    └── Low Confidence (<0.55) → Escalate → Create Ticket
```

## ✅ Features

- **RAG Chatbot** — Claude searches 4 KB articles (16+ sections) to answer questions
- **Citations** — Every answer shows which article & section it came from
- **Confidence Scoring** — Visual bar showing answer reliability (0–100%)
- **Auto-Escalation** — Creates support ticket when confidence is low
- **Live Dashboard** — Real-time metrics: deflection rate, topic distribution, activity log
- **Ticket System** — Full form with priority levels, auto-fills issue context

## 📁 Project Structure

```
kb-chatbot/
├── index.html              ← Complete frontend + RAG logic
├── README.md               ← This file
├── requirements.txt        ← Python dependencies (for FastAPI backend)
├── src/
│   ├── app.py              ← FastAPI backend (optional)
│   ├── rag_engine.py       ← RAG search logic
│   └── ticket_service.py   ← Ticket management
├── data/
│   └── kb_articles/
│       ├── account_management.md
│       ├── billing_payments.md
│       ├── technical_support.md
│       └── getting_started.md
├── outputs/
│   └── sample_output.json  ← Sample RAG response
└── tests/
    └── test_basic.py       ← Unit tests
```

## 🚀 Quick Start

### Option 1: Just open the HTML file
```bash
open index.html
# or
python3 -m http.server 8080  # then visit http://localhost:8080
```

### Option 2: With FastAPI backend
```bash
pip install -r requirements.txt
uvicorn src.app:app --reload
# Visit http://localhost:8000
```

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Vanilla HTML/CSS/JS | Zero dependencies, fast load |
| AI Model | Claude Sonnet (Anthropic) | Best RAG accuracy, free tier |
| KB Format | Markdown files | Easy to edit, human-readable |
| Backend | FastAPI (optional) | Lightweight Python API |
| Testing | Pytest | Simple happy-path tests |

## 📊 Sample Output

```json
{
  "answer": "To reset your password, go to the login page and click 'Forgot Password'...",
  "confidence": 0.92,
  "citations": [
    {
      "article": "Account Management",
      "section": "How to Reset Your Password",
      "file": "account_management"
    }
  ],
  "topic": "account",
  "should_escalate": false
}
```

## 👥 Team

| Name | Role |
|------|------|
| [Your Name] | AI & Backend |
| [Team Member 2] | Frontend |
| [Team Member 3] | Testing & Docs |

## 📋 Submission Checklist

- [x] Working prototype (index.html — open and use immediately)
- [x] GitHub-ready folder structure
- [x] Sample data (4 KB articles, 16+ sections)
- [x] README with architecture diagram
- [x] Sample output (outputs/sample_output.json)
- [ ] Demo video (record a 2-min walkthrough)
- [ ] Team resumes (add to repo)
