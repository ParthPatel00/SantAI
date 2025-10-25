"""
Gift Communication Protocol
Defines the message types and protocols for gift-sending communication between agents
"""

from uagents import Model
from typing import Dict, Any, Optional, List
from datetime import datetime


class GiftPreferencesRequest(Model):
    """Request message asking for gift preferences"""
    type: str = "gift_preferences_request"
    from_agent: str
    recipient: str
    timestamp: str
    request: str
    message: str = "What would you like as a gift? Please share your interests, preferences, and any gift ideas."


class GiftPreferencesResponse(Model):
    """Response message with gift preferences"""
    type: str = "gift_preferences_response"
    username: str
    interests: List[str]
    personality: str
    gift_preferences: str
    budget_range: str
    occasion: str
    specific_requests: str
    timestamp: str
    note: Optional[str] = None


class GiftSentNotification(Model):
    """Notification that a gift has been sent"""
    type: str = "gift_sent_notification"
    from_agent: str
    recipient: str
    gift_name: str
    gift_price: str
    gift_description: str
    gift_url: str
    timestamp: str
    message: str = "🎁 A gift has been sent to you! Check your notifications for details."


class GiftAcknowledgment(Model):
    """Acknowledgment of gift receipt"""
    type: str = "gift_acknowledgment"
    recipient: str
    gift_name: str
    timestamp: str
    message: str = "Thank you for the gift!"


# Protocol definition for gift communication
GIFT_COMMUNICATION_PROTOCOL = {
    "name": "gift_communication",
    "version": "1.0",
    "messages": {
        "gift_preferences_request": GiftPreferencesRequest,
        "gift_preferences_response": GiftPreferencesResponse,
        "gift_sent_notification": GiftSentNotification,
        "gift_acknowledgment": GiftAcknowledgment
    }
}
