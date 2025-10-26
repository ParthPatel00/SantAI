# 🔍 SantAI Payment Gateway - Swagger UI

## 🎯 **Swagger UI Access**

Your SantAI Payment Gateway now includes **Swagger UI** for interactive API documentation and testing!

### 📋 **Access URLs**

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **Health Check**: http://localhost:8001/health

## 🚀 **Getting Started**

1. **Start the Payment Server**:
   ```bash
   python payment_server.py
   ```

2. **Open Swagger UI**: Navigate to http://localhost:8001/docs in your browser

3. **Explore the API**: You'll see all available endpoints with detailed documentation

## 🔧 **Available Endpoints**

### **HTML Endpoints** (User Interface)
- `GET /payment/{payment_id}` - Display Stripe-style checkout page
- `POST /process-payment/{payment_id}` - Process payment and redirect
- `GET /payment-success/{payment_id}` - Show order confirmation page

### **API Endpoints** (JSON Responses)
- `GET /api/payment/{payment_id}` - Get payment request details
- `POST /api/process-payment/{payment_id}` - Process payment via API
- `GET /health` - Health check endpoint

## 🧪 **Testing with Swagger UI**

### **Step 1: Create a Test Payment**
```bash
python create_swagger_test.py
```

This will generate a payment ID you can use for testing.

### **Step 2: Test in Swagger UI**

1. **Open** http://localhost:8001/docs
2. **Expand** any endpoint (click on it)
3. **Click** "Try it out"
4. **Enter** the payment ID from step 1
5. **Click** "Execute"
6. **View** the response

### **Step 3: Test All Endpoints**

Try these endpoints in order:

1. **Health Check** (`GET /health`)
   - No parameters needed
   - Should return: `{"status":"healthy","service":"SantAI Payment Gateway"}`

2. **Get Payment Request** (`GET /api/payment/{payment_id}`)
   - Use the payment ID from `create_swagger_test.py`
   - Returns payment details in JSON format

3. **Process Payment** (`POST /api/process-payment/{payment_id}`)
   - Use the same payment ID
   - Returns transaction details

## 🎨 **Swagger UI Features**

### **Interactive Documentation**
- **Try it out**: Test endpoints directly in the browser
- **Request/Response Examples**: See expected data formats
- **Parameter Descriptions**: Understand what each parameter does
- **Response Codes**: See all possible response types

### **API Models**
- **PaymentRequestModel**: Structure of payment request data
- **PaymentResponseModel**: Structure of payment response data
- **HealthResponseModel**: Structure of health check response

### **Example Data**
All endpoints include example data:
- Payment ID: `abc123-def456-ghi789`
- Gift Name: `Wireless Bluetooth Headphones`
- Price: `$79.99`
- Transaction ID: `txn_a5e9de06`

## 🔍 **API Documentation Details**

### **Payment Request Model**
```json
{
  "payment_id": "abc123-def456-ghi789",
  "gift_id": "gift_001",
  "gift_name": "Wireless Bluetooth Headphones",
  "price": "$79.99",
  "description": "High-quality wireless headphones with noise cancellation",
  "user_id": "user_123",
  "timestamp": "2025-10-26T04:00:00"
}
```

### **Payment Response Model**
```json
{
  "success": true,
  "payment_id": "abc123-def456-ghi789",
  "transaction_id": "txn_a5e9de06",
  "amount": "$79.99",
  "status": "completed",
  "timestamp": "2025-10-26T04:00:00",
  "gift_name": "Wireless Bluetooth Headphones"
}
```

## 🛒 **Complete Payment Flow**

1. **SantAI generates gift recommendations** with buy links
2. **User clicks "Buy Now"** → Goes to `/payment/{payment_id}`
3. **User completes payment form** → Submits to `/process-payment/{payment_id}`
4. **Payment processed** → Redirects to `/payment-success/{payment_id}`
5. **Order confirmation displayed** → Shows transaction details

## 🎉 **Success!**

Your SantAI Payment Gateway now has:

✅ **Swagger UI** for interactive API documentation  
✅ **ReDoc** for alternative documentation view  
✅ **Complete API testing** capabilities  
✅ **Detailed endpoint documentation**  
✅ **Request/Response examples**  
✅ **Interactive testing** in the browser  

**Open http://localhost:8001/docs to start exploring!**
