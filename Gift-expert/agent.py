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
  
   # Always send back an acknowledgement when a message is received
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
           if sender in friend_agent_addresses:
               # This is a response from a friend agent
               ctx.logger.info(f"Received response from friend agent: {sender}")
               
               # Determine which friend this is based on sender address
               friend_name = None
               for name, address in friend_interface.agent_addresses.items():
                   if address == sender:
                       friend_name = name
                       break
               
               if friend_name:
                   # Determine response type based on content
                   response_text = item.text.lower()
                   if "personality" in response_text or "i am" in response_text or "my personality" in response_text:
                       friend_interface.handle_friend_response(friend_name, item.text, "personality")
                       ctx.logger.info(f"Stored personality response from {friend_name}")
                   elif "gift" in response_text or "materialistic" in response_text or "enjoy" in response_text:
                       friend_interface.handle_friend_response(friend_name, item.text, "gift_preferences")
                       ctx.logger.info(f"Stored gift preferences response from {friend_name}")
                   else:
                       # Generic response, try to determine type
                       friend_interface.handle_friend_response(friend_name, item.text, "general")
                       ctx.logger.info(f"Stored general response from {friend_name}")
               
               # Send acknowledgment
               response_message = create_text_chat("Thank you for the information! I'll use this to find the perfect gift.")
               await ctx.send(sender, response_message)
           else:
               # Regular user message
               try:
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


# Handle acknowledgements for messages this agent has sent out
@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
   ctx.logger.info(f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}")


# Include the chat protocol and publish the manifest to Agentverse
agent.include(chat_proto, publish_manifest=True)

 
if __name__ == "__main__":
    agent.run()