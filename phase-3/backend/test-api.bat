@echo off
REM Phase 3 Backend Test Script for Windows
REM Tests all endpoints to verify the backend is working

echo ==========================================
echo Phase 3 Backend - API Test Suite
echo ==========================================
echo.

set BASE_URL=http://localhost:8001

echo 1. Testing Health Check...
curl -s %BASE_URL%/health
echo.
echo.

echo 2. Testing Gemini API Connection...
curl -s %BASE_URL%/api/test-gemini
echo.
echo.

echo 3. Creating a test task...
curl -s -X POST %BASE_URL%/api/tasks -H "Content-Type: application/json" -d "{\"title\": \"Test Task\", \"description\": \"This is a test\", \"priority\": \"high\"}"
echo.
echo.

echo 4. Getting all tasks...
curl -s %BASE_URL%/api/tasks
echo.
echo.

echo 5. Testing AI Chat...
curl -s -X POST %BASE_URL%/api/chat -H "Content-Type: application/json" -d "{\"message\": \"Hello! Can you help me manage my tasks?\"}"
echo.
echo.

echo ==========================================
echo Test Suite Complete!
echo ==========================================
pause
