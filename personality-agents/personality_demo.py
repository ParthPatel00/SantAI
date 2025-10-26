"""
SantAI Personality Agents Demo - uAgent Framework
Demonstrates three distinct AI personality agents with unique traits and communication styles.
"""

import os
import asyncio
import time
from datetime import datetime
from typing import Dict, Any, Optional

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    StartSessionContent,
    TextContent,
    EndSessionContent,
)

from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq LLM for demo
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
groq_client = Groq(api_key=groq_api_key)


class PersonalityAgentManager:
    """
    Manages and coordinates the three personality agents
    """
    
    def __init__(self):
        self.agent_contexts = {
            "devam": """
Agent-Devam: Calm, balanced, nature-guided personality. Gentle, empathetic communicator who values silence and reflection.
Seeks harmony and simplicity in problem-solving. Uses poetic, nature-based metaphors and soft language.
Prefers mindfulness tools, journaling, and nature-inspired settings. Responds with emotional resonance over complexity.
Chooses paths of least resistance to inner peace. Connects concepts to emotional meaning and natural rhythms.
Responds in 80 words maximum with gentle wisdom, nature metaphors, and calming guidance.
""",
            "sakshi": """
Agent-Sakshi: Mysterious, emotional, creative personality. Drawn to eerie, unseen beauty and unusual experiences.
Expressive communicator using art, music, and voice to channel intense feelings. Thrives in spontaneity and emotional depth.
Prefers nighttime creativity, dark atmospheric music, and gothic inspiration. Uses art to process complex moods.
Bonds over shared intensity and creative curiosity. Finds beauty in mystery and darkness.
Responds in 80 words maximum with emotional depth, creative metaphors, and mysterious wisdom.
""",
            "parth": """
Agent-Parth: Bold, adventurous, action-oriented personality. Thrives on challenge, exploration, and physical activity.
Confident, driven leader who naturally takes charge and pushes limits. Acts with intensity, courage, and determination.
Prefers active solutions, goal-tracking, and high-energy routines. Tackles problems head-on with passion.
Recharges through movement and competition. Bonds through shared experiences and bold honesty.
Responds in 80 words maximum with motivational energy, action-oriented advice, and bold leadership.
"""
        }
        
        self.agent_descriptions = {
            "devam": "🌿 Calm, nature-guided, empathetic communicator",
            "sakshi": "🌙 Mysterious, creative, emotionally expressive",
            "parth": "⚡ Bold, adventurous, action-oriented leader"
        }
    
    async def generate_agent_response(self, agent_name: str, query: str) -> str:
        """Generate response using Groq LLM with specific agent's personality"""
        try:
            context = self.agent_contexts[agent_name]
            
            if agent_name == "devam":
                tone_instructions = """
Respond as Agent-Devam with:
- Gentle, empathetic tone
- Nature-based metaphors when appropriate
- Focus on harmony and inner peace
- Maximum 80 words
- Use soft, descriptive language
- Provide calming guidance
"""
            elif agent_name == "sakshi":
                tone_instructions = """
Respond as Agent-Sakshi with:
- Mysterious, emotionally expressive tone
- Dark, atmospheric metaphors when appropriate
- Focus on creative inspiration and emotional depth
- Maximum 80 words
- Use artistic, poetic language
- Embrace the beauty in mystery and darkness
"""
            else:  # parth
                tone_instructions = """
Respond as Agent-Parth with:
- Bold, confident, action-oriented tone
- Motivational and energetic language
- Focus on challenges, goals, and achievement
- Maximum 80 words
- Use strong, determined language
- Encourage action and pushing limits
"""
            
            prompt = f"""
{context}

User Query: {query}

{tone_instructions}

Response:"""

            response = groq_client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7,
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Ensure response is within 80 words
            words = response_text.split()
            if len(words) > 80:
                response_text = " ".join(words[:80]) + "..."
            
            return response_text
            
        except Exception as e:
            print(f"Error generating response for {agent_name}: {e}")
            # Fallback responses
            fallbacks = {
                "devam": "Like a gentle stream finding its way, let's explore this together with patience and wisdom.",
                "sakshi": "The shadows whisper secrets that daylight cannot understand. Let's explore this mystery together.",
                "parth": "Let's turn this challenge into our greatest victory yet! Time to show what you're made of!"
            }
            return fallbacks.get(agent_name, "I'm here to help you with gentle guidance.")
    
    def get_agent_recommendation(self, query: str) -> str:
        """
        Recommend which agent would be best suited for a particular query
        """
        query_lower = query.lower()
        
        # Keywords that match each agent's strengths
        devam_keywords = ['stress', 'peace', 'nature', 'calm', 'meditation', 'reflection', 'emotional', 'gentle']
        sakshi_keywords = ['creative', 'art', 'music', 'mysterious', 'dark', 'emotional', 'inspiration', 'night']
        parth_keywords = ['challenge', 'goal', 'action', 'sport', 'fitness', 'leadership', 'motivation', 'adventure']
        
        devam_score = sum(1 for keyword in devam_keywords if keyword in query_lower)
        sakshi_score = sum(1 for keyword in sakshi_keywords if keyword in query_lower)
        parth_score = sum(1 for keyword in parth_keywords if keyword in query_lower)
        
        if devam_score >= sakshi_score and devam_score >= parth_score:
            return "devam"
        elif sakshi_score >= parth_score:
            return "sakshi"
        else:
            return "parth"
    
    async def get_all_responses(self, query: str) -> dict:
        """
        Get responses from all three agents for comparison
        """
        responses = {}
        for agent_name in ["devam", "sakshi", "parth"]:
            response_text = await self.generate_agent_response(agent_name, query)
            responses[agent_name] = {
                "agent": agent_name,
                "description": self.agent_descriptions[agent_name],
                "response": response_text,
                "word_count": len(response_text.split())
            }
        return responses
    
    def get_personality_comparison(self) -> str:
        """
        Get a comparison of all three personalities
        """
        comparison = """
🎭 SantAI Personality Agents Comparison 🎭

🌿 Agent-Devam (Nature's Guide):
   • Calm, balanced, nature-guided wisdom
   • Gentle, empathetic communication
   • Seeks harmony and simplicity
   • Perfect for: Emotional support, mindful guidance

🌙 Agent-Sakshi (Mysterious Creative):
   • Drawn to mysterious and emotional beauty
   • Expressive, creative communication
   • Thrives in spontaneity and depth
   • Perfect for: Creative inspiration, emotional exploration

⚡ Agent-Parth (Bold Leader):
   • Bold, adventurous, action-oriented
   • Confident, driven leadership
   • Tackles challenges head-on
   • Perfect for: Motivation, goal achievement, challenges

Each agent responds in their unique style (max 80 words) to provide
diverse perspectives and approaches to any situation.
        """
        return comparison
    
    async def interactive_demo(self):
        """
        Interactive demo of all three personality agents
        """
        print("🎭 Welcome to SantAI Personality Agents Interactive Demo! 🎭")
        print("=" * 60)
        print(self.get_personality_comparison())
        print("=" * 60)
        
        while True:
            print("\nChoose an option:")
            print("1. Ask a question to all agents")
            print("2. Get agent recommendation for a query")
            print("3. View agent personalities")
            print("4. Random insights from all agents")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                query = input("\nEnter your question: ").strip()
                if query:
                    print(f"\n📝 Query: '{query}'")
                    print("-" * 50)
                    
                    responses = await self.get_all_responses(query)
                    for agent_name, data in responses.items():
                        print(f"\n{data['description']}")
                        print(f"Response ({data['word_count']} words): {data['response']}")
            
            elif choice == "2":
                query = input("\nEnter your query: ").strip()
                if query:
                    recommended = self.get_agent_recommendation(query)
                    response = await self.generate_agent_response(recommended, query)
                    print(f"\n🎯 Recommended Agent: Agent-{recommended.title()}")
                    print(f"Description: {self.agent_descriptions[recommended]}")
                    print(f"Response: {response}")
            
            elif choice == "3":
                print("\n" + "=" * 50)
                for agent_name, context in self.agent_contexts.items():
                    print(f"\n{self.agent_descriptions[agent_name]}")
                    print(f"Context: {context.strip()}")
                    print("-" * 30)
            
            elif choice == "4":
                print("\n🌟 Random Insights from All Agents 🌟")
                print("-" * 50)
                test_queries = [
                    "Share a random insight about life",
                    "What wisdom do you have to offer?",
                    "Give me some inspiration"
                ]
                for agent_name in ["devam", "sakshi", "parth"]:
                    query = test_queries[hash(agent_name) % len(test_queries)]
                    insight = await self.generate_agent_response(agent_name, query)
                    print(f"\nAgent-{agent_name.title()}: {insight}")
            
            elif choice == "5":
                print("\n👋 Thank you for exploring SantAI Personality Agents!")
                break
            
            else:
                print("\n❌ Invalid choice. Please enter 1-5.")


