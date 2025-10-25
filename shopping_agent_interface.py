"""
Shopping Agent Interface
This module provides the interface for calling the shopping agent
"""

from typing import List, Dict, Any
from models import GiftItem, UserPreferences
import asyncio
import uuid


class ShoppingAgentInterface:
    """
    Interface for calling the shopping agent
    This is a placeholder implementation - replace with actual shopping agent integration
    """
    
    def __init__(self):
        self.shopping_agent_address = None  # Set this to actual shopping agent address
    
    async def call_shopping_agent(self, preferences: UserPreferences) -> List[GiftItem]:
        """
        Call the shopping agent with user preferences
        
        Args:
            preferences: User preferences for gift search
            
        Returns:
            List of gift items found by shopping agent
        """
        # This is a placeholder implementation
        # Replace with actual shopping agent call
        
        search_params = {
            "occasion": preferences.occasion,
            "preferences": preferences.preferences,
            "budget": preferences.budget,
            "category": preferences.category
        }
        
        # TODO: Implement actual shopping agent call
        # Example:
        # response = await self._send_message_to_agent(
        #     self.shopping_agent_address,
        #     ShoppingRequest(**search_params)
        # )
        # return self._parse_shopping_response(response)
        
        # For now, return mock data
        return await self._get_mock_gifts(search_params)
    
    async def _get_mock_gifts(self, search_params: Dict[str, Any]) -> List[GiftItem]:
        """
        Generate mock gift data for testing
        Replace this with actual shopping agent integration
        """
        # Simulate API delay
        await asyncio.sleep(2)
        
        category = search_params.get('category', 'general')
        budget = search_params.get('budget', '$50-100')
        occasion = search_params.get('occasion', 'general')
        
        # Generate mock gifts based on category
        mock_gifts = []
        
        if category.lower() == 'electronics':
            mock_gifts = [
                GiftItem(
                    id=f"elec_{i}",
                    name=f"Electronic Device {i}",
                    price=f"${100 + i*50}",
                    description=f"High-quality electronic device perfect for {occasion}",
                    source=f"TechStore{i%3 + 1}",
                    url=f"https://techstore{i%3 + 1}.com/device{i}",
                    rating=4.2 + (i * 0.1),
                    availability="In Stock"
                )
                for i in range(1, 11)
            ]
        elif category.lower() == 'books':
            mock_gifts = [
                GiftItem(
                    id=f"book_{i}",
                    name=f"Amazing Book {i}",
                    price=f"${15 + i*5}",
                    description=f"Bestselling book perfect for {occasion}",
                    source=f"BookStore{i%2 + 1}",
                    url=f"https://bookstore{i%2 + 1}.com/book{i}",
                    rating=4.5 + (i * 0.05),
                    availability="In Stock"
                )
                for i in range(1, 11)
            ]
        elif category.lower() == 'jewelry':
            mock_gifts = [
                GiftItem(
                    id=f"jewelry_{i}",
                    name=f"Beautiful Jewelry {i}",
                    price=f"${75 + i*25}",
                    description=f"Elegant jewelry piece for {occasion}",
                    source=f"JewelryStore{i%2 + 1}",
                    url=f"https://jewelry{i%2 + 1}.com/item{i}",
                    rating=4.7 + (i * 0.02),
                    availability="In Stock"
                )
                for i in range(1, 11)
            ]
        else:
            # General gifts
            mock_gifts = [
                GiftItem(
                    id=f"gift_{i}",
                    name=f"Special Gift {i}",
                    price=f"${30 + i*15}",
                    description=f"Thoughtful gift for {occasion}",
                    source=f"GiftStore{i%3 + 1}",
                    url=f"https://giftstore{i%3 + 1}.com/gift{i}",
                    rating=4.0 + (i * 0.1),
                    availability="In Stock"
                )
                for i in range(1, 11)
            ]
        
        # Filter by budget if specified
        if budget:
            # Simple budget filtering (this is very basic)
            if 'under' in budget.lower() or 'below' in budget.lower():
                # Extract number from budget string
                try:
                    max_price = int(''.join(filter(str.isdigit, budget)))
                    mock_gifts = [g for g in mock_gifts if int(''.join(filter(str.isdigit, g.price))) <= max_price]
                except:
                    pass
        
        return mock_gifts
    
    def set_shopping_agent_address(self, address: str):
        """
        Set the address of the shopping agent
        
        Args:
            address: The agent address for the shopping agent
        """
        self.shopping_agent_address = address
    
    async def _send_message_to_agent(self, agent_address: str, message: Any) -> Any:
        """
        Send message to another agent
        This is a placeholder - implement with actual agent communication
        
        Args:
            agent_address: Address of the target agent
            message: Message to send
            
        Returns:
            Response from the agent
        """
        # TODO: Implement actual agent communication
        # This would use the uAgent framework's messaging system
        pass
    
    def _parse_shopping_response(self, response: Any) -> List[GiftItem]:
        """
        Parse response from shopping agent into GiftItem objects
        
        Args:
            response: Response from shopping agent
            
        Returns:
            List of GiftItem objects
        """
        # TODO: Implement actual response parsing
        # This would depend on the shopping agent's response format
        pass


# Global instance
shopping_agent_interface = ShoppingAgentInterface()
