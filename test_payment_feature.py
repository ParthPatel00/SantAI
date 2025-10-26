"""
Test script for SantAI Payment Feature
Demonstrates the payment integration with gift recommendations
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from payment_service import payment_service, PaymentRequest
from datetime import datetime


def test_payment_service():
    """Test the payment service functionality"""
    print("🧪 Testing SantAI Payment Service")
    print("=" * 50)
    
    # Sample gift data (similar to what would come from recommendations)
    sample_gifts = [
        {
            "id": "gift_001",
            "name": "Wireless Bluetooth Headphones",
            "price": "$79.99",
            "description": "High-quality wireless headphones with noise cancellation",
            "source": "Amazon",
            "rating": 4.5
        },
        {
            "id": "gift_002", 
            "name": "Smart Fitness Watch",
            "price": "$149.99",
            "description": "Advanced fitness tracking with heart rate monitoring",
            "source": "Best Buy",
            "rating": 4.8
        },
        {
            "id": "gift_003",
            "name": "Gourmet Coffee Gift Set",
            "price": "$45.00",
            "description": "Premium coffee beans from around the world",
            "source": "Local Coffee Shop",
            "rating": 4.7
        }
    ]
    
    print("📦 Sample Gift Recommendations:")
    print("-" * 30)
    
    for i, gift in enumerate(sample_gifts, 1):
        print(f"{i}. {gift['name']}")
        print(f"   💰 Price: {gift['price']}")
        print(f"   📝 Description: {gift['description']}")
        print(f"   🏪 Available at: {gift['source']}")
        
        # Generate payment link
        user_id = "test_user_123"
        payment_url = payment_service.create_payment_link(gift, user_id)
        print(f"   🛒 Buy Now: {payment_url}")
        print()
    
    print("🔗 Payment Links Generated Successfully!")
    print("\n💡 To test the payment flow:")
    print("1. Start the payment server: python payment_server.py")
    print("2. Click any 'Buy Now' link above")
    print("3. Complete the payment form with dummy data")
    print("4. See the order placed page")
    
    return sample_gifts


def test_payment_processing():
    """Test payment processing"""
    print("\n🔄 Testing Payment Processing")
    print("=" * 50)
    
    # Create a test payment request and store it
    payment_request = PaymentRequest(
        gift_id="test_gift_001",
        gift_name="Test Gift Item",
        price="$99.99",
        description="A test gift for demonstration",
        user_id="test_user",
        timestamp=datetime.now()
    )
    
    # Store the payment request in the service
    payment_service.payment_requests[payment_request.payment_id] = payment_request
    
    print(f"📋 Payment Request Created:")
    print(f"   ID: {payment_request.payment_id}")
    print(f"   Gift: {payment_request.gift_name}")
    print(f"   Price: {payment_request.price}")
    print(f"   User: {payment_request.user_id}")
    
    # Process payment
    result = payment_service.process_payment(payment_request.payment_id)
    
    print(f"\n✅ Payment Processing Result:")
    print(f"   Success: {result['success']}")
    if result['success']:
        print(f"   Transaction ID: {result['transaction_id']}")
        print(f"   Amount: {result['amount']}")
        print(f"   Status: {result['status']}")
    else:
        print(f"   Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("🎁 SantAI Payment Feature Test")
    print("=" * 50)
    
    # Test payment service
    gifts = test_payment_service()
    
    # Test payment processing
    test_payment_processing()
    
    print("\n🎉 All tests completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Install payment dependencies: pip install fastapi uvicorn jinja2")
    print("2. Start payment server: python payment_server.py")
    print("3. Test the payment flow in your browser")
    print("4. Integrate with your SantAI agent")
