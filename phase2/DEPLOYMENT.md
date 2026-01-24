# 🚀 Deployment Guide - Todo App Phase 2

Complete guide to deploy both backend (FastAPI) and frontend (Next.js) to Vercel.

---

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ GitHub account with your repository pushed
- ✅ Vercel account (sign up at https://vercel.com)
- ✅ Neon PostgreSQL database set up (https://neon.tech)
- ✅ Database connection string ready

---

## 🗄️ Part 1: Set Up Neon Database

### 1.1 Create Neon Database (if not done)

1. Go to https://neon.tech and sign in
2. Click "Create Project"
3. Choose a name (e.g., "todo-app-db")
4. Select a region close to your users
5. Click "Create Project"

### 1.2 Get Connection String

1. In your Neon dashboard, go to your project
2. Click "Connection Details"
3. Copy the connection string (format: `postgresql://user:password@host/database`)
4. **Important**: Make sure it includes `?sslmode=require` at the end
5. Save this - you'll need it for Vercel environment variables

Example format:
```
postgresql://username:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

---

## 🔧 Part 2: Deploy Backend (FastAPI)

### 2.1 Create New Vercel Project for Backend

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. **Important**: Configure the project:
   - **Project Name**: `todo-app-backend` (or your choice)
   - **Framework Preset**: Other
   - **Root Directory**: `phase2/backend` ← **CRITICAL**
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

### 2.2 Configure Environment Variables

In the Vercel project settings, add these environment variables:

| Variable | Value | Example |
|----------|-------|---------|
| `DATABASE_URL` | Your Neon connection string | `postgresql://user:pass@host/db?sslmode=require` |
| `CORS_ORIGINS` | Your frontend URL (add after frontend deployment) | `https://your-frontend.vercel.app` |
| `ENVIRONMENT` | `production` | `production` |

**Steps**:
1. In your Vercel backend project, go to "Settings" → "Environment Variables"
2. Add each variable above
3. Select "Production", "Preview", and "Development" for each
4. Click "Save"

### 2.3 Deploy Backend

1. Click "Deploy" button
2. Wait for deployment to complete (2-3 minutes)
3. Once deployed, copy your backend URL (e.g., `https://todo-app-backend.vercel.app`)
4. Test the backend:
   - Visit: `https://your-backend.vercel.app/`
   - Should see: `{"message": "Todo API - Phase II", ...}`
   - Visit: `https://your-backend.vercel.app/docs`
   - Should see: Interactive API documentation

### 2.4 Update CORS Origins

1. Go back to backend project "Settings" → "Environment Variables"
2. Edit `CORS_ORIGINS` variable
3. Add your frontend URL (you'll get this after deploying frontend)
4. Format: `https://your-frontend.vercel.app` (no trailing slash)
5. Click "Save"
6. Redeploy: Go to "Deployments" → Click "..." on latest → "Redeploy"

---

## 🎨 Part 3: Deploy Frontend (Next.js)

### 3.1 Create New Vercel Project for Frontend

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import the **same** GitHub repository
4. **Important**: Configure the project:
   - **Project Name**: `todo-app-frontend` (or your choice)
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `phase2/frontend` ← **CRITICAL**
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)
   - **Install Command**: `npm install` (auto-filled)

### 3.2 Configure Environment Variables

In the Vercel project settings, add this environment variable:

| Variable | Value | Example |
|----------|-------|---------|
| `NEXT_PUBLIC_API_URL` | Your backend URL + `/api/v1` | `https://todo-app-backend.vercel.app/api/v1` |

**Steps**:
1. In your Vercel frontend project, go to "Settings" → "Environment Variables"
2. Add `NEXT_PUBLIC_API_URL` with your backend URL
3. **Important**: Add `/api/v1` at the end
4. Select "Production", "Preview", and "Development"
5. Click "Save"

### 3.3 Deploy Frontend

1. Click "Deploy" button
2. Wait for deployment to complete (2-3 minutes)
3. Once deployed, copy your frontend URL (e.g., `https://todo-app-frontend.vercel.app`)
4. Visit your frontend URL - your app should be live!

### 3.4 Update Backend CORS (Final Step)

Now that you have your frontend URL:

1. Go to your **backend** Vercel project
2. Settings → Environment Variables
3. Edit `CORS_ORIGINS`
4. Update to: `https://your-actual-frontend.vercel.app`
5. Save and redeploy backend

---

## ✅ Part 4: Verify Deployment

### 4.1 Test Backend

Visit these URLs (replace with your actual backend URL):

1. **Root**: `https://your-backend.vercel.app/`
   - Should return JSON with API info

2. **Health Check**: `https://your-backend.vercel.app/api/v1/health`
   - Should return: `{"status": "healthy", "database": "connected", ...}`

3. **API Docs**: `https://your-backend.vercel.app/docs`
   - Should show interactive Swagger UI

4. **Get Tasks**: `https://your-backend.vercel.app/api/v1/tasks`
   - Should return: `{"data": [], "message": "Tasks retrieved successfully", ...}`

### 4.2 Test Frontend

1. Visit your frontend URL: `https://your-frontend.vercel.app`
2. You should see the todo app interface
3. Try creating a task:
   - Click "New Task"
   - Fill in title, description, priority
   - Click "Create Task"
   - Task should appear in the list
4. Test filters, search, and sorting
5. Try marking tasks complete/incomplete
6. Try editing and deleting tasks

### 4.3 Test Full Integration

1. Create a task in the frontend
2. Refresh the page - task should persist (stored in database)
3. Open browser DevTools (F12) → Network tab
4. Create another task
5. Check network requests - should see successful API calls to your backend

---

## 🔄 Part 5: Redeployment & Updates

### When You Make Code Changes

**Backend Changes**:
1. Push changes to GitHub
2. Vercel auto-deploys from `main` branch
3. Or manually: Vercel Dashboard → Backend Project → Deployments → Redeploy

**Frontend Changes**:
1. Push changes to GitHub
2. Vercel auto-deploys from `main` branch
3. Or manually: Vercel Dashboard → Frontend Project → Deployments → Redeploy

### Update Environment Variables

1. Go to project Settings → Environment Variables
2. Edit the variable
3. Save
4. **Important**: Redeploy for changes to take effect

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: "Internal Server Error" or 500 errors

**Solutions**:
1. Check Vercel logs: Project → Deployments → Click deployment → "View Function Logs"
2. Verify `DATABASE_URL` is correct and includes `?sslmode=require`
3. Check Neon database is active (not paused)
4. Verify all dependencies in `requirements.txt`

**Problem**: CORS errors in browser console

**Solutions**:
1. Check `CORS_ORIGINS` includes your frontend URL
2. No trailing slash in URL
3. Must be exact match (https, not http)
4. Redeploy backend after changing CORS

**Problem**: Database connection errors

**Solutions**:
1. Verify Neon database is running
2. Check connection string format
3. Ensure `?sslmode=require` is at the end
4. Test connection string locally first

### Frontend Issues

**Problem**: "Failed to load tasks" error

**Solutions**:
1. Check `NEXT_PUBLIC_API_URL` is set correctly
2. Must include `/api/v1` at the end
3. Backend must be deployed and running
4. Check browser console for CORS errors
5. Redeploy frontend after changing env vars

**Problem**: Environment variable not working

**Solutions**:
1. Verify variable name starts with `NEXT_PUBLIC_`
2. Redeploy after adding/changing variables
3. Clear browser cache (Ctrl+Shift+R)

**Problem**: Build fails

**Solutions**:
1. Check build logs in Vercel
2. Verify `package.json` dependencies
3. Ensure Node.js version compatibility (18+)
4. Check for TypeScript errors

---

## 📊 Monitoring & Logs

### View Logs

**Backend**:
1. Vercel Dashboard → Backend Project
2. Deployments → Click latest deployment
3. "View Function Logs" - see real-time API logs

**Frontend**:
1. Vercel Dashboard → Frontend Project
2. Deployments → Click latest deployment
3. "View Build Logs" - see build output

### Performance Monitoring

Vercel provides:
- Request analytics
- Performance metrics
- Error tracking
- Usage statistics

Access via: Project → Analytics

---

## 🔒 Security Best Practices

1. **Never commit `.env` files** - already in `.gitignore`
2. **Use environment variables** for all secrets
3. **Enable HTTPS only** - Vercel does this automatically
4. **Restrict CORS** - only allow your frontend domain
5. **Keep dependencies updated** - check for security updates
6. **Monitor logs** - watch for suspicious activity

---

## 💰 Vercel Pricing

**Free Tier Includes**:
- Unlimited deployments
- 100GB bandwidth/month
- Automatic HTTPS
- Preview deployments
- Analytics

**Limits**:
- Serverless function execution: 100GB-hours/month
- Build execution: 100 hours/month

For most hackathon projects, free tier is sufficient!

---

## 📝 Quick Reference

### Backend URLs
- Root: `https://your-backend.vercel.app/`
- API Docs: `https://your-backend.vercel.app/docs`
- Health: `https://your-backend.vercel.app/api/v1/health`
- Tasks: `https://your-backend.vercel.app/api/v1/tasks`

### Frontend URL
- App: `https://your-frontend.vercel.app`

### Environment Variables

**Backend**:
```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
CORS_ORIGINS=https://your-frontend.vercel.app
ENVIRONMENT=production
```

**Frontend**:
```
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app/api/v1
```

---

## 🎉 Success Checklist

- [ ] Backend deployed to Vercel
- [ ] Backend health check returns "healthy"
- [ ] Backend API docs accessible
- [ ] Frontend deployed to Vercel
- [ ] Frontend loads without errors
- [ ] Can create tasks
- [ ] Tasks persist after refresh
- [ ] All CRUD operations work
- [ ] Filters and search work
- [ ] No CORS errors in console

---

## 📞 Support

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review Vercel logs for error messages
3. Verify all environment variables are set correctly
4. Test backend endpoints directly (using `/docs`)
5. Check browser console for frontend errors

---

**Deployment Complete! 🚀**

Your full-stack todo app is now live on Vercel!
