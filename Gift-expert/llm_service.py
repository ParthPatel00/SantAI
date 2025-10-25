"""
LLM Service for Gift Agent using Groq
Handles all LLM interactions and prompt management
"""

import os
from typing import List, Dict, Any, Optional
from groq import Groq
import json
import random
from global_parameters import global_params
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
        Extract occasion, preferences, and budget from user input using global parameters
        ONLY updates parameters that are currently null
        """
        # Get current global parameters
        current_params = global_params.to_dict()
        missing_info = global_params.get_missing_info()
        
        print(f"DEBUG: Current global parameters: {current_params}")
        print(f"DEBUG: Missing info: {missing_info}")
        
        # Create context info for LLM
        context_info = f"\nCurrent Parameters: {current_params}\nMissing Parameters: {missing_info}\n"
        
        prompt = f"""
        You are a parameter extraction assistant. Extract ONLY the missing parameters from user input.
        
        User Input: "{user_input}"{context_info}
        
        CRITICAL RULES:
        1. ONLY extract parameters that are currently NULL in current parameters
        2. DO NOT change parameters that already have values
        3. DO NOT assume or infer information - only extract what is explicitly stated
        4. Return ONLY a JSON object with the parameters you can extract from the user input
        
        Extract and return JSON with these exact fields:
        {{
            "occasion": "birthday/anniversary/holiday/wedding/promotion/graduation/christmas/festival/etc or null",
            "recipient": "mother/father/friend/boss/girlfriend/boyfriend/sister/brother/grandmother/grandfather/aunt/uncle/cousin/etc or null", 
            "preferences": "cooking/art/sports/tech-related/hiking/outdoor/nature/etc or null",
            "budget_min": "integer or null",
            "budget_max": "integer or null",
            "missing_info": ["list of fields that are null"]
        }}
        
        IMPORTANT: 
        - If user says "for my brother/sister/mother/father/etc", extract that as recipient
        - If user says "for my boss/friend/girlfriend/etc", extract that as recipient
        - Only extract preferences if user mentions specific interests/hobbies
        - Do NOT use example text as preferences
        - Look for patterns like "for my [person]" or "for [person]" to identify recipient
        
        CRITICAL: Only include fields in missing_info if they are null. If a field has a value, do NOT include it in missing_info.
        
        Examples:
        - Current: {{"occasion": null, "recipient": null, "preferences": null, "budget_min": null, "budget_max": null}}
        - User: "gift for my sister"
        - Return: {{"occasion": null, "recipient": "sister", "preferences": null, "budget_min": null, "budget_max": null}}
        
        - Current: {{"occasion": "graduation", "recipient": "sister", "preferences": null, "budget_min": null, "budget_max": null}}
        - User: "she likes hiking"
        - Return: {{"occasion": null, "recipient": null, "preferences": "hiking", "budget_min": null, "budget_max": null}}
        
        - Current: {{"occasion": "graduation", "recipient": "sister", "preferences": "hiking", "budget_min": null, "budget_max": null}}
        - User: "budget is 100-200"
        - Return: {{"occasion": null, "recipient": null, "preferences": null, "budget_min": 100, "budget_max": 200}}
        
        Return ONLY the JSON object. No other text.
        """
        
        # Debug: Print the full prompt being sent to LLM
        print(f"DEBUG: Full prompt being sent to LLM:")
        print(f"DEBUG: {prompt}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a JSON extraction assistant. You ONLY return valid JSON objects. Never return code, explanations, or any other text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Extract JSON from response
            response_text = response.choices[0].message.content.strip()
            print(f"DEBUG: Raw LLM response: {response_text}")
            
            # Clean the response - remove any code blocks or extra text
            import re
            import json
            
            # Try to find JSON object in the response
            json_match = re.search(r'\{[^{}]*\}', response_text)
            if json_match:
                json_str = json_match.group(0)
            else:
                # Try to find JSON with nested objects
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    json_str = response_text
            
            # Parse JSON
            try:
                result = json.loads(json_str)
                print(f"DEBUG: Parsed result: {result}")
                
                # Validate and update global parameters
                updated_params = self._validate_and_update_parameters(result, current_params)
                print(f"DEBUG: Updated parameters: {updated_params}")
                
                # Update missing info
                missing_info = global_params.get_missing_info()
                
                return {
                    "occasion": updated_params.get("occasion"),
                    "recipient": updated_params.get("recipient"),
                    "preferences": updated_params.get("preferences"),
                    "budget_min": updated_params.get("budget_min"),
                    "budget_max": updated_params.get("budget_max"),
                    "missing_info": missing_info
                }
            except json.JSONDecodeError as e:
                print(f"DEBUG: JSON decode error: {e}")
                print(f"DEBUG: Attempting to parse: {json_str}")
                # Try to fix common JSON issues
                json_str = json_str.replace("'", '"')  # Replace single quotes with double quotes
                try:
                    result = json.loads(json_str)
                    print(f"DEBUG: Fixed and parsed result: {result}")
                    return result
                except:
                    print(f"DEBUG: Still failed to parse, using fallback")
                    return self._fallback_extraction(user_input, current_context)
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            # Fallback to simple extraction
            return self._fallback_extraction(user_input, current_context)
    
    def _fallback_extraction(self, user_input: str, current_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fallback extraction using simple rules
        """
        result = {
            "occasion": None,
            "recipient": None,
            "preferences": None,
            "budget_min": None,
            "budget_max": None,
            "missing_info": []
        }
        
        # Preserve existing context
        if current_context:
            result["occasion"] = current_context.get("occasion")
            result["recipient"] = current_context.get("recipient")
            result["preferences"] = current_context.get("preferences")
            result["budget_min"] = current_context.get("budget_min")
            result["budget_max"] = current_context.get("budget_max")
        
        # Simple keyword extraction
        user_lower = user_input.lower()
        
        # Extract occasion
        if not result["occasion"]:
            if "birthday" in user_lower:
                result["occasion"] = "birthday"
            elif "anniversary" in user_lower:
                result["occasion"] = "anniversary"
            elif "wedding" in user_lower:
                result["occasion"] = "wedding"
            elif "holiday" in user_lower:
                result["occasion"] = "holiday"
            elif "graduation" in user_lower:
                result["occasion"] = "graduation"
            elif "promotion" in user_lower:
                result["occasion"] = "promotion"
        
        # Extract recipient
        if not result["recipient"]:
            if "mother" in user_lower or "mom" in user_lower:
                result["recipient"] = "mother"
            elif "father" in user_lower or "dad" in user_lower:
                result["recipient"] = "father"
            elif "boss" in user_lower:
                result["recipient"] = "boss"
            elif "friend" in user_lower:
                result["recipient"] = "friend"
            elif "sister" in user_lower:
                result["recipient"] = "sister"
            elif "brother" in user_lower:
                result["recipient"] = "brother"
        
        # Extract preferences
        if not result["preferences"]:
            if "cooking" in user_lower:
                result["preferences"] = "cooking, kitchen, culinary"
            elif "sports" in user_lower or "athletic" in user_lower:
                result["preferences"] = "athletic, sports, fitness"
            elif "art" in user_lower:
                result["preferences"] = "art"
            elif "tech" in user_lower:
                result["preferences"] = "tech-related"
            elif "hiking" in user_lower:
                result["preferences"] = "hiking, outdoor, nature"
        
        # Extract budget
        import re
        budget_match = re.search(r'(\d+)\s*-\s*(\d+)', user_input)
        if budget_match:
            result["budget_min"] = int(budget_match.group(1))
            result["budget_max"] = int(budget_match.group(2))
        elif "under" in user_lower:
            under_match = re.search(r'under\s+(\d+)', user_input)
            if under_match:
                result["budget_max"] = int(under_match.group(1))
        elif "$" in user_input:
            dollar_match = re.search(r'\$(\d+)', user_input)
            if dollar_match:
                result["budget_min"] = int(dollar_match.group(1))
        
        # Determine missing info
        if not result["occasion"]:
            result["missing_info"].append("occasion")
        if not result["recipient"]:
            result["missing_info"].append("recipient")
        if not result["preferences"]:
            result["missing_info"].append("preferences")
        if not result["budget_min"] and not result["budget_max"]:
            result["missing_info"].append("budget_min")
            result["missing_info"].append("budget_max")
        
        return result
    
    def _validate_and_update_parameters(self, extracted_params: Dict[str, Any], current_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that extracted parameters don't override existing non-null values
        Only update parameters that are currently null
        """
        print(f"DEBUG: Validating extracted params: {extracted_params}")
        print(f"DEBUG: Against current params: {current_params}")
        
        # Check for violations - parameters that are being changed from non-null to something else
        violations = []
        valid_params = {}
        
        for param, value in extracted_params.items():
            if value is not None:
                if current_params.get(param) is not None and current_params.get(param) != value:
                    violations.append(f"Attempted to change {param} from '{current_params[param]}' to '{value}'")
                    print(f"DEBUG: VIOLATION - Ignoring {param}: {current_params[param]} -> {value}")
                else:
                    valid_params[param] = value
                    print(f"DEBUG: VALID - Processing {param}: {value}")
        
        if violations:
            print(f"DEBUG: VIOLATIONS DETECTED: {violations}")
            print("DEBUG: Processing only valid parameters")
        
        # Update global parameters with only valid new values
        updated_params = current_params.copy()
        
        if valid_params.get("occasion") is not None and global_params.occasion is None:
            global_params.occasion = valid_params["occasion"]
            updated_params["occasion"] = valid_params["occasion"]
            print(f"DEBUG: Updated occasion to: {valid_params['occasion']}")
        
        if valid_params.get("recipient") is not None and global_params.recipient is None:
            global_params.recipient = valid_params["recipient"]
            updated_params["recipient"] = valid_params["recipient"]
            print(f"DEBUG: Updated recipient to: {valid_params['recipient']}")
        
        if valid_params.get("preferences") is not None and global_params.preferences is None:
            global_params.preferences = valid_params["preferences"]
            updated_params["preferences"] = valid_params["preferences"]
            print(f"DEBUG: Updated preferences to: {valid_params['preferences']}")
        
        if valid_params.get("budget_min") is not None and global_params.budget_min is None:
            global_params.budget_min = valid_params["budget_min"]
            updated_params["budget_min"] = valid_params["budget_min"]
            print(f"DEBUG: Updated budget_min to: {valid_params['budget_min']}")
        
        if valid_params.get("budget_max") is not None and global_params.budget_max is None:
            global_params.budget_max = valid_params["budget_max"]
            updated_params["budget_max"] = valid_params["budget_max"]
            print(f"DEBUG: Updated budget_max to: {valid_params['budget_max']}")
        
        return updated_params
    
    def reset_global_parameters(self):
        """Reset all global parameters"""
        global_params.reset()
        print("DEBUG: Reset all global parameters")
    
    async def get_gift_categories(self, occasion: str, preferences: str, budget_min: int, budget_max: int) -> List[str]:
        """
        Generate relevant gift categories based on occasion, preferences, and budget
        """
        prompt = f"""
        Based on the following information, suggest 6-8 relevant gift categories:
        
        Occasion: {occasion}
        Preferences: {preferences}
        Budget: ${budget_min}-${budget_max}
        
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
        - Handle number selections (e.g., "1", "first one", "option 1", "Category 5", "5")
        - IMPORTANT: If user says just a number like "5", map it to the 5th option in the list
        - IMPORTANT: If user says "Category 5", map it to the 5th option in the list
        
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
        
        Examples:
        - "Electronics" → {{"selected_option": "Electronics", "wants_more_options": false, "updated_preferences": false, "action": "select"}}
        - "Something for my girlfriend" → {{"selected_option": "Jewelry" (if available), "wants_more_options": false, "updated_preferences": false, "action": "select"}}
        - "Show me more" → {{"selected_option": null, "wants_more_options": true, "updated_preferences": false, "action": "more_options"}}
        - "5" → {{"selected_option": "5th option in list", "wants_more_options": false, "updated_preferences": false, "action": "select"}}
        - "Category 5" → {{"selected_option": "5th option in list", "wants_more_options": false, "updated_preferences": false, "action": "select"}}
        
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
            }
