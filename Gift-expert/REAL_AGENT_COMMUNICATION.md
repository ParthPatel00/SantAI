# 🤖 Real Agent-to-Agent Communication Setup

## Overview

This document explains how to set up real agent-to-agent communication for the SantAI gift-sending system. Instead of hardcoded responses, the system now communicates with actual personality agents to get real preferences.

## Architecture

```
User: "Send @devam a gift"
    ↓
SantAI Agent
    ↓ (GiftPreferencesRequest)
Devam's Personality Agent
    ↓ (GiftPreferencesResponse)
SantAI Agent
    ↓ (Amazon API call with real preferences)
Amazon Products
    ↓
User sees personalized gifts
```

## Setup Instructions

### 1. **Start Devam's Personality Agent**

First, start Devam's personality agent in a separate terminal:

```bash
cd /Users/parthpatel/frontend/CalHacks/SantAI/Gift-expert
python example_personality_agent.py
```

This will start Devam's agent and show you its address (e.g., `agent1q0k6srkjt3meajrqhnd3y5d5js50a3ml2u63k78vnvkxpvn2ufrh6p603pt`).

### 2. **Update Agent Registration**

Update the agent registration in `agent_communication.py` with the real agent address:

```python
# Replace the placeholder addresses with real ones
agent_communication.register_agent("devam", "ACTUAL_DEVAM_AGENT_ADDRESS")
agent_communication.register_agent("parth", "ACTUAL_PARTH_AGENT_ADDRESS")
agent_communication.register_agent("sakshi", "ACTUAL_SAKSHI_AGENT_ADDRESS")
```

### 3. **Start SantAI Agent**

Start the main SantAI agent:

```bash
python agent.py
```

### 4. **Test the Communication**

Now when you say `"Send @devam a gift"`, the system will:

1. **Send a real message** to Devam's personality agent
2. **Wait for a real response** with his actual preferences
3. **Use those preferences** to search Amazon for suitable gifts
4. **Return personalized recommendations** based on his real interests

## Communication Protocol

### Message Types

#### `GiftPreferencesRequest`

Sent by SantAI to ask for gift preferences:

```python
GiftPreferencesRequest(
    from_agent="santa_clause",
    recipient="devam",
    timestamp="2025-01-27T10:00:00Z",
    request="What would you like as a gift? Please share your interests, preferences, and any gift ideas."
)
```

#### `GiftPreferencesResponse`

Sent by personality agent with preferences:

```python
GiftPreferencesResponse(
    username="devam",
    interests=["technology", "gaming", "coffee", "programming"],
    personality="tech-savvy, creative, loves gadgets",
    gift_preferences="tech gadgets, programming books, coffee accessories",
    budget_range="$25-100",
    occasion="just because",
    specific_requests="something that helps with coding"
)
```

#### `GiftSentNotification`

Sent by SantAI when a gift is selected:

```python
GiftSentNotification(
    from_agent="santa_clause",
    recipient="devam",
    gift_name="Wireless Gaming Headset",
    gift_price="$45.99",
    gift_description="High-quality gaming headset",
    gift_url="https://amazon.com/...",
    timestamp="2025-01-27T10:00:00Z"
)
```

## Creating Custom Personality Agents

### Template for New Personality Agent

```python
from uagents import Agent, Context, Protocol
from gift_communication_protocol import (
    GiftPreferencesRequest,
    GiftPreferencesResponse,
    GiftSentNotification,
    GiftAcknowledgment
)

# Create the personality agent
personality_agent = Agent(
    name="Person-Name-Personality",
    seed="person-name-personality-seed",
    port=8002,  # Use different port
    mailbox=True,
)

gift_protocol = Protocol("gift_communication")

@gift_protocol.on_message(GiftPreferencesRequest)
async def handle_gift_preferences_request(ctx: Context, sender: str, msg: GiftPreferencesRequest):
    # Define the person's preferences
    response = GiftPreferencesResponse(
        username="person_name",
        interests=["interest1", "interest2", "interest3"],
        personality="personality description",
        gift_preferences="specific gift preferences",
        budget_range="$25-100",
        occasion="just because",
        specific_requests="what they specifically want"
    )

    await ctx.send(sender, response)

# Include protocol and run
personality_agent.include(gift_protocol, publish_manifest=True)
personality_agent.run()
```

## Testing the System

### 1. **Start Both Agents**

Terminal 1 (Personality Agent):

```bash
python example_personality_agent.py
```

Terminal 2 (SantAI Agent):

```bash
python agent.py
```

### 2. **Test Commands**

Try these commands in the SantAI interface:

- `"Send @devam a gift"`
- `"Can you send @devam a gift?"`
- `"@santa clause, send a gift to '@devam'"`

### 3. **Expected Flow**

1. SantAI detects the gift-sending command
2. SantAI sends `GiftPreferencesRequest` to Devam's agent
3. Devam's agent responds with `GiftPreferencesResponse`
4. SantAI uses those preferences to search Amazon
5. SantAI presents personalized gift recommendations
6. User selects a gift
7. SantAI sends `GiftSentNotification` to Devam's agent
8. Devam's agent acknowledges with `GiftAcknowledgment`

## Troubleshooting

### Common Issues

1. **Agent not found**: Make sure the personality agent is running and registered
2. **Timeout**: Check network connectivity and agent addresses
3. **Protocol errors**: Ensure both agents are using the same protocol version

### Debug Steps

1. Check agent addresses are correct
2. Verify both agents are running
3. Check logs for communication errors
4. Test with simple messages first

## Production Deployment

### Agent Discovery

In production, you would use:

- **Agent Registry**: Central service to find agent addresses
- **Service Discovery**: Automatic discovery of running agents
- **Load Balancing**: Multiple instances of personality agents

### Security

- **Authentication**: Verify agent identities
- **Encryption**: Encrypt sensitive communication
- **Rate Limiting**: Prevent spam requests

## Benefits of Real Agent Communication

1. **Dynamic Preferences**: Each person's agent can have different, evolving preferences
2. **Real-time Updates**: Preferences can change based on recent interests
3. **Personalized Responses**: Each agent can have unique personality and preferences
4. **Scalable**: Easy to add new people by creating their personality agents
5. **Realistic**: Mimics how real people would respond to gift requests

## Next Steps

1. **Create more personality agents** for different people
2. **Add preference learning** so agents get smarter over time
3. **Implement agent discovery** for automatic registration
4. **Add authentication** for secure communication
5. **Create agent management dashboard** for easy setup

This system now provides **real agent-to-agent communication** instead of hardcoded responses! 🎁✨
