# 🎁 Gift Expert Agent - Fetch.ai uAgents

An AI-powered gift recommendation agent built with Fetch.ai's uAgents framework, designed for ASI:One integration. This agent responds to @mentions with "Hey, I'm a gift expert" and provides smart gift recommendations.

## 🌟 Features

- **ASI:One Integration**: Responds to @mentions with "Hey, I'm a gift expert"
- **Smart Gift Recommendations**: AI-powered suggestions based on multiple criteria
- **HTTP-based Architecture**: FastAPI server for ASI:One compatibility
- **Flexible Message Handling**: Handles any message format from ASI:One
- **Real-time Processing**: Instant responses to gift queries
- **ngrok Integration**: Public access via secure tunnel

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get API Key

1. Go to [agentverse.ai](https://agentverse.ai)
2. Sign in to your account
3. Go to Profile/Settings → API Keys
4. Create a new API key
5. Copy the key

### 3. Set Environment Variables

```bash
# Set your real API key
export AGENTVERSE_KEY='your_real_api_key_here'
export AGENT_SEED_PHRASE='gift-expert-seed-2025-parth-sakshi-devam'
```

### 4. Start the Agent

```bash
# Start the HTTP-based agent (recommended for ASI:One)
python http_gift_agent.py
```

### 5. Setup ngrok Tunnel

```bash
# Install ngrok (if not already installed)
brew install ngrok/ngrok/ngrok

# Start ngrok tunnel
ngrok http 8001
```

### 6. Register with Agentverse

```bash
# Register agent programmatically
python launch_agent_script.py
```

### 7. Test with ASI:One

1. Go to [ASI:One](https://asi1.ai)
2. Send: `@gift-expert hello`
3. Expected response: "Hey, I'm a gift expert"

## 📁 Project Structure

- `http_gift_agent.py` - **Main HTTP-based agent (ASI:One compatible)**
- `gift_expert_agent.py` - Original uAgents-based agent
- `launch_agent_script.py` - Programmatic registration with Agentverse
- `deploy_gift_agent.py` - Manual deployment instructions
- `fix_registration.py` - Troubleshooting script for registration issues
- `context.txt` - Project context and current status
- `requirements.txt` - Python dependencies
- `README.md` - This documentation

## 🔧 Current Architecture

### HTTP Agent (Recommended)

- **File**: `http_gift_agent.py`
- **Framework**: FastAPI + Uvicorn
- **Port**: 8001
- **Endpoints**: `/submit` and `/`
- **Compatibility**: ASI:One optimized

### uAgents Agent (Alternative)

- **File**: `gift_expert_agent.py`
- **Framework**: Fetch.ai uAgents
- **Port**: 8001
- **Endpoint**: `/submit`
- **Compatibility**: Standard uAgents protocol

## 🎯 Agent Capabilities

### ASI:One Integration

- **@mentions**: Responds with "Hey, I'm a gift expert"
- **Gift queries**: Provides smart recommendations
- **Empty messages**: Responds with default greeting
- **Any format**: Handles various message formats

### Message Types Supported

1. **@mentions**: ASI:One integration

   - "@gift-expert hello" → "Hey, I'm a gift expert"

2. **Gift Queries**: Natural language requests

   - "I need help with gifts"
   - "What should I get for my friend's birthday?"

3. **Structured Requests**: Detailed specifications
   ```python
   GiftRequest(
       recipient_age=25,
       recipient_gender="female",
       occasion="birthday",
       budget_range="$50-100",
       interests=["tech", "fashion"],
       relationship="friend"
   )
   ```

### Gift Categories

- **Technology**: Wireless earbuds, smart watches, speakers
- **Books**: Novels, coffee table books, cookbooks
- **Fashion**: Scarves, wallets, jewelry
- **Experiences**: Spa days, cooking classes, concerts
- **Home**: Smart devices, art prints, plants

## 🔧 Configuration

### Agent Details

- **Agent Name**: gift-expert
- **Address**: agent1qgfvp4ks356mxug5qcgg7mwfl8tql3vkv6r6sqspt4yp49ghanuayhdhnwn
- **Wallet**: fetch18w99uw73n56mktqxp2248lmsesppmyzl4sfvdn
- **Port**: 8001
- **Seed**: gift-expert-seed-2025-parth-sakshi-devam

### Environment Variables

```bash
export AGENTVERSE_KEY='your_real_api_key_here'
export AGENT_SEED_PHRASE='gift-expert-seed-2025-parth-sakshi-devam'
```

### HTTP Agent Configuration

```python
# http_gift_agent.py
uvicorn.run(app, host="127.0.0.1", port=8001)
```

### uAgents Agent Configuration

```python
# gift_expert_agent.py
agent = Agent(
    name="gift-expert",
    seed="gift-expert-seed-2025-parth-sakshi-devam",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)
```

## 🚀 Deployment to Agentverse

### Automatic Registration (Recommended)

```bash
# Set environment variables
export AGENTVERSE_KEY='your_real_api_key_here'
export AGENT_SEED_PHRASE='gift-expert-seed-2025-parth-sakshi-devam'

# Register agent programmatically
python launch_agent_script.py
```

### Manual Registration

1. Go to [Agentverse](https://agentverse.ai)
2. Sign in to your account
3. Look for "Create Agent" or "Add Agent"
4. Use these details:
   - **Agent Name**: Gift Expert
   - **Agent Address**: agent1qgfvp4ks356mxug5qcgg7mwfl8tql3vkv6r6sqspt4yp49ghanuayhdhnwn
   - **Endpoint**: https://geostatic-sang-hoverfly.ngrok-free.dev/submit
   - **Wallet**: fetch18w99uw73n56mktqxp2248lmsesppmyzl4sfvdn

### Troubleshooting

If you get 403 Forbidden errors:

1. Get a real API key from agentverse.ai
2. Update the AGENTVERSE_KEY environment variable
3. Re-run the registration script
4. Check the `fix_registration.py` script for detailed instructions

## 🧪 Testing

### Local Testing

```bash
# Test HTTP agent locally
curl -X POST http://127.0.0.1:8001/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "@gift-expert hello"}'

# Test ngrok endpoint
curl -X POST https://geostatic-sang-hoverfly.ngrok-free.dev/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "@gift-expert hello"}'
```

### ASI:One Testing

1. Go to [ASI:One](https://asi1.ai)
2. Send: `@gift-expert hello`
3. Expected response: "Hey, I'm a gift expert"

### Test Scripts

- `test_gift_agent.py` - Test uAgents agent functionality
- `test_mention.py` - Test @mention functionality
- `test_gift_agent.py` - Test gift recommendation logic

## 🎁 Example Usage

### ASI:One Integration

```
User: @gift-expert hello
Agent: Hey, I'm a gift expert
```

### Gift Recommendations

```
User: I need a gift for my friend's birthday
Agent: 🎁 I'd love to help you find the perfect gift! Please tell me about the recipient - their age, interests, and the occasion. You can also specify your budget range.
```

### Structured Requests

```python
# Send a gift request
request = GiftRequest(
    recipient_age=30,
    occasion="anniversary",
    budget_range="$100-200",
    interests=["tech", "experiences"]
)

# Agent will respond with:
# - 5 personalized gift recommendations
# - Reasoning for the suggestions
# - Budget considerations
```

## 🔗 Resources

- [Fetch.ai Innovation Lab](https://innovationlab.fetch.ai/resources/docs/intro)
- [uAgents Documentation](https://uagents.fetch.ai/docs)
- [Agentverse Platform](https://agentverse.ai)
- [ASI:One Platform](https://asi1.ai)
- [ngrok Documentation](https://ngrok.com/docs)

## 📋 Current Status

- ✅ **HTTP Agent**: Running on localhost:8001
- ✅ **ngrok Tunnel**: Public URL active
- ✅ **Agentverse Registration**: Agent registered
- ❌ **ASI:One Integration**: 403 Forbidden (API key issue)
- 🔧 **Next Step**: Get real API key from agentverse.ai
