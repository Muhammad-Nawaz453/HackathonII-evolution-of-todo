"""
Vercel serverless function entry point for FastAPI application.
"""
from src.main import app

# Vercel expects a variable named 'app' or a handler function
# The FastAPI app instance is already created in src.main
