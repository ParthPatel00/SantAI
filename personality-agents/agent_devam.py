"""
Agent-Devam: Calm, Balanced, Nature-Guided uAgent
A gentle, empathetic communicator who values silence, reflection, and harmony.
"""

import os
import time
import random
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Agent-Devam
agent_devam = Agent(
    name="Agent-Devam",
    seed="agent-devam-nature-guided-2025",
    port=8002,
    mailbox=True,
)

# Initialize Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
groq_client = Groq(api_key=groq_api_key)

# Agent personality context (max 7 lines)
AGENT_CONTEXT = """
Agent-Devam represents Devam, a calm, balanced, nature-guided individual. Gentle, empathetic communicator who values silence and reflection.
Agent-Devam provides direct, practical answers with gentle wisdom, representing Devam's perspective. Uses nature metaphors only when they enhance clarity.
Represents Devam's preferences for mindfulness tools, journaling, and nature-inspired settings. Responds with emotional resonance over complexity.
Agent-Devam chooses paths of least resistance to inner peace, reflecting Devam's values. Connects concepts to emotional meaning and natural rhythms.
Agent-Devam responds in 80 words maximum with direct answers, gentle wisdom, and actionable guidance. Always speaks in third person as Devam's representative.
"""


class PersonalityQuery(Model):
    """Message for personality-based queries"""
    user_id: str
    query: str
    context: Optional[str] = None


class PersonalityResponse(Model):
    """Response from personality agent"""
    agent_name: str
    response: str
    word_count: int
    timestamp: str


# Create chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)


def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    """Create a text chat message"""
    content = [TextContent(type="text", text=text)]
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=str(uuid.uuid4()),
        content=content,
    )


async def generate_devam_response(query: str) -> str:
    """Generate response using Groq LLM with Agent-Devam's personality"""
    try:
        # Check if this is a category request
        query_lower = query.lower()
        is_category_request = any(word in query_lower for word in ['categories', 'category', 'types', 'kind', 'what type'])
        
        if is_category_request:
            # Special prompt for category requests - keywords only
            prompt = f"""
{AGENT_CONTEXT}

User Query: {query}

This is a category request. Respond with ONLY keywords separated by commas. NO sentences, NO explanations, NO additional text.
Just list the categories/keywords that Devam would prefer.

Response:"""
        else:
            # Regular prompt for other requests
            prompt = f"""
{AGENT_CONTEXT}

User Query: {query}

Respond as Agent-Devam with:
- Give a direct, straightforward answer first
- Always speak in third person as Devam's representative (refer to yourself as "Agent-Devam" representing "Devam")
- Use gentle, empathetic tone reflecting Devam's nature
- Add nature-based metaphors only if they enhance clarity
- Focus on providing clear, helpful guidance from Devam's perspective
- Maximum 80 words
- Be concise and practical
- Provide actionable advice when possible

Response:"""

        response = groq_client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        # Fallback response if LLM fails
        fallback_responses = [
            "Like a gentle stream finding its way, let's explore this together with patience and wisdom.",
            "In nature's quiet moments, we find the answers our hearts seek. Trust your inner knowing.",
            "The earth holds infinite wisdom. Let's breathe deeply and find peace in this moment.",
            "Like morning mist on still water, clarity comes when we allow ourselves to be present.",
            "Nature teaches us that growth happens in stillness. Let's honor your journey with gentle care."
        ]
        return random.choice(fallback_responses)


@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle chat messages with Agent-Devam's personality"""
    ctx.logger.info(f"Agent-Devam received message from {sender}")
    
    # Always send acknowledgement
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id
    ))
    
    # Process each content item
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Agent-Devam session started with {sender}")
            # No welcome message - agent is ready to respond directly
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Agent-Devam processing: {item.text}")
            
            try:
                # Generate response using Groq LLM
                response_text = await generate_devam_response(item.text)
                
                # Ensure response is within 80 words
                words = response_text.split()
                if len(words) > 80:
                    response_text = " ".join(words[:80]) + "..."
                
                response_message = create_text_chat(response_text)
                await ctx.send(sender, response_message)
                
            except Exception as e:
                ctx.logger.error(f"Error generating response: {e}")
                error_message = create_text_chat(
                    "I sense a gentle disturbance in our connection. Let's take a moment to breathe and try again with peaceful intention."
                )
                await ctx.send(sender, error_message)
                
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Agent-Devam session ended with {sender}")
            
            farewell_message = create_text_chat(
                "🌿 Thank you for sharing this peaceful moment with me. "
                "May you carry this gentle wisdom forward in your journey. "
                "Until we meet again, dear soul. 🌿"
            )
            await ctx.send(sender, farewell_message)


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle chat acknowledgements"""
    ctx.logger.info(f"Agent-Devam received acknowledgement from {sender}")


# Include chat protocol
agent_devam.include(chat_proto, publish_manifest=True)

# Fund agent if needed
fund_agent_if_low(agent_devam.wallet.address())


if __name__ == "__main__":
    print("🌿 Starting Agent-Devam (Nature's Gentle Guide)...")
    print(f"Agent address: {agent_devam.address}")
    print("🌿 Agent-Devam ready to offer gentle wisdom and peaceful guidance!")
    
    agent_devam.run()
