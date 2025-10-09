"""
RX4M Chatbot Backend API
Simple FastAPI server for chat and SMS support with OpenAI Assistants API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import os
import yaml
import traceback
import re
from openai import OpenAI

app = FastAPI(title="RX4M Chatbot API", version="2.0.0")

# CORS configuration
# For production, restrict to actual domains
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load minimal site configurations (only branding for widget)
def load_widget_config(site_name: str) -> dict:
    """Load minimal widget configuration from YAML"""
    config_path = Path(__file__).parent.parent / 'config' / f'{site_name}.yaml'
    try:
        with open(config_path, 'r') as f:
            full_config = yaml.safe_load(f)
            # Only extract what we need for the widget endpoint
            return {
                "site": full_config.get("site", {}),
                "branding": full_config.get("branding", {})
            }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Configuration for {site_name} not found")

# Load minimal configurations for widget endpoint only
WIDGET_CONFIGS = {
    "rx4miracles": load_widget_config("rx4miracles"),
    "louisianadental": load_widget_config("louisianadental"),
}

# Load assistant IDs
ASSISTANTS = {
    "rx4miracles": os.getenv("RX4M_ASSISTANT_ID"),
    "louisianadental": os.getenv("LOUISIANA_ASSISTANT_ID"),
}

# Verify assistants are configured
for site, assistant_id in ASSISTANTS.items():
    if assistant_id:
        print(f"✓ {site}: assistant {assistant_id}")
    else:
        print(f"⚠ {site}: Assistant ID not configured")


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
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "RX4M Chatbot API",
        "version": "2.0.0",
        "rag_provider": "OpenAI Assistants API"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Handle chat messages using OpenAI Assistants API
    """
    if message.site not in ASSISTANTS:
        raise HTTPException(status_code=400, detail="Invalid site identifier")

    assistant_id = ASSISTANTS.get(message.site)
    if not assistant_id:
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
            assistant_id=assistant_id
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
async def get_widget_config(site: str):
    """
    Get widget configuration for a specific site
    """
    if site not in WIDGET_CONFIGS:
        raise HTTPException(status_code=404, detail="Site not found")

    config = WIDGET_CONFIGS[site]
    return WidgetConfig(
        site_name=config["site"]["name"],
        primary_color=config["branding"]["primary_color"],
        greeting_message=config["branding"]["greeting"],
    )


@app.post("/api/sms/webhook")
async def sms_webhook(message: SMSMessage):
    """
    Handle incoming SMS messages (Twilio webhook)
    TODO: Implement SMS handling with Assistants API
    """
    return {"status": "received", "message": "SMS handling coming soon"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
