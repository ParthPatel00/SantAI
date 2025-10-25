"""
Global Memory System for storing gift search results and user contexts
"""

from typing import Dict, List, Optional
from models import ConversationContext, GiftItem, GiftRecommendation
import json
import threading
from datetime import datetime, timedelta


class GlobalMemory:
    """
    Thread-safe global memory system for storing gift search results and user contexts
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._user_contexts: Dict[str, ConversationContext] = {}
        self._gift_search_results: Dict[str, List[GiftItem]] = {}  # search_id -> gifts
        self._search_metadata: Dict[str, Dict] = {}  # search_id -> metadata
    
    def get_user_context(self, user_id: str) -> Optional[ConversationContext]:
        """Get user context by user ID"""
        with self._lock:
            return self._user_contexts.get(user_id)
    
    def set_user_context(self, user_id: str, context: ConversationContext):
        """Set user context"""
        with self._lock:
            self._user_contexts[user_id] = context
    
    def update_user_preferences(self, user_id: str, preferences: dict):
        """Update user preferences"""
        with self._lock:
            if user_id in self._user_contexts:
                context = self._user_contexts[user_id]
                if 'occasion' in preferences:
                    context.preferences.occasion = preferences['occasion']
                if 'preferences' in preferences:
                    context.preferences.preferences = preferences['preferences']
                if 'budget_min' in preferences or 'budget_max' in preferences:
                    context.preferences.budget_min = preferences.get('budget_min')
                    context.preferences.budget_max = preferences.get('budget_max')
                if 'category' in preferences:
                    context.preferences.category = preferences['category']
    
    def store_gift_search_results(self, search_id: str, gifts: List[GiftItem], metadata: Dict = None):
        """Store gift search results from shopping agent"""
        with self._lock:
            self._gift_search_results[search_id] = gifts
            self._search_metadata[search_id] = metadata or {}
            self._search_metadata[search_id]['timestamp'] = datetime.utcnow().isoformat()
    
    def get_gift_search_results(self, search_id: str) -> Optional[List[GiftItem]]:
        """Get gift search results by search ID"""
        with self._lock:
            return self._gift_search_results.get(search_id)
    
    def get_all_gifts_for_user(self, user_id: str) -> List[GiftItem]:
        """Get all gifts stored for a user across all searches"""
        with self._lock:
            if user_id not in self._user_contexts:
                return []
            
            context = self._user_contexts[user_id]
            return context.all_gifts
    
    def add_gifts_to_user(self, user_id: str, gifts: List[GiftItem]):
        """Add gifts to user's collection"""
        with self._lock:
            if user_id not in self._user_contexts:
                return
            
            context = self._user_contexts[user_id]
            # Avoid duplicates based on gift ID
            existing_ids = {gift.id for gift in context.all_gifts}
            new_gifts = [gift for gift in gifts if gift.id not in existing_ids]
            context.all_gifts.extend(new_gifts)
    
    def set_user_recommendations(self, user_id: str, recommendations: List[GiftRecommendation]):
        """Set gift recommendations for user"""
        with self._lock:
            if user_id in self._user_contexts:
                self._user_contexts[user_id].current_recommendations = recommendations
    
    def get_user_recommendations(self, user_id: str) -> List[GiftRecommendation]:
        """Get current gift recommendations for user"""
        with self._lock:
            if user_id in self._user_contexts:
                return self._user_contexts[user_id].current_recommendations
            return []
    
    def set_selected_gift(self, user_id: str, gift: GiftItem):
        """Set the selected gift for user"""
        with self._lock:
            if user_id in self._user_contexts:
                self._user_contexts[user_id].selected_gift = gift
    
    def get_selected_gift(self, user_id: str) -> Optional[GiftItem]:
        """Get the selected gift for user"""
        with self._lock:
            if user_id in self._user_contexts:
                return self._user_contexts[user_id].selected_gift
            return None
    
    def clear_user_data(self, user_id: str):
        """Clear all data for a user"""
        with self._lock:
            if user_id in self._user_contexts:
                del self._user_contexts[user_id]
    
    def cleanup_old_data(self, max_age_hours: int = 24):
        """Clean up old search results and contexts"""
        with self._lock:
            cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
            
            # Clean up old search results
            old_searches = []
            for search_id, metadata in self._search_metadata.items():
                if 'timestamp' in metadata:
                    timestamp = datetime.fromisoformat(metadata['timestamp'])
                    if timestamp < cutoff_time:
                        old_searches.append(search_id)
            
            for search_id in old_searches:
                if search_id in self._gift_search_results:
                    del self._gift_search_results[search_id]
                if search_id in self._search_metadata:
                    del self._search_metadata[search_id]
    
    def get_memory_stats(self) -> Dict[str, int]:
        """Get memory usage statistics"""
        with self._lock:
            return {
                "active_users": len(self._user_contexts),
                "stored_searches": len(self._gift_search_results),
                "total_gifts": sum(len(gifts) for gifts in self._gift_search_results.values())
            }
    
    def export_user_data(self, user_id: str) -> Dict:
        """Export all data for a user (for debugging/backup)"""
        with self._lock:
            if user_id not in self._user_contexts:
                return {}
            
            context = self._user_contexts[user_id]
            return {
                "user_id": user_id,
                "context": context.to_dict(),
                "all_gifts": [gift.to_dict() for gift in context.all_gifts],
                "recommendations": [rec.to_dict() for rec in context.current_recommendations],
                "export_timestamp": datetime.utcnow().isoformat()
            }


# Global instance
global_memory = GlobalMemory()
