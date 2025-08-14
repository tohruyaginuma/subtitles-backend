# 🎤 Subtitles - Live Transcription App — Backend

This is the **backend** of the Live Transcription Application.  
It receives audio streams from the frontend via **WebSockets**, processes them with **AWS Transcribe**, and returns real-time text updates.

## 🔗 Links

- **App:** [https://subtitles-frontend-production.up.railway.app/](https://subtitles-frontend-production.up.railway.app/)
- **Frontend Code:** [https://github.com/tohruyaginuma/subtitles-frontend/](https://github.com/tohruyaginuma/subtitles-frontend/)
- **Backend Code:** This repository

## 💡 Motivation

The Subtitles app was created to help English learners, especially those learning it as a second language, check and understand spoken English quickly and easily.  
It’s designed for use in conferences, classrooms, and other real-time situations.

While there are many great transcription apps with advanced AI features, I wanted something much simpler — just live transcription and a history of past transcriptions, without unnecessary complexity.

## 🚀 Features

- Real-time audio transcription via AWS Transcribe
- WebSocket-based streaming (Django Channels + Daphne)
- JWT authentication support
- History set & history item management API

## 🛠 Tech Stack

- **Framework:** Django + Django REST Framework
- **Real-time:** Django Channels (ASGI)
- **Language:** Python 3
- **Database:** PostgreSQL

## 📦 Installation

```bash
git clone <backend-repo-url>
cd backend
pip install -r requirements.txt
```

## ▶️ Running Locally

```bash
python manage.py migrate
daphne -b 0.0.0.0 -p 8000 subtitles.asgi:application
```

## ⚙️ Environment Variables

Create a `.env` file with:

```
DATABASE_URL=***
SECRET_KEY=***
DEBUG=***
ALLOWED_HOSTS=***
AWS_ACCESS_KEY_ID=***
AWS_SECRET_ACCESS_KEY=***
AWS_REGION=***
DJANGO_SETTINGS_MODULE=***
CORS_ALLOWED_ORIGINS=***
CSRF_TRUSTED_ORIGINS=***
```

## 📄 API Contract

All API requests and responses follow this structure:

```json
{
  "data": { ... },
  "error": null
}
```

Errors will have the form:

```json
{
  "data": null,
  "error": {
    "code": "",
    "message": "",
    "details":  { ... },
  }
}
```

## 🔌 WebSocket Endpoint

```
ws://<backend-domain>/ws/transcribe/
```

- Accepts raw PCM audio chunks
- Returns live transcription messages
