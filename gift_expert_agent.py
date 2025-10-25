"""
Gift Expert Agent - Fetch.ai uAgents
A specialized agent that provides gift recommendations based on user preferences.
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
    seed="gift-expert-seed-2025-parth-sakshi-devam",  # Your custom seed phrase
    port=8001,  # Using different port to avoid conflicts
    endpoint=["http://127.0.0.1:8001/submit"],
)

# Fund the agent if needed
fund_agent_if_low(agent.wallet.address())

# Message models for structured communication
class GiftRequest(Model):
    """Request model for gift recommendations"""
    recipient_age: Optional[int] = None
    recipient_gender: Optional[str] = None
    occasion: Optional[str] = None
    budget_range: Optional[str] = None
    interests: Optional[List[str]] = None
    relationship: Optional[str] = None

class GiftRecommendation(Model):
    """Response model for gift recommendations"""
    recommendations: List[Dict[str, str]]
    reasoning: str
    budget_notes: str

class SimpleMessage(Model):
    """Simple text message model"""
    text: str

# Gift database (in a real app, this would be a proper database)
GIFT_DATABASE = {
    "tech": [
        {"name": "Wireless Earbuds", "price": "$50-100", "description": "High-quality audio experience"},
        {"name": "Smart Watch", "price": "$100-300", "description": "Fitness tracking and notifications"},
        {"name": "Bluetooth Speaker", "price": "$30-80", "description": "Portable music anywhere"},
    ],
    "books": [
        {"name": "Bestseller Novel", "price": "$15-25", "description": "Popular fiction or non-fiction"},
        {"name": "Coffee Table Book", "price": "$30-60", "description": "Beautiful photography or art"},
        {"name": "Cookbook", "price": "$20-40", "description": "Culinary inspiration"},
    ],
    "fashion": [
        {"name": "Designer Scarf", "price": "$40-120", "description": "Elegant accessory"},
        {"name": "Leather Wallet", "price": "$50-150", "description": "Durable and stylish"},
        {"name": "Jewelry", "price": "$30-200", "description": "Beautiful accessories"},
    ],
    "experiences": [
        {"name": "Spa Day", "price": "$80-200", "description": "Relaxation and pampering"},
        {"name": "Cooking Class", "price": "$60-120", "description": "Learn new culinary skills"},
        {"name": "Concert Tickets", "price": "$50-300", "description": "Live music experience"},
    ],
    "home": [
        {"name": "Smart Home Device", "price": "$30-150", "description": "Automate your home"},
        {"name": "Art Print", "price": "$20-80", "description": "Beautiful wall decoration"},
        {"name": "Plants", "price": "$15-50", "description": "Bring nature indoors"},
    ]
}

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

@agent.on_message(model=GiftRequest)
async def handle_gift_request(ctx: Context, sender: str, msg: GiftRequest):
    """Handle structured gift recommendation requests"""
    ctx.logger.info(f"Received gift request from {sender}")
    
    # Generate recommendations based on the request
    recommendations = generate_gift_recommendations(msg)
    
    # Create response
    response = GiftRecommendation(
        recommendations=recommendations,
        reasoning=f"Based on your preferences: {msg.occasion or 'general occasion'}, budget: {msg.budget_range or 'flexible'}, interests: {', '.join(msg.interests or ['general']) if msg.interests else 'general'}",
        budget_notes=f"Budget range: {msg.budget_range or 'flexible'}"
    )
    
    await ctx.send(sender, response)
    ctx.logger.info(f"Sent {len(recommendations)} gift recommendations to {sender}")

@agent.on_message(model=SimpleMessage)
async def handle_simple_message(ctx: Context, sender: str, msg: SimpleMessage):
    """Handle simple text messages"""
    ctx.logger.info(f"Received message from {sender}: {msg.text}")
    
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

# Add a flexible message handler for ASI:One format
class ASIMessage(Model):
    """Message model for ASI:One integration"""
    text: Optional[str] = None
    content: Optional[str] = None
    message: Optional[str] = None
    data: Optional[dict] = None
    # Add more fields that ASI:One might send
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: Optional[str] = None

@agent.on_message(model=ASIMessage)
async def handle_asi_message(ctx: Context, sender: str, msg: ASIMessage):
    """Handle ASI:One message format"""
    ctx.logger.info(f"Received ASI message from {sender}: {msg}")
    
    # Extract text from various message formats
    message_text = ""
    if msg.text:
        message_text = msg.text
    elif msg.content:
        message_text = msg.content
    elif msg.message:
        message_text = msg.message
    elif msg.data and isinstance(msg.data, dict):
        # Try to extract text from data dict
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

# Add a catch-all handler for any message format
class AnyMessage(Model):
    """Catch-all message model for any format"""
    pass

@agent.on_message(model=AnyMessage)
async def handle_any_message(ctx: Context, sender: str, msg: AnyMessage):
    """Handle any message format - fallback handler"""
    ctx.logger.info(f"Received any message from {sender}: {msg}")
    
    # Try to extract text from the message object
    message_text = str(msg)
    
    # Check if this is a mention (starts with @) - for ASI:One integration
    if message_text.startswith("@"):
        response_text = "Hey, I'm a gift expert"
        response = SimpleMessage(text=response_text)
        await ctx.send(sender, response)
        return
    
    # Default response for any message
    response_text = "🎁 Hello! I'm your Gift Expert. I can help you find the perfect gift for any occasion. What kind of gift are you looking for?"
    response = SimpleMessage(text=response_text)
    await ctx.send(sender, response)

def generate_gift_recommendations(request: GiftRequest) -> List[Dict[str, str]]:
    """Generate gift recommendations based on the request"""
    recommendations = []
    
    # If interests are specified, prioritize those categories
    if request.interests:
        for interest in request.interests:
            if interest.lower() in GIFT_DATABASE:
                recommendations.extend(GIFT_DATABASE[interest.lower()][:2])  # Top 2 from each category
    
    # If no specific interests or not enough recommendations, add general ones
    if len(recommendations) < 3:
        # Add some general recommendations
        general_categories = ["tech", "books", "fashion", "experiences", "home"]
        for category in general_categories:
            if len(recommendations) >= 5:
                break
            if category in GIFT_DATABASE:
                recommendations.extend(GIFT_DATABASE[category][:1])
    
    # Limit to 5 recommendations
    return recommendations[:5]

if __name__ == "__main__":
    agent.run()
