"""
Conversation Flow Manager for Gift Agent
Handles the interactive conversation flow and state management
"""

from typing import Dict, Any, List, Optional
from models import ConversationContext, ConversationState, UserPreferences, GiftItem, GiftRecommendation
from llm_service import LLMService
from global_memory import global_memory
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
    
    async def process_user_input(self, user_id: str, user_input: str) -> str:
        """
        Process user input and return appropriate response
        """
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
        Handle initial user input and extract preferences intelligently
        """
        # Extract preferences using LLM with enhanced understanding
        extracted_info = await self.llm_service.get_occasion_and_preferences(user_input)
        
        # Store confidence level for context
        context.extraction_confidence = extracted_info.get('confidence', 'medium')
        
        # Update preferences with intelligent defaults
        if extracted_info.get('occasion'):
            context.preferences.occasion = extracted_info['occasion']
        if extracted_info.get('preferences'):
            context.preferences.preferences = extracted_info['preferences']
        if extracted_info.get('budget'):
            context.preferences.budget = extracted_info['budget']
        
        # For high confidence extractions, be more flexible about completeness
        if context.extraction_confidence == 'high':
            # If we have good information, proceed even if not "complete"
            # We need at least occasion and budget to proceed
            if context.preferences.occasion and context.preferences.budget:
                context.state = ConversationState.SELECTING_CATEGORY
                return await self._show_category_options(context)
        
        # Check if we have enough information for standard flow
        # We need at least occasion and budget to proceed (preferences can be collected later)
        if context.preferences.occasion and context.preferences.budget:
            context.state = ConversationState.SELECTING_CATEGORY
            return await self._show_category_options(context)
        else:
            context.state = ConversationState.COLLECTING_PREFERENCES
            missing_info = extracted_info.get('missing_info', [])
            return await self._ask_for_missing_info(context, missing_info)
    
    async def _handle_preferences_collection(self, context: ConversationContext, user_input: str) -> str:
        """
        Handle collecting missing preferences in a conversational way
        """
        # Extract preferences from user input
        extracted_info = await self.llm_service.get_occasion_and_preferences(user_input)
        
        # Store confidence level
        context.extraction_confidence = extracted_info.get('confidence', 'medium')
        
        # Track what we learned
        learned_info = []
        if extracted_info.get('occasion'):
            context.preferences.occasion = extracted_info['occasion']
            learned_info.append("occasion")
        if extracted_info.get('preferences'):
            context.preferences.preferences = extracted_info['preferences']
            learned_info.append("preferences")
        if extracted_info.get('budget'):
            context.preferences.budget = extracted_info['budget']
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
            confidence = selection_result.get('confidence', 'medium')
            
            if selected == "surprise me":
                # Select random category
                selected_category = await self.llm_service.select_random_category(context.available_categories)
                context.preferences.category = selected_category
                context.add_message("assistant", f"I've selected '{selected_category}' for you! Let me find some great gifts...")
            elif selected in context.available_categories:
                context.preferences.category = selected
                context.add_message("assistant", f"Great choice! I'll look for gifts in the '{selected}' category...")
            else:
                # Try to find a close match
                close_match = self._find_close_category_match(selected, context.available_categories)
                if close_match:
                    context.preferences.category = close_match
                    context.add_message("assistant", f"I think you meant '{close_match}' - great choice! Let me find some gifts...")
                else:
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
        # Get confidence level from the extraction
        confidence = getattr(context, 'extraction_confidence', 'medium')
        
        # Count how many pieces of info we're missing
        missing_count = len(missing_info)
        
        if missing_count >= 3:
            # Missing most information - be very friendly and encouraging
            return ("I'm excited to help you find the perfect gift! 🎁\n\n"
                   "To get started, could you tell me:\n\n"
                   "• **What's the occasion?** (birthday, anniversary, holiday, just because, etc.)\n"
                   "• **Who is it for?** (friend, family member, partner, colleague, etc.)\n"
                   "• **What's your budget?** (any range that works for you)\n\n"
                   "Don't worry if you're not sure about everything - we can figure it out together! 😊")
        
        elif missing_count == 2:
            # Missing two pieces - be conversational
            if 'occasion' in missing_info and 'preferences' in missing_info:
                return ("Great start! I can help you find something perfect. Could you tell me:\n\n"
                       "• **What's the special occasion?** (birthday, anniversary, holiday, etc.)\n"
                       "• **Tell me about the person** - what do they like? (hobbies, interests, personality, etc.)")
            
            elif 'occasion' in missing_info and 'budget' in missing_info:
                return ("I'm getting a good sense of what you're looking for! Just need a couple more details:\n\n"
                       "• **What's the occasion?** (birthday, anniversary, holiday, etc.)\n"
                       "• **What's your budget range?** (any range that works for you)")
            
            elif 'preferences' in missing_info and 'budget' in missing_info:
                return ("Perfect! I know the occasion. Now tell me:\n\n"
                       "• **What does this person like?** (interests, hobbies, favorite things, etc.)\n"
                       "• **What's your budget?** (any range that works for you)")
        
        elif missing_count == 1:
            # Missing one piece - be specific and helpful
            if 'occasion' in missing_info:
                return ("I love what you've told me so far! Just one more thing - what's the special occasion? "
                       "(birthday, anniversary, holiday, graduation, or just a thoughtful surprise)")
            
            elif 'preferences' in missing_info:
                return ("Perfect! I know the occasion and budget. Now tell me about the person - "
                       "what do they enjoy? (hobbies, interests, favorite colors, personality, etc.)")
            
            elif 'budget' in missing_info:
                return ("Almost there! What's your budget range? "
                       "(under $50, $50-100, $100-200, or any range that works for you)")
        
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
            context.preferences.budget
        )
        
        context.available_categories = categories
        
        # Create personalized introduction
        occasion = context.preferences.occasion or "this special occasion"
        preferences = context.preferences.preferences or "what you're looking for"
        budget = context.preferences.budget or "your budget"
        
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
            context.preferences.budget,
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
        Call shopping agent to find gifts in a conversational way
        """
        # Generate search ID
        search_id = str(uuid.uuid4())
        
        # Create personalized search message
        category = context.preferences.category
        occasion = context.preferences.occasion
        budget = context.preferences.budget or "your budget"
        preferences = context.preferences.preferences or "what you're looking for"
        
        response = f"Excellent choice! I love the {category} idea for {occasion}! 🎁\n\n"
        response += f"Let me search through multiple marketplaces to find the perfect {category.lower()} gifts that match {preferences} and fit {budget}...\n\n"
        response += "🔍 **Searching for you now...**\n"
        response += "⏳ This might take a moment, but I promise it'll be worth it!\n\n"
        response += "I'm looking for something that will make this {occasion} truly special! ✨"
        
        context.add_message("assistant", response)
        
        # Simulate shopping agent call (replace with actual implementation)
        await self._simulate_shopping_agent_call(context, search_id)
        
        return response
    
    async def _simulate_shopping_agent_call(self, context: ConversationContext, search_id: str):
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
    
    def _acknowledge_learned_info(self, learned_info: List[str], extracted_info: Dict[str, Any]) -> str:
        """
        Acknowledge what we learned from the user in a natural way
        """
        acknowledgments = []
        
        if "occasion" in learned_info:
            occasion = extracted_info.get('occasion', '')
            if occasion.lower() in ['birthday', 'anniversary', 'holiday', 'graduation']:
                acknowledgments.append(f"Perfect! A {occasion} gift - that's so thoughtful! 🎉")
            else:
                acknowledgments.append(f"Great! A {occasion} gift - I love that! 😊")
        
        if "preferences" in learned_info:
            preferences = extracted_info.get('preferences', '')
            if 'mother' in preferences.lower() or 'mom' in preferences.lower():
                acknowledgments.append("Aww, something for your mom - that's so sweet! 💕")
            elif 'girlfriend' in preferences.lower() or 'boyfriend' in preferences.lower():
                acknowledgments.append("How romantic! I'll help you find something special! 💖")
            elif 'friend' in preferences.lower():
                acknowledgments.append("A gift for a friend - that's wonderful! 👫")
            else:
                acknowledgments.append(f"Nice! I can see you're thinking about {preferences} - that's helpful! 👍")
        
        if "budget" in learned_info:
            budget = extracted_info.get('budget', '')
            if 'under' in budget.lower() or 'affordable' in budget.lower():
                acknowledgments.append("Smart budgeting! I'll find something great within your range! 💰")
            elif 'premium' in budget.lower() or 'fancy' in budget.lower():
                acknowledgments.append("Going all out! I love it - let's find something amazing! ✨")
            else:
                acknowledgments.append(f"Perfect! I'll keep your budget of {budget} in mind! 💵")
        
        if len(acknowledgments) == 1:
            return acknowledgments[0]
        elif len(acknowledgments) == 2:
            return f"{acknowledgments[0]} {acknowledgments[1]}"
        else:
            return f"{acknowledgments[0]} {acknowledgments[1]} {acknowledgments[2]}"
