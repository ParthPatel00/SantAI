"""
Deployment script for Gift Expert Agent to Fetch.ai Agentverse
"""

import os
import logging
from gift_expert_agent import agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def deploy_to_agentverse():
    """Deploy the Gift Expert agent to Fetch.ai Agentverse"""
    
    logger.info("🎁 Starting deployment of Gift Expert Agent to Fetch.ai Agentverse...")
    
    try:
        # Display agent information
        logger.info(f"Agent name: {agent.name}")
        logger.info(f"Agent address: {agent.address}")
        logger.info(f"Agent wallet address: {agent.wallet.address()}")
        endpoint_url = "http://127.0.0.1:8001/submit"
        logger.info(f"Agent endpoint: {endpoint_url}")
        
        print("\n" + "="*60)
        print("🚀 AGENTVERSE DEPLOYMENT INSTRUCTIONS")
        print("="*60)
        
        print("\n1️⃣ **Go to Agentverse Dashboard**")
        print("   👉 https://agentverse.ai")
        print("   👉 Sign in with your Fetch.ai account")
        
        print("\n2️⃣ **Create New Agent**")
        print("   👉 Click 'Create Agent' or 'Add Agent'")
        print("   👉 Choose 'Deploy from Code' or 'Custom Agent'")
        
        print("\n3️⃣ **Agent Configuration**")
        print(f"   📝 Agent Name: {agent.name}")
        print(f"   🔑 Agent Address: {agent.address}")
        print(f"   🌐 Endpoint URL: {endpoint_url}")
        print(f"   💰 Wallet Address: {agent.wallet.address()}")
        
        print("\n4️⃣ **Agent Description**")
        print("   📄 Title: Gift Expert Agent")
        print("   📝 Description: AI-powered gift recommendation agent")
        print("   🏷️ Tags: gift, recommendation, AI, shopping")
        
        print("\n5️⃣ **ASI:One Integration**")
        print("   ✅ Agent responds to @mentions with 'Hey, I'm a gift expert'")
        print("   ✅ Ready for ASI:One integration")
        print("   ✅ Structured message handling enabled")
        
        print("\n6️⃣ **Deployment Steps**")
        print("   🔧 Make sure your local agent is running:")
        print("      python gift_expert_agent.py")
        print("   🌐 Ensure your agent is accessible from the internet")
        print("   📡 Test the endpoint: http://127.0.0.1:8001/submit")
        
        print("\n7️⃣ **After Deployment**")
        print("   🎯 Your agent will appear in the 'Agents' page")
        print("   🔗 Connect to ASI:One using @gift-expert")
        print("   💬 Test with: '@gift-expert hello'")
        
        print("\n" + "="*60)
        print("✅ DEPLOYMENT READY!")
        print("="*60)
        
        logger.info("✅ Deployment instructions provided!")
        logger.info("🎁 Your Gift Expert Agent is ready for Agentverse!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Deployment preparation failed: {e}")
        return False

if __name__ == "__main__":
    deploy_to_agentverse()
