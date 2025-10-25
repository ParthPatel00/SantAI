"""
Example Personality Agent for Devam
This agent represents Devam's personality and can respond to gift preference requests
"""

from uagents import Agent, Context, Protocol
from gift_communication_protocol import (
    GiftPreferencesRequest, 
    GiftPreferencesResponse, 
    GiftSentNotification,
    GiftAcknowledgment
)
from datetime import datetime
import asyncio


# Create Devam's personality agent
devam_agent = Agent(
    name="Devam-Personality",
    seed="devam-personality-seed-2025",
    port=8001,
    mailbox=True,
)

# Create protocol for gift communication
gift_protocol = Protocol("gift_communication")


@gift_protocol.on_message(GiftPreferencesRequest)
async def handle_gift_preferences_request(ctx: Context, sender: str, msg: GiftPreferencesRequest):
    """
    Handle gift preferences request from Santa Clause
    """
    ctx.logger.info(f"Received gift preferences request from {msg.from_agent}")
    
    # Devam's personality and preferences
    response = GiftPreferencesResponse(
        username="devam",
        interests=["technology", "gaming", "coffee", "books", "programming", "AI/ML", "startups", "entrepreneurship"],
        personality="tech-savvy, creative, loves gadgets and learning, entrepreneurial, always building something new",
        gift_preferences="tech gadgets, programming books, coffee accessories, gaming peripherals, coding tools, AI/ML resources, startup books, productivity tools",
        budget_range="$25-100",
        occasion="just because",
        specific_requests="something that helps with coding, learning new technologies, building projects, or improving productivity",
        timestamp=datetime.utcnow().isoformat()
    )
    
    # Send response back to Santa Clause
    await ctx.send(sender, response)
    ctx.logger.info(f"Sent gift preferences response to {sender}")


@gift_protocol.on_message(GiftSentNotification)
async def handle_gift_sent_notification(ctx: Context, sender: str, msg: GiftSentNotification):
    """
    Handle gift sent notification
    """
    ctx.logger.info(f"Received gift notification: {msg.gift_name}")
    
    # Acknowledge receipt of the gift
    acknowledgment = GiftAcknowledgment(
        recipient="devam",
        gift_name=msg.gift_name,
        timestamp=datetime.utcnow().isoformat(),
        message=f"Thank you for the {msg.gift_name}! I'm excited to use it!"
    )
    
    # Send acknowledgment back to Santa Clause
    await ctx.send(sender, acknowledgment)
    ctx.logger.info(f"Sent gift acknowledgment to {sender}")


# Include the protocol
devam_agent.include(gift_protocol, publish_manifest=True)


if __name__ == "__main__":
    print("🤖 Starting Devam's Personality Agent...")
    print(f"Agent address: {devam_agent.address}")
    print("This agent represents Devam's personality and can respond to gift requests.")
    print("Make sure to register this agent address in the SantAI system.")
    devam_agent.run()
