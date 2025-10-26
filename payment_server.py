"""
Stripe Payment Page for SantAI Gift Recommendations
Provides a mock Stripe checkout experience with dummy data
"""

from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from payment_service import payment_service, PaymentRequest
from typing import Dict, Any
import json


app = FastAPI(
    title="SantAI Payment Gateway", 
    version="1.0.0",
    description="Payment gateway for SantAI gift recommendations with Stripe-style checkout",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Templates for HTML rendering
templates = Jinja2Templates(directory="templates")


# Pydantic models for API documentation
class PaymentRequestModel(BaseModel):
    """Payment request model"""
    payment_id: str
    gift_id: str
    gift_name: str
    price: str
    description: str
    user_id: str
    timestamp: str

    class Config:
        json_schema_extra = {
            "example": {
                "payment_id": "abc123-def456-ghi789",
                "gift_id": "gift_001",
                "gift_name": "Wireless Bluetooth Headphones",
                "price": "$79.99",
                "description": "High-quality wireless headphones with noise cancellation",
                "user_id": "user_123",
                "timestamp": "2025-10-26T04:00:00"
            }
        }


class PaymentResponseModel(BaseModel):
    """Payment processing response model"""
    success: bool
    payment_id: str
    transaction_id: str
    amount: str
    status: str
    timestamp: str
    gift_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "payment_id": "abc123-def456-ghi789",
                "transaction_id": "txn_a5e9de06",
                "amount": "$79.99",
                "status": "completed",
                "timestamp": "2025-10-26T04:00:00",
                "gift_name": "Wireless Bluetooth Headphones"
            }
        }


class HealthResponseModel(BaseModel):
    """Health check response model"""
    status: str
    service: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "SantAI Payment Gateway"
            }
        }


@app.get(
    "/payment/{payment_id}", 
    response_class=HTMLResponse,
    summary="Display Payment Page",
    description="Shows a Stripe-style checkout page with dummy card and address details pre-filled",
    responses={
        200: {"description": "Payment page HTML"},
        404: {"description": "Payment request not found"}
    }
)
async def payment_page(
    request: Request, 
    payment_id: str = Path(..., description="Unique payment request ID", example="abc123-def456-ghi789")
):
    """
    Display payment page with dummy Stripe checkout
    
    - **payment_id**: Unique identifier for the payment request
    - Returns HTML page with pre-filled dummy data:
        - Card: 4242 4242 4242 4242
        - Expiry: 12/25
        - CVC: 123
        - Name: John Doe
        - Address: 123 Main Street, San Francisco, CA 94105
    """
    
    # Get payment request
    payment_request = payment_service.get_payment_request(payment_id)
    if not payment_request:
        raise HTTPException(status_code=404, detail="Payment request not found")
    
    # Extract price value for processing
    price_value = payment_service._extract_price_value(payment_request.price)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "payment_request": payment_request,
        "price_value": price_value,
        "payment_id": payment_id
    })


@app.post(
    "/process-payment/{payment_id}",
    summary="Process Payment",
    description="Processes the payment and redirects to success page",
    responses={
        303: {"description": "Redirect to success page"},
        404: {"description": "Payment request not found"},
        400: {"description": "Payment processing failed"}
    }
)
async def process_payment(
    payment_id: str = Path(..., description="Unique payment request ID", example="abc123-def456-ghi789")
):
    """
    Process payment and redirect to success page
    
    - **payment_id**: Unique identifier for the payment request
    - Simulates payment processing with dummy data
    - Redirects to order confirmation page on success
    """
    
    # Get payment request
    payment_request = payment_service.get_payment_request(payment_id)
    if not payment_request:
        raise HTTPException(status_code=404, detail="Payment request not found")
    
    # Process payment
    result = payment_service.process_payment(payment_id)
    
    if result["success"]:
        # Redirect to success page
        return RedirectResponse(url=f"/payment-success/{payment_id}", status_code=303)
    else:
        raise HTTPException(status_code=400, detail=result.get("error", "Payment failed"))


