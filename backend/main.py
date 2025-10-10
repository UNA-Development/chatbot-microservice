"""
Chatbot Microservice Backend API
Multi-tenant FastAPI server for chat and SMS support with OpenAI Assistants API
Database-driven configuration - no redeployment needed for new companies!
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.orm import Session
import os
import traceback
import re
from openai import OpenAI
from models import Company, init_db, get_db
from admin_api import router as admin_router

app = FastAPI(title="Multi-Tenant Chatbot API", version="3.0.0")

# Include admin API routes
app.include_router(admin_router)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    init_db()
    db = next(get_db())
    company_count = db.query(Company).count()
    print(f"✓ Database connected: {company_count} companies loaded")
    db.close()


# Pydantic models
class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None
    site: str = Field(..., description="Site identifier: rx4miracles or louisianadental")


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str


class SMSMessage(BaseModel):
    from_number: str
    body: str
    site: str


class WidgetConfig(BaseModel):
    site_name: str
    primary_color: str
    greeting_message: str


@app.get("/")
async def root(db: Session = Depends(get_db)):
    """Health check endpoint"""
    company_count = db.query(Company).filter(Company.active == True).count()
    return {
        "status": "online",
        "service": "Chatbot Microservice API",
        "version": "3.0.0",
        "rag_provider": "OpenAI Assistants API",
        "active_companies": company_count
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Handle chat messages using OpenAI Assistants API
    Loads company config from database dynamically
    """
    # Get company from database
    company = db.query(Company).filter(
        Company.site_id == message.site,
        Company.active == True
    ).first()

    if not company:
        raise HTTPException(status_code=404, detail=f"Company '{message.site}' not found or inactive")

    if not company.assistant_id:
        raise HTTPException(status_code=500, detail=f"Assistant not configured for {message.site}")

    try:
        # Create a simple thread without file attachments (faster)
        # The assistant instructions already contain the knowledge
        thread = client.beta.threads.create(
            messages=[{
                "role": "user",
                "content": message.message
            }]
        )

        # Run the assistant
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=company.assistant_id
        )

        # Wait for completion and get response
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            ai_response = messages.data[0].content[0].text.value

            # Remove citation annotations like 【4:0†source】
            ai_response = re.sub(r'【\d+:\d+†[^】]+】', '', ai_response)

            return ChatResponse(
                response=ai_response,
                session_id=message.session_id or thread.id,
                timestamp=datetime.now().isoformat(),
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Assistant run failed with status: {run.status}"
            )

    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"Error processing chat message: {str(e)}"
        )


@app.get("/api/config/{site}", response_model=WidgetConfig)
async def get_widget_config(site: str, db: Session = Depends(get_db)):
    """
    Get widget configuration for a specific site
    Loads from database - no hardcoded configs!
    """
    company = db.query(Company).filter(
        Company.site_id == site,
        Company.active == True
    ).first()

    if not company:
        raise HTTPException(status_code=404, detail="Site not found")

    return WidgetConfig(
        site_name=company.name,
        primary_color=company.primary_color,
        greeting_message=company.greeting,
    )


@app.post("/api/sms/webhook")
async def sms_webhook(message: SMSMessage):
    """
    Handle incoming SMS messages (Twilio webhook)
    TODO: Implement SMS handling with Assistants API
    """
    return {"status": "received", "message": "SMS handling coming soon"}


# Serve widget static files
from fastapi.staticfiles import StaticFiles
widget_path = Path(__file__).parent.parent / 'widget'
app.mount("/widget", StaticFiles(directory=str(widget_path)), name="widget")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
