# Feature 006: Urdu Translation - Developer Quickstart Guide

**Quick Setup Time**: ~10 minutes
**Target Audience**: Developers setting up the Urdu translation feature locally

---

## Prerequisites

✅ **Required**:
- Python 3.10+ (`python3 --version`)
- Node.js 18+ (`node --version`)
- npm 9+ (`npm --version`)
- Git (`git --version`)

✅ **Accounts Needed**:
- [OpenRouter Account](https://openrouter.ai/) (free tier)
- [Neon Postgres Account](https://neon.tech/) (free tier)

---

## 🚀 Quick Start (5 Steps)

### 1. Clone & Install Dependencies

```bash
# Clone repository
git clone https://github.com/YOUR_ORG/AI-native-textbook.git
cd AI-native-textbook

# Backend setup
cd backend
pip install -r requirements.txt
# or with --break-system-packages if needed:
# pip install --break-system-packages -r requirements.txt

# Frontend setup
cd ../frontend
npm install

cd ..
```

### 2. Get API Keys

#### OpenRouter API Key
1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up (no credit card required for free tier)
3. Go to [API Keys page](https://openrouter.ai/keys)
4. Click **"Create API Key"**
5. Copy the key (starts with `sk-or-v1-...`)

#### Neon Postgres URL
1. Visit [Neon Console](https://console.neon.tech/)
2. Create new project: **"AI Textbook DB"**
3. Go to **Dashboard → Connection Details**
4. Copy the **Connection String** (starts with `postgresql://...`)

### 3. Configure Environment Variables

Create `backend/.env` file:

```bash
cd backend
cat > .env << EOF
# OpenRouter API (for translation)
OPENROUTER_API_KEY=sk-or-v1-YOUR_KEY_HERE

# Neon Postgres (for caching)
NEON_POSTGRES_URL=postgresql://user:pass@host.neon.tech/dbname?sslmode=require

# JWT Secret (generate random string)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# Optional: Enable debug logging
LOG_LEVEL=INFO
EOF
```

**Security Note**: Never commit `.env` file to Git! It's already in `.gitignore`.

### 4. Run Database Migrations

```bash
# Still in backend/ directory
alembic upgrade head

# Expected output:
# INFO  [alembic.runtime.migration] Running upgrade  -> 57c6b0ea13f8, add translations table
# INFO  [alembic.runtime.migration] Running upgrade 57c6b0ea13f8 -> 809b34b1c5dc, add translation_feedback table
```

**Verify Migration**:
```bash
alembic current
# Should show: 809b34b1c5dc (head)
```

### 5. Start Servers

**Terminal 1 - Backend**:
```bash
cd backend
python3 main.py

# Expected output:
# INFO:     Started server process [12345]
# INFO:     Uvicorn running on http://0.0.0.0:8001
# INFO:     Database initialized successfully
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm start

# Expected output:
# [INFO] Starting the development server...
# [SUCCESS] Docusaurus website is running at http://localhost:3000/
```

---

## ✅ Verify Installation

### 1. Check Backend Health

```bash
curl http://localhost:8001/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### 2. Test Translation API (requires signup first)

**Step 1**: Create test user
```bash
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234!",
    "software_background": "Python, JavaScript",
    "hardware_background": "Arduino, Raspberry Pi"
  }'

# Save the token from response
```

**Step 2**: Test translation
```bash
TOKEN="YOUR_JWT_TOKEN_HERE"

curl -X POST http://localhost:8001/api/translate/urdu \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "chapter_id": "test",
    "content": "ROS2 is a robotics middleware framework.",
    "content_hash": "8f3a9d2b7c4e5f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5"
  }'

# Expected response (takes 8-10 seconds first time):
{
  "translated_content": "ROS2 ایک روبوٹکس middleware فریم ورک ہے۔",
  "cached": false,
  "translation_id": "a1b2c3d4-..."
}
```

### 3. Test Frontend

1. Open browser: http://localhost:3000/
2. Click **"Sign Up"** (top-right)
3. Create account with software/hardware background
4. Navigate to any chapter (e.g., "ROS2 Fundamentals")
5. Click **"🇵🇰 Translate to Urdu"** button
6. Verify:
   - Loading spinner appears
   - Translation completes in 8-10 seconds
   - Urdu content displays with RTL alignment
   - "🇬🇧 View in English" button appears

---

## 📁 Project Structure

```
AI-native-textbook/
├── backend/
│   ├── api/
│   │   ├── translation.py         # Translation endpoint
│   │   ├── feedback.py            # Feedback endpoint
│   │   └── auth.py                # Authentication
│   ├── services/
│   │   ├── translation_service.py # OpenRouter integration
│   │   └── rate_limiter.py        # Rate limiting logic
│   ├── models/
│   │   └── translation_feedback.py
│   ├── database/
│   │   ├── db.py                  # Database connection
│   │   ├── models.py              # Translation model
│   │   └── migrations/            # Alembic migrations
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── .env                       # ⚠️ NOT COMMITTED TO GIT
│   ├── requirements.txt
│   └── main.py                    # FastAPI app entry point
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── translation/
│   │   │       ├── UrduTranslationButton.jsx
│   │   │       ├── FeedbackButton.jsx
│   │   │       └── *.module.css
│   │   ├── hooks/
│   │   │   └── useTranslation.js
│   │   ├── services/
│   │   │   └── translationApi.js
│   │   └── theme/
│   │       └── DocItem/Layout/index.js  # Docusaurus theme override
│   ├── docs/                      # Markdown chapters (add chapter_id to frontmatter)
│   ├── package.json
│   └── docusaurus.config.js
└── specs/
    └── 006-urdu-translation/
        ├── spec.md                # Feature requirements
        ├── plan.md                # Architecture
        ├── tasks.md               # Task breakdown
        ├── research.md            # OpenRouter integration findings
        ├── data-model.md          # Database schema
        └── quickstart.md          # This file!
```

---

## 🐛 Troubleshooting

### Issue 1: "Database connection failed"

**Symptoms**: Backend starts but shows `database: disconnected` in health check

**Solutions**:
```bash
# 1. Verify NEON_POSTGRES_URL format
echo $NEON_POSTGRES_URL
# Should start with postgresql:// and end with ?sslmode=require

# 2. Test connection directly
python3 -c "import os; from sqlalchemy import create_engine; engine = create_engine(os.getenv('NEON_POSTGRES_URL')); conn = engine.connect(); print('✅ Connection successful')"

# 3. Check Neon project status at https://console.neon.tech/
```

### Issue 2: "OpenRouter API key invalid"

**Symptoms**: Translation returns 401 or 403 error

**Solutions**:
```bash
# 1. Verify API key format (should start with sk-or-v1-)
echo $OPENROUTER_API_KEY

# 2. Test API key directly
curl https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Expected response: {"data": {"label": "..."}}

# 3. Generate new key at https://openrouter.ai/keys if invalid
```

### Issue 3: "Alembic migration fails"

**Symptoms**: `alembic upgrade head` shows errors

**Solutions**:
```bash
# 1. Check current migration status
alembic current

# 2. If no migrations applied, start fresh
alembic stamp head

# 3. If migration conflict, downgrade and retry
alembic downgrade -1
alembic upgrade head

# 4. Nuclear option (⚠️ DELETES ALL DATA):
# Drop all tables in Neon console, then:
alembic upgrade head
```

### Issue 4: "Frontend can't reach backend"

**Symptoms**: CORS errors or "Network request failed"

**Solutions**:
```bash
# 1. Verify backend is running
curl http://localhost:8001/health

# 2. Check CORS configuration in backend/main.py
# Should include http://localhost:3000 in allow_origins

# 3. Verify frontend API URL in translationApi.js
# Should use http://localhost:8001 for local dev
```

### Issue 5: "Translations show '???' characters"

**Symptoms**: Urdu text displays as boxes or question marks

**Solutions**:
1. **Install Urdu fonts** on your system:
   - Windows: Download "Jameel Noori Nastaleeq" font
   - macOS: "Noto Nastaliq Urdu" (pre-installed)
   - Linux: `sudo apt install fonts-nafees`

2. **Check browser**: Chrome/Firefox/Edge support Urdu natively (Safari has better font rendering)

3. **Verify CSS** in `UrduTranslationButton.module.css`:
   ```css
   .urdu-content {
     direction: rtl;
     font-family: 'Jameel Noori Nastaleeq', 'Noto Nastaliq Urdu', ...;
   }
   ```

---

## 🧪 Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_translation_service.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Expected output:
# ===== 33 passed in 4.21s =====
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage

# Expected output:
# Test Suites: 1 passed, 1 total
# Tests:       11 passed, 11 total
```

---

## 📚 Key Endpoints

### Backend API

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/auth/signup` | POST | ❌ | Create user account |
| `/api/auth/login` | POST | ❌ | Get JWT token |
| `/api/translate/urdu` | POST | ✅ JWT | Translate chapter to Urdu |
| `/api/translate/feedback` | POST | ✅ JWT | Report translation issue |
| `/health` | GET | ❌ | Server health check |

**Full API Docs**: http://localhost:8001/docs (Swagger UI)

### Frontend Routes

| Route | Description |
|-------|-------------|
| `/` | Homepage |
| `/docs/intro` | Introduction chapter (has translation button) |
| `/docs/ros2-fundamentals` | ROS2 chapter (translatable) |
| `/signup` | User registration |
| `/login` | User login |

---

## 🔒 Security Best Practices

1. **Never commit `.env` file**:
   ```bash
   # Already in .gitignore, but double-check:
   git status
   # Should NOT show .env
   ```

2. **Use strong JWT secrets**:
   ```bash
   # Generate new secret:
   openssl rand -hex 32
   ```

3. **Enable HTTPS in production**:
   - Backend: Use reverse proxy (Nginx, Caddy)
   - Frontend: Deploy to Vercel/Netlify (auto-HTTPS)

4. **Rate limit API keys**:
   - OpenRouter free tier: ~100 requests/day
   - Application enforces: 10 translations/user/hour

---

## 🚀 Deployment Checklist

**Backend** (Hugging Face Spaces recommended):
- [ ] Set environment variables in Spaces settings
- [ ] Run `alembic upgrade head` in Dockerfile
- [ ] Verify health check endpoint responds
- [ ] Test translation endpoint with Postman

**Frontend** (Vercel/Netlify recommended):
- [ ] Set `REACT_APP_API_URL` to production backend URL
- [ ] Build: `npm run build`
- [ ] Test production build locally: `npx serve build`
- [ ] Deploy and verify HTTPS works

---

## 📖 Additional Resources

- [Feature Spec](./spec.md) - Requirements and user stories
- [Implementation Plan](./plan.md) - Architecture decisions
- [Research Findings](./research.md) - OpenRouter integration details
- [Data Model](./data-model.md) - Database schema documentation
- [OpenRouter Docs](https://openrouter.ai/docs) - API reference
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) - Migration tool

---

## 🆘 Getting Help

1. **Check logs**:
   ```bash
   # Backend
   tail -f backend/app.log

   # Frontend (browser console)
   # Open DevTools (F12) → Console tab
   ```

2. **Enable debug mode**:
   ```bash
   # In backend/.env
   LOG_LEVEL=DEBUG
   ```

3. **Common error codes**:
   - `400`: Invalid request (check content_hash calculation)
   - `401`: Authentication failed (JWT token expired or invalid)
   - `429`: Rate limit exceeded (wait 1 hour or reset rate limiter)
   - `503`: OpenRouter API down (check https://status.openrouter.ai/)

4. **Contact team**:
   - GitHub Issues: [Project Issues](https://github.com/YOUR_ORG/AI-native-textbook/issues)
   - Documentation: [README.md](../../README.md)

---

**Setup Complete!** 🎉

You're now ready to develop with the Urdu Translation feature. Try translating a chapter and report any issues via the feedback button!

**کامیابی!** Translation feature is ready! ✅
