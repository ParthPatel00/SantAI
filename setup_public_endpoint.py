"""
Setup script to make your agent publicly accessible using ngrok
"""

import subprocess
import time
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_public_endpoint():
    """Set up ngrok tunnel to make agent publicly accessible"""
    
    print("\n" + "="*60)
    print("🌐 SETTING UP PUBLIC ENDPOINT")
    print("="*60)
    
    print("\n📋 **Steps to Make Your Agent Publicly Accessible:**")
    
    print("\n1️⃣ **Start Your Agent** (in one terminal):")
    print("   python gift_expert_agent.py")
    
    print("\n2️⃣ **Create Public Tunnel** (in another terminal):")
    print("   ngrok http 8001")
    
    print("\n3️⃣ **Get Public URL:**")
    print("   • ngrok will show a public URL like: https://abc123.ngrok.io")
    print("   • Use this URL as your endpoint in Agentverse")
    print("   • Example: https://abc123.ngrok.io/submit")
    
    print("\n4️⃣ **Register with Agentverse:**")
    print("   • Go to https://agentverse.ai")
    print("   • Use the ngrok URL as your endpoint")
    print("   • Agent Address: agent1qgfvp4ks356mxug5qcgg7mwfl8tql3vkv6r6sqspt4yp49ghanuayhdhnwn")
    
    print("\n🔧 **Alternative: Use Agentverse Hosting**")
    print("   • Some platforms offer direct hosting")
    print("   • Look for 'Deploy to Cloud' options")
    print("   • Upload your agent code directly")
    
    print("\n⚠️ **Important Notes:**")
    print("   • Keep both your agent AND ngrok running")
    print("   • ngrok URLs change when you restart")
    print("   • For production, use a permanent hosting solution")
    
    print("\n" + "="*60)
    print("✅ READY TO SET UP PUBLIC ACCESS!")
    print("="*60)

def test_ngrok_connection():
    """Test if ngrok is working"""
    try:
        # Check if ngrok is running
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('tunnels'):
                tunnel = data['tunnels'][0]
                public_url = tunnel['public_url']
                print(f"\n🌐 **Public URL Found:** {public_url}")
                print(f"📡 **Use this endpoint:** {public_url}/submit")
                return public_url
    except:
        pass
    
    print("\n❌ **ngrok not running yet**")
    print("   • Start your agent: python gift_expert_agent.py")
    print("   • In another terminal: ngrok http 8001")
    return None

if __name__ == "__main__":
    setup_public_endpoint()
    print("\n🧪 **Testing ngrok connection...**")
    test_ngrok_connection()
