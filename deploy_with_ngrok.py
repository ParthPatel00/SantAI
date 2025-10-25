"""
Deploy Gift Expert Agent with ngrok public URL
"""

import json
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ngrok_url():
    """Get the public ngrok URL"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('tunnels'):
                tunnel = data['tunnels'][0]
                public_url = tunnel['public_url']
                return public_url
    except Exception as e:
        logger.error(f"Error getting ngrok URL: {e}")
    return None

def deploy_with_ngrok():
    """Deploy agent with ngrok public URL"""
    
    print("\n" + "="*60)
    print("🚀 DEPLOYING WITH NGROK PUBLIC URL")
    print("="*60)
    
    # Get the ngrok URL
    ngrok_url = get_ngrok_url()
    
    if ngrok_url:
        print(f"\n🌐 **Public URL Found:** {ngrok_url}")
        print(f"📡 **Endpoint URL:** {ngrok_url}/submit")
        
        print("\n📋 **Agent Information for Agentverse:**")
        print(f"   🔑 Agent Name: gift-expert")
        print(f"   📍 Agent Address: agent1qgfvp4ks356mxug5qcgg7mwfl8tql3vkv6r6sqspt4yp49ghanuayhdhnwn")
        print(f"   🌐 Endpoint URL: {ngrok_url}/submit")
        print(f"   💰 Wallet Address: fetch18w99uw73n56mktqxp2248lmsesppmyzl4sfvdn")
        
        print("\n✅ **Next Steps:**")
        print("1️⃣ Go to https://agentverse.ai")
        print("2️⃣ Sign in to your account")
        print("3️⃣ Look for 'Create Agent' or 'Deploy Agent'")
        print("4️⃣ Use the information above")
        print("5️⃣ Test with ASI:One using @gift-expert")
        
        print("\n🧪 **Test Your Agent:**")
        print(f"   • Visit: {ngrok_url}")
        print("   • Should show your agent is running")
        print("   • Ready for Agentverse registration!")
        
        print("\n⚠️ **Important Notes:**")
        print("   • Keep both your agent AND ngrok running")
        print("   • ngrok URL changes when you restart")
        print("   • For production, consider hosted deployment")
        
        print("\n" + "="*60)
        print("✅ READY FOR AGENTVERSE DEPLOYMENT!")
        print("="*60)
        
        return ngrok_url
    else:
        print("\n❌ **ngrok not running or accessible**")
        print("   • Make sure ngrok is running: ngrok http 8001")
        print("   • Check if your agent is running: python gift_expert_agent.py")
        print("   • Verify ngrok authentication is working")
        return None

if __name__ == "__main__":
    deploy_with_ngrok()
