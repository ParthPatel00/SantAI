"""
Register Gift Expert Agent with Agentverse Marketplace
"""

import os
import logging
from gift_expert_agent import agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_with_agentverse():
    """Register the gift-expert agent with Agentverse marketplace"""
    
    print("\n" + "="*60)
    print("📝 AGENTVERSE REGISTRATION INSTRUCTIONS")
    print("="*60)
    
    print("\n🔑 **Required Information:**")
    print(f"   Agent Name: {agent.name}")
    print(f"   Agent Address: {agent.address}")
    print(f"   Wallet Address: {agent.wallet.address()}")
    print(f"   Endpoint: http://127.0.0.1:8001/submit")
    
    print("\n📋 **Registration Steps:**")
    print("1️⃣ Go to https://agentverse.ai")
    print("2️⃣ Sign in to your account")
    print("3️⃣ Look for one of these options:")
    print("   • 'Register Agent' button")
    print("   • 'Add Agent' button") 
    print("   • 'Deploy Agent' button")
    print("   • 'Publish Agent' button")
    print("   • 'Create Agent' → 'From Code'")
    
    print("\n📝 **Agent Details to Enter:**")
    print(f"   • Agent Name: {agent.name}")
    print(f"   • Agent Address: {agent.address}")
    print(f"   • Endpoint URL: http://127.0.0.1:8001/submit")
    print(f"   • Wallet Address: {agent.wallet.address()}")
    print("   • Title: Gift Expert Agent")
    print("   • Description: AI-powered gift recommendation agent")
    print("   • Tags: gift, recommendation, AI, shopping")
    
    print("\n🔧 **Before Registration:**")
    print("   ✅ Make sure your agent is running: python gift_expert_agent.py")
    print("   ✅ Keep it running during registration")
    print("   ✅ Test locally first")
    
    print("\n🎯 **After Registration:**")
    print("   • Your agent will appear in the 'Agents' tab")
    print("   • It will be discoverable in the marketplace")
    print("   • You can test it with ASI:One using @gift-expert")
    
    print("\n" + "="*60)
    print("✅ READY FOR REGISTRATION!")
    print("="*60)
    
    logger.info("Registration instructions provided!")
    return True

if __name__ == "__main__":
    register_with_agentverse()
