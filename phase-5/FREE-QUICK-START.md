# Phase 5: FREE Cloud Deployment - Quick Start Guide

**Total Setup Time**: ~1 hour
**Total Cost**: $0/month 🎉
**No Credit Card Required!**

## 📋 Prerequisites

- GitHub account
- Phase 3 code completed
- Basic understanding of environment variables

## 🚀 Step-by-Step Setup

### Step 1: Create Free Accounts (10 minutes)

#### 1.1 Render.com (Frontend Hosting)
```
1. Go to https://render.com/register
2. Sign up with GitHub
3. No credit card required
4. Verify email
```

#### 1.2 Railway.app (Backend Hosting)
```
1. Go to https://railway.app/
2. Sign up with GitHub
3. No credit card required
4. Get $5 free credit per month
```

#### 1.3 Upstash (Kafka + Redis)
```
1. Go to https://upstash.com/
2. Sign up with GitHub or email
3. No credit card required
4. Free tier: 10k messages/day
```

#### 1.4 Sentry (Error Tracking)
```
1. Go to https://sentry.io/signup/
2. Sign up with GitHub or email
3. No credit card required
4. Free tier: 5k events/month
```

### Step 2: Setup Upstash Kafka (10 minutes)

#### 2.1 Create Kafka Cluster
```
1. Login to Upstash Console: https://console.upstash.com/
2. Click "Kafka" in sidebar
3. Click "Create Cluster"
4. Select region closest to you
5. Click "Create" (free tier)
```

#### 2.2 Create Topics
```
1. Click on your cluster
2. Click "Topics" tab
3. Create 4 topics:
   - Name: task.created, Partitions: 1, Retention: 7 days
   - Name: task.updated, Partitions: 1, Retention: 7 days
   - Name: task.deleted, Partitions: 1, Retention: 7 days
   - Name: task.completed, Partitions: 1, Retention: 7 days
```

#### 2.3 Get Credentials
```
1. Click "Details" tab
2. Copy these values:
   - REST API URL
   - REST API Username
   - REST API Password
3. Save them for later
```

### Step 3: Setup Upstash Redis (5 minutes)

#### 3.1 Create Redis Database
```
1. Click "Redis" in sidebar
2. Click "Create Database"
3. Name: todo-app-cache
4. Region: Same as Kafka
5. Click "Create" (free tier)
```

#### 3.2 Get Credentials
```
1. Click on your database
2. Click "Details" tab
3. Copy these values:
   - REST API URL
   - REST API Token
4. Save them for later
```

### Step 4: Setup Sentry (5 minutes)

#### 4.1 Create Project
```
1. Login to Sentry: https://sentry.io/
2. Click "Create Project"
3. Platform: Python
4. Project name: todo-app-backend
5. Click "Create Project"
```

#### 4.2 Get DSN
```
1. Go to Project Settings
2. Click "Client Keys (DSN)"
3. Copy the DSN URL
4. Save it for later
```

### Step 5: Update Backend Code (15 minutes)

#### 5.1 Install Dependencies
```bash
cd phase-3/backend

# Add to requirements.txt
echo "upstash-kafka>=0.1.0" >> requirements.txt
echo "upstash-redis>=0.1.0" >> requirements.txt
echo "sentry-sdk[fastapi]>=1.39.0" >> requirements.txt

pip install -r requirements.txt
```

#### 5.2 Create Kafka Producer

Create `src/kafka_producer.py`:

```python
import os
import json
from datetime import datetime
from upstash_kafka import KafkaProducer
from typing import Dict, Any

class EventProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            url=os.getenv("UPSTASH_KAFKA_REST_URL"),
            username=os.getenv("UPSTASH_KAFKA_REST_USERNAME"),
            password=os.getenv("UPSTASH_KAFKA_REST_PASSWORD")
        )

    def publish_event(self, topic: str, event_data: Dict[str, Any]):
        """Publish event to Kafka topic"""
        try:
            event = {
                "event_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "payload": event_data
            }

            self.producer.produce(
                topic=topic,
                value=json.dumps(event),
                key=str(event_data.get("task_id", ""))
            )

            print(f"Published event to {topic}: {event_data}")
        except Exception as e:
            print(f"Failed to publish event: {e}")
            # Don't fail the request if event publishing fails

# Global instance
event_producer = EventProducer()
```

