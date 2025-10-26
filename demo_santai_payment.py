"""
Test SantAI with Payment Integration
Demonstrates the complete flow from gift recommendations to payment
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from payment_service import payment_service
from datetime import datetime


def simulate_santai_recommendations():
    """Simulate SantAI gift recommendations with buy links"""
    
    print("🎁 SantAI Gift Recommendations with Payment Integration")
    print("=" * 60)
    
    # Simulate what SantAI would show to a user
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
    
    # Simulate user context
    user_id = "demo_user_123"
    occasion = "birthday"
    category = "electronics"
    
    print(f"🎉 I found some amazing {category} gifts for {occasion}!")
    print()
    print("I've carefully selected these based on what you told me. Here are my top recommendations:")
    print()
    
    for i, gift in enumerate(sample_gifts, 1):
        print(f"**{i}. {gift['name']}**")
        print(f"   💰 **Price:** {gift['price']}")
        print(f"   📝 **Description:** {gift['description']}")
        print(f"   🏪 **Available at:** {gift['source']}")
        print(f"   💡 **Why I think you'll love it:** Perfect for {occasion} celebrations!")
        
        # Generate payment link (this is what SantAI now does automatically)
        payment_url = payment_service.create_payment_link(gift, user_id)
        print(f"   🛒 **Buy Now:** {payment_url}")
        print()
    
    print("**What would you like to do?**")
    print("• **Pick a number (1-3)** to choose your favorite! 🎯")
    print("• **Click any 'Buy Now' link** to purchase directly! 💳")
    print("• **Ask me anything** about these gifts! I'm here to help! 💬")
    print()
    print("I'm so excited to see which one catches your eye! What do you think? 😊")
    
    return sample_gifts


def show_payment_flow_demo():
    """Show the complete payment flow"""
    
    print("\n" + "="*60)
    print("🛒 COMPLETE PAYMENT FLOW DEMONSTRATION")
    print("="*60)
    
    print("\n📋 **Step-by-Step Process:**")
    print()
    print("1️⃣ **SantAI Shows Recommendations**")
    print("   • User asks for gift recommendations")
    print("   • SantAI shows products with buy links")
    print("   • Each product has a 'Buy Now' link")
    print()
    
    print("2️⃣ **User Clicks Buy Link**")
    print("   • Redirects to Stripe-style checkout page")
    print("   • Shows product details and total")
    print("   • Form pre-filled with dummy data:")
    print("     - Card: 4242 4242 4242 4242")
    print("     - Expiry: 12/25")
    print("     - CVC: 123")
    print("     - Name: John Doe")
    print("     - Address: 123 Main Street, San Francisco, CA 94105")
    print()
    
    print("3️⃣ **User Completes Payment**")
    print("   • Clicks 'Complete Payment' button")
    print("   • Payment processes successfully")
    print("   • Redirects to order confirmation page")
    print()
    
    print("4️⃣ **Order Confirmation**")
    print("   • Shows 'Order Placed Successfully!'")
    print("   • Displays transaction details")
    print("   • Shows next steps (shipping, tracking, etc.)")
    print()
    
    print("🌐 **Live Demo URLs:**")
    print("• SantAI Agent: http://localhost:8000")
    print("• Payment Server: http://localhost:8001")
    print("• Swagger UI: http://localhost:8001/docs")
    print("• Health Check: http://localhost:8001/health")


def create_test_payment_for_demo():
    """Create a test payment for live demo"""
    
    print("\n" + "="*60)
    print("🧪 LIVE DEMO - Test Payment Created!")
    print("="*60)
    
    # Create a test payment
    gift_data = {
        "id": "demo_gift",
        "name": "Demo Gift for Live Testing",
        "price": "$99.99",
        "description": "A demo gift to test the complete payment flow",
        "source": "Demo Store",
        "rating": 5.0
    }
    
    user_id = "demo_user"
    payment_url = payment_service.create_payment_link(gift_data, user_id)
    payment_id = payment_url.split("/")[-1]
    
    print(f"🎁 **Demo Gift Created:**")
    print(f"   Name: {gift_data['name']}")
    print(f"   Price: {gift_data['price']}")
    print(f"   Payment ID: {payment_id}")
    print()
    
    print("🔗 **Test These URLs in Your Browser:**")
    print(f"1. **Payment Page:** {payment_url}")
    print("2. **Swagger UI:** http://localhost:8001/docs")
    print("3. **Health Check:** http://localhost:8001/health")
    print()
    
    print("💡 **Instructions:**")
    print("1. Open the payment page URL above")
    print("2. You'll see the Stripe-style checkout page")
    print("3. Click 'Complete Payment' (form is pre-filled)")
    print("4. You'll see the order confirmation page")
    print("5. Try the Swagger UI to test API endpoints")
    
    return payment_url


if __name__ == "__main__":
    print("🎁 SantAI Payment Integration - Complete Demo")
    print("=" * 60)
    
    # Show simulated SantAI recommendations
    simulate_santai_recommendations()
    
    # Show payment flow explanation
    show_payment_flow_demo()
    
    # Create test payment for live demo
    payment_url = create_test_payment_for_demo()
    
    print("\n🎉 **Integration Complete!**")
    print("Your SantAI now has full payment integration with:")
    print("✅ Buy links in gift recommendations")
    print("✅ Stripe-style checkout pages")
    print("✅ Order confirmation pages")
    print("✅ Complete API documentation")
    print("✅ Swagger UI for testing")
