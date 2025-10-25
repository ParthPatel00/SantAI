#!/usr/bin/env python3
"""
Test script for the gift-sending functionality
"""

import asyncio
from conversation_flow import ConversationFlowManager


async def test_gift_sending():
    """
    Test the gift-sending functionality
    """
    print("🎁 Testing SantAI Gift-Sending Functionality")
    print("=" * 60)
    
    # Initialize conversation manager
    conversation_manager = ConversationFlowManager()
    
    # Test cases
    test_cases = [
        "Can you send @devam a gift?",
        "@santa clause, send a gift to '@devam'",
        "send a gift to @parth",
        "gift for @sakshi"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_input}")
        print("-" * 40)
        
        try:
            # Process the input
            response = await conversation_manager.process_user_input("test_user", test_input)
            print(f"Response: {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
    
    print("\n✅ Testing completed!")


if __name__ == "__main__":
    asyncio.run(test_gift_sending())
