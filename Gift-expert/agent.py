from uagents import Agent, Context, Model, Protocol
from datetime import datetime, timezone
from uuid import uuid4
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import (
   ChatAcknowledgement,
   ChatMessage,
   EndSessionContent,
   StartSessionContent,
   TextContent,
   chat_protocol_spec,
)

# Import our custom modules
from conversation_flow import ConversationFlowManager
from global_memory import global_memory
from models import ConversationState
from friend_interface import friend_interface


agent = Agent(
    name="Gift-Expert",
    seed="agent-seed-2025-parth-new",
    port=8000,
    mailbox=True,
)

# Initialize conversation flow manager
conversation_manager = ConversationFlowManager()


# Initialize the chat protocol with the standard chat spec
chat_proto = Protocol(spec=chat_protocol_spec)


# Utility function to wrap plain text into a ChatMessage
def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=content,
        )


# Handle incoming chat messages
@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
   ctx.logger.info(f"Received message from {sender}")
  
   # Check if this is a friend agent before sending acknowledgment
   friend_agent_addresses = list(friend_interface.agent_addresses.values())
   if sender not in friend_agent_addresses:
       # Only send acknowledgment to regular users, not friend agents
       await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.now(timezone.utc), acknowledged_msg_id=msg.msg_id))

   # Process each content item inside the chat message
   for item in msg.content:
       # Marks the start of a chat session
       if isinstance(item, StartSessionContent):
           ctx.logger.info(f"Session started with {sender}")
           # Initialize conversation for new user
           response_message = create_text_chat(
               "🎁 Welcome to the Gift Expert Agent! I'm here to help you find the perfect gift.\n\n"
               "To get started, please tell me:\n"
               "• What's the occasion? (birthday, anniversary, holiday, etc.)\n"
               "• What are your preferences? (colors, brands, interests, etc.)\n"
               "• What's your budget range?\n\n"
               "Just tell me about the gift you're looking for and I'll help you find it!"
           )
           await ctx.send(sender, response_message)
      
       # Handles plain text messages (from another agent or ASI:One)
       elif isinstance(item, TextContent):
           ctx.logger.info(f"Text message from {sender}: {item.text}")
           
           # Check if this is a response from a friend agent
           friend_agent_addresses = list(friend_interface.agent_addresses.values())
           ctx.logger.info(f"🔍 DEBUG: Checking if sender {sender} is in friend addresses: {friend_agent_addresses}")
           
           # Log all incoming messages for debugging
           ctx.logger.info(f"🔍 DEBUG: Received message from {sender} with content: {item.text[:100]}...")
           
           # Check specifically for Parth's agent
           if sender == "agent1q0ammultdzelux7l6u72wnwh8ze8ne6wmsqfu4dygkah8ada2gqhqyrnzsf":
               ctx.logger.info(f"🔍 DEBUG: This is Parth's agent! Processing message...")
               ctx.logger.info(f"🔍 DEBUG: Parth's message content: {item.text}")
           
           # Log any message that contains "parth" in the content
           if "parth" in item.text.lower():
               ctx.logger.info(f"🔍 DEBUG: Message contains 'parth': {item.text[:100]}...")
           
           if sender in friend_agent_addresses:
               # This is a response from a friend agent
               ctx.logger.info(f"Received response from friend agent: {sender}")
               
               # Determine which friend this is based on sender address
               friend_name = None
               for name, address in friend_interface.agent_addresses.items():
                   if address == sender:
                       friend_name = name
                       break
               
                    # Process all responses from friend agents
               
               if friend_name:
                   
                   # Determine response type based on content
                   response_text = item.text.lower()
                   
                   # Classify responses by content, not order
                   friend_name_lower = friend_name.lower()
                   
                   # Determine if this is personality or preferences based on content
                   response_text = item.text.lower()
                   is_personality_response = (
                       "personality" in response_text or 
                       "represents" in response_text or
                       "spirit" in response_text or
                       "character" in response_text or
                       "nature" in response_text or
                       len(item.text) > 100  # Longer responses are usually personality
                   )
                   
                   is_preferences_response = (
                       "sports" in response_text or
                       "gear" in response_text or
                       "equipment" in response_text or
                       "tools" in response_text or
                       "activities" in response_text or
                       "experiences" in response_text or
                       len(item.text) < 100  # Shorter responses are usually preferences
                   )
                   
                   ctx.logger.info(f"🔍 DEBUG: {friend_name} - Is personality: {is_personality_response}, Is preferences: {is_preferences_response}")
                   
                   if is_personality_response and not (friend_name_lower in friend_interface.personality and friend_interface.personality[friend_name_lower] is not None):
                       # Store as personality
                       friend_interface.store_personality(friend_name, item.text)
                       ctx.logger.info(f"Stored personality response from {friend_name}")
                   elif is_preferences_response and not (friend_name_lower in friend_interface.preferences and friend_interface.preferences[friend_name_lower] is not None):
                       # Store as preferences and call Amazon API
                       amazon_result = await friend_interface.store_preferences(friend_name, item.text)
                       ctx.logger.info(f"Stored preferences response from {friend_name}")
                       
                       # Send Amazon results to user if we got them
                       if amazon_result:
                           amazon_message = create_text_chat(amazon_result)
                           # Send to original user, not the friend agent
                           if friend_interface.original_user:
                               await ctx.send(friend_interface.original_user, amazon_message)
                               ctx.logger.info(f"🔍 DEBUG: Sent Amazon results to original user: {friend_interface.original_user}")
                           else:
                               ctx.logger.info(f"🔍 DEBUG: No original user found, cannot send Amazon results")
                   else:
                       # Already have this type or unclear classification
                       ctx.logger.info(f"Already have this response type from {friend_name} or unclear classification")
               
               # Don't send acknowledgment to friend agents to avoid spam loops
               continue
           else:
               # Regular user message
               try:
                   # Store the original user address for gift requests
                   if any(name in item.text.lower() for name in ["devam", "parth", "sakshi"]):
                       friend_interface.original_user = sender
                       ctx.logger.info(f"🔍 DEBUG: Stored original user address: {sender}")
                   
                   # Process user input through conversation flow with context
                   response_text = await conversation_manager.process_user_input(sender, item.text, ctx)
                   
                   # Create and send response
                   response_message = create_text_chat(response_text)
                   await ctx.send(sender, response_message)
                   
               except Exception as e:
                   ctx.logger.error(f"Error processing message: {str(e)}")
                   error_message = create_text_chat(
                       "I apologize, but I encountered an error processing your request. "
                       "Please try again or rephrase your message."
                   )
                   await ctx.send(sender, error_message)

       # Marks the end of a chat session
       elif isinstance(item, EndSessionContent):
           ctx.logger.info(f"Session ended with {sender}")
           # Clean up user data if needed
           # global_memory.clear_user_data(sender)  # Uncomment if you want to clear data on session end
       
       # Catches anything unexpected
       else:
           ctx.logger.info(f"Received unexpected content type from {sender}")
           ctx.logger.info(f"🔍 DEBUG: Unexpected content type: {type(item)}")
           ctx.logger.info(f"🔍 DEBUG: Content: {item}")


# Handle acknowledgements for messages this agent has sent out
@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
   ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")


# Include the chat protocol and publish the manifest to Agentverse
agent.include(chat_proto, publish_manifest=True)

# Add a startup delay to prevent immediate communication
@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info("🎁 Gift Expert Agent is starting up...")
    ctx.logger.info("⏳ Waiting 5 seconds to prevent startup communication...")
    import asyncio
    await asyncio.sleep(5)
    ctx.logger.info("✅ Agent is ready to receive messages!")

 
if __name__ == "__main__":
    agent.run()