#### 5.3 Update CRUD Operations

Update `src/crud.py` to publish events:

```python
from .kafka_producer import event_producer

def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Publish event
    event_producer.publish_event("task.created", {
        "task_id": db_task.id,
        "title": db_task.title,
        "status": db_task.status
    })

    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate) -> Task:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    # Publish event
    event_producer.publish_event("task.updated", {
        "task_id": db_task.id,
        "title": db_task.title,
        "status": db_task.status
    })

    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()

    # Publish event
    event_producer.publish_event("task.deleted", {
        "task_id": task_id
    })

    return True
```

#### 5.4 Add Sentry Integration

Update `src/main.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

# Initialize Sentry
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
    environment="production"
)

# Rest of your FastAPI app...
```

#### 5.5 Create Railway Configuration

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn src.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 6: Deploy Backend to Railway (10 minutes)

#### 6.1 Push Code to GitHub
```bash
git add .
git commit -m "Add Upstash Kafka and Railway configuration"
git push origin main
```

#### 6.2 Deploy on Railway
```
1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Click "Deploy Now"
```

#### 6.3 Add Environment Variables
```
1. Click on your service
2. Click "Variables" tab
3. Add these variables:
   - GEMINI_API_KEY=<your-gemini-key>
   - DATABASE_URL=<your-neon-url>
   - UPSTASH_KAFKA_REST_URL=<from-step-2>
   - UPSTASH_KAFKA_REST_USERNAME=<from-step-2>
   - UPSTASH_KAFKA_REST_PASSWORD=<from-step-2>
   - UPSTASH_REDIS_REST_URL=<from-step-3>
   - UPSTASH_REDIS_REST_TOKEN=<from-step-3>
   - SENTRY_DSN=<from-step-4>
4. Click "Deploy" to restart with new variables
```

#### 6.4 Get Backend URL
```
1. Click "Settings" tab
2. Copy the "Public Domain" URL
3. Example: https://todo-backend-production.up.railway.app
4. Save this URL for frontend configuration
```

### Step 7: Create Event Service (10 minutes)

#### 7.1 Create Event Service Code

Create `phase-5/event-service/main.py`:

```python
import os
import json
import time
from upstash_kafka import KafkaConsumer

def process_event(topic: str, message: dict):
    """Process event from Kafka"""
    print(f"Processing event from {topic}: {message}")

    # Add your event processing logic here
    # Examples:
    # - Send notifications
    # - Update analytics
    # - Trigger workflows
    # - Log to external systems

def main():
    consumer = KafkaConsumer(
        url=os.getenv("UPSTASH_KAFKA_REST_URL"),
        username=os.getenv("UPSTASH_KAFKA_REST_USERNAME"),
        password=os.getenv("UPSTASH_KAFKA_REST_PASSWORD"),
        group_id="event-service",
        topics=["task.created", "task.updated", "task.deleted", "task.completed"]
    )

    print("Event service started. Listening for events...")

    for message in consumer:
        try:
            event = json.loads(message.value)
            process_event(message.topic, event)
        except Exception as e:
            print(f"Error processing event: {e}")
            # Log to Sentry
            import sentry_sdk
            sentry_sdk.capture_exception(e)

if __name__ == "__main__":
    main()
```

Create `phase-5/event-service/requirements.txt`:

```
upstash-kafka>=0.1.0
sentry-sdk>=1.39.0
```

Create `phase-5/event-service/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

#### 7.2 Deploy Event Service to Railway
```
1. Push event-service code to GitHub
2. Go to Railway project
3. Click "New Service"
4. Select "Deploy from GitHub repo"
5. Choose event-service directory
6. Add same environment variables as backend
7. Deploy!
```

### Step 8: Deploy Frontend to Render (10 minutes)

#### 8.1 Update Frontend Configuration

Update `phase-3/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=https://todo-backend-production.up.railway.app
```

#### 8.2 Create Render Configuration

Create `phase-3/frontend/render.yaml`:

```yaml
services:
  - type: web
    name: todo-frontend
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./out
    envVars:
      - key: NEXT_PUBLIC_API_URL
        value: https://todo-backend-production.up.railway.app
