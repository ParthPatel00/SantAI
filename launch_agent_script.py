"""
Launch Agent Script - Exact code from Agentverse page
"""

import os
from uagents_core.utils.registration import (
    register_chat_agent,
    RegistrationRequestCredentials,
)

def launch_gift_expert_agent():
    """Launch the Gift Expert agent into Agentverse"""
    
    print("🚀 Launching Gift Expert Agent into Agentverse...")
    
    # Check if environment variables are set
    if not os.environ.get("AGENTVERSE_KEY"):
        print("❌ AGENTVERSE_KEY not found!")
        print("   Set it with: export AGENTVERSE_KEY='your_api_key_here'")
        return False
    
    if not os.environ.get("AGENT_SEED_PHRASE"):
        print("❌ AGENT_SEED_PHRASE not found!")
        print("   Set it with: export AGENT_SEED_PHRASE='gift-expert-seed-2025-parth-sakshi-devam'")
        return False
    
    try:
        # Register the agent using the exact code from Agentverse
        result = register_chat_agent(
            "Gift Expert",
            "https://geostatic-sang-hoverfly.ngrok-free.dev/submit",
            active=True,
            credentials=RegistrationRequestCredentials(
                agentverse_api_key=os.environ["AGENTVERSE_KEY"],
                agent_seed_phrase=os.environ["AGENT_SEED_PHRASE"],
            ),
        )
        
        print("✅ Agent launched successfully!")
        print("   🎁 Gift Expert is now registered in Agentverse")
        print("   🌐 Endpoint: https://geostatic-sang-hoverfly.ngrok-free.dev/submit")
        print("   🔗 Ready for ASI:One integration with @gift-expert")
        
        return True
        
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        print("   Make sure your agent is running and ngrok is active")
        return False

if __name__ == "__main__":
    launch_gift_expert_agent()
