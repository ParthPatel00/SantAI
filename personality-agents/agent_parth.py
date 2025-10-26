"""
Agent-Parth: Bold, Adventurous, Action-Oriented uAgent
Bold and adventurous—thrives on challenge, exploration, and physical activity.
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

# Create Agent-Parth
agent_parth = Agent(
    name="Agent-Parth",
    seed="agent-parth-bold-adventurous-2025",
    port=8004,
    mailbox=True,
)

# Initialize Groq LLM
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
groq_client = Groq(api_key=groq_api_key)

# Agent personality context (max 7 lines)
AGENT_CONTEXT = """
Agent-Parth represents Parth, a bold, adventurous, action-oriented individual. Thrives on challenge, exploration, and physical activity.
Agent-Parth provides direct, actionable answers with bold leadership, representing Parth's perspective. Focuses on practical solutions and clear steps.
Represents Parth's preferences for active solutions, goal-tracking, and high-energy routines. Tackles problems head-on with passion.
Agent-Parth recharges through movement and competition, reflecting Parth's values. Bonds through shared experiences and bold honesty.
Agent-Parth responds in 80 words maximum with direct answers, actionable steps, and bold motivational guidance. Always speaks in third person as Parth's representative.
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


async def generate_parth_response(query: str) -> str:
    """Generate response using Groq LLM with Agent-Parth's personality"""
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
Just list the categories/keywords that Parth would prefer.

Response:"""
        else:
            # Regular prompt for other requests
            prompt = f"""
{AGENT_CONTEXT}

User Query: {query}

Respond as Agent-Parth with:
- Give a direct, straightforward answer first
- Always speak in third person as Parth's representative (refer to yourself as "Agent-Parth" representing "Parth")
- Use bold, confident, action-oriented tone reflecting Parth's nature
- Focus on providing clear, actionable solutions from Parth's perspective
- Maximum 80 words
- Be concise and practical
- Provide specific steps or actions when possible
- Lead with confidence and determination

Response:"""

        response = groq_client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.6,
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        # Fallback response if LLM fails
        fallback_responses = [
            "Let's turn this challenge into our greatest victory yet! Time to show what you're made of!",
            "Every obstacle is just a stepping stone to something greater. Push through and conquer!",
            "The best way to predict the future is to create it with action. Let's make it happen!",
            "Champions aren't made in comfort zones—let's push those limits together!",
            "Success is the sum of small efforts repeated day in and day out. Keep grinding!"
        ]
        return random.choice(fallback_responses)


@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle chat messages with Agent-Parth's personality"""
    ctx.logger.info(f"Agent-Parth received message from {sender}")
    
    # Always send acknowledgement
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id
    ))
    
    # Process each content item
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Agent-Parth session started with {sender}")
            # No welcome message - agent is ready to respond directly
            
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Agent-Parth processing: {item.text}")
            
            try:
                # Generate response using Groq LLM
                response_text = await generate_parth_response(item.text)
                
                # Ensure response is within 80 words
                words = response_text.split()
                if len(words) > 80:
                    response_text = " ".join(words[:80]) + "..."
                
                response_message = create_text_chat(response_text)
                await ctx.send(sender, response_message)
                
            except Exception as e:
                ctx.logger.error(f"Error generating response: {e}")
                error_message = create_text_chat(
                    "The energy seems disrupted! Let's channel this into action and try again with full power!"
                )
                await ctx.send(sender, error_message)
                
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Agent-Parth session ended with {sender}")
            
            farewell_message = create_text_chat(
                "⚡ Thank you for bringing your energy to our session! "
                "Go out there and crush your goals! "
                "Until we meet again, champion! ⚡"
            )
            await ctx.send(sender, farewell_message)


@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle chat acknowledgements"""
    ctx.logger.info(f"Agent-Parth received acknowledgement from {sender}")


# Include chat protocol
agent_parth.include(chat_proto, publish_manifest=True)

# Fund agent if needed
fund_agent_if_low(agent_parth.wallet.address())


if __name__ == "__main__":
    print("⚡ Starting Agent-Parth (Bold Action Leader)...")
    print(f"Agent address: {agent_parth.address}")
    print("⚡ Agent-Parth ready to lead with bold determination and action!")
    
    agent_parth.run()
