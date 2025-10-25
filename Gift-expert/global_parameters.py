"""
Global parameter store for gift preferences
"""
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class GlobalParameters:
    """Global parameter store that persists across conversations"""
    occasion: str = None
    recipient: str = None
    preferences: str = None
    budget_min: int = None
    budget_max: int = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for LLM context"""
        return {
            "occasion": self.occasion,
            "recipient": self.recipient,
            "preferences": self.preferences,
            "budget_min": self.budget_min,
            "budget_max": self.budget_max
        }
    
    def get_missing_info(self) -> List[str]:
        """Get list of missing parameters"""
        missing = []
        if not self.occasion:
            missing.append("occasion")
        if not self.recipient:
            missing.append("recipient")
        if not self.preferences:
            missing.append("preferences")
        if not self.budget_min and not self.budget_max:
            missing.append("budget_min")
            missing.append("budget_max")
        return missing
    
    def is_complete(self) -> bool:
        """Check if all required parameters are filled"""
        return (self.occasion is not None and 
                self.recipient is not None and 
                self.preferences is not None and 
                (self.budget_min is not None or self.budget_max is not None))
    
    def reset(self):
        """Reset all parameters to None"""
        self.occasion = None
        self.recipient = None
        self.preferences = None
        self.budget_min = None
        self.budget_max = None

# Global instance
global_params = GlobalParameters()
