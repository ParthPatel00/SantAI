"""
Fix agent registration with proper API key
"""

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_agent_registration():
    """Fix agent registration with proper API key"""
    
    print("\n" + "="*60)
    print("🔧 FIXING AGENT REGISTRATION")
    print("="*60)
    
    print("\n❌ **Current Issue:**")
    print("   • 403 Forbidden error from Agentverse")
    print("   • 'Could not validate credentials' warning")
    print("   • ASI:One can't access your agent")
    
    print("\n🔑 **Solution: Get Real API Key**")
    print("   1. Go to https://agentverse.ai")
    print("   2. Sign in to your account")
    print("   3. Go to your profile/settings")
    print("   4. Look for 'API Keys' or 'Developer Settings'")
    print("   5. Create a new API key")
    print("   6. Copy the API key")
    
    print("\n🔧 **Steps to Fix:**")
    print("   1. Get your real API key from Agentverse")
    print("   2. Set it as environment variable:")
    print("      export AGENTVERSE_KEY='your_real_api_key_here'")
    print("   3. Re-register your agent:")
    print("      python launch_agent_script.py")
    
    print("\n🎯 **Alternative: Manual Registration**")
    print("   1. Go to https://agentverse.ai")
    print("   2. Look for 'Create Agent' or 'Add Agent'")
    print("   3. Use these details:")
    print("      • Agent Name: Gift Expert")
    print("      • Agent Address: agent1qgfvp4ks356mxug5qcgg7mwfl8tql3vkv6r6sqspt4yp49ghanuayhdhnwn")
    print("      • Endpoint: https://geostatic-sang-hoverfly.ngrok-free.dev/submit")
    print("      • Wallet: fetch18w99uw73n56mktqxp2248lmsesppmyzl4sfvdn")
    
    print("\n🧪 **Test After Fix:**")
    print("   1. Make sure your HTTP agent is running")
    print("   2. Test with ASI:One: @gift-expert hello")
    print("   3. Should respond: 'Hey, I'm a gift expert'")
    
    print("\n" + "="*60)
    print("✅ READY TO FIX REGISTRATION!")
    print("="*60)

if __name__ == "__main__":
    fix_agent_registration()
