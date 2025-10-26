"""
Deployment script for SantAI with Payment Integration
Starts both the main agent and payment server
"""

import subprocess
import sys
import os
import time
import signal
from threading import Thread


def start_payment_server():
    """Start the payment server in a separate process"""
    print("🚀 Starting Payment Server...")
    try:
        # Start payment server
        payment_process = subprocess.Popen([
            sys.executable, "payment_server.py"
        ], cwd=os.getcwd())
        
        print("✅ Payment Server started on http://localhost:8001")
        return payment_process
    except Exception as e:
        print(f"❌ Failed to start payment server: {e}")
        return None


def start_main_agent():
    """Start the main SantAI agent"""
    print("🚀 Starting SantAI Agent...")
    try:
        # Change to Gift-expert directory
        agent_dir = os.path.join(os.getcwd(), "Gift-expert")
        if not os.path.exists(agent_dir):
            print(f"❌ Gift-expert directory not found: {agent_dir}")
            return None
        
        # Start main agent
        agent_process = subprocess.Popen([
            sys.executable, "agent.py"
        ], cwd=agent_dir)
        
        print("✅ SantAI Agent started")
        return agent_process
    except Exception as e:
        print(f"❌ Failed to start main agent: {e}")
        return None


def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "jinja2"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install fastapi uvicorn jinja2")
        return False
    
    print("✅ All dependencies are installed")
    return True


def main():
    """Main deployment function"""
    print("🎁 SantAI with Payment Integration - Deployment Script")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Start payment server
    payment_process = start_payment_server()
    if not payment_process:
        return
    
    # Wait a moment for payment server to start
    time.sleep(2)
    
    # Start main agent
    agent_process = start_main_agent()
    if not agent_process:
        payment_process.terminate()
        return
    
    print("\n🎉 Both services started successfully!")
    print("\n📋 Service URLs:")
    print("   • SantAI Agent: Check your agent configuration")
    print("   • Payment Server: http://localhost:8001")
    print("   • Health Check: http://localhost:8001/health")
    
    print("\n🛒 Payment Integration Features:")
    print("   • Buy links in gift recommendations")
    print("   • Stripe-style payment page with dummy data")
    print("   • Order processing and confirmation")
    print("   • Secure payment flow simulation")
    
    print("\n⌨️  Press Ctrl+C to stop both services")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if payment_process.poll() is not None:
                print("❌ Payment server stopped unexpectedly")
                break
            
            if agent_process.poll() is not None:
                print("❌ Main agent stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        
        # Terminate processes
        if payment_process:
            payment_process.terminate()
            print("✅ Payment server stopped")
        
        if agent_process:
            agent_process.terminate()
            print("✅ Main agent stopped")
        
        print("👋 All services stopped. Goodbye!")


if __name__ == "__main__":
    main()
