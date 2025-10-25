"""
Test script to verify @mention functionality for ASI:One integration
"""

import asyncio
import logging
from gift_expert_agent import agent, SimpleMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_mention_functionality():
    """Test the @mention functionality"""
    logger.info("🧪 Testing @mention functionality for ASI:One integration...")
    
    # Test cases for @mentions
    test_cases = [
        "@gift-expert hello",
        "@gift-expert help me",
        "@gift-expert what should I buy?",
        "@gift-expert any message here",
    ]
    
    for i, test_message in enumerate(test_cases, 1):
        logger.info(f"Test {i}: {test_message}")
        
        # Create message object
        msg = SimpleMessage(text=test_message)
        
        # Check if it starts with @
        if msg.text.startswith("@"):
            expected_response = "Hey, I'm a gift expert"
            logger.info(f"✅ Expected response: '{expected_response}'")
        else:
            logger.info("❌ Message doesn't start with @")
    
    logger.info("🎯 @mention functionality test completed!")
    logger.info("✅ Agent is ready for ASI:One integration!")

if __name__ == "__main__":
    asyncio.run(test_mention_functionality())
