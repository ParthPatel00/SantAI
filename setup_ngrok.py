"""
Setup ngrok for local agent development
"""

import subprocess
import time
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_ngrok_guide():
    """Guide for setting up ngrok for local agent development"""
    
    print("\n" + "="*60)
    print("🔧 NGROK SETUP FOR LOCAL AGENT")
    print("="*60)
    
    print("\n📋 **Step 1: Create Free ngrok Account**")
    print("   1. Go to: https://dashboard.ngrok.com/signup")
    print("   2. Sign up for a free account")
    print("   3. Verify your email")
    
    print("\n🔑 **Step 2: Get Your Authtoken**")
    print("   1. Go to: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("   2. Copy your authtoken (looks like: 2abc123def456ghi789)")
    print("   3. Run this command:")
    print("      ngrok config add-authtoken YOUR_AUTHTOKEN_HERE")
    
    print("\n🚀 **Step 3: Start Your Agent**")
    print("   Terminal 1:")
    print("   python gift_expert_agent.py")
    
    print("\n🌐 **Step 4: Create Public Tunnel**")
    print("   Terminal 2:")
    print("   ngrok http 8001")
    
    print("\n📡 **Step 5: Get Public URL**")
    print("   • ngrok will show a URL like: https://abc123.ngrok.io")
    print("   • Copy this URL")
    print("   • Use in Agentverse: https://abc123.ngrok.io/submit")
    
    print("\n✅ **Step 6: Register with Agentverse**")
    print("   • Go to https://agentverse.ai")
    print("   • Use the ngrok URL as endpoint")
    print("   • Agent Address: agent1qgfvp4ks356mxug5qcgg7mwfl8tql3vkv6r6sqspt4yp49ghanuayhdhnwn")
    
    print("\n🔧 **Alternative: Use Different Tunnel Service**")
    print("   If ngrok doesn't work, try:")
    print("   • Cloudflare Tunnel (free)")
    print("   • LocalTunnel (free)")
    print("   • Serveo (free)")
    
    print("\n📚 **Additional Libraries Support**")
    print("   ✅ You can install any Python library you need:")
    print("   pip install requests numpy pandas scikit-learn")
    print("   pip install openai anthropic")
    print("   pip install any-other-library")
    
    print("\n" + "="*60)
    print("🎯 READY FOR LOCAL DEVELOPMENT!")
    print("="*60)

def test_ngrok_status():
    """Test if ngrok is working"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('tunnels'):
                tunnel = data['tunnels'][0]
                public_url = tunnel['public_url']
                print(f"\n🌐 **ngrok is running!**")
                print(f"📡 **Public URL:** {public_url}")
                print(f"🔗 **Use this endpoint:** {public_url}/submit")
                return public_url
    except:
        pass
    
    print("\n❌ **ngrok not running yet**")
    print("   Follow the setup steps above")
    return None

if __name__ == "__main__":
    setup_ngrok_guide()
    print("\n🧪 **Testing ngrok status...**")
    test_ngrok_status()