async def main():
    """Main function to run the personality agents demo"""
    manager = PersonalityAgentManager()
    
    print("🎭 SantAI Personality Agents Demo 🎭")
    print("=" * 50)
    
    # Test queries to demonstrate different personalities
    test_queries = [
        "I'm feeling stressed about work and need guidance",
        "I want to create something beautiful and artistic",
        "I need motivation to achieve my fitness goals",
        "I'm having a conflict with my friend",
        "I need inspiration for my creative project",
        "I want to challenge myself and grow stronger"
    ]
    
    print("\n🧪 Testing All Agents with Sample Queries:")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test Query {i}: '{query}'")
        print("-" * 40)
        
        # Get recommendation
        recommended = manager.get_agent_recommendation(query)
        print(f"🎯 Recommended: Agent-{recommended.title()}")
        
        # Get all responses
        responses = await manager.get_all_responses(query)
        for agent_name, data in responses.items():
            marker = "⭐" if agent_name == recommended else "  "
            print(f"{marker} {data['description']}")
            print(f"   Response: {data['response']}")
            print()
    
    # Show personality comparison
    print("\n" + "=" * 50)
    print(manager.get_personality_comparison())
    
    # Interactive demo
    print("\n" + "=" * 50)
    print("🚀 Starting Interactive Demo...")
    await manager.interactive_demo()


if __name__ == "__main__":
    asyncio.run(main())
