from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from source.agents.personal_agents import PersonalAssistantOrchestrator

# FastAPI app setup
app = FastAPI(title="Personal Assistant API", version="1.0.0")

assistant = PersonalAssistantOrchestrator()


@app.get("/", include_in_schema=False)
async def home():
    frontend_index = Path(__file__).parent / "frontend" / "dist" / "index.html"
    legacy_index = Path(__file__).parent / "ui" / "index.html"
    return FileResponse(frontend_index if frontend_index.exists() else legacy_index)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a direct assistant request."""
    if not request.message.strip():
        return ChatResponse(response="Please provide a message.")

    response = await assistant.process_request(request.message)
    return ChatResponse(response=response)


frontend_dist = Path(__file__).parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
