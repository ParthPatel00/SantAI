#!/usr/bin/env python3
"""
Test script to verify the OpenWeb Ninja API is working correctly
"""

import asyncio
from shopping_agent_interface import shopping_agent_interface
from models import UserPreferences


async def test_api():
    """
    Test the OpenWeb Ninja API directly
    """
    print("🔍 Testing OpenWeb Ninja API")
    print("=" * 40)
    
    # Create test preferences with very simple query
    preferences = UserPreferences(
        occasion="just because",
        recipient="devam",
        preferences="gift",  # Very simple query
        budget_min=None,
        budget_max=None,
        category=None
    )
    
    print(f"📋 Test preferences: {preferences.to_dict()}")
    
    try:
        # Test the API call
        gift_items, success, errors = await shopping_agent_interface.call_shopping_agent(preferences)
        
        print(f"\n📊 Results:")
        print(f"   Success: {success}")
        print(f"   Items found: {len(gift_items) if gift_items else 0}")
        print(f"   Errors: {errors}")
        
        if gift_items:
            print(f"\n🎁 Found {len(gift_items)} gifts:")
            for i, gift in enumerate(gift_items[:3], 1):  # Show first 3
                print(f"   {i}. {gift.name} - {gift.price}")
                print(f"      Description: {gift.description}")
                print(f"      URL: {gift.url}")
                print()
        else:
            print("❌ No gifts found")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")


if __name__ == "__main__":
    asyncio.run(test_api())
