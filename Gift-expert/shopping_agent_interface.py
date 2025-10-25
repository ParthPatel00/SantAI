"""
Shopping Agent Interface
This module provides the interface for calling the shopping agent using OpenWeb Ninja Amazon API
"""

from typing import List, Dict, Any, Optional
from models import GiftItem, UserPreferences
import asyncio
import uuid
import httpx
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ShoppingAgentInterface:
    """
    Interface for calling the shopping agent using OpenWeb Ninja Amazon Data API
    """
    
    def __init__(self):
        self.shopping_agent_address = None  # Set this to actual shopping agent address
        self.api_key = os.getenv("OPENWEB_NINJA_API_KEY")
        self.base_url = "https://api.openwebninja.com/realtime-amazon-data"
        self.client = httpx.AsyncClient(timeout=30.0)
        
        if not self.api_key:
            print("⚠️  OPENWEB_NINJA_API_KEY not found. Set it with: export OPENWEB_NINJA_API_KEY='your-key-here'")
    
    def validate_requirements(self, preferences: UserPreferences) -> tuple[bool, List[str]]:
        """
        Validate if minimum requirements are present for API call
        
        Args:
            preferences: User preferences to validate
            
        Returns:
            Tuple of (is_valid, missing_requirements)
        """
        missing_requirements = []
        
        # Check for minimum requirements
        if not preferences.occasion:
            missing_requirements.append("occasion")
        
        if not preferences.recipient:
            missing_requirements.append("recipient")
        
        if not preferences.preferences:
            missing_requirements.append("preferences")
        
        # Check for budget (required)
        if not preferences.budget_min and not preferences.budget_max:
            missing_requirements.append("budget_min")
            missing_requirements.append("budget_max")
        
        is_valid = len(missing_requirements) == 0
        return is_valid, missing_requirements
    
    async def call_shopping_agent(self, preferences: UserPreferences) -> tuple[List[GiftItem], bool, List[str]]:
        """
        Call the shopping agent with user preferences using OpenWeb Ninja Amazon API
        
        Args:
            preferences: User preferences for gift search
            
        Returns:
            Tuple of (gift_items, is_valid, missing_requirements)
        """
        if not self.api_key:
            print("❌ OpenWeb Ninja API key not found. Cannot search for products.")
            return [], False, ["API key not configured"]
        
        # Validate requirements first
        is_valid, missing_requirements = self.validate_requirements(preferences)
        
        if not is_valid:
            print(f"❌ Missing requirements: {missing_requirements}")
            return [], False, missing_requirements
        
        try:
            # Build search query from preferences
            search_query = self._build_search_query(preferences)
            
            # Search for products using OpenWeb Ninja API
            products = await self._search_amazon_products(search_query, preferences)
            
            # Convert API results to GiftItem objects
            gift_items = self._convert_to_gift_items(products)
            
            # Send results back to the calling agent if address is set
            if self.shopping_agent_address:
                await self._send_message_to_agent(self.shopping_agent_address, {
                    "type": "shopping_results",
                    "products": gift_items,
                    "query": search_query,
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            return gift_items, True, []
            
        except Exception as e:
            print(f"❌ Error calling shopping agent: {str(e)}")
            return [], False, [f"API error: {str(e)}"]
    
    def _build_search_query(self, preferences: UserPreferences) -> str:
        """
        Build search query from user preferences
        
        Args:
            preferences: User preferences for gift search
            
        Returns:
            Search query string for Amazon API
        """
        query_parts = []
        
        # Add category if specified
        if preferences.category:
            query_parts.append(preferences.category)
        
        # Add recipient-specific terms
        if preferences.recipient:
            recipient_terms = {
                "mother": "for mom",
                "mom": "for mom", 
                "mothers": "for mom",
                "father": "for dad",
                "dad": "for dad",
                "fathers": "for dad",
                "girlfriend": "for girlfriend",
                "boyfriend": "for boyfriend",
                "wife": "for wife",
                "husband": "for husband",
                "friend": "for friend",
                "sister": "for sister",
                "brother": "for brother"
            }
            recipient_lower = preferences.recipient.lower()
            if recipient_lower in recipient_terms:
                query_parts.append(recipient_terms[recipient_lower])
            else:
                query_parts.append(f"for {preferences.recipient}")
        
        # Add occasion-specific terms
        if preferences.occasion:
            occasion_terms = {
                "birthday": "birthday gift",
                "anniversary": "anniversary gift", 
                "wedding": "wedding gift",
                "holiday": "holiday gift",
                "christmas": "christmas gift",
                "valentine": "valentine gift",
                "graduation": "graduation gift",
                "mothers day": "mothers day gift",
                "fathers day": "fathers day gift"
            }
            if preferences.occasion.lower() in occasion_terms:
                query_parts.append(occasion_terms[preferences.occasion.lower()])
            else:
                query_parts.append(f"{preferences.occasion} gift")
        
        # Add preferences/interest terms
        if preferences.preferences:
            # Split preferences and add them
            prefs = preferences.preferences.split(',')
            for pref in prefs[:3]:  # Limit to 3 preferences to avoid overly long queries
                query_parts.append(pref.strip())
        
        # Join all parts
        query = " ".join(query_parts)
        
        # If no specific query built, use a generic gift search
        if not query.strip():
            query = "gift"
        
        return query
    
    async def _search_amazon_products(self, query: str, preferences: UserPreferences) -> List[Dict]:
        """
        Search Amazon products using OpenWeb Ninja Product Search API
        
        Args:
            query: Search query string
            preferences: User preferences for filtering
            
        Returns:
            List of product dictionaries from API
        """
        try:
            headers = {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": "GiftAgent/1.0"
            }
            
            # Build search parameters for Product Search API
            params = {
                "query": query,
                "country": "US",  # Default to US market
                "sort_by": "relevance"  # Sort by relevance
            }
            
            # Add price filtering if budget is specified
            if preferences.budget_min is not None:
                params["min_price"] = preferences.budget_min
            if preferences.budget_max is not None:
                params["max_price"] = preferences.budget_max
            
            # Make API request to Product Search endpoint
            response = await self.client.get(
                f"{self.base_url}/search",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("products", [])
            else:
                print(f"❌ API request failed with status {response.status_code}: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error searching Amazon products: {str(e)}")
            return []
    
    def _parse_budget_range(self, budget: str) -> Optional[tuple]:
        """
        Parse budget string to extract min/max price range
        
        Args:
            budget: Budget string (e.g., "$50-100", "under $50", "$100+")
            
        Returns:
            Tuple of (min_price, max_price) or None if parsing fails
        """
        try:
            budget = budget.lower().replace("$", "").replace(",", "")
            
            if "under" in budget or "below" in budget:
                # Extract number after "under" or "below"
                import re
                numbers = re.findall(r'\d+', budget)
                if numbers:
                    max_price = int(numbers[0])
                    return (0, max_price)
            
            elif "+" in budget:
                # Extract number before "+"
                import re
                numbers = re.findall(r'\d+', budget)
                if numbers:
                    min_price = int(numbers[0])
                    return (min_price, None)
            
            elif "-" in budget:
                # Extract range
                parts = budget.split("-")
                if len(parts) == 2:
                    min_price = int(parts[0].strip())
                    max_price = int(parts[1].strip())
                    # Validate that min_price <= max_price
                    if min_price <= max_price:
                        return (min_price, max_price)
                    else:
                        print(f"⚠️  Invalid budget range: {budget} (min_price > max_price)")
                        return None
            
            else:
                # Single number
                import re
                numbers = re.findall(r'\d+', budget)
                if numbers:
                    price = int(numbers[0])
                    return (price, price)
            
        except Exception as e:
            print(f"⚠️  Could not parse budget range: {budget}")
        
        return None
    
    def _convert_to_gift_items(self, products: List[Dict]) -> List[GiftItem]:
        """
        Convert API product data to GiftItem objects
        
        Args:
            products: List of product dictionaries from API
            
        Returns:
            List of GiftItem objects
        """
        gift_items = []
        
        for product in products:
            try:
                # Extract product information
                name = product.get("title", "Unknown Product")
                price = product.get("price", {}).get("current", "N/A")
                description = product.get("description", "")
                url = product.get("url", "")
                rating = product.get("rating", {}).get("average", 0.0)
                availability = "In Stock" if product.get("availability", {}).get("in_stock", False) else "Out of Stock"
                
                # Create unique ID
                product_id = product.get("asin", str(uuid.uuid4()))
                
                # Create GiftItem
                gift_item = GiftItem(
                    id=product_id,
                    name=name,
                    price=str(price) if price != "N/A" else "Price not available",
                    description=description,
                    source="Amazon",
                    url=url,
                    rating=float(rating) if rating else 0.0,
                    availability=availability
                )
                
                gift_items.append(gift_item)
                
            except Exception as e:
                print(f"⚠️  Error converting product: {str(e)}")
                continue
        
        return gift_items
    
    def set_shopping_agent_address(self, address: str):
        """
        Set the address of the shopping agent
        
        Args:
            address: The agent address for the shopping agent
        """
        self.shopping_agent_address = address
    
    async def _send_message_to_agent(self, agent_address: str, message: Dict[str, Any]) -> bool:
        """
        Send message to another agent using uAgent messaging
        
        Args:
            agent_address: Address of the target agent
            message: Message data to send
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # This would typically use the uAgent framework's messaging system
            # For now, we'll simulate sending the message
            print(f"📤 Sending message to agent {agent_address}: {message.get('type', 'unknown')}")
            print(f"   Products found: {len(message.get('products', []))}")
            print(f"   Query: {message.get('query', 'N/A')}")
            
            # In a real implementation, you would use:
            # from uagents import send_message
            # await send_message(agent_address, message)
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending message to agent: {str(e)}")
            return False
    
    async def search_products_direct(self, query: str, max_results: int = 10) -> List[GiftItem]:
        """
        Direct product search method for external calls
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of GiftItem objects
        """
        if not self.api_key:
            print("❌ OpenWeb Ninja API key not found. Cannot search for products.")
            return []
        
        try:
            # Create a basic preferences object for the search
            preferences = UserPreferences(
                category="",
                occasion="",
                preferences="",
                budget_min=None,
                budget_max=None
            )
            
            # Search for products
            products = await self._search_amazon_products(query, preferences)
            
            # Convert to GiftItem objects
            gift_items = self._convert_to_gift_items(products)
            
            # Limit results
            return gift_items[:max_results]
            
        except Exception as e:
            print(f"❌ Error in direct product search: {str(e)}")
            return []
    
    async def get_product_details(self, product_id: str) -> Optional[GiftItem]:
        """
        Get detailed information about a specific product
        
        Args:
            product_id: Product ID (ASIN) to get details for
            
        Returns:
            GiftItem object with detailed information or None if not found
        """
        if not self.api_key:
            print("❌ OpenWeb Ninja API key not found. Cannot get product details.")
            return None
        
        try:
            headers = {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": "GiftAgent/1.0"
            }
            
            # Make API request for product details
            response = await self.client.get(
                f"{self.base_url}/product/{product_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                product = data.get("product", {})
                
                if product:
                    # Convert to GiftItem
                    gift_items = self._convert_to_gift_items([product])
                    return gift_items[0] if gift_items else None
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting product details: {str(e)}")
            return None
    
    async def close(self):
        """
        Close the HTTP client connection
        """
        await self.client.aclose()


# Global instance
shopping_agent_interface = ShoppingAgentInterface()
