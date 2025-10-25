"""
HTTP-based Gift Expert Agent for ASI:One compatibility
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gift Expert Agent")

class MessageRequest(BaseModel):
    text: Optional[str] = None
    content: Optional[str] = None
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: Optional[str] = None

@app.post("/submit")
async def handle_message(request: MessageRequest):
    """Handle incoming messages from ASI:One"""
    logger.info(f"Received message: {request}")
    
    # Extract text from various message formats
    message_text = ""
    if request.text:
        message_text = request.text
    elif request.content:
        message_text = request.content
    elif request.message:
        message_text = request.message
    elif request.data and isinstance(request.data, dict):
        if 'text' in request.data:
            message_text = request.data['text']
        elif 'content' in request.data:
            message_text = request.data['content']
        elif 'message' in request.data:
            message_text = request.data['message']
        else:
            message_text = str(request.data)
    else:
        message_text = str(request)
    
    logger.info(f"Extracted text: {message_text}")
    
    # Handle empty or null messages
    if not message_text or message_text == "None" or message_text.strip() == "":
        logger.info("Received empty message, responding with default greeting")
        return {"response": "🎁 Hello! I'm your Gift Expert. I can help you find the perfect gift for any occasion. What kind of gift are you looking for?"}
    
    # Check if this is a mention (starts with @) - for ASI:One integration
    if message_text.startswith("@"):
        logger.info("Received @mention, responding with gift expert greeting")
        return {"response": "Hey, I'm a gift expert"}
    
    # Simple keyword-based responses for other messages
    text = message_text.lower()
    
    if "gift" in text or "present" in text:
        response_text = "🎁 I'd love to help you find the perfect gift! Please tell me about the recipient - their age, interests, and the occasion. You can also specify your budget range."
    elif "help" in text:
        response_text = "💝 I'm your Gift Expert! I can help you find perfect gifts based on:\n- Recipient's age and interests\n- Occasion (birthday, holiday, etc.)\n- Budget range\n- Relationship to the person\n\nJust tell me what you're looking for!"
    else:
        response_text = "🎁 Hello! I'm your Gift Expert. I can help you find the perfect gift for any occasion. What kind of gift are you looking for?"
    
    logger.info(f"Sending response: {response_text}")
    return {"response": response_text}

@app.post("/")
async def handle_any_message(request: dict):
    """Handle any message format - fallback endpoint"""
    logger.info(f"Received any message: {request}")
    
    # Extract text from any format
    message_text = ""
    if isinstance(request, dict):
        if 'text' in request:
            message_text = request['text']
        elif 'content' in request:
            message_text = request['content']
        elif 'message' in request:
            message_text = request['message']
        else:
            message_text = str(request)
    else:
        message_text = str(request)
    
    logger.info(f"Extracted text: {message_text}")
    
    # Handle empty or null messages
    if not message_text or message_text == "None" or message_text.strip() == "":
        logger.info("Received empty message, responding with default greeting")
        return {"response": "🎁 Hello! I'm your Gift Expert. I can help you find the perfect gift for any occasion. What kind of gift are you looking for?"}
    
    # Check if this is a mention (starts with @) - for ASI:One integration
    if message_text.startswith("@"):
        logger.info("Received @mention, responding with gift expert greeting")
        return {"response": "Hey, I'm a gift expert"}
    
    # Simple keyword-based responses for other messages
    text = message_text.lower()
    
    if "gift" in text or "present" in text:
        response_text = "🎁 I'd love to help you find the perfect gift! Please tell me about the recipient - their age, interests, and the occasion. You can also specify your budget range."
    elif "help" in text:
        response_text = "💝 I'm your Gift Expert! I can help you find perfect gifts based on:\n- Recipient's age and interests\n- Occasion (birthday, holiday, etc.)\n- Budget range\n- Relationship to the person\n\nJust tell me what you're looking for!"
    else:
        response_text = "🎁 Hello! I'm your Gift Expert. I can help you find the perfect gift for any occasion. What kind of gift are you looking for?"
    
    logger.info(f"Sending response: {response_text}")
    return {"response": response_text}

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "Gift Expert Agent is running", "message": "Ready to help with gift recommendations!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
