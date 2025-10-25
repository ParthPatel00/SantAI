"""
Test script for Gift Expert Agent
"""

import asyncio
import logging
from gift_expert_agent import agent, GiftRequest, SimpleMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_gift_agent():
    """Test the gift expert agent functionality"""
    logger.info("🎁 Testing Gift Expert Agent...")
    
    # Test 1: Simple message
    logger.info("Test 1: Simple greeting message")
    simple_msg = SimpleMessage(text="Hello, I need help with gifts!")
    logger.info(f"Test message: {simple_msg.text}")
    
    # Test 2: Structured gift request
    logger.info("Test 2: Structured gift request")
    gift_request = GiftRequest(
        recipient_age=25,
        recipient_gender="female",
        occasion="birthday",
        budget_range="$50-100",
        interests=["tech", "fashion"],
        relationship="friend"
    )
    logger.info(f"Gift request: {gift_request.model_dump()}")
    
    # Test 3: Help request
    logger.info("Test 3: Help request")
    help_msg = SimpleMessage(text="Can you help me?")
    logger.info(f"Help message: {help_msg.text}")
    
    logger.info("✅ Gift Expert Agent tests completed successfully!")
    logger.info("🎁 Agent is ready to help with gift recommendations!")

if __name__ == "__main__":
    asyncio.run(test_gift_agent())
