"""
Programmatic Agent Registration with Agentverse
"""

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment_variables():
    """Set up the required environment variables"""
    
    print("\n" + "="*60)
    print("🔧 ENVIRONMENT VARIABLES SETUP")
    print("="*60)
    
    print("\n📋 **Required Environment Variables:**")
    
    print("\n1️⃣ **AGENTVERSE_KEY**")
    print("   • Go to: https://agentverse.ai")
    print("   • Sign in to your account")
    print("   • Go to your profile/settings")
    print("   • Look for 'API Keys' or 'Developer Settings'")
    print("   • Create a new API key")
    print("   • Copy the API key")
    
    print("\n2️⃣ **AGENT_SEED_PHRASE**")
    print("   • Use your agent's seed phrase:")
    print("   • gift-expert-seed-2025-parth-sakshi-devam")
    
    print("\n🔧 **Set Environment Variables:**")
    print("   Option 1 - Export in terminal:")
    print("   export AGENTVERSE_KEY='your_api_key_here'")
    print("   export AGENT_SEED_PHRASE='gift-expert-seed-2025-parth-sakshi-devam'")
    
    print("\n   Option 2 - Create .env file:")
    print("   Create a .env file with:")
    print("   AGENTVERSE_KEY=your_api_key_here")
    print("   AGENT_SEED_PHRASE=gift-expert-seed-2025-parth-sakshi-devam")
    
    print("\n📝 **Complete Registration Code:**")
    print("""
import os
from fetchai.registration import register_chat_agent, RegistrationRequestCredentials

# Make sure environment variables are set
register_chat_agent(
    "Gift Expert",  # Agent name
    "https://geostatic-sang-hoverfly.ngrok-free.dev/submit",  # Your ngrok URL
    active=True,
    credentials=RegistrationRequestCredentials(
        agentverse_api_key=os.environ["AGENTVERSE_KEY"],
        agent_seed_phrase=os.environ["AGENT_SEED_PHRASE"],
    ),
)
""")
    
    print("\n🎯 **Your Specific Values:**")
    print("   • Agent Name: 'Gift Expert'")
    print("   • Endpoint: 'https://geostatic-sang-hoverfly.ngrok-free.dev/submit'")
    print("   • Agent Seed: 'gift-expert-seed-2025-parth-sakshi-devam'")
    print("   • API Key: [Get from Agentverse dashboard]")
    
    print("\n" + "="*60)
    print("✅ READY FOR PROGRAMMATIC REGISTRATION!")
    print("="*60)

def create_registration_script():
    """Create the complete registration script"""
    
    script_content = '''"""
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
'''
    
    with open("register_agent_complete.py", "w") as f:
        f.write(script_content)
    
    print("\n📁 **Created: register_agent_complete.py**")
    print("   Run with: python register_agent_complete.py")

if __name__ == "__main__":
    setup_environment_variables()
    create_registration_script()
