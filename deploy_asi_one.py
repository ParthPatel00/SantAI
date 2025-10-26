"""
ASI.one Deployment Script for SantAI Payment Integration
This script helps you deploy and test your SantAI agent with payment integration on ASI.one
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path


def check_asi_one_setup():
    """Check if ASI.one setup is ready"""
    print("🔍 Checking ASI.one Setup...")
    
    try:
        # Check if uagents is installed
        import uagents
        print("✅ uagents framework installed")
    except ImportError:
        print("❌ uagents not installed. Run: pip install uagents")
        return False
    
    # Check if agent.py exists
    agent_path = Path("Gift-expert/agent.py")
    if agent_path.exists():
        print("✅ SantAI agent found")
    else:
        print("❌ SantAI agent not found at Gift-expert/agent.py")
        return False
    
    # Check if payment files exist
    payment_files = [
        "payment_server.py",
        "payment_service.py", 
        "templates/index.html",
        "templates/payment_success.html"
    ]
    
    for file in payment_files:
        if Path(file).exists():
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            return False
    
    return True


def test_payment_server():
    """Test payment server locally"""
    print("\n🧪 Testing Payment Server...")
    
    try:
        # Start payment server in background
        print("Starting payment server...")
        payment_process = subprocess.Popen([
            sys.executable, "payment_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:8001/health", timeout=5)
            if response.status_code == 200:
                print("✅ Payment server is running")
                print("✅ Health check passed")
                return payment_process
            else:
                print(f"❌ Health check failed: {response.status_code}")
                payment_process.terminate()
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to payment server: {e}")
            payment_process.terminate()
            return None
            
    except Exception as e:
        print(f"❌ Failed to start payment server: {e}")
        return None


def test_agent_deployment():
    """Test agent deployment to ASI.one"""
    print("\n🤖 Testing Agent Deployment...")
    
    try:
        # Change to Gift-expert directory
        os.chdir("Gift-expert")
        
        # Start agent (this will publish to ASI.one)
        print("Starting SantAI agent...")
        print("This will publish your agent to ASI.one (Agentverse)")
        print("Look for the agent address in the output")
        
        # Run agent
        agent_process = subprocess.Popen([
            sys.executable, "agent.py"
        ])
        
        print("✅ Agent started successfully")
        print("📋 Agent should now be available on ASI.one")
        print("🔗 Check ASI.one dashboard for your agent")
        
        return agent_process
        
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")
        return None


def create_test_commands():
    """Create test commands for ASI.one"""
    print("\n📝 Test Commands for ASI.one:")
    print("=" * 50)
    
    test_commands = [
        "Send me gift recommendations",
        "I need a gift for my friend's birthday",
        "What gifts do you recommend for Christmas?",
        "Show me some tech gifts",
        "I want to buy a gift for my mom"
    ]
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"{i}. \"{cmd}\"")
    
    print("\n💡 Expected Results:")
    print("• Agent should respond with gift recommendations")
    print("• Each recommendation should include a 'Buy Now' link")
    print("• Buy links should redirect to payment pages")
    print("• Payment pages should have dummy data pre-filled")
    print("• Order processing should work end-to-end")


def show_deployment_urls():
    """Show important URLs for testing"""
    print("\n🌐 Important URLs:")
    print("=" * 30)
    print("• ASI.one Dashboard: https://asi.one/dashboard")
    print("• Payment Server: http://localhost:8001")
    print("• Swagger UI: http://localhost:8001/docs")
    print("• Health Check: http://localhost:8001/health")
    print("• Payment Test: http://localhost:8001/api/create-test-payment")


def main():
    """Main deployment function"""
    print("🚀 SantAI Payment Integration - ASI.one Deployment")
    print("=" * 60)
    
    # Check setup
    if not check_asi_one_setup():
        print("\n❌ Setup check failed. Please fix the issues above.")
        return
    
    print("\n✅ Setup check passed!")
    
    # Test payment server
    payment_process = test_payment_server()
    if not payment_process:
        print("\n❌ Payment server test failed.")
        return
    
    # Show URLs
    show_deployment_urls()
    
    # Create test commands
    create_test_commands()
    
    print("\n🎯 Next Steps:")
    print("1. Test payment server in browser: http://localhost:8001/docs")
    print("2. Start SantAI agent: cd Gift-expert && python agent.py")
    print("3. Test agent on ASI.one with the commands above")
    print("4. Verify buy links work in gift recommendations")
    print("5. Test complete payment flow")
    
    print("\n⌨️  Press Ctrl+C to stop services")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        if payment_process:
            payment_process.terminate()
        print("✅ Services stopped")


if __name__ == "__main__":
    main()
