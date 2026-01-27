# Quickstart: Integration, Testing & Deployment

**Feature**: 004-integration-deployment
**Date**: 2026-01-26

---

## Overview

This quickstart guide helps you run the full Todo application locally and deploy it to production.

## Prerequisites

- **Docker Desktop** (for local development with Docker Compose)
- **Node.js 18+** (for frontend development)
- **Python 3.11+** (for backend development)
- **Git** (for version control)
- **GitHub account** (for repository hosting)
- **Neon account** (database already configured)
- **Vercel account** (for frontend deployment)
- **Railway account** (for backend deployment)

---

## Local Development

### Option 1: Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-username/Hackathon-2-todo-app.git
cd Hackathon-2-todo-app

# 2. Copy environment file
cp .env.example .env
# Edit .env with your Neon database URL and secrets

# 3. Start all services
docker-compose up

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Health check: http://localhost:8000/
```

### Option 2: Manual Setup

**Backend**:
```bash
# Navigate to backend
cd phase-2/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Start the server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
# Navigate to frontend (new terminal)
cd phase-2/frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local
# Edit .env.local with your configuration

# Start the development server
npm run dev
```

---

## Environment Variables

### Backend (.env)

```bash
# Database (Neon)
DATABASE_URL=postgresql://neondb_owner:***@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# JWT Authentication
JWT_SECRET=your-super-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS (comma-separated)
CORS_ORIGINS=http://localhost:3000

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Frontend (.env.local)

```bash
# Better Auth (must match backend JWT_SECRET)
BETTER_AUTH_SECRET=your-super-secret-key-at-least-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Database (same as backend)
DATABASE_URL=postgresql://neondb_owner:***@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

---

## Production Deployment

### Backend (Railway)

1. **Create Railway account** at https://railway.app
2. **Connect GitHub repository**
3. **Set root directory** to `phase-2/backend`
4. **Configure environment variables**:
   - `DATABASE_URL`
   - `JWT_SECRET`
   - `JWT_ALGORITHM=HS256`
   - `JWT_EXPIRATION_DAYS=7`
   - `CORS_ORIGINS=https://your-frontend.vercel.app`
   - `ENVIRONMENT=production`
5. **Deploy**

Railway will automatically detect the Python project and use uvicorn.

### Frontend (Vercel)

1. **Create Vercel account** at https://vercel.com
2. **Import GitHub repository**
3. **Set root directory** to `phase-2/frontend`
4. **Configure build settings**:
   - Framework Preset: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. **Configure environment variables**:
   - `BETTER_AUTH_SECRET`
   - `BETTER_AUTH_URL=https://your-app.vercel.app`
   - `DATABASE_URL`
   - `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`
   - `NEXT_PUBLIC_APP_URL=https://your-app.vercel.app`
6. **Deploy**

---

## Verification Checklist

### Local Development
- [ ] `docker-compose up` starts all services
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend accessible at http://localhost:8000
- [ ] Health check returns `{"status": "healthy", "database": "connected"}`
- [ ] Can register a new user
- [ ] Can login with registered user
- [ ] Can create, edit, complete, and delete tasks
- [ ] Can logout and session is cleared

### Production Deployment
- [ ] Backend deployed and accessible via HTTPS
- [ ] Frontend deployed and accessible via HTTPS
- [ ] CORS allows frontend to call backend
- [ ] End-to-end flow works (register → login → CRUD → logout)
- [ ] No console errors in browser
- [ ] No secrets exposed in repository

---

## Troubleshooting

### CORS Errors

```
Access to fetch at 'https://api.example.com' from origin 'https://app.example.com' has been blocked by CORS policy
```

**Solution**: Ensure `CORS_ORIGINS` in backend includes the frontend URL.

### JWT Validation Failed

```
Invalid JWT token
```

**Solution**: Ensure `JWT_SECRET` in backend matches `BETTER_AUTH_SECRET` in frontend.

### Database Connection Failed

```
Cannot connect to database
```

**Solutions**:
1. Check `DATABASE_URL` is correct
2. Ensure `?sslmode=require` is in the URL for Neon
3. Check Neon project is active (not suspended)

### Docker Build Fails

```
npm ERR! code ENOENT
```

**Solution**: Ensure you're in the correct directory and `package.json` exists.

---

## Quick Reference

| Service | Local URL | Production URL |
|---------|-----------|----------------|
| Frontend | http://localhost:3000 | https://your-app.vercel.app |
| Backend | http://localhost:8000 | https://your-api.railway.app |
| Database | N/A (Neon) | N/A (Neon) |

| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Health check |
| /api/tasks | GET | List user's tasks |
| /api/tasks | POST | Create task |
| /api/tasks/{id} | GET | Get task |
| /api/tasks/{id} | PUT | Update task |
| /api/tasks/{id} | DELETE | Delete task |
| /api/tasks/{id}/toggle | PATCH | Toggle completion |
