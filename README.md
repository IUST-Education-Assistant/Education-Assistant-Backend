## Backend (local)

```bash
cd backend
uvicorn main:app --reload
```

## Backend + Postgres (Docker)

1) Create env file:

```bash
copy .env.example .env
```

2) Edit `.env` and set at least:
- `GROQ_API_KEY`
- `SECRET_KEY`
- (optional) SMTP settings for OTP emails

3) Start services:

```bash
docker compose up --build
```

If you prefer running from `backend/` instead, use:

```bash
cd backend
copy .env.example .env
docker compose up --build
```

API will be available at `http://localhost:8000` (Swagger: `/docs`).

## Frontend (local)

```bash
cd front
npm run dev
```