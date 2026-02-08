# Frontend Package.json - Phase 3 Dependencies

Add these dependencies to your existing Phase 2 `package.json`:

```json
{
  "dependencies": {
    "@openai/chatkit": "^1.0.0",
    "lucide-react": "^0.300.0",
    "eventsource": "^2.0.2"
  },
  "devDependencies": {
    "@types/eventsource": "^1.1.15"
  }
}
```

## Installation

```bash
# Install new dependencies
npm install @openai/chatkit lucide-react eventsource

# Install dev dependencies
npm install -D @types/eventsource
```

## Full Package.json Example

```json
{
  "name": "todo-app-frontend-phase3",
  "version": "3.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\""
  },
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.3",

    "@openai/chatkit": "^1.0.0",
    "lucide-react": "^0.300.0",
    "eventsource": "^2.0.2"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@types/eventsource": "^1.1.15",

    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0",
    "prettier": "^3.2.4",
    "tailwindcss": "^3.4.1",
    "postcss": "^8.4.33",
    "autoprefixer": "^10.4.17",

    "jest": "^29.7.0",
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.2.0"
  }
}
```

## Dependency Descriptions

### Production Dependencies

- **@openai/chatkit** (^1.0.0)
  - Official OpenAI ChatKit components
  - Pre-built chat UI (messages, input, typing indicators)
  - Required for Phase 3 chat interface

- **lucide-react** (^0.300.0)
  - Icon library for React
  - Used for tool execution indicators, status icons
  - Lightweight alternative to Font Awesome

- **eventsource** (^2.0.2)
  - Server-Sent Events (SSE) client
  - Handles streaming responses from backend
  - Polyfill for browsers without native SSE support

### Development Dependencies

- **@types/eventsource** (^1.1.15)
  - TypeScript types for eventsource
  - Enables type-safe SSE handling

## Verification

After installation, verify dependencies:

```bash
# Check installed versions
npm list @openai/chatkit
npm list lucide-react
npm list eventsource

# Verify no peer dependency warnings
npm ls
```

## Troubleshooting

### "Cannot find module '@openai/chatkit'"

**Solution**: Install the package
```bash
npm install @openai/chatkit
```

### "Peer dependency warnings"

**Solution**: Update React to version 18.2+
```bash
npm install react@^18.2.0 react-dom@^18.2.0
```

### "Type errors with eventsource"

**Solution**: Install type definitions
```bash
npm install -D @types/eventsource
```

## Optional Dependencies

Consider adding these for enhanced functionality:

```bash
# State management (if needed)
npm install zustand

# Form handling
npm install react-hook-form

# Date handling
npm install date-fns

# Animation library
npm install framer-motion

# Error tracking
npm install @sentry/nextjs
```

## Notes

- All Phase 2 dependencies should remain in package.json
- ChatKit requires React 18+
- Lucide React is tree-shakeable (only imports used icons)
- EventSource polyfill ensures cross-browser compatibility
