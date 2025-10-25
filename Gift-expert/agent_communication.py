"""
Agent-to-Agent Communication Module
Handles communication between SantAI and other personality agents
"""

from typing import Dict, Any, Optional, List
import asyncio
import json
from datetime import datetime
from uagents import Agent, Context, send_message, wait_for_message
from models import UserPreferences, GiftItem
from gift_communication_protocol import (
    GiftPreferencesRequest, 
    GiftPreferencesResponse, 
    GiftSentNotification
)


class AgentCommunication:
    """
    Handles communication with other personality agents
    """
    
    def __init__(self):
        self.agent_registry = {}  # username -> agent_address mapping
        self.timeout = 30  # seconds
    
    def register_agent(self, username: str, agent_address: str):
        """
        Register a personality agent in the registry
        
        Args:
            username: The username of the person
            agent_address: The uAgent address of their personality agent
        """
        self.agent_registry[username.lower()] = agent_address
        print(f"📝 Registered agent for @{username}: {agent_address}")
    
    async def query_agent_preferences(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Query a personality agent for gift preferences
        
        Args:
            username: The username to query
            
        Returns:
            Dictionary with preferences or None if failed
        """
        try:
            agent_address = self.agent_registry.get(username.lower())
            if not agent_address:
                print(f"❌ No registered agent found for @{username}")
                return None
            
            # Create a message to request gift preferences using the protocol
            message = GiftPreferencesRequest(
                from_agent="santa_clause",
                recipient=username,
                timestamp=datetime.utcnow().isoformat(),
                request="What would you like as a gift? Please share your interests, preferences, and any gift ideas."
            )
            
            # Send message to the agent (this would use uAgents messaging in real implementation)
            response = await self._send_message_to_agent(agent_address, message, username)
            
            if response:
                return self._parse_preferences_response(response)
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error querying agent for @{username}: {e}")
            return None
    
    async def _send_message_to_agent(self, agent_address: str, message, username: str = None) -> Optional[Dict[str, Any]]:
        """
        Send a message to another agent and wait for response
        
        Args:
            agent_address: The target agent's address
            message: The message to send (protocol message)
            username: The username of the recipient
            
        Returns:
            Response from the agent or None if failed
        """
        try:
            print(f"📤 Sending message to {agent_address}: {message.type}")
            
            # Use uAgents messaging to communicate with the actual agent
            await send_message(agent_address, message)
            
            # Wait for response from the agent
            response = await wait_for_message(timeout=self.timeout)
            
            if response:
                print(f"📥 Received response from {agent_address}")
                # Convert protocol response to dictionary
                if hasattr(response, 'dict'):
                    return response.dict()
                else:
                    return response
            else:
                print(f"⏰ Timeout waiting for response from {agent_address}")
                return None
            
        except Exception as e:
            print(f"❌ Error sending message to agent: {e}")
            # Fallback: if agent communication fails, return a basic response
            return self._get_fallback_response(username or getattr(message, 'recipient', 'unknown'))
    
    def _get_fallback_response(self, username: str) -> Dict[str, Any]:
        """
        Fallback response when agent communication fails
        """
        return {
            "type": "gift_preferences_response",
            "username": username,
            "interests": ["technology", "books", "music", "art"],
            "personality": "creative, thoughtful, enjoys learning",
            "gift_preferences": "books, tech gadgets, art supplies, music accessories",
            "budget_range": "$25-100",
            "occasion": "just because",
            "specific_requests": "something thoughtful and useful",
            "timestamp": datetime.utcnow().isoformat(),
            "note": "Agent communication failed, using fallback preferences"
        }
    
    def _parse_preferences_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the response from a personality agent
        
        Args:
            response: Raw response from the agent
            
        Returns:
            Parsed preferences dictionary
        """
        try:
            return {
                "username": response.get("username", "unknown"),
                "interests": response.get("interests", []),
                "personality": response.get("personality", ""),
                "gift_preferences": response.get("gift_preferences", ""),
                "budget_range": response.get("budget_range", "$25-75"),
                "occasion": response.get("occasion", "just because"),
                "specific_requests": response.get("specific_requests", ""),
                "timestamp": response.get("timestamp", datetime.utcnow().isoformat())
            }
        except Exception as e:
            print(f"❌ Error parsing preferences response: {e}")
            return None
    
    async def notify_gift_sent(self, recipient_username: str, gift: GiftItem, sender_username: str = "santa_clause"):
        """
        Notify the recipient's agent that a gift has been sent
        
        Args:
            recipient_username: Username of the gift recipient
            gift: The gift that was sent
            sender_username: Username of the gift sender
        """
        try:
            agent_address = self.agent_registry.get(recipient_username.lower())
            if not agent_address:
                print(f"❌ No registered agent found for @{recipient_username}")
                return False
            
            notification = GiftSentNotification(
                from_agent=sender_username,
                recipient=recipient_username,
                gift_name=gift.name,
                gift_price=gift.price,
                gift_description=gift.description,
                gift_url=gift.url,
                timestamp=datetime.utcnow().isoformat()
            )
            
            # Send notification to recipient's agent
            await self._send_message_to_agent(agent_address, notification)
            print(f"📬 Notified @{recipient_username} about their gift!")
            return True
            
        except Exception as e:
            print(f"❌ Error notifying recipient: {e}")
            return False
    
    def get_registered_agents(self) -> List[str]:
        """
        Get list of all registered agent usernames
        
        Returns:
            List of registered usernames
        """
        return list(self.agent_registry.keys())
    
    def is_agent_registered(self, username: str) -> bool:
        """
        Check if an agent is registered for a username
        
        Args:
            username: Username to check
            
        Returns:
            True if agent is registered, False otherwise
        """
        return username.lower() in self.agent_registry


# Global instance
agent_communication = AgentCommunication()

# Register some example agents (in real implementation, this would be done dynamically)
# These are placeholder addresses - in production, you would get these from a registry or discovery service
agent_communication.register_agent("devam", "agent1q0k6srkjt3meajrqhnd3y5d5js50a3ml2u63k78vnvkxpvn2ufrh6p603pt")  # Example address
agent_communication.register_agent("parth", "agent1q0k6srkjt3meajrqhnd3y5d5js50a3ml2u63k78vnvkxpvn2ufrh6p603pt")  # Example address  
agent_communication.register_agent("sakshi", "agent1q0k6srkjt3meajrqhnd3y5d5js50a3ml2u63k78vnvkxpvn2ufrh6p603pt")  # Example address
