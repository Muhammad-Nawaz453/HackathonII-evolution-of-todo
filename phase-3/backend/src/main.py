"""
Phase 3 Backend - AI-Powered Todo Chatbot
Minimal implementation for testing Gemini API integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="Phase 3 - AI-powered todo management with Google Gemini",
    version="3.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not set. Chat functionality will not work.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    print("SUCCESS: Gemini API configured successfully")

# In-memory storage (for demo purposes)
tasks_db = []
task_id_counter = 1

# Pydantic models
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = "incomplete"
    priority: Optional[str] = "medium"
    category: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    action_taken: Optional[str] = None
    task_data: Optional[dict] = None

# System instruction for Gemini
SYSTEM_INSTRUCTION = """You are an intelligent todo management assistant. Your role is to help users manage their tasks through natural conversation.

Your Capabilities:
- Create new tasks with details (title, priority, category)
- List all tasks
- Update existing tasks
- Delete tasks
- Mark tasks as complete or incomplete
- Search and filter tasks

Response Guidelines:
- Be conversational and friendly
- Confirm actions taken
- Ask for clarification when needed
- Provide helpful suggestions
- Keep responses concise but informative

When the user wants to create a task, extract:
- Title (required)
- Description (optional)
- Priority (high/medium/low)
- Category (work/personal/shopping/etc)

Always confirm what action you took and provide relevant details."""

# Routes
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Todo AI Chatbot API",
        "version": "3.0.0",
        "ai_provider": "Google Gemini",
        "gemini_configured": GEMINI_API_KEY is not None
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "gemini_api": "configured" if GEMINI_API_KEY else "not_configured",
        "tasks_count": len(tasks_db)
    }

@app.get("/api/tasks")
async def get_tasks():
    """Get all tasks"""
    return {"tasks": tasks_db, "count": len(tasks_db)}

@app.post("/api/tasks")
async def create_task(task: Task):
    """Create a new task"""
    global task_id_counter
    task.id = task_id_counter
    task_id_counter += 1
    tasks_db.append(task.dict())
    return {"message": "Task created successfully", "task": task.dict()}

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    """Update an existing task"""
    for i, t in enumerate(tasks_db):
        if t["id"] == task_id:
            task.id = task_id
            tasks_db[i] = task.dict()
            return {"message": "Task updated successfully", "task": task.dict()}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    global tasks_db
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return {"message": "Task deleted successfully"}

@app.post("/api/chat")
async def chat(message: ChatMessage):
    """
    Chat endpoint - processes natural language commands using Gemini with function calling
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Gemini API not configured. Please set GEMINI_API_KEY environment variable."
        )

    try:
        global task_id_counter

        # Define function declarations for Gemini
        tools = [
            {
                "function_declarations": [
                    {
                        "name": "create_task",
                        "description": "Create a new task with title, description, priority, and category",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "The title of the task"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Optional description of the task"
                                },
                                "priority": {
                                    "type": "string",
                                    "enum": ["high", "medium", "low"],
                                    "description": "Priority level of the task"
                                },
                                "category": {
                                    "type": "string",
                                    "description": "Category of the task (e.g., work, personal, shopping)"
                                }
                            },
                            "required": ["title"]
                        }
                    },
                    {
                        "name": "list_tasks",
                        "description": "List all current tasks",
                        "parameters": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "delete_task",
                        "description": "Delete a task by its ID",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "integer",
                                    "description": "The ID of the task to delete"
                                }
                            },
                            "required": ["task_id"]
                        }
                    }
                ]
            }
        ]

        # Initialize Gemini model with tools
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=SYSTEM_INSTRUCTION,
            tools=tools
        )

        # Add context about current tasks
        context = f"\n\nCurrent tasks in the system:\n"
        if tasks_db:
            for task in tasks_db:
                context += f"- ID {task['id']}: {task['title']} (Status: {task['status']}, Priority: {task.get('priority', 'medium')})\n"
        else:
            context += "No tasks yet.\n"

        # Generate response with function calling
        full_prompt = message.message + context
        response = model.generate_content(full_prompt)

        # Check if Gemini wants to call a function
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = dict(function_call.args)

            # Execute the function
            function_result = None
            action_taken = None

            if function_name == "create_task":
                # Create the task
                new_task = {
                    "id": task_id_counter,
                    "title": function_args.get("title"),
                    "description": function_args.get("description"),
                    "status": "incomplete",
                    "priority": function_args.get("priority", "medium"),
                    "category": function_args.get("category")
                }
                tasks_db.append(new_task)
                task_id_counter += 1
                function_result = {"success": True, "task": new_task}
                action_taken = "task_created"

            elif function_name == "list_tasks":
                function_result = {"tasks": tasks_db, "count": len(tasks_db)}
                action_taken = "tasks_listed"

            elif function_name == "delete_task":
                task_id = function_args.get("task_id")
                tasks_db[:] = [t for t in tasks_db if t["id"] != task_id]
                function_result = {"success": True, "deleted_id": task_id}
                action_taken = "task_deleted"

            # Send function result back to Gemini for natural language response
            response2 = model.generate_content([
                {"role": "user", "parts": [{"text": full_prompt}]},
                {"role": "model", "parts": [{"function_call": function_call}]},
                {"role": "user", "parts": [{"function_response": {
                    "name": function_name,
                    "response": function_result
                }}]}
            ])

            response_text = response2.text

            return ChatResponse(
                response=response_text,
                action_taken=action_taken,
                task_data=function_result
            )
        else:
            # No function call, just return the text response
            response_text = response.text
            return ChatResponse(
                response=response_text,
                action_taken=None,
                task_data=None
            )

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in chat endpoint: {error_details}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )

@app.get("/api/test-gemini")
async def test_gemini():
    """Test Gemini API connection"""
    if not GEMINI_API_KEY:
        return {
            "status": "error",
            "message": "GEMINI_API_KEY not configured"
        }

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello! Gemini API is working!' in a friendly way.")
        return {
            "status": "success",
            "message": "Gemini API is working!",
            "response": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Gemini API error: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
