#!/usr/bin/env python3
"""
Example script demonstrating the gift-sending functionality
"""

import asyncio
from conversation_flow import ConversationFlowManager
from agent_communication import agent_communication


async def demo_gift_sending():
    """
    Demonstrate the gift-sending functionality
    """
    print("🎁 SantAI Gift-Sending Demo")
    print("=" * 50)
    
    # Initialize conversation manager
    conversation_manager = ConversationFlowManager()
    
    # Register some example agents
    agent_communication.register_agent("devam", "agent_address_for_devam")
    agent_communication.register_agent("parth", "agent_address_for_parth")
    agent_communication.register_agent("sakshi", "agent_address_for_sakshi")
    
    print("📝 Registered agents:")
    for username in agent_communication.get_registered_agents():
        print(f"   • @{username}")
    
    print("\n" + "=" * 50)
    print("🎯 Example 1: Send gift to @devam")
    print("=" * 50)
    
    # Simulate user input
    user_input = "@santa clause, send a gift to '@devam'"
    print(f"User: {user_input}")
    
    # Process the request
    response = await conversation_manager.process_user_input("demo_user", user_input)
    print(f"Santa: {response}")
    
    print("\n" + "=" * 50)
    print("🎯 Example 2: Select gift option")
    print("=" * 50)
    
    # Simulate user selecting option 1
    user_input = "1"
    print(f"User: {user_input}")
    
    # Process the selection
    response = await conversation_manager.process_user_input("demo_user", user_input)
    print(f"Santa: {response}")
    
    print("\n" + "=" * 50)
    print("🎯 Example 3: Send gift to @parth")
    print("=" * 50)
    
    # Simulate user input
    user_input = "@santa clause, send a gift to '@parth'"
    print(f"User: {user_input}")
    
    # Process the request
    response = await conversation_manager.process_user_input("demo_user", user_input)
    print(f"Santa: {response}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(demo_gift_sending())
