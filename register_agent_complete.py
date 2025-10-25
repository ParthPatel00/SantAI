"""
Complete Agent Registration Script
"""

import os
from fetchai.registration import register_chat_agent, RegistrationRequestCredentials

def register_gift_expert_agent():
    """Register the Gift Expert agent with Agentverse"""
    
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
        # Register the agent
        result = register_chat_agent(
            "Gift Expert",  # Agent name
            "https://geostatic-sang-hoverfly.ngrok-free.dev/submit",  # Your ngrok URL
            active=True,
            credentials=RegistrationRequestCredentials(
                agentverse_api_key=os.environ["AGENTVERSE_KEY"],
                agent_seed_phrase=os.environ["AGENT_SEED_PHRASE"],
            ),
        )
        
        print("✅ Agent registered successfully!")
        print(f"   Agent Name: Gift Expert")
        print(f"   Endpoint: https://geostatic-sang-hoverfly.ngrok-free.dev/submit")
        print(f"   Status: Active")
        
        return True
        
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return False

if __name__ == "__main__":
    register_gift_expert_agent()
