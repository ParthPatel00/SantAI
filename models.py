"""
Data models for the Gift Agent
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ConversationState(Enum):
    """States in the conversation flow"""
    INITIAL = "initial"
    COLLECTING_PREFERENCES = "collecting_preferences"
    SELECTING_CATEGORY = "selecting_category"
    SHOWING_RECOMMENDATIONS = "showing_recommendations"
    SELECTING_GIFT = "selecting_gift"
    PAYMENT = "payment"
    COMPLETED = "completed"


@dataclass
class UserPreferences:
    """User preferences for gift selection"""
    occasion: Optional[str] = None
    preferences: Optional[str] = None
    budget: Optional[str] = None
    category: Optional[str] = None
    
    def is_complete(self) -> bool:
        """Check if all required preferences are collected"""
        # We need at least occasion and budget to proceed
        # Preferences can be collected later or inferred from categories
        return all([
            self.occasion is not None,
            self.budget is not None
        ])
    
    def is_fully_complete(self) -> bool:
        """Check if all preferences including specific preferences are collected"""
        return all([
            self.occasion is not None,
            self.preferences is not None,
            self.budget is not None
        ])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for LLM processing"""
        return {
            "occasion": self.occasion,
            "preferences": self.preferences,
            "budget": self.budget,
            "category": self.category
        }


@dataclass
class GiftItem:
    """Individual gift item from shopping agent"""
    id: str
    name: str
    price: str
    description: str
    source: str  # marketplace/source
    url: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    availability: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage and processing"""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "source": self.source,
            "url": self.url,
            "image_url": self.image_url,
            "rating": self.rating,
            "availability": self.availability
        }


@dataclass
class GiftRecommendation:
    """Gift recommendation with reasoning"""
    gift: GiftItem
    reason: str
    rank: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for display"""
        return {
            "id": self.gift.id,
            "name": self.gift.name,
            "price": self.gift.price,
            "description": self.gift.description,
            "reason": self.reason,
            "rank": self.rank,
            "source": self.gift.source,
            "url": self.gift.url
        }


@dataclass
class ConversationContext:
    """Context for the current conversation"""
    user_id: str
    state: ConversationState
    preferences: UserPreferences
    available_categories: List[str] = None
    current_recommendations: List[GiftRecommendation] = None
    all_gifts: List[GiftItem] = None
    selected_gift: Optional[GiftItem] = None
    conversation_history: List[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.available_categories is None:
            self.available_categories = []
        if self.current_recommendations is None:
            self.current_recommendations = []
        if self.all_gifts is None:
            self.all_gifts = []
        if self.conversation_history is None:
            self.conversation_history = []
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": str(datetime.utcnow())
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for LLM processing"""
        return {
            "user_id": self.user_id,
            "state": self.state.value,
            "preferences": self.preferences.to_dict(),
            "available_categories": self.available_categories,
            "current_recommendations": [rec.to_dict() for rec in self.current_recommendations],
            "all_gifts": [gift.to_dict() for gift in self.all_gifts],
            "selected_gift": self.selected_gift.to_dict() if self.selected_gift else None,
            "conversation_history": self.conversation_history
        }


# Import datetime for the add_message method
from datetime import datetime
