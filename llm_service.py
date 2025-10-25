"""
LLM Service for Gift Agent using Groq
Handles all LLM interactions and prompt management
"""

import os
from typing import List, Dict, Any, Optional
from groq import Groq
import json
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LLMService:
    def __init__(self):
        """Initialize the LLM service with Groq client"""
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key or api_key == "your-groq-api-key-here":
            raise ValueError(
                "GROQ_API_KEY not found! Please:\n"
                "1. Get your API key from https://console.groq.com/keys\n"
                "2. Create a .env file with: GROQ_API_KEY=your_actual_key_here\n"
                "3. Make sure .env is in your project root directory"
            )
        
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")  # Use model from env or default
    
    async def get_occasion_and_preferences(self, user_input: str) -> Dict[str, Any]:
        """
        Extract occasion, preferences, and budget from user input
        Handles abstract and conversational inputs intelligently
        """
        prompt = f"""
        You are an intelligent gift recommendation assistant. Analyze the user's input and extract information, even if it's abstract or conversational.
        
        User Input: "{user_input}"
        
        Guidelines:
        - Be flexible in interpreting abstract inputs (e.g., "something nice for mom" → occasion: "general gift", preferences: "for mother")
        - Infer context from conversational cues (e.g., "for my girlfriend" → occasion: "romantic gift", preferences: "for girlfriend")
        - Extract budget hints even if not explicit (e.g., "not too expensive" → budget: "affordable", "something fancy" → budget: "premium")
        - Consider seasonal context (e.g., "for Christmas" → occasion: "Christmas", "holiday gift")
        - Handle incomplete information gracefully
        
        Return a JSON object with:
        - occasion: The occasion for the gift (birthday, anniversary, holiday, graduation, romantic, general, etc.)
        - preferences: Any specific preferences mentioned (colors, brands, interests, recipient type, etc.)
        - budget: Budget range mentioned or inferred (affordable, moderate, premium, specific range, etc.)
        - missing_info: List of information that still needs to be collected
        - confidence: Your confidence level in the extracted information (high/medium/low)
        
        Examples:
        - "I need something for my mom's birthday" → {{"occasion": "birthday", "preferences": "for mother", "budget": null, "missing_info": ["preferences", "budget"], "confidence": "medium"}}
        - "Looking for a romantic gift under $100" → {{"occasion": "romantic", "preferences": "romantic", "budget": "under $100", "missing_info": ["specific preferences"], "confidence": "high"}}
        - "Something cool for my tech-savvy friend" → {{"occasion": "general", "preferences": "tech-related", "budget": null, "missing_info": ["occasion", "budget"], "confidence": "medium"}}
        
        Return only valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Debug: Print the raw response
            raw_response = response.choices[0].message.content
            print(f"DEBUG: Raw LLM response: {raw_response}")
            
            # Clean the response - remove markdown code blocks if present
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]  # Remove ```json
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]   # Remove ```
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]  # Remove trailing ```
            
            # Find JSON object in the response
            json_start = cleaned_response.find('{')
            json_end = cleaned_response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_response[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                # Fallback: try to parse the whole cleaned response
                result = json.loads(cleaned_response)
                return result
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON decode error: {e}")
            print(f"DEBUG: Raw response was: {raw_response}")
            return {
                "occasion": None,
                "preferences": None,
                "budget": None,
                "missing_info": ["occasion", "preferences", "budget"],
                "confidence": "low"
            }
        except Exception as e:
            print(f"DEBUG: General error: {e}")
            return {
                "occasion": None,
                "preferences": None,
                "budget": None,
                "missing_info": ["occasion", "preferences", "budget"],
                "confidence": "low"
            }
    
    async def get_gift_categories(self, occasion: str, preferences: str, budget: str) -> List[str]:
        """
        Generate relevant gift categories based on occasion, preferences, and budget
        """
        prompt = f"""
        Based on the following information, suggest 6-8 relevant gift categories:
        
        Occasion: {occasion}
        Preferences: {preferences}
        Budget: {budget}
        
        Return a JSON array of category names. Categories should be specific and relevant.
        Examples: "Electronics", "Books", "Jewelry", "Home Decor", "Sports Equipment", "Art & Crafts", "Fashion Accessories", "Kitchen Gadgets"
        
        Return only the JSON array, no other text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            # Clean the response - remove markdown code blocks if present
            raw_response = response.choices[0].message.content
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]  # Remove ```json
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]   # Remove ```
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]  # Remove trailing ```
            
            # Find JSON array in the response
            json_start = cleaned_response.find('[')
            json_end = cleaned_response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_response[json_start:json_end]
                categories = json.loads(json_str)
            else:
                # Fallback: try to parse the whole cleaned response
                categories = json.loads(cleaned_response)
            
            # Ensure all categories are strings
            if isinstance(categories, list):
                return [str(cat) for cat in categories]
            else:
                # If it's a dict, extract values
                if isinstance(categories, dict):
                    return [str(cat) for cat in categories.values()]
                else:
                    return [str(categories)]
                    
        except Exception as e:
            # Fallback categories
            return [
                "Electronics", "Books", "Jewelry", "Home Decor", 
                "Sports Equipment", "Fashion Accessories", "Kitchen Gadgets", "Art & Crafts"
            ]
    
    async def get_additional_categories(self, occasion: str, preferences: str, budget: str, existing_categories: List[str]) -> List[str]:
        """
        Generate additional gift categories when user asks for more options
        """
        prompt = f"""
        The user has already seen these categories: {existing_categories}
        
        For the occasion: {occasion}, preferences: {preferences}, budget: {budget}
        
        Suggest 6-8 different gift categories that are relevant but different from the existing ones.
        
        Return a JSON array of category names. Return only the JSON array, no other text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            categories = json.loads(response.choices[0].message.content)
            return categories
        except Exception as e:
            # Fallback additional categories
            return [
                "Experiences", "Gourmet Food", "Pet Supplies", "Garden Tools",
                "Travel Accessories", "Health & Wellness", "Office Supplies", "Toys & Games"
            ]
    
    async def select_random_category(self, categories: List[str]) -> str:
        """
        Select a random category for 'surprise me' option
        """
        return random.choice(categories)
    
    async def generate_gift_recommendations(self, gifts: List[Dict[str, Any]], user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate personalized gift recommendations based on user preferences
        """
        if not gifts:
            return []
        
        prompt = f"""
        Based on the user's preferences and the available gifts, rank and recommend the top 5 gifts.
        
        User Preferences:
        - Occasion: {user_preferences.get('occasion', 'Not specified')}
        - Preferences: {user_preferences.get('preferences', 'Not specified')}
        - Budget: {user_preferences.get('budget', 'Not specified')}
        
        Available Gifts: {json.dumps(gifts, indent=2)}
        
        Return a JSON array of the top 5 gifts with the following structure:
        [
            {{
                "id": "gift_id",
                "name": "gift_name",
                "price": "price",
                "description": "brief_description",
                "reason": "why_this_gift_is_good_for_the_user"
            }}
        ]
        
        Return only the JSON array, no other text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            
            recommendations = json.loads(response.choices[0].message.content)
            return recommendations
        except Exception as e:
            # Fallback: return first 5 gifts
            return gifts[:5]
    
    async def generate_conversation_response(self, user_input: str, context: Dict[str, Any]) -> str:
        """
        Generate a conversational response based on the current context
        """
        prompt = f"""
        You are a friendly gift recommendation assistant. Generate a natural, helpful response.
        
        User Input: "{user_input}"
        Context: {json.dumps(context, indent=2)}
        
        Guidelines:
        - Be conversational and helpful
        - Ask for missing information naturally
        - Guide the user through the gift selection process
        - Keep responses concise but informative
        
        Return only your response, no additional formatting.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "I'm here to help you find the perfect gift! Could you tell me more about what you're looking for?"
    
    async def process_user_selection(self, user_input: str, available_options: List[str]) -> Dict[str, Any]:
        """
        Process user's selection from available options with intelligent understanding
        """
        prompt = f"""
        You are an intelligent assistant that understands user intent from abstract or conversational input.
        
        User said: "{user_input}"
        
        Available options: {available_options}
        
        Guidelines:
        - Be flexible in interpreting user intent (e.g., "I like electronics" → select "Electronics" if available)
        - Understand conversational responses (e.g., "something romantic" → look for romantic categories)
        - Handle partial matches (e.g., "books" → select "Books" if available)
        - Recognize requests for more options (e.g., "show me more", "what else", "other options")
        - Detect preference updates (e.g., "actually, I want something different", "change my mind")
        - Handle number selections (e.g., "1", "first one", "option 1")
        
        Determine:
        1. Did the user select one of the available options (exact match, partial match, or intent match)?
        2. Did the user ask for more options?
        3. Did the user provide updated preferences?
        4. What is the selected option (if any)?
        
        Return a JSON object with:
        - selected_option: The selected option or null
        - wants_more_options: true/false
        - updated_preferences: true/false
        - action: "select", "more_options", "update_preferences", or "unclear"
        - confidence: Your confidence in the interpretation (high/medium/low)
        
        Examples:
        - "Electronics" → {{"selected_option": "Electronics", "wants_more_options": false, "updated_preferences": false, "action": "select", "confidence": "high"}}
        - "Something for my girlfriend" → {{"selected_option": "Jewelry" (if available), "wants_more_options": false, "updated_preferences": false, "action": "select", "confidence": "medium"}}
        - "Show me more" → {{"selected_option": null, "wants_more_options": true, "updated_preferences": false, "action": "more_options", "confidence": "high"}}
        
        Return only the JSON object, no other text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Clean the response - remove markdown code blocks if present
            raw_response = response.choices[0].message.content
            cleaned_response = raw_response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]  # Remove ```json
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]   # Remove ```
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]  # Remove trailing ```
            
            # Find JSON object in the response
            json_start = cleaned_response.find('{')
            json_end = cleaned_response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = cleaned_response[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                # Fallback: try to parse the whole cleaned response
                result = json.loads(cleaned_response)
                return result
        except Exception as e:
            return {
                "selected_option": None,
                "wants_more_options": False,
                "updated_preferences": False,
                "action": "unclear",
                "confidence": "low"
            }
