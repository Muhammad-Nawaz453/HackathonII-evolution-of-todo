# Phase 3 Frontend - AI Todo Chatbot

## ✅ Setup Complete!

The frontend has been created with:
- ✅ Next.js 14 with TypeScript
- ✅ Tailwind CSS for styling
- ✅ Chat interface with split view
- ✅ Real-time task list
- ✅ Backend status indicator
- ✅ Responsive design

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd phase-3/frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

## 📋 Prerequisites

- ✅ Node.js 18+ installed
- ✅ Backend running at http://localhost:8001
- ✅ npm or yarn package manager

## 🧪 Testing

### 1. Check Backend Connection
The frontend will automatically check if the backend is online. You should see a green dot with "Backend Online" in the header.

### 2. Try These Commands
- "Add a task to buy groceries"
- "Show me my tasks"
- "Create a high priority task to review the report by Friday"
- "Add a personal task for doctor appointment"

### 3. Watch Tasks Update
As you chat with the AI, tasks will appear in the right panel in real-time!

## 🎨 Features

### Chat Interface
- ✅ Natural language input
- ✅ Real-time AI responses (Google Gemini)
- ✅ Message history
- ✅ Typing indicators
- ✅ Auto-scroll to latest message

### Task Panel
- ✅ Live task list
- ✅ Priority badges (high/medium/low)
- ✅ Category tags
- ✅ Status indicators
- ✅ Refresh button

### Backend Integration
- ✅ Automatic health checks
- ✅ Status indicator (online/offline)
- ✅ Error handling
- ✅ Axios for API calls

## 🔧 Configuration

### Environment Variables (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_CHAT_ENDPOINT=http://localhost:8001/api/chat
```

## 📁 Project Structure

```
phase-3/frontend/
├── app/
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Main chat page
├── public/                  # Static assets
├── .env.local               # Environment variables
├── .gitignore              # Git ignore rules
├── next.config.js          # Next.js configuration
├── package.json            # Dependencies
├── postcss.config.js       # PostCSS configuration
├── tailwind.config.js      # Tailwind CSS configuration
└── tsconfig.json           # TypeScript configuration
```

## 🐛 Troubleshooting

### Issue: "Backend Offline"
**Solution**: Make sure the backend is running:
```bash
cd ../backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

### Issue: "npm install" fails
**Solution**: Clear npm cache and try again:
```bash
npm cache clean --force
npm install
```

### Issue: Port 3000 already in use
**Solution**: Use a different port:
```bash
npm run dev -- -p 3001
```

### Issue: "Module not found"
**Solution**: Delete node_modules and reinstall:
```bash
rm -rf node_modules
npm install
```

## 💡 Usage Examples

### Example 1: Create a Task
**You:** "Add a high priority task to buy groceries by tomorrow"
**AI:** "I'll help you create that task..." (task appears in right panel)

### Example 2: View Tasks
**You:** "Show me all my tasks"
**AI:** "Here are your current tasks..." (lists tasks)

### Example 3: Update Task
**You:** "Mark the grocery task as complete"
**AI:** "I've marked that task as complete" (task updates in panel)

## 🎯 Next Steps

1. ✅ **Frontend is ready** - Install and run
2. 🔄 **Test the chat** - Try natural language commands
3. 🎨 **Customize UI** - Modify colors, layout, etc.
4. 💾 **Add features** - Voice input, notifications, etc.

## 📚 Documentation

- **Next.js**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **TypeScript**: https://www.typescriptlang.org/docs

---

**Status**: ✅ READY TO RUN
**Last Updated**: 2026-02-08
**Version**: 3.0.0

**Install dependencies and start the dev server!** 🚀
