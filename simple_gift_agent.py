"""
Simple Gift Expert Agent with flexible message handling
"""

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import asyncio
import logging
import json
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the gift expert agent
agent = Agent(
    name="gift-expert",
    seed="gift-expert-seed-2025-parth-sakshi-devam",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

# Fund the agent if needed
fund_agent_if_low(agent.wallet.address())

# Simple message model
class SimpleMessage(Model):
    text: str

# Very flexible message model
class FlexibleMessage(Model):
    text: Optional[str] = None
    content: Optional[str] = None
    message: Optional[str] = None
    data: Optional[dict] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: Optional[str] = None
    # Allow any additional fields
    class Config:
        extra = "allow"

@agent.on_event("startup")
async def startup(ctx: Context):
    """Handle agent startup"""
    ctx.logger.info("🎁 Gift Expert Agent is starting up...")
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Agent wallet address: {agent.wallet.address()}")
    ctx.logger.info("Ready to help with gift recommendations!")

@agent.on_interval(period=60.0)
async def heartbeat(ctx: Context):
    """Send periodic heartbeat messages"""
    ctx.logger.info("💝 Gift Expert Agent is alive and ready to help!")

@agent.on_message(model=SimpleMessage)
async def handle_simple_message(ctx: Context, sender: str, msg: SimpleMessage):
    """Handle simple text messages"""
    ctx.logger.info(f"Received simple message from {sender}: {msg.text}")
    
    # Check if this is a mention (starts with @) - for ASI:One integration
    if msg.text.startswith("@"):
        response_text = "Hey, I'm a gift expert"
        response = SimpleMessage(text=response_text)
        await ctx.send(sender, response)
        return
    
    # Simple keyword-based responses for other messages
    text = msg.text.lower()
    
    if "gift" in text or "present" in text:
        response_text = "🎁 I'd love to help you find the perfect gift! Please tell me about the recipient - their age, interests, and the occasion. You can also specify your budget range."
    elif "help" in text:
        response_text = "💝 I'm your Gift Expert! I can help you find perfect gifts based on:\n- Recipient's age and interests\n- Occasion (birthday, holiday, etc.)\n- Budget range\n- Relationship to the person\n\nJust tell me what you're looking for!"
    else:
        response_text = "🎁 Hello! I'm your Gift Expert. I can help you find the perfect gift for any occasion. What kind of gift are you looking for?"
    
    response = SimpleMessage(text=response_text)
    await ctx.send(sender, response)

@agent.on_message(model=FlexibleMessage)
async def handle_flexible_message(ctx: Context, sender: str, msg: FlexibleMessage):
    """Handle flexible message format"""
    ctx.logger.info(f"Received flexible message from {sender}: {msg}")
    
    # Extract text from various message formats
    message_text = ""
    if msg.text:
        message_text = msg.text
    elif msg.content:
        message_text = msg.content
    elif msg.message:
        message_text = msg.message
    elif msg.data and isinstance(msg.data, dict):
        if 'text' in msg.data:
            message_text = msg.data['text']
        elif 'content' in msg.data:
            message_text = msg.data['content']
        elif 'message' in msg.data:
            message_text = msg.data['message']
        else:
            message_text = str(msg.data)
    else:
        message_text = str(msg)
    
    ctx.logger.info(f"Extracted text: {message_text}")
    
    # Check if this is a mention (starts with @) - for ASI:One integration
    if message_text.startswith("@"):
        response_text = "Hey, I'm a gift expert"
        response = SimpleMessage(text=response_text)
        await ctx.send(sender, response)
        return
    
    # Simple keyword-based responses for other messages
    text = message_text.lower()
    
    if "gift" in text or "present" in text:
        response_text = "🎁 I'd love to help you find the perfect gift! Please tell me about the recipient - their age, interests, and the occasion. You can also specify your budget range."
    elif "help" in text:
        response_text = "💝 I'm your Gift Expert! I can help you find perfect gifts based on:\n- Recipient's age and interests\n- Occasion (birthday, holiday, etc.)\n- Budget range\n- Relationship to the person\n\nJust tell me what you're looking for!"
    else:
        response_text = "🎁 Hello! I'm your Gift Expert. I can help you find the perfect gift for any occasion. What kind of gift are you looking for?"
    
    response = SimpleMessage(text=response_text)
    await ctx.send(sender, response)

if __name__ == "__main__":
    agent.run()
