"""
RX4M Chatbot Backend API
Simple FastAPI server for chat and SMS support
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
from datetime import datetime
import openai
import yaml

app = FastAPI(title="RX4M Chatbot API", version="1.0.0")

# CORS configuration - update with your actual domains in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI API key from environment
from dotenv import load_dotenv
from pathlib import Path
# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

# Load site configurations from YAML files
def load_site_config(site_name: str) -> dict:
    """Load configuration from YAML file"""
    config_path = Path(__file__).parent.parent / 'config' / f'{site_name}.yaml'
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Configuration for {site_name} not found")

# Load configurations for both sites
SITE_CONFIGS = {
    "rx4miracles": load_site_config("rx4miracles"),
    "louisianadental": load_site_config("louisianadental"),
}


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
        "version": "1.0.0",
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Handle chat messages from the widget
    """
    if message.site not in SITE_CONFIGS:
        raise HTTPException(status_code=400, detail="Invalid site identifier")

    site_config = SITE_CONFIGS[message.site]

    try:
        # Call OpenAI API using config from YAML
        response = client.chat.completions.create(
            model=site_config["ai"]["model"],
            messages=[
                {"role": "system", "content": site_config["ai"]["system_prompt"]},
                {"role": "user", "content": message.message},
            ],
            temperature=site_config["ai"]["temperature"],
            max_tokens=site_config["ai"]["max_tokens"],
        )

        ai_response = response.choices[0].message.content

        return ChatResponse(
            response=ai_response,
            session_id=message.session_id or f"session_{datetime.now().timestamp()}",
            timestamp=datetime.now().isoformat(),
        )

    except Exception as e:
        import traceback
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
    if site not in SITE_CONFIGS:
        raise HTTPException(status_code=404, detail="Site not found")

    config = SITE_CONFIGS[site]
    return WidgetConfig(
        site_name=config["site"]["name"],
        primary_color=config["branding"]["primary_color"],
        greeting_message=config["branding"]["greeting"],
    )


@app.post("/api/sms/webhook")
async def sms_webhook(message: SMSMessage):
    """
    Handle incoming SMS messages (Twilio webhook)
    TODO: Implement SMS handling
    """
    # This will be called by Twilio when SMS is received
    # For now, just acknowledge receipt
    return {"status": "received", "message": "SMS handling coming soon"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
