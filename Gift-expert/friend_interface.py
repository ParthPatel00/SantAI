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
            "devam": "agent1q2zn6sat56y3l600ya07pjsq2pmfcv2yjg3x3u65dk5acaj03kd767mlfl9",
            "parth": "agent1q0ammultdzelux7l6u72wnwh8ze8ne6wmsqfu4dygkah8ada2gqhqyrnzsf",
            "sakshi": "agent1q2jndpvu9re38sjkuz6qs97tvcd7nxc0d6lwt0frz0zqakvfk65csmgvkv8"
        }
        self.timeout = 30  # seconds
        self.pending_responses = {}  # Store responses from friend agents
        self.response_handlers = {}  # Store response handlers for each friend
    
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
            
            # Clear any previous responses for this friend
            self.clear_friend_responses(friend_name)
            
            # Step 1: Ask about personality
            personality_response = await self._ask_about_personality(friend_name, agent_address, ctx)
            
            # Step 2: Ask about gift preferences
            gift_preferences_response = await self._ask_about_gift_preferences(friend_name, agent_address, ctx)
            
            # Step 3: Search for gifts based on preferences
            gift_recommendations = await self._search_gifts_for_friend(friend_name, gift_preferences_response)
            
            # Debug logging
            print(f"🔍 DEBUG: Gift recommendations type: {type(gift_recommendations)}")
            print(f"🔍 DEBUG: Gift recommendations length: {len(gift_recommendations) if gift_recommendations else 0}")
            if gift_recommendations:
                print(f"🔍 DEBUG: First gift type: {type(gift_recommendations[0])}")
                print(f"🔍 DEBUG: First gift: {gift_recommendations[0]}")
            
            # Format the complete response
            response = f"🎁 **Gift Recommendations for {friend_name.title()}**\n\n"
            response += f"**Personality:** {personality_response}\n\n"
            response += f"**Gift Preferences:** {gift_preferences_response}\n\n"
            response += "**Recommended Gifts:\n**"
            
            if gift_recommendations:
                for i, gift in enumerate(gift_recommendations[:3], 1):
                    try:
                        response += f"{i}. **{gift.name}** - {gift.price}\n"
                        if gift.description:
                            response += f"   {gift.description[:100]}{'...' if len(gift.description) > 100 else ''}\n"
                        if gift.url:
                            response += f"   [View on Amazon]({gift.url})\n"
                        response += "\n"
                    except AttributeError as e:
                        print(f"❌ Error processing gift {i}: {e}")
                        print(f"🔍 DEBUG: Gift object: {gift}")
                        response += f"{i}. **Gift {i}** - Price not available\n"
                        response += f"   [View on Amazon]({gift.url if hasattr(gift, 'url') else 'N/A'})\n\n"
            else:
                response += "No gifts found. Please try again with different preferences.\n"
            
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
            
            # Wait for actual response from the agent
            print(f"⏳ Waiting for personality response from {friend_name}...")
            
            # Wait for response with timeout
            import time
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                response = self.get_friend_response(friend_name, "personality")
                if response:
                    print(f"📥 Received personality response from {friend_name}: {response[:100]}...")
                    return response
                await asyncio.sleep(0.5)  # Check every 500ms
            
            # Timeout reached
            print(f"⏰ Timeout waiting for personality response from {friend_name}")
            return f"⏰ Timeout waiting for {friend_name}'s personality information. Please try again."
            
        except Exception as e:
            print(f"❌ Error asking about personality: {e}")
            return f"❌ Could not communicate with {friend_name}'s agent: {str(e)}"
    
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
            
            # Wait for actual response from the agent
            print(f"⏳ Waiting for gift preferences response from {friend_name}...")
            
            # Wait for response with timeout
            import time
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                response = self.get_friend_response(friend_name, "gift_preferences")
                if response:
                    print(f"📥 Received gift preferences response from {friend_name}: {response[:100]}...")
                    return response
                await asyncio.sleep(0.5)  # Check every 500ms
            
            # Timeout reached
            print(f"⏰ Timeout waiting for gift preferences response from {friend_name}")
            return f"⏰ Timeout waiting for {friend_name}'s gift preferences. Please try again."
            
        except Exception as e:
            print(f"❌ Error asking about gift preferences: {e}")
            return f"❌ Could not communicate with {friend_name}'s agent: {str(e)}"
    
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
            gift_recommendations, is_valid, missing_requirements = await shopping_interface.call_shopping_agent(preferences)
            
            if gift_recommendations and is_valid:
                print(f"✅ Found {len(gift_recommendations)} gifts for {friend_name}")
                return gift_recommendations
            else:
                print(f"❌ No gifts found for {friend_name}")
                return []
                
        except Exception as e:
            print(f"❌ Error searching for gifts: {e}")
            return []
    
    def handle_friend_response(self, friend_name: str, response_text: str, response_type: str):
        """
        Handle responses from friend agents
        
        Args:
            friend_name: Name of the friend who responded
            response_text: The response text from the friend
            response_type: Type of response (personality, gift_preferences)
        """
        friend_name_lower = friend_name.lower()
        
        if friend_name_lower not in self.pending_responses:
            self.pending_responses[friend_name_lower] = {}
        
        self.pending_responses[friend_name_lower][response_type] = response_text
        print(f"📥 Stored {response_type} response from {friend_name}: {response_text[:100]}...")
    
    def get_friend_response(self, friend_name: str, response_type: str) -> str:
        """
        Get a stored response from a friend agent
        
        Args:
            friend_name: Name of the friend
            response_type: Type of response to get (personality, gift_preferences)
            
        Returns:
            The stored response or None if not available
        """
        friend_name_lower = friend_name.lower()
        
        if friend_name_lower in self.pending_responses:
            return self.pending_responses[friend_name_lower].get(response_type)
        
        return None
    
    def clear_friend_responses(self, friend_name: str):
        """
        Clear stored responses for a friend
        
        Args:
            friend_name: Name of the friend to clear responses for
        """
        friend_name_lower = friend_name.lower()
        if friend_name_lower in self.pending_responses:
            del self.pending_responses[friend_name_lower]


# Global instance
friend_interface = FriendInterface()
