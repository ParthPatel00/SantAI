"""
Conversation Flow Manager for Gift Agent
Handles the interactive conversation flow and state management
"""

from typing import Dict, Any, List, Optional
from models import ConversationContext, ConversationState, UserPreferences, GiftItem, GiftRecommendation
from llm_service import LLMService
from global_memory import global_memory
from shopping_agent_interface import shopping_agent_interface
import uuid
import asyncio


class ConversationFlowManager:
    """
    Manages the conversation flow for the Gift Agent
    """
    
    def __init__(self):
        self.llm_service = LLMService()
    
    async def start_conversation(self, user_id: str, initial_input: str) -> str:
        """
        Start a new conversation and return the initial response
        """
        # Reset global parameters for new conversation
        self.llm_service.reset_global_parameters()
        
        # Create new conversation context
        context = ConversationContext(
            user_id=user_id,
            state=ConversationState.INITIAL,
            preferences=UserPreferences()
        )
        
        # Store context in global memory
        global_memory.set_user_context(user_id, context)
        
        # Process initial input
        return await self.process_user_input(user_id, initial_input)
    
    async def process_user_input(self, user_id: str, user_input: str, ctx=None) -> str:
        """
        Process user input and return appropriate response
        """
        # Check if this is a response from a friend agent (prevent infinite loop)
        if any(phrase in user_input.lower() for phrase in [
            "i am devam", "i am parth", "i am sakshi", 
            "as devam", "as parth", "as sakshi",
            "my personality", "my essence", "my core being",
            "devam is glad", "agent-devam", "calm and balanced",
            "gentle", "empathetic", "nature-guided"
        ]):
            # This is a response from a friend agent, don't process it
            return "🎁 Thank you for the information! I'll use this to find the perfect gift."
        
        # Check if user mentioned a friend's name
        friend_names = ["devam", "parth", "sakshi"]
        user_input_lower = user_input.lower()
        
        for friend_name in friend_names:
            if friend_name in user_input_lower:
                
                # Check if this is a check command
                if "check" in user_input_lower and friend_name in user_input_lower:
                    from friend_interface import friend_interface
                    personality = friend_interface.get_personality(friend_name)
                    preferences = friend_interface.get_preferences(friend_name)
                    
                    if personality or preferences:
                        response_text = f"🔍 **Responses from {friend_name.title()}'s agent:**\n\n"
                        if personality:
                            response_text += f"**Personality:** {personality}\n\n"
                        if preferences:
                            response_text += f"**Preferences:** {preferences}\n\n"
                        return response_text
                    else:
                        return f"❌ No responses received from {friend_name.title()}'s agent yet."
                
                # Route to friend interface
                from friend_interface import friend_interface
                if ctx is None:
                    return f"❌ Cannot communicate with {friend_name.title()}'s agent - no context available. Please try again."
                
                # Send messages and return status
                return await friend_interface.communicate_with_friend(friend_name, ctx)
        
        # Process regular conversation flow
        
        context = global_memory.get_user_context(user_id)
        if not context:
            return await self.start_conversation(user_id, user_input)
        
        # Add user message to history
        context.add_message("user", user_input)
        
        # Process based on current state
        if context.state == ConversationState.INITIAL:
            return await self._handle_initial_input(context, user_input)
        elif context.state == ConversationState.COLLECTING_PREFERENCES:
            return await self._handle_preferences_collection(context, user_input)
        elif context.state == ConversationState.SELECTING_CATEGORY:
            return await self._handle_category_selection(context, user_input)
        elif context.state == ConversationState.SHOWING_RECOMMENDATIONS:
            return await self._handle_recommendation_selection(context, user_input)
        elif context.state == ConversationState.SELECTING_GIFT:
            return await self._handle_gift_selection(context, user_input)
        else:
            return "I'm not sure how to help with that. Let's start over!"
    
    async def _handle_initial_input(self, context: ConversationContext, user_input: str) -> str:
        """
        Handle initial user input and extract preferences using global parameters
        """
        # Use global parameter approach
        extracted_info = await self.llm_service.get_occasion_and_preferences(user_input)
        missing_info = extracted_info.get("missing_info", [])
        is_complete = len(missing_info) == 0
        
        
        # Update context preferences with global parameters
        context.preferences.occasion = extracted_info.get('occasion')
        context.preferences.recipient = extracted_info.get('recipient')
        context.preferences.preferences = extracted_info.get('preferences')
        context.preferences.budget_min = extracted_info.get('budget_min')
        context.preferences.budget_max = extracted_info.get('budget_max')
        
        # Check if we have enough information to proceed
        if is_complete:
            context.state = ConversationState.SELECTING_CATEGORY
            return await self._show_category_options(context)
        else:
            # Acknowledge what we learned and ask for missing information
            learned_info = []
            if extracted_info.get('occasion'):
                learned_info.append("occasion")
            if extracted_info.get('recipient'):
                learned_info.append("recipient")
            if extracted_info.get('preferences'):
                learned_info.append("preferences")
            if extracted_info.get('budget_min') or extracted_info.get('budget_max'):
                learned_info.append("budget")
            
            acknowledgment = ""
            if learned_info:
                acknowledgment = self._acknowledge_learned_info(learned_info, extracted_info)
            
            context.state = ConversationState.COLLECTING_PREFERENCES
            missing_info = extracted_info.get('missing_info', [])
            
            if acknowledgment:
                return f"{acknowledgment}\n\n{await self._ask_for_missing_info(context, missing_info)}"
            else:
                return await self._ask_for_missing_info(context, missing_info)
    
    async def _handle_preferences_collection(self, context: ConversationContext, user_input: str) -> str:
        """
        Handle collecting missing preferences in a conversational way
        """
        # Use global parameter approach
        extracted_info = await self.llm_service.get_occasion_and_preferences(user_input)
        
        
        # Update context preferences with global parameters
        context.preferences.occasion = extracted_info.get('occasion')
        context.preferences.recipient = extracted_info.get('recipient')
        context.preferences.preferences = extracted_info.get('preferences')
        context.preferences.budget_min = extracted_info.get('budget_min')
        context.preferences.budget_max = extracted_info.get('budget_max')
        
        # Track what we learned
        learned_info = []
        if extracted_info.get('occasion'):
            learned_info.append("occasion")
        if extracted_info.get('recipient'):
            learned_info.append("recipient")
        if extracted_info.get('preferences'):
            learned_info.append("preferences")
        if extracted_info.get('budget_min') or extracted_info.get('budget_max'):
            learned_info.append("budget")
        
        # Acknowledge what we learned before asking for more
        if learned_info:
            acknowledgment = self._acknowledge_learned_info(learned_info, extracted_info)
        else:
            acknowledgment = ""
        
        # Check if we have enough information now
        if context.preferences.is_complete():
            context.state = ConversationState.SELECTING_CATEGORY
            if acknowledgment:
                return f"{acknowledgment}\n\n{await self._show_category_options(context)}"
            else:
                return await self._show_category_options(context)
        else:
            missing_info = extracted_info.get('missing_info', [])
            if acknowledgment:
                return f"{acknowledgment}\n\n{await self._ask_for_missing_info(context, missing_info)}"
            else:
                return await self._ask_for_missing_info(context, missing_info)
    
    async def _handle_category_selection(self, context: ConversationContext, user_input: str) -> str:
        """
        Handle category selection with intelligent understanding
        """
        # Process user selection with enhanced understanding
        selection_result = await self.llm_service.process_user_selection(
            user_input, 
            context.available_categories + ["surprise me", "show other categories"]
        )
        
        if selection_result['action'] == 'select' and selection_result['selected_option']:
            selected = selection_result['selected_option']
            
            if selected == "surprise me":
                # Select random category
                selected_category = await self.llm_service.select_random_category(context.available_categories)
                context.preferences.category = selected_category
                context.add_message("assistant", f"I've selected '{selected_category}' for you! Let me find some great gifts...")
            elif selected in context.available_categories:
                context.preferences.category = selected
                context.add_message("assistant", f"Great choice! I'll look for gifts in the '{selected}' category...")
            else:
                # Handle number selections (e.g., "5" -> 5th category)
                try:
                    if selected.isdigit():
                        index = int(selected) - 1
                        if 0 <= index < len(context.available_categories):
                            selected_category = context.available_categories[index]
                            context.preferences.category = selected_category
                            context.add_message("assistant", f"Perfect! I'll look for gifts in the '{selected_category}' category...")
                        else:
                            return ("That number is not valid. Please choose a number between 1 and " + 
                                   str(len(context.available_categories)) + " or select a category by name.")
                    else:
                        # Try to find a close match
                        close_match = self._find_close_category_match(selected, context.available_categories)
                        if close_match:
                            context.preferences.category = close_match
                            context.add_message("assistant", f"I think you meant '{close_match}' - great choice! Let me find some gifts...")
                        else:
                            return ("I didn't quite understand your selection. Could you please choose from the available options "
                                   "or say 'surprise me' if you'd like me to pick for you?")
                except ValueError:
                    return ("I didn't quite understand your selection. Could you please choose from the available options "
                           "or say 'surprise me' if you'd like me to pick for you?")
            
            # Call shopping agent
            return await self._call_shopping_agent(context)
            
        elif selection_result['wants_more_options']:
            return await self._show_additional_categories(context)
        elif selection_result['updated_preferences']:
            context.state = ConversationState.COLLECTING_PREFERENCES
            return "I'd be happy to help you update your preferences! What would you like to change?"
        else:
            return ("I didn't quite understand your selection. You can:\n"
                   "• Choose a category by name or number\n"
                   "• Say 'surprise me' for a random selection\n"
                   "• Ask for 'more options' to see additional categories\n"
                   "• Tell me more about what you're looking for")
    
    async def _handle_recommendation_selection(self, context: ConversationContext, user_input: str) -> str:
        """
        Handle gift recommendation selection
        """
        # Process user selection
        available_options = [f"{i+1}. {rec.gift.name}" for i, rec in enumerate(context.current_recommendations)]
        selection_result = await self.llm_service.process_user_selection(
            user_input, 
            available_options + ["show more options", "update preferences"]
        )
        
        if selection_result['action'] == 'select' and selection_result['selected_option']:
            # Parse selection (e.g., "1. Gift Name" -> index 0)
            try:
                selection_text = selection_result['selected_option']
                if selection_text.startswith(('1', '2', '3', '4', '5')):
                    index = int(selection_text[0]) - 1
                    if 0 <= index < len(context.current_recommendations):
                        selected_gift = context.current_recommendations[index].gift
                        context.selected_gift = selected_gift
                        context.state = ConversationState.PAYMENT
                        context.add_message("assistant", f"Excellent choice! You've selected: {selected_gift.name}")
                        return f"Perfect! You've selected: **{selected_gift.name}**\n\nPrice: {selected_gift.price}\nDescription: {selected_gift.description}\n\nI'll now connect you with the payment agent to complete your purchase!"
            except (ValueError, IndexError):
                pass
            
            return "I didn't understand your selection. Please choose a number (1-5) or say 'show more options' or 'update preferences'."
            
        elif selection_result['wants_more_options']:
            return await self._show_next_recommendations(context)
        elif selection_result['updated_preferences']:
            context.state = ConversationState.COLLECTING_PREFERENCES
            return "I'd be happy to help you update your preferences! What would you like to change about your gift requirements?"
        else:
            return "I didn't understand your selection. Please choose a number (1-5) or say 'show more options' or 'update preferences'."
    
    async def _handle_gift_selection(self, context: ConversationContext, user_input: str) -> str:
        """
        Handle final gift selection (if needed)
        """
        # This would be called if there are additional steps before payment
        return await self._handle_recommendation_selection(context, user_input)
    
    async def _ask_for_missing_info(self, context: ConversationContext, missing_info: List[str]) -> str:
        """
        Ask user for missing information in a natural, conversational way
        """
        
        # Count how many pieces of info we're missing
        missing_count = len(missing_info)
        
        # Build dynamic message based on what's actually missing
        questions = []
        
        if "occasion" in missing_info:
            questions.append("• **What's the occasion?** (birthday, anniversary, holiday, just because, etc.)")
        
        if "recipient" in missing_info:
            questions.append("• **Who is it for?** (friend, family member, partner, colleague, etc.)")
        
        if "preferences" in missing_info:
            questions.append("• **What are their preferences?** (hobbies, interests, favorite things, etc.)")
        
        if "budget_min" in missing_info or "budget_max" in missing_info:
            questions.append("• **What's your budget?** (e.g., $50-100, under $50, $100+)")
        
        if missing_count >= 3:
            # Missing most information - be very friendly and encouraging
            return ("I'm excited to help you find the perfect gift! 🎁\n\n"
                   "To get started, could you tell me:\n\n" + 
                   "\n".join(questions) + 
                   "\n\nDon't worry if you're not sure about everything - we can figure it out together! 😊")
        
        elif missing_count == 2:
            # Missing two pieces - be conversational
            return ("I'm getting a good sense of what you're looking for! Just need a couple more details:\n\n" + 
                   "\n".join(questions))
        
        elif missing_count == 1:
            # Missing one piece - be specific and helpful
            return ("I love what you've told me so far! Just one more thing - " + 
                   questions[0].replace("• **", "").replace("**", "").replace("?", "").lower() + "?")
        
        else:
            return ("I'm getting a great sense of what you're looking for! "
                   "Could you share a bit more about the person or occasion to help me find the perfect gift?")
    
    async def _show_category_options(self, context: ConversationContext) -> str:
        """
        Show gift category options to user in a conversational way
        """
        # Get categories from LLM
        categories = await self.llm_service.get_gift_categories(
            context.preferences.occasion,
            context.preferences.preferences,
            context.preferences.budget_min,
            context.preferences.budget_max
        )
        
        context.available_categories = categories
        
        # Create personalized introduction
        occasion = context.preferences.occasion or "this special occasion"
        preferences = context.preferences.preferences or "what you're looking for"
        budget = f"${context.preferences.budget_min}-${context.preferences.budget_max}" if context.preferences.budget_min and context.preferences.budget_max else "your budget"
        
        # Format response with personality
        response = f"Perfect! I've got some great ideas for {occasion}! 🎁\n\n"
        response += f"Based on {preferences} and {budget}, here are the categories I think would work best:\n\n"
        
        for i, category in enumerate(categories, 1):
            response += f"**{i}. {category}**\n"
        
        response += "\n**What would you like to do?**\n"
        response += "• **Pick a number** (1-8) to choose a category\n"
        response += "• **Say 'surprise me'** and I'll pick something perfect for you! 🎲\n"
        response += "• **Ask for 'more options'** if you want to see different categories\n"
        response += "• **Tell me more** about what you're looking for if you're not sure\n\n"
        response += "I'm excited to help you find the perfect gift! What sounds good to you? 😊"
        
        context.add_message("assistant", response)
        return response
    
    async def _show_additional_categories(self, context: ConversationContext) -> str:
        """
        Show additional category options in a conversational way
        """
        additional_categories = await self.llm_service.get_additional_categories(
            context.preferences.occasion,
            context.preferences.preferences,
            f"${context.preferences.budget_min}-${context.preferences.budget_max}" if context.preferences.budget_min and context.preferences.budget_max else "your budget",
            context.available_categories
        )
        
        context.available_categories.extend(additional_categories)
        
        response = "Great idea! Let me show you some more options that might be perfect:\n\n"
        start_index = len(context.available_categories) - len(additional_categories) + 1
        for i, category in enumerate(additional_categories, start_index):
            response += f"**{i}. {category}**\n"
        
        response += "\n**What would you like to do?**\n"
        response += "• **Pick a number** to choose a category\n"
        response += "• **Say 'surprise me'** and I'll pick something amazing! 🎲\n"
        response += "• **Ask for 'more options'** if you want to see even more categories\n"
        response += "• **Go back** to the previous categories if you prefer those\n\n"
        response += "I'm here to help you find exactly what you're looking for! What catches your eye? 👀"
        
        context.add_message("assistant", response)
        return response
    
    async def _call_shopping_agent(self, context: ConversationContext) -> str:
        """
        Call shopping agent to find gifts with validation
        """
        # Validate requirements first
        is_valid, missing_requirements = shopping_agent_interface.validate_requirements(context.preferences)
        
        if not is_valid:
            # Ask user for missing requirements
            missing_list = ", ".join(missing_requirements)
            response = f"I need a bit more information to find the perfect gift for you! 🎁\n\n"
            response += f"**Missing information:** {missing_list}\n\n"
            
            if "occasion" in missing_requirements:
                response += "• **What's the occasion?** (birthday, anniversary, holiday, etc.)\n"
            if "recipient" in missing_requirements:
                response += "• **Who is the gift for?** (mother, father, girlfriend, boyfriend, friend, etc.)\n"
            if "preferences" in missing_requirements:
                response += "• **What are your preferences?** (colors, brands, interests, etc.)\n"
            if "budget_min" in missing_requirements or "budget_max" in missing_requirements:
                response += "• **What's your budget?** (e.g., $50-100, under $50, $100+)\n"
            
            response += "\nPlease provide the missing information so I can search for the perfect gift!"
            
            context.add_message("assistant", response)
            return response
        
        # All requirements met, call shopping agent
        try:
            # Call the real shopping agent
            products, success, errors = await shopping_agent_interface.call_shopping_agent(context.preferences)
            
            if success and products:
                # Format product recommendations
                response = f"🎁 **Perfect! I found {len(products)} great gift options for you:**\n\n"
                
                for i, product in enumerate(products[:5], 1):  # Show top 5 products
                    response += f"**{i}. {product.name}**\n"
                    response += f"   💰 Price: {product.price}\n"
                    response += f"   ⭐ Rating: {product.rating}/5\n"
                    response += f"   🔗 [View Product]({product.url})\n\n"
                
                if len(products) > 5:
                    response += f"... and {len(products) - 5} more options available!\n\n"
                
                response += "Would you like me to search for more options or help you with anything else?"
                
            else:
                response = "I'm sorry, I couldn't find any products matching your criteria. "
                response += "Could you try adjusting your preferences or budget? I'd be happy to search again!"
                
        except Exception as e:
            response = f"I encountered an error while searching for gifts: {str(e)}. "
            response += "Please try again or let me know if you'd like to adjust your search criteria."
        
        context.add_message("assistant", response)
        return response
    
    # async def _simulate_shopping_agent_call(self, context: ConversationContext, search_id: str):
        """
        Simulate shopping agent call (replace with actual implementation)
        """
        # This is a placeholder - replace with actual shopping agent integration
        # For now, we'll create some mock data
        mock_gifts = [
            GiftItem(
                id=f"gift_{i}",
                name=f"Mock Gift {i}",
                price=f"${50 + i*25}",
                description=f"This is a great {context.preferences.category.lower()} gift for {context.preferences.occasion.lower()}",
                source=f"Marketplace {i%3 + 1}",
                url=f"https://example.com/gift{i}",
                rating=4.0 + (i * 0.1)
            )
            for i in range(1, 16)  # 15 mock gifts
        ]
        
        # Store results in global memory
        global_memory.store_gift_search_results(search_id, mock_gifts)
        global_memory.add_gifts_to_user(context.user_id, mock_gifts)
        
        # Generate recommendations
        recommendations = await self.llm_service.generate_gift_recommendations(
            [gift.to_dict() for gift in mock_gifts],
            context.preferences.to_dict()
        )
        
        # Convert to GiftRecommendation objects
        gift_recommendations = []
        for i, rec_data in enumerate(recommendations[:5]):
            # Find the corresponding gift
            gift = next((g for g in mock_gifts if g.id == rec_data['id']), None)
            if gift:
                gift_recommendations.append(GiftRecommendation(
                    gift=gift,
                    reason=rec_data.get('reason', 'Great choice!'),
                    rank=i+1
                ))
        
        # Update context
        context.current_recommendations = gift_recommendations
        context.state = ConversationState.SHOWING_RECOMMENDATIONS
        global_memory.set_user_context(context.user_id, context)
        global_memory.set_user_recommendations(context.user_id, gift_recommendations)
        
        # Send recommendations to user
        await self._show_recommendations(context)
    
    async def _show_recommendations(self, context: ConversationContext) -> str:
        """
        Show gift recommendations to user in a conversational way
        """
        if not context.current_recommendations:
            return "Hmm, I couldn't find any suitable gifts with those preferences. Let me try with different criteria - what would you like to change?"
        
        occasion = context.preferences.occasion or "this special occasion"
        category = context.preferences.category or "this category"
        
        response = f"🎉 **I found some amazing {category.lower()} gifts for {occasion}!**\n\n"
        response += "I've carefully selected these based on what you told me. Here are my top 5 recommendations:\n\n"
        
        for i, rec in enumerate(context.current_recommendations, 1):
            response += f"**{i}. {rec.gift.name}**\n"
            response += f"   💰 **Price:** {rec.gift.price}\n"
            response += f"   📝 **Description:** {rec.gift.description}\n"
            response += f"   🏪 **Available at:** {rec.gift.source}\n"
            response += f"   💡 **Why I think you'll love it:** {rec.reason}\n\n"
        
        response += "**What would you like to do?**\n"
        response += "• **Pick a number (1-5)** to choose your favorite! 🎯\n"
        response += "• **Say 'show more options'** to see additional gifts 🔄\n"
        response += "• **Tell me to 'update preferences'** if you want to change something 🔧\n"
        response += "• **Ask me anything** about these gifts! I'm here to help! 💬\n\n"
        response += "I'm so excited to see which one catches your eye! What do you think? 😊"
        
        context.add_message("assistant", response)
        return response
    
    async def _show_next_recommendations(self, context: ConversationContext) -> str:
        """
        Show next set of recommendations
        """
        # Get next 5 gifts from all available gifts
        all_gifts = context.all_gifts
        current_count = len(context.current_recommendations)
        
        if current_count >= len(all_gifts):
            return "I've shown you all available gifts. Please select one or update your preferences."
        
        # Get next 5 gifts
        next_gifts = all_gifts[current_count:current_count + 5]
        
        # Generate recommendations for next batch
        recommendations = await self.llm_service.generate_gift_recommendations(
            [gift.to_dict() for gift in next_gifts],
            context.preferences.to_dict()
        )
        
        # Convert to GiftRecommendation objects
        gift_recommendations = []
        for i, rec_data in enumerate(recommendations):
            gift = next((g for g in next_gifts if g.id == rec_data['id']), None)
            if gift:
                gift_recommendations.append(GiftRecommendation(
                    gift=gift,
                    reason=rec_data.get('reason', 'Great choice!'),
                    rank=current_count + i + 1
                ))
        
        # Update context
        context.current_recommendations = gift_recommendations
        global_memory.set_user_context(context.user_id, context)
        global_memory.set_user_recommendations(context.user_id, gift_recommendations)
        
        return await self._show_recommendations(context)
    
    def _find_close_category_match(self, user_input: str, available_categories: List[str]) -> Optional[str]:
        """
        Find a close match for user input in available categories
        """
        user_input_lower = user_input.lower()
        
        # Direct substring matches
        for category in available_categories:
            # Handle both string and dict categories
            if isinstance(category, dict):
                category_str = str(category.get('category', category))
            else:
                category_str = str(category)
                
            if user_input_lower in category_str.lower() or category_str.lower() in user_input_lower:
                return category_str
        
        # Common synonyms and variations
        synonyms = {
            'tech': 'Electronics',
            'electronic': 'Electronics',
            'gadget': 'Electronics',
            'book': 'Books',
            'reading': 'Books',
            'jewel': 'Jewelry',
            'jewellery': 'Jewelry',
            'ring': 'Jewelry',
            'necklace': 'Jewelry',
            'home': 'Home Decor',
            'decor': 'Home Decor',
            'decoration': 'Home Decor',
            'sport': 'Sports Equipment',
            'fitness': 'Sports Equipment',
            'exercise': 'Sports Equipment',
            'fashion': 'Fashion Accessories',
            'clothes': 'Fashion Accessories',
            'clothing': 'Fashion Accessories',
            'kitchen': 'Kitchen Gadgets',
            'cooking': 'Kitchen Gadgets',
            'art': 'Art & Crafts',
            'craft': 'Art & Crafts',
            'creative': 'Art & Crafts'
        }
        
        for synonym, category in synonyms.items():
            if synonym in user_input_lower and category in available_categories:
                return category
        
        return None
    
    async def _handle_gift_sending_command(self, user_input: str) -> Optional[str]:
        """
        Handle gift-sending commands like "@santa clause, send a gift to '@devam'"
        """
        import re
        
        # Check for gift-sending pattern: various forms of "send a gift to @username"
        gift_patterns = [
            r'@santa\s+clause,?\s+send\s+a\s+gift\s+to\s+[\'"]?@?(\w+)[\'"]?',  # @santa clause, send a gift to @devam
            r'can\s+you\s+send\s+@(\w+)\s+a\s+gift',  # can you send @devam a gift
            r'send\s+a\s+gift\s+to\s+@(\w+)',  # send a gift to @devam
            r'send\s+@(\w+)\s+a\s+gift',  # send @devam a gift
            r'gift\s+for\s+@(\w+)',  # gift for @devam
        ]
        
        match = None
        for pattern in gift_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                break
        
        if not match:
            return None
        
        recipient_username = match.group(1)
        
        try:
            # Step 1: Query the recipient's personality agent for preferences
            recipient_preferences = await self._query_recipient_agent(recipient_username)
            
            if not recipient_preferences:
                return f"🎁 I'd love to send a gift to @{recipient_username}, but I couldn't reach their personality agent. " \
                       f"Make sure their agent is online and accessible!"
            
            # Step 2: Use recipient's preferences to find a gift
            gift_recommendations = await self._find_gift_for_recipient(recipient_username, recipient_preferences)
            
            if not gift_recommendations:
                return f"🎁 I couldn't find any suitable gifts for @{recipient_username} based on their preferences. " \
                       f"Let me try with different criteria or you can specify what you'd like to send!"
            
            # Step 3: Present gift options and handle selection
            return await self._present_gift_options_for_sending(recipient_username, gift_recommendations)
            
        except Exception as e:
            return f"🎁 I encountered an error while trying to send a gift to @{recipient_username}: {str(e)}. " \
                   f"Please try again or let me know if you need help!"
    
    async def _query_recipient_agent(self, recipient_username: str) -> Optional[Dict[str, Any]]:
        """
        Query the recipient's personality agent for their preferences and gift ideas
        """
        try:
            # Import agent communication module
            from agent_communication import agent_communication
            
            # Check if agent is registered
            if not agent_communication.is_agent_registered(recipient_username):
                print(f"❌ No registered agent found for @{recipient_username}")
                return None
            
            # Query the agent for preferences
            preferences = await agent_communication.query_agent_preferences(recipient_username)
            
            if preferences:
                print(f"✅ Successfully queried preferences from @{recipient_username}")
                return preferences
            else:
                print(f"❌ Failed to get preferences from @{recipient_username}")
                return None
            
        except Exception as e:
            print(f"Error querying recipient agent: {e}")
            return None
    
    async def _find_gift_for_recipient(self, recipient_username: str, preferences: Dict[str, Any]) -> List[GiftItem]:
        """
        Find suitable gifts for the recipient based on their preferences
        """
        try:
            # Create user preferences object from recipient's data
            from models import UserPreferences
            
            recipient_prefs = UserPreferences(
                occasion="just because",  # Remove occasion filter
                recipient=recipient_username,
                preferences=preferences.get("gift_preferences", ""),
                budget_min=None,  # Remove budget filter
                budget_max=None,
                category=None  # Let the system determine category
            )
            
            # Use the shopping agent to find gifts
            from shopping_agent_interface import shopping_agent_interface
            gift_items, success, errors = await shopping_agent_interface.call_shopping_agent(recipient_prefs)
            
            if success and gift_items:
                return gift_items[:5]  # Return top 5 gifts
            else:
                print(f"❌ No gifts found for @{recipient_username}. API returned: success={success}, items={len(gift_items) if gift_items else 0}")
                return []
                
        except Exception as e:
            print(f"Error finding gifts for recipient: {e}")
            return []
    
    
    async def _present_gift_options_for_sending(self, recipient_username: str, gift_recommendations: List[GiftItem]) -> str:
        """
        Present gift options for sending to the recipient
        """
        if not gift_recommendations:
            return f"🎁 I couldn't find any suitable gifts for @{recipient_username}. " \
                   f"Let me try with different preferences or you can tell me what you'd like to send!"
        
        # Get recipient preferences for context
        from agent_communication import agent_communication
        recipient_preferences = await agent_communication.query_agent_preferences(recipient_username)
        
        response = f"🎁 **Perfect! I found some great gift options for @{recipient_username}:**\n\n"
        
        if recipient_preferences:
            response += f"*Based on @{recipient_username}'s interests: {', '.join(recipient_preferences.get('interests', [])[:3])}*\n\n"
        
        for i, gift in enumerate(gift_recommendations, 1):
            response += f"**{i}. {gift.name}**\n"
            response += f"   💰 Price: {gift.price}\n"
            response += f"   📝 Description: {gift.description}\n"
            response += f"   🔗 [View Product]({gift.url})\n\n"
        
        response += f"**What would you like to do?**\n"
        response += f"• **Pick a number (1-{len(gift_recommendations)})** to select a gift for @{recipient_username} 🎯\n"
        response += f"• **Ask for more options** if you want to see different gifts 🔄\n"
        response += f"• **Tell me more** about what you'd like to send specifically 💬\n\n"
        response += f"I'm excited to help you send something special to @{recipient_username}! What catches your eye? 😊"
        
        # Store the gift recommendations for this recipient
        global_memory.store_gift_search_results(f"gift_for_{recipient_username}", gift_recommendations)
        
        return response
    
    async def _handle_gift_selection_for_sending(self, user_input: str) -> str:
        """
        Handle gift selection when sending to a recipient
        """
        try:
            # Find the most recent gift search results
            recent_recipient = None
            gift_recommendations = None
            
            # Look for stored gift recommendations
            for search_id, gifts in global_memory._gift_search_results.items():
                if search_id.startswith("gift_for_"):
                    recent_recipient = search_id.replace("gift_for_", "")
                    gift_recommendations = gifts
                    break
            
            if not gift_recommendations or not recent_recipient:
                return "🎁 I don't have any gift options stored. Please start by saying '@santa clause, send a gift to @username' first!"
            
            # Parse user selection
            import re
            number_match = re.search(r'(\d+)', user_input)
            
            if number_match:
                selected_index = int(number_match.group(1)) - 1
                
                if 0 <= selected_index < len(gift_recommendations):
                    selected_gift = gift_recommendations[selected_index]
                    
                    # Send the gift
                    success = await self._send_gift_to_recipient(recent_recipient, selected_gift)
                    
                    if success:
                        return f"🎁 **Perfect! I've sent the gift to @{recent_recipient}!**\n\n" \
                               f"**Gift:** {selected_gift.name}\n" \
                               f"**Price:** {selected_gift.price}\n" \
                               f"**Description:** {selected_gift.description}\n" \
                               f"**Link:** [View on Amazon]({selected_gift.url})\n\n" \
                               f"@{recent_recipient} has been notified about their gift! 🎉"
                    else:
                        return f"🎁 I selected the gift for @{recent_recipient}, but encountered an issue " \
                               f"completing the purchase. Please try again or contact support."
                else:
                    return f"🎁 Please select a number between 1 and {len(gift_recommendations)} for @{recent_recipient}'s gift."
            else:
                return f"🎁 Please select a number (1-{len(gift_recommendations)}) to choose a gift for @{recent_recipient}."
                
        except Exception as e:
            return f"🎁 I encountered an error processing your gift selection: {str(e)}. Please try again!"
    
    async def _send_gift_to_recipient(self, recipient_username: str, gift: GiftItem) -> bool:
        """
        Send a gift to the recipient (simulate purchase and notification)
        """
        try:
            # Import agent communication
            from agent_communication import agent_communication
            
            # In a real implementation, this would:
            # 1. Process payment through Amazon API
            # 2. Handle shipping details
            # 3. Send confirmation to recipient's agent
            
            # For now, we'll simulate the process
            print(f"🎁 Processing gift purchase for @{recipient_username}: {gift.name}")
            
            # Simulate purchase processing
            await asyncio.sleep(2)  # Simulate API call delay
            
            # Notify the recipient's agent
            notification_sent = await agent_communication.notify_gift_sent(recipient_username, gift)
            
            if notification_sent:
                print(f"✅ Gift sent successfully to @{recipient_username}")
                return True
            else:
                print(f"❌ Failed to notify @{recipient_username} about their gift")
                return False
                
        except Exception as e:
            print(f"❌ Error sending gift to @{recipient_username}: {e}")
            return False
    
    def _acknowledge_learned_info(self, learned_info: List[str], extracted_info: Dict[str, Any]) -> str:
        """
        Acknowledge what we learned from the user in a natural way
        """
        acknowledgments = []
        
        if "occasion" in learned_info:
            occasion = extracted_info.get('occasion', '')
            if occasion and occasion.lower() != 'general':
                acknowledgments.append(f"Perfect! A {occasion} gift - that's so thoughtful! 🎉")
        
        if "recipient" in learned_info:
            recipient = extracted_info.get('recipient', '')
            if 'mother' in recipient.lower() or 'mom' in recipient.lower():
                acknowledgments.append("Aww, something for your mom - that's so sweet! 💕")
            elif 'girlfriend' in recipient.lower() or 'boyfriend' in recipient.lower():
                acknowledgments.append("How romantic! I'll help you find something special! 💖")
            elif 'friend' in recipient.lower():
                acknowledgments.append("A gift for a friend - that's wonderful! 👫")
            else:
                acknowledgments.append(f"Perfect! A gift for {recipient} - that's thoughtful! 🎁")
        
        if "preferences" in learned_info:
            preferences = extracted_info.get('preferences', '')
            acknowledgments.append(f"Nice! I can see you're thinking about {preferences} - that's helpful! 👍")
        
        if "budget_min" in learned_info or "budget_max" in learned_info:
            budget_min = extracted_info.get('budget_min')
            budget_max = extracted_info.get('budget_max')
            if budget_min and budget_max:
                acknowledgments.append(f"Perfect! I'll keep your budget of ${budget_min}-${budget_max} in mind! 💵")
            elif budget_max:
                acknowledgments.append(f"Smart budgeting! I'll find something under ${budget_max}! 💰")
            elif budget_min:
                acknowledgments.append(f"Going all out! I'll find something ${budget_min}+! ✨")
        
        if len(acknowledgments) == 1:
            return acknowledgments[0]
        elif len(acknowledgments) == 2:
            return f"{acknowledgments[0]} {acknowledgments[1]}"
        else:
            return f"{acknowledgments[0]} {acknowledgments[1]} {acknowledgments[2]}"
