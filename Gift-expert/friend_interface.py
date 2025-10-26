"""
Simple Friend Interface for Agent-to-Agent Communication
Sends "personality" and "preferences" messages, then calls Amazon API
"""

from typing import Dict, Any, Optional
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
from datetime import datetime, timezone
from uuid import uuid4
from shopping_agent_interface import ShoppingAgentInterface
from models import UserPreferences


class FriendInterface:
    """
    Simple interface to send 2 messages to friend agents and call Amazon API
    """
    
    def __init__(self):
        # Agent addresses for Devam, Parth, and Sakshi
        self.agent_addresses = {
            "devam": "agent1q2zn6sat56y3l600ya07pjsq2pmfcv2yjg3x3u65dk5acaj03kd767mlfl9",
            "parth": "agent1q0ammultdzelux7l6u72wnwh8ze8ne6wmsqfu4dygkah8ada2gqhqyrnzsf",
            "sakshi": "agent1q2jndpvu9re38sjkuz6qs97tvcd7nxc0d6lwt0frz0k65csmgvkv8"
        }
        self.personality = {}  # Store personality responses
        self.preferences = {}  # Store preferences responses
        self.original_user = None  # Store the original user who requested the gift
        self.link = "https://sant-ai-sd7k.vercel.app/"
    
    async def communicate_with_friend(self, friend_name: str, ctx) -> str:
        """
        Send "personality" and "preferences" messages, then call Amazon API
        
        Args:
            friend_name: Name of the friend (devam, parth, or sakshi)
            ctx: Context object for sending messages
            
        Returns:
            Status message
        """
        try:
            friend_name_lower = friend_name.lower()
            
            if friend_name_lower not in self.agent_addresses:
                return f"❌ I don't have contact information for {friend_name}."
            
            if ctx is None:
                return f"❌ Cannot communicate with {friend_name}'s agent - no context available."
            
            agent_address = self.agent_addresses[friend_name_lower]
            
            # Clear any previous responses
            self.personality[friend_name_lower] = None
            self.preferences[friend_name_lower] = None
            
            # Message 1: Send "personality"
            personality_message = ChatMessage(
                timestamp=datetime.now(timezone.utc),
                msg_id=uuid4(),
                content=[TextContent(type="text", text="personality")]
            )
            await ctx.send(agent_address, personality_message)
            print(f"📤 Sent 'personality' message to {friend_name}")
            
            # Message 2: Send "preferences"
            preferences_message = ChatMessage(
                timestamp=datetime.now(timezone.utc),
                msg_id=uuid4(),
                content=[TextContent(type="text", text="preferences")]
            )
            await ctx.send(agent_address, preferences_message)
            print(f"📤 Sent 'preferences' message to {friend_name}")
            
            return f"🎁 Getting gift recommendations for {friend_name.title()}..."
            
        except Exception as e:
            return f"❌ Error sending messages to {friend_name}: {str(e)}"
    
    def store_personality(self, friend_name: str, response_text: str):
        """
        Store personality response from friend agent
        
        Args:
            friend_name: Name of the friend who responded
            response_text: The personality response text
        """
        friend_name_lower = friend_name.lower()
        self.personality[friend_name_lower] = response_text
        print(f"📥 Stored personality from {friend_name}: {response_text[:100]}...")
    
    async def store_preferences(self, friend_name: str, response_text: str):
        """
        Store preferences response from friend agent
        
        Args:
            friend_name: Name of the friend who responded
            response_text: The preferences response text
        """
        friend_name_lower = friend_name.lower()
        self.preferences[friend_name_lower] = response_text
        print(f"📥 Stored preferences from {friend_name}: {response_text[:100]}...")
        
        # If we have both personality and preferences, call Amazon API
        if self.personality.get(friend_name_lower) and self.preferences.get(friend_name_lower):
            print(f"🎁 Have both responses from {friend_name}, calling Amazon API...")
            return await self._call_amazon_api(friend_name)
        
        return None
    
    async def _call_amazon_api(self, friend_name: str) -> str:
        """
        Call Amazon API with friend's preferences
        
        Args:
            friend_name: Name of the friend
            
        Returns:
            Formatted gift recommendations
        """
        try:
            friend_name_lower = friend_name.lower()
            preferences_text = self.preferences[friend_name_lower]
            
            # Create UserPreferences object
            preferences = UserPreferences(
                occasion="just because",
                recipient=friend_name,
                preferences=preferences_text,
                budget_min=None,
                budget_max=None,
                category=None
            )
            
            # Call shopping agent
            shopping_interface = ShoppingAgentInterface()
            gift_recommendations, is_valid, missing_requirements = await shopping_interface.call_shopping_agent(preferences)
            
            if gift_recommendations and is_valid:
                response_text = f"🎁 **Gift Recommendations for {friend_name.title()}**\n\n"
                response_text += f"**Based on preferences:** {preferences_text}\n\n"
                response_text += "**Recommended Gifts:**\n"
                for i, gift in enumerate(gift_recommendations[:3], 1):
                    response_text += f"{i}. **{gift.name}** - ${gift.price}\n"
                    response_text += f"   {gift.description}\n"
                    response_text += f"   [Buy via Stripe]({self.link})\n\n"
                return response_text
            else:
                return f"❌ No gifts found for {friend_name.title()}. Please try again."
            
        except Exception as e:
            return f"❌ Error calling Amazon API: {str(e)}"
    
    def get_personality(self, friend_name: str) -> str:
        """
        Get stored personality response
        
        Args:
            friend_name: Name of the friend
            
        Returns:
            Personality response or None
        """
        friend_name_lower = friend_name.lower()
        return self.personality.get(friend_name_lower)
    
    def get_preferences(self, friend_name: str) -> str:
        """
        Get stored preferences response
        
        Args:
            friend_name: Name of the friend
            
        Returns:
            Preferences response or None
        """
        friend_name_lower = friend_name.lower()
        return self.preferences.get(friend_name_lower)


# Global instance
friend_interface = FriendInterface()