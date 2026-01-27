# Deployment Guide

This guide covers deploying the Todo App to production using Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account with repository pushed
- [Railway](https://railway.app) account
- [Vercel](https://vercel.com) account
- [Neon](https://neon.tech) database (already configured)

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Vercel    │────▶│   Railway   │────▶│    Neon     │
│  (Frontend) │     │  (Backend)  │     │ (PostgreSQL)│
│  Next.js    │     │   FastAPI   │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
     HTTPS              HTTPS              SSL
```

## Step 1: Database Setup (Neon)

If not already configured:

1. Go to [neon.tech](https://neon.tech) and create an account
2. Create a new project
3. Copy the connection string:
   ```
   postgresql://neondb_owner:***@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

## Step 2: Deploy Backend to Railway

### 2.1 Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select your repository

### 2.2 Configure Service

1. Set the **Root Directory** to `phase-2/backend`
2. Railway will auto-detect Python/FastAPI

### 2.3 Set Environment Variables

Add these environment variables in Railway dashboard:

```bash
DATABASE_URL=postgresql://neondb_owner:***@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
JWT_SECRET=your-production-secret-at-least-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=https://your-app.vercel.app
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 2.4 Deploy

1. Click "Deploy"
2. Wait for build to complete
3. Note your backend URL: `https://your-app.railway.app`

### 2.5 Verify Backend

```bash
curl https://your-app.railway.app/
# Should return: {"status":"healthy","database":"connected"}
```

## Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Project

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import your GitHub repository

### 3.2 Configure Build Settings

- **Framework Preset**: Next.js
- **Root Directory**: `phase-2/frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

### 3.3 Set Environment Variables

Add these environment variables in Vercel dashboard:

```bash
DATABASE_URL=postgresql://neondb_owner:***@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=your-production-secret-at-least-32-characters
BETTER_AUTH_URL=https://your-app.vercel.app
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
```

**IMPORTANT**: `BETTER_AUTH_SECRET` must match `JWT_SECRET` from backend!

### 3.4 Deploy

1. Click "Deploy"
2. Wait for build to complete
3. Note your frontend URL: `https://your-app.vercel.app`

## Step 4: Update CORS Configuration

After deploying frontend, update backend CORS:

1. Go to Railway dashboard
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```
3. Redeploy backend

## Step 5: Verify Production

### Test Health Check
```bash
curl https://your-backend.railway.app/
```

### Test Full Flow
1. Visit `https://your-app.vercel.app`
2. Register a new account
3. Login
4. Create a task
5. Edit the task
6. Mark as complete
7. Delete the task
8. Logout

## Environment Variables Reference

### Backend (Railway)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Neon PostgreSQL connection string |
| `JWT_SECRET` | Yes | Secret for JWT signing (32+ chars) |
| `JWT_ALGORITHM` | Yes | `HS256` |
| `JWT_EXPIRATION_DAYS` | Yes | Token expiration (e.g., `7`) |
| `CORS_ORIGINS` | Yes | Frontend URL(s), comma-separated |
| `ENVIRONMENT` | No | `production` |
| `LOG_LEVEL` | No | `INFO` |

### Frontend (Vercel)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Neon PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | Must match backend `JWT_SECRET` |
| `BETTER_AUTH_URL` | Yes | Frontend URL |
| `NEXT_PUBLIC_API_URL` | Yes | Backend URL |
| `NEXT_PUBLIC_APP_URL` | Yes | Frontend URL |

## Troubleshooting

### CORS Errors

**Symptom**: Browser console shows CORS policy errors

**Solution**:
1. Verify `CORS_ORIGINS` in backend includes exact frontend URL
2. Include protocol (`https://`)
3. No trailing slash
4. Redeploy backend after changes

### JWT Validation Failed

**Symptom**: 401 Unauthorized on API requests

**Solution**:
1. Verify `JWT_SECRET` (backend) matches `BETTER_AUTH_SECRET` (frontend)
2. Check token expiration settings
3. Clear browser cookies and re-login

### Database Connection Failed

**Symptom**: 503 Service Unavailable or database errors

**Solution**:
1. Verify `DATABASE_URL` is correct
2. Check Neon project is active (not suspended)
3. Ensure `?sslmode=require` is in connection string

### Build Failures

**Backend (Railway)**:
- Check `requirements.txt` is complete
- Verify Python version compatibility

**Frontend (Vercel)**:
- Check `package.json` dependencies
- Verify environment variables are set before build
- Check for TypeScript errors

### Slow Cold Starts

Railway and Vercel free tiers may have cold starts:
- First request after inactivity may be slow (5-30 seconds)
- Subsequent requests are fast
- Consider upgrading for always-on instances

## Monitoring

### Railway
- View logs in Railway dashboard
- Monitor resource usage
- Set up alerts for failures

### Vercel
- View function logs in Vercel dashboard
- Monitor build times
- Check analytics for performance

### Neon
- Monitor connection count
- Check query performance
- Review storage usage

## Security Checklist

- [ ] All secrets are in environment variables (not in code)
- [ ] HTTPS is enabled on all endpoints
- [ ] CORS is restricted to known origins
- [ ] JWT secrets are strong (32+ characters)
- [ ] Database uses SSL (`sslmode=require`)
- [ ] No `.env` files committed to repository

## Rollback

### Railway
1. Go to Deployments tab
2. Click on previous successful deployment
3. Click "Redeploy"

### Vercel
1. Go to Deployments tab
2. Find previous successful deployment
3. Click "..." → "Promote to Production"

## Cost Considerations

### Free Tier Limits

**Railway**:
- $5 free credit per month
- Sufficient for hackathon demo

**Vercel**:
- 100GB bandwidth/month
- Unlimited deployments
- Sufficient for hackathon demo

**Neon**:
- 0.5 GB storage
- 10 branches
- Sufficient for hackathon demo

### Scaling Up

For production use beyond hackathon:
- Railway: Upgrade to Pro ($20/month)
- Vercel: Upgrade to Pro ($20/month)
- Neon: Upgrade to Launch ($19/month)
