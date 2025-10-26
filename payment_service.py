"""
Payment Service for SantAI Gift Recommendations
Handles payment link generation and Stripe integration
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class PaymentRequest:
    """Payment request data structure"""
    gift_id: str
    gift_name: str
    price: str
    description: str
    user_id: str
    timestamp: datetime
    payment_id: str = None
    
    def __post_init__(self):
        if self.payment_id is None:
            self.payment_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "payment_id": self.payment_id,
            "gift_id": self.gift_id,
            "gift_name": self.gift_name,
            "price": self.price,
            "description": self.description,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat()
        }


class PaymentService:
    """Service for handling payment operations"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.payment_requests: Dict[str, PaymentRequest] = {}
    
    def create_payment_link(self, gift_data: Dict[str, Any], user_id: str) -> str:
        """
        Create a payment link for a gift recommendation
        
        Args:
            gift_data: Gift information from recommendation
            user_id: User identifier
            
        Returns:
            Payment URL string
        """
        # Extract price as float for processing
        price_str = gift_data.get('price', '$0')
        price_value = self._extract_price_value(price_str)
        
        # Create payment request
        payment_request = PaymentRequest(
            gift_id=gift_data.get('id', 'unknown'),
            gift_name=gift_data.get('name', 'Gift Item'),
            price=price_str,
            description=gift_data.get('description', ''),
            user_id=user_id,
            timestamp=datetime.now()
        )
        
        # Store payment request
        self.payment_requests[payment_request.payment_id] = payment_request
        
        # Generate payment URL
        payment_url = f"{self.base_url}/payment/{payment_request.payment_id}"
        return payment_url
    
    def get_payment_request(self, payment_id: str) -> Optional[PaymentRequest]:
        """Get payment request by ID"""
        return self.payment_requests.get(payment_id)
    
    def _extract_price_value(self, price_str: str) -> float:
        """Extract numeric price value from price string"""
        import re
        # Remove currency symbols and extract number
        price_match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
        if price_match:
            return float(price_match.group())
        return 0.0
    
    def process_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Process payment (simulated)
        
        Args:
            payment_id: Payment request ID
            
        Returns:
            Payment result dictionary
        """
        payment_request = self.get_payment_request(payment_id)
        if not payment_request:
            return {"success": False, "error": "Payment request not found"}
        
        # Simulate payment processing
        return {
            "success": True,
            "payment_id": payment_id,
            "transaction_id": f"txn_{uuid.uuid4().hex[:8]}",
            "amount": payment_request.price,
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "gift_name": payment_request.gift_name
        }


# Global payment service instance
payment_service = PaymentService()