```

#### 8.3 Configure Next.js for Static Export

Update `next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
```

#### 8.4 Push and Deploy
```bash
git add .
git commit -m "Add Render configuration"
git push origin main
```

```
1. Go to https://dashboard.render.com/
2. Click "New" → "Static Site"
3. Connect GitHub repository
4. Configure:
   - Name: todo-frontend
   - Branch: main
   - Build Command: npm install && npm run build
   - Publish Directory: out
5. Add environment variable:
   - NEXT_PUBLIC_API_URL=<railway-backend-url>
6. Click "Create Static Site"
```

### Step 9: Verify Deployment (5 minutes)

#### 9.1 Check Backend
```bash
# Get Railway backend URL from dashboard
curl https://todo-backend-production.up.railway.app/health

# Should return: {"status": "healthy"}
```

#### 9.2 Check Frontend
```
1. Get Render frontend URL from dashboard
2. Open in browser
3. Should see todo app interface
```

#### 9.3 Test Event Flow
```
1. Create a task in the UI
2. Check Railway backend logs (should see event published)
3. Check Railway event-service logs (should see event consumed)
4. Check Upstash Kafka console (should see message count increase)
```

#### 9.4 Check Monitoring
```
1. Go to Sentry dashboard
2. Should see events from backend
3. Check for any errors
```

## ✅ Success Checklist

- [ ] All accounts created (no credit card required)
- [ ] Upstash Kafka cluster created with 4 topics
- [ ] Upstash Redis database created
- [ ] Sentry project created
- [ ] Backend code updated with Kafka producer
- [ ] Backend deployed to Railway
- [ ] Event service deployed to Railway
- [ ] Frontend deployed to Render
- [ ] Frontend can access backend API
- [ ] Events flowing through Kafka
- [ ] Event service consuming events
- [ ] Errors tracked in Sentry
- [ ] Total cost: $0/month 🎉

## 🎯 URLs to Save

```
Frontend URL: https://<your-app>.onrender.com
Backend URL: https://<your-app>.up.railway.app
Upstash Console: https://console.upstash.com/
Sentry Dashboard: https://sentry.io/organizations/<your-org>/
Railway Dashboard: https://railway.app/project/<project-id>
Render Dashboard: https://dashboard.render.com/
```

## 🐛 Troubleshooting

### Backend not starting on Railway
- Check logs in Railway dashboard
- Verify all environment variables are set
- Check Dockerfile is correct

### Frontend not loading
- Check build logs in Render dashboard
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS settings in backend

### Events not flowing
- Check Upstash Kafka credentials
- Verify topics exist
- Check backend logs for publishing errors
- Check event service logs for consumption errors

### Sentry not receiving events
- Verify SENTRY_DSN is correct
- Check Sentry project settings
- Ensure sentry-sdk is installed

## 📚 Next Steps

1. Add more event consumers
2. Implement notifications
3. Add analytics dashboard
4. Set up custom domain
5. Configure alerts in Sentry
6. Optimize performance

## 💰 Cost Summary

| Service | Usage | Cost |
|---------|-------|------|
| Render.com | Frontend hosting | $0 |
| Railway.app | Backend + Event Service | $0 |
| Upstash Kafka | 10k messages/day | $0 |
| Upstash Redis | 10k commands/day | $0 |
| Neon PostgreSQL | 3GB storage | $0 |
| Sentry | 5k events/month | $0 |
| **TOTAL** | | **$0/month** 🎉 |

---

**Setup Time**: ~1 hour
**Maintenance**: 0 hours/month
**Scalability**: Auto-scaling included
**Reliability**: 99.9% uptime SLA
**Cost**: $0/month forever (free tiers)
