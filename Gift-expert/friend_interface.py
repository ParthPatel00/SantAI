"""
Friend Interface for Agent-to-Agent Communication
Handles communication with Devam, Parth, and Sakshi's personality agents
"""

import asyncio
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
from shopping_agent_interface import ShoppingAgentInterface
from models import UserPreferences


class FriendInterface:
    """
    Handles communication with friend's personality agents
    """
    
    def __init__(self):
        # Agent addresses for Devam, Parth, and Sakshi
        self.agent_addresses = {
            "devam": "agent1qt99m2w7s63v5tm7ntpz6l9k95vdrmqqn5h407mu0fm30peym552wuxtj0f",
            "parth": "agent1q05setm2a9xtxepdng70uxklj94nzdskrve6mh0w7gna0fxjy8s2zatdy5v",
            "sakshi": "agent1q05setm2a9xtxepdng70uxklj94nzdskrve6mh0w7gna0fxjy8s2zatdy5v"
        }
        self.timeout = 30  # seconds
    
    async def communicate_with_friend(self, friend_name: str, ctx) -> str:
        """
        Communicate with a friend's personality agent
        
        Args:
            friend_name: Name of the friend (devam, parth, or sakshi)
            ctx: Context object for sending messages
            
        Returns:
            Formatted response with personality and gift categories
        """
        try:
            friend_name_lower = friend_name.lower()
            
            if friend_name_lower not in self.agent_addresses:
                return f"❌ I don't have contact information for {friend_name}. I can only communicate with Devam, Parth, and Sakshi."
            
            if ctx is None:
                return f"❌ Cannot communicate with {friend_name}'s agent - no context available."
            
            agent_address = self.agent_addresses[friend_name_lower]
            
            # Step 1: Ask about personality
            personality_response = await self._ask_about_personality(friend_name, agent_address, ctx)
            
            # Step 2: Ask about gift preferences
            gift_preferences_response = await self._ask_about_gift_preferences(friend_name, agent_address, ctx)
            
            # Step 3: Search for gifts based on preferences
            gift_recommendations = await self._search_gifts_for_friend(friend_name, gift_preferences_response)
            
            # Format the complete response
            response = f"🎁 **Gift Recommendations for {friend_name.title()}**\n\n"
            response += f"**Personality:** {personality_response}\n\n"
            response += f"**Gift Preferences:** {gift_preferences_response}\n\n"
            response += "**Recommended Gifts:\n**"
            
            for i, gift in enumerate(gift_recommendations[:3], 1):
                response += f"{i}. **{gift.name}** - {gift.price}\n"
                if gift.description:
                    response += f"   {gift.description[:100]}{'...' if len(gift.description) > 100 else ''}\n"
                if gift.url:
                    response += f"   [View on Amazon]({gift.url})\n"
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"❌ I had trouble communicating with {friend_name}'s agent: {str(e)}. Please try again!"
    
    async def _ask_about_personality(self, friend_name: str, agent_address: str, ctx) -> str:
        """
        Ask the friend's agent about their personality
        """
        try:
            message_text = f"Can you describe '{friend_name.title()}'s personality?"
            print(f"📤 Sending personality question to {agent_address}: {message_text}")
            
            # Create a proper message object
            from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
            from datetime import datetime, timezone
            from uuid import uuid4
            
            message = ChatMessage(
                timestamp=datetime.now(timezone.utc),
                msg_id=uuid4(),
                content=[TextContent(type="text", text=message_text)]
            )
            
            # Send message to friend's agent
            await ctx.send(agent_address, message)
            
            # Wait for response (simulated for now)
            await asyncio.sleep(2)  # Simulate network delay
            
            # For now, return a simulated response
            # In real implementation, this would wait for actual response
            simulated_responses = {
                "devam": "Tech-savvy, creative, loves gadgets and learning, entrepreneurial, always building something new",
                "parth": "Innovative, fitness-focused, travel enthusiast, creative, business-minded",
                "sakshi": "Creative, artistic, loves beauty and wellness, thoughtful, enjoys art and music"
            }
            
            response = simulated_responses.get(friend_name.lower(), f"{friend_name} is a wonderful person with unique interests and personality.")
            print(f"📥 Received personality response: {response}")
            print(f"🔍 DEBUG: Personality response type: {type(response)}")
            return response
            
        except Exception as e:
            print(f"❌ Error asking about personality: {e}")
            return f"{friend_name} has a great personality with diverse interests."
    
    async def _ask_about_gift_preferences(self, friend_name: str, agent_address: str, ctx) -> str:
        """
        Ask the friend's agent about gift preferences
        """
        try:
            message_text = f"What type of materialistic gifts would '{friend_name.title()}' enjoy? (2-3 categories)"
            print(f"📤 Sending gift preferences question to {agent_address}: {message_text}")
            
            # Create a proper message object
            from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
            from datetime import datetime, timezone
            from uuid import uuid4
            
            message = ChatMessage(
                timestamp=datetime.now(timezone.utc),
                msg_id=uuid4(),
                content=[TextContent(type="text", text=message_text)]
            )
            
            # Send message to friend's agent
            await ctx.send(agent_address, message)
            
            # Wait for response (simulated for now)
            await asyncio.sleep(2)  # Simulate network delay
            
            # For now, return a simulated response
            # In real implementation, this would wait for actual response
            simulated_responses = {
                "devam": "tech gadgets, programming books, coffee accessories",
                "parth": "fitness equipment, travel accessories, business books",
                "sakshi": "art supplies, beauty products, wellness items"
            }
            
            response = simulated_responses.get(friend_name.lower(), f"gifts related to {friend_name}'s interests")
            print(f"📥 Received gift preferences response: {response}")
            print(f"🔍 DEBUG: Gift preferences response type: {type(response)}")
            return response
            
        except Exception as e:
            print(f"❌ Error asking about gift preferences: {e}")
            return f"gifts that match {friend_name}'s interests and personality"
    
    async def _search_gifts_for_friend(self, friend_name: str, gift_preferences: str) -> List[Any]:
        """
        Search for gifts based on friend's preferences
        """
        try:
            print(f"🔍 Searching for gifts for {friend_name} with preferences: {gift_preferences}")
            
            # Create UserPreferences object
            preferences = UserPreferences(
                occasion="just because",
                recipient=friend_name,
                preferences=gift_preferences,
                budget_min=None,
                budget_max=None,
                category=None
            )
            
            # Call shopping agent with friend's preferences
            shopping_interface = ShoppingAgentInterface()
            gift_recommendations = await shopping_interface.call_shopping_agent(preferences)
            
            if gift_recommendations:
                print(f"✅ Found {len(gift_recommendations)} gifts for {friend_name}")
                return gift_recommendations
            else:
                print(f"❌ No gifts found for {friend_name}")
                return []
                
        except Exception as e:
            print(f"❌ Error searching for gifts: {e}")
            return []


# Global instance
friend_interface = FriendInterface()