@app.get(
    "/payment-success/{payment_id}", 
    response_class=HTMLResponse,
    summary="Order Confirmation Page",
    description="Shows order placed successfully page with transaction details",
    responses={
        200: {"description": "Order confirmation page HTML"},
        404: {"description": "Payment request not found"}
    }
)
async def payment_success(
    request: Request, 
    payment_id: str = Path(..., description="Unique payment request ID", example="abc123-def456-ghi789")
):
    """
    Display payment success page with order confirmation
    
    - **payment_id**: Unique identifier for the payment request
    - Shows transaction details and order information
    - Displays celebration animations and next steps
    """
    
    # Get payment request
    payment_request = payment_service.get_payment_request(payment_id)
    if not payment_request:
        raise HTTPException(status_code=404, detail="Payment request not found")
    
    # Process payment to get transaction details
    result = payment_service.process_payment(payment_id)
    
    return templates.TemplateResponse("payment_success.html", {
        "request": request,
        "payment_request": payment_request,
        "transaction": result
    })


@app.get(
    "/health",
    response_model=HealthResponseModel,
    summary="Health Check",
    description="Check if the payment gateway service is running",
    responses={
        200: {"description": "Service is healthy", "model": HealthResponseModel}
    }
)
async def health_check():
    """
    Health check endpoint for monitoring service status
    
    Returns the current status of the SantAI Payment Gateway service.
    """
    return {"status": "healthy", "service": "SantAI Payment Gateway"}


@app.get(
    "/api/payment/{payment_id}",
    response_model=PaymentRequestModel,
    summary="Get Payment Request",
    description="Retrieve payment request details by ID",
    responses={
        200: {"description": "Payment request details", "model": PaymentRequestModel},
        404: {"description": "Payment request not found"}
    }
)
async def get_payment_request(
    payment_id: str = Path(..., description="Unique payment request ID", example="abc123-def456-ghi789")
):
    """
    Get payment request details by ID
    
    - **payment_id**: Unique identifier for the payment request
    - Returns payment request information in JSON format
    """
    payment_request = payment_service.get_payment_request(payment_id)
    if not payment_request:
        raise HTTPException(status_code=404, detail="Payment request not found")
    
    return payment_request.to_dict()


@app.post(
    "/api/process-payment/{payment_id}",
    response_model=PaymentResponseModel,
    summary="Process Payment (API)",
    description="Process payment and return transaction details",
    responses={
        200: {"description": "Payment processed successfully", "model": PaymentResponseModel},
        404: {"description": "Payment request not found"},
        400: {"description": "Payment processing failed"}
    }
)
async def process_payment_api(
    payment_id: str = Path(..., description="Unique payment request ID", example="abc123-def456-ghi789")
):
    """
    Process payment via API and return transaction details
    
    - **payment_id**: Unique identifier for the payment request
    - Returns transaction details in JSON format
    - Simulates payment processing with dummy data
    """
    payment_request = payment_service.get_payment_request(payment_id)
    if not payment_request:
        raise HTTPException(status_code=404, detail="Payment request not found")
    
    result = payment_service.process_payment(payment_id)
    
    if result["success"]:
        return result
    else:
        raise HTTPException(status_code=400, detail=result.get("error", "Payment failed"))


@app.post(
    "/api/create-test-payment",
    response_model=PaymentRequestModel,
    summary="Create Test Payment",
    description="Create a test payment request for Swagger UI testing",
    responses={
        200: {"description": "Test payment created successfully", "model": PaymentRequestModel}
    }
)
async def create_test_payment():
    """
    Create a test payment request for Swagger UI testing
    
    - Creates a sample gift with dummy data
    - Returns payment request details in JSON format
    - Use the returned payment_id to test other endpoints
    """
    # Sample gift data
    gift_data = {
        "id": "swagger_test_gift",
        "name": "Swagger Test Gift",
        "price": "$99.99",
        "description": "A test gift for Swagger UI testing",
        "source": "Test Store",
        "rating": 5.0
    }
    
    # Create payment request
    user_id = "swagger_test_user"
    payment_url = payment_service.create_payment_link(gift_data, user_id)
    
    # Get the payment ID from the URL
    payment_id = payment_url.split("/")[-1]
    
    # Get the payment request
    payment_request = payment_service.get_payment_request(payment_id)
    
    return payment_request.to_dict()


if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    import os
    os.makedirs("templates", exist_ok=True)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
