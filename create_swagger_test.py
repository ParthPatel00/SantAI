"""
Generate test payment request for Swagger UI testing
"""

from payment_service import payment_service
import json

def create_test_payment():
    """Create a test payment request for Swagger UI testing"""
    
    # Sample gift data
    gift_data = {
        "id": "swagger_test_gift",
        "name": "Swagger Test Gift",
        "price": "$99.99",
        "description": "A test gift for Swagger UI testing",
        "source": "Test Store",
        "rating": 5.0
    }
    
    # Create payment link
    user_id = "swagger_test_user"
    payment_url = payment_service.create_payment_link(gift_data, user_id)
    
    # Get the payment ID from the URL
    payment_id = payment_url.split("/")[-1]
    
    print("🧪 Swagger UI Test Payment Created!")
    print("=" * 50)
    print(f"Payment ID: {payment_id}")
    print(f"Payment URL: {payment_url}")
    print()
    print("🔗 Swagger UI URLs:")
    print(f"• Swagger UI: http://localhost:8001/docs")
    print(f"• ReDoc: http://localhost:8001/redoc")
    print()
    print("🧪 Test these API endpoints:")
    print(f"• GET /api/payment/{payment_id}")
    print(f"• POST /api/process-payment/{payment_id}")
    print(f"• GET /health")
    print()
    print("💡 Instructions:")
    print("1. Open http://localhost:8001/docs in your browser")
    print("2. Try the 'Get Payment Request' endpoint with the payment ID above")
    print("3. Try the 'Process Payment (API)' endpoint")
    print("4. Test the 'Health Check' endpoint")
    print("5. Click 'Try it out' and 'Execute' for each endpoint")
    
    return payment_id

if __name__ == "__main__":
    create_test_payment()
