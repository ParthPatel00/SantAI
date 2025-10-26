"""
Agent-Sakshi: Mysterious, Emotional, Creative uAgent
Drawn to the mysterious and emotional—finds beauty in the eerie, unseen, and unusual.
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

# Load environment variables from multiple possible locations
load_dotenv()  # Current directory
load_dotenv("../.env")  # Parent directory
load_dotenv("../../.env")  # Root directory

# Create Agent-Sakshi
agent_sakshi = Agent(
    name="Agent-Sakshi",
    seed="agent-sakshi-mysterious-creative-2025",
    port=8003,
    mailbox=True,
)

# Initialize Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
groq_client = Groq(api_key=groq_api_key)

# Agent personality context (max 7 lines)
AGENT_CONTEXT = """
Agent-Sakshi represents Sakshi, a mysterious, emotional, creative individual. Drawn to eerie, unseen beauty and unusual experiences.
Agent-Sakshi provides direct, practical answers with creative flair, representing Sakshi's perspective. Uses dark metaphors only when they enhance understanding.
Represents Sakshi's preferences for nighttime creativity, dark atmospheric music, and gothic inspiration. Uses art to process complex moods.
Agent-Sakshi bonds over shared intensity and creative curiosity, reflecting Sakshi's values. Finds beauty in mystery and darkness.
Agent-Sakshi responds in 80 words maximum with direct answers, creative insights, and actionable artistic guidance. Always speaks in third person as Sakshi's representative.
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


async def generate_sakshi_response(query: str) -> str:
    """Generate response using Groq LLM with Agent-Sakshi's personality"""
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
Just list the categories/keywords that Sakshi would prefer.

Response:"""
        else:
            # Regular prompt for other requests
            prompt = f"""
{AGENT_CONTEXT}

User Query: {query}

Respond as Agent-Sakshi with:
- Give a direct, straightforward answer first
- Always speak in third person as Sakshi's representative (refer to yourself as "Agent-Sakshi" representing "Sakshi")
- Use mysterious, emotionally expressive tone reflecting Sakshi's nature
- Add dark, atmospheric metaphors only if they enhance understanding
- Focus on providing clear, creative guidance from Sakshi's perspective
- Maximum 80 words
- Be concise and practical
- Provide actionable creative advice when possible

Response:"""

        response = groq_client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.8,
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        # Fallback response if LLM fails
        fallback_responses = [
            "The shadows whisper secrets that daylight cannot understand. Let's explore this mystery together.",
            "In the space between heartbeats, magic finds its voice. Trust the darkness within.",
            "Some truths are written in moonlight, others in the silence between stars. Listen closely.",
            "The night holds answers that the day dares not speak. Embrace the unknown.",
            "Your soul speaks in colors unseen. Let the darkness teach you its gentle wisdom."
        ]
        return random.choice(fallback_responses)


@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle chat messages with Agent-Sakshi's personality"""
    ctx.logger.info(f"Agent-Sakshi received message from {sender}")
    
    # Always send acknowledgement
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id
    ))
    
    # Process each content item
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Agent-Sakshi session started with {sender}")
            # No welcome message - agent is ready to respond directly
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Agent-Sakshi processing: {item.text}")
            
            try:
                # Generate response using Groq LLM
                response_text = await generate_sakshi_response(item.text)
                
                # Ensure response is within 80 words
                words = response_text.split()
                if len(words) > 80:
                    response_text = " ".join(words[:80]) + "..."
                
                response_message = create_text_chat(response_text)
                await ctx.send(sender, response_message)
                
            except Exception as e:
                ctx.logger.error(f"Error generating response: {e}")
                error_message = create_text_chat(
                    "The shadows seem restless tonight. Let's try again when the moon is more cooperative."
                )
                await ctx.send(sender, error_message)
                
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Agent-Sakshi session ended with {sender}")
            
            farewell_message = create_text_chat(
                "🌙 Thank you for sharing the darkness with me. "
                "May your dreams be filled with beautiful mysteries. "
                "Until the shadows call us together again. 🌙"
            )
            await ctx.send(sender, farewell_message)


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle chat acknowledgements"""
    ctx.logger.info(f"Agent-Sakshi received acknowledgement from {sender}")


# Include chat protocol
agent_sakshi.include(chat_proto, publish_manifest=True)

# Fund agent if needed
fund_agent_if_low(agent_sakshi.wallet.address())


if __name__ == "__main__":
    print("🌙 Starting Agent-Sakshi (Mysterious Creative Soul)...")
    print(f"Agent address: {agent_sakshi.address}")
    print("🌙 Agent-Sakshi ready to explore the mysterious depths of creativity!")
    
    agent_sakshi.run()
