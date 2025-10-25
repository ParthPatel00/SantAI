# Gift Agent - uAgent Framework Implementation

This is a comprehensive Gift Agent implementation using the uAgent framework and Groq LLM. The agent helps users find perfect gifts by collecting preferences, suggesting categories, and recommending specific items.

## Features

### Step 1: Interactive Preference Collection
- Collects occasion, preferences, and budget from users
- Provides relevant gift categories based on user input
- Offers "surprise me" option for random category selection
- Allows users to request additional categories

### Step 2: Shopping Agent Integration
- Calls shopping agent with four parameters: occasion, budget, preferences, and category
- Shopping agent searches multiple marketplaces
- Results are sorted and stored in global memory

### Step 3: Gift Recommendation & Selection
- Displays top 5 gift recommendations
- Users can select a gift, request more options, or update preferences
- Handles preference updates and refreshes recommendations

### Step 4: Payment Integration (Placeholder)
- Ready for payment agent integration
- Selected gift information is prepared for payment processing

## File Structure

```
├── agent.py                          # Main agent implementation
├── llm_service.py                    # Groq LLM integration and prompts
├── models.py                         # Data models and structures
├── global_memory.py                  # Global memory system
├── conversation_flow.py              # Conversation flow management
├── shopping_agent_interface.py       # Shopping agent integration
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   Create a `.env` file with:
   ```
   GROQ_API_KEY=your-groq-api-key-here
   ```

3. **Run the Agent**
   ```bash
   python agent.py
   ```

## Key Components

### LLM Service (`llm_service.py`)
- Handles all Groq LLM interactions
- Manages prompt templates for different conversation stages
- Extracts user preferences and generates responses

### Conversation Flow (`conversation_flow.py`)
- Manages the complete conversation flow
- Handles state transitions between different stages
- Integrates with shopping agent and recommendation system

### Global Memory (`global_memory.py`)
- Thread-safe storage for gift search results
- Manages user contexts and conversation history
- Provides data persistence across conversation stages

### Data Models (`models.py`)
- Defines data structures for user preferences, gift items, and recommendations
- Includes conversation state management
- Provides type safety and data validation

## Usage Flow

1. **User starts conversation** → Agent welcomes and asks for preferences
2. **User provides input** → Agent extracts occasion, preferences, budget
3. **Agent shows categories** → User selects category or asks for more options
4. **Shopping agent called** → Searches marketplaces and stores results
5. **Agent shows recommendations** → Top 5 gifts displayed with reasoning
6. **User selects gift** → Agent prepares for payment integration

## Integration Points

### Shopping Agent Integration
The `shopping_agent_interface.py` provides a placeholder for shopping agent integration. To connect with an actual shopping agent:

1. Set the shopping agent address
2. Implement the `call_shopping_agent` method
3. Define the message format for shopping requests

### Payment Agent Integration
The system is ready for payment agent integration. When a user selects a gift, the selected gift information is stored and can be passed to a payment agent.

## Customization

### Adding New Gift Categories
Modify the `get_gift_categories` method in `llm_service.py` to include new categories.

### Modifying Conversation Flow
Update the state handling methods in `conversation_flow.py` to customize the conversation flow.

### Changing LLM Model
Modify the `model` parameter in the `LLMService` class constructor.

## Error Handling

The system includes comprehensive error handling:
- LLM API errors are caught and handled gracefully
- User input parsing errors are managed
- Conversation state errors are handled with fallbacks

## Future Enhancements

1. **Real Shopping Agent Integration**: Replace mock data with actual marketplace APIs
2. **Payment Agent Integration**: Complete the payment flow
3. **User Authentication**: Add user account management
4. **Gift History**: Track user's gift selection history
5. **Advanced Filtering**: Add more sophisticated filtering options
6. **Multi-language Support**: Add support for multiple languages

## Testing

The system includes mock data for testing without external dependencies. To test:

1. Run the agent
2. Connect via ASI:One or another agent
3. Follow the conversation flow with test inputs

## Troubleshooting

### Common Issues

1. **Groq API Key Error**: Ensure `GROQ_API_KEY` is set in environment variables
2. **Import Errors**: Ensure all dependencies are installed
3. **Agent Connection Issues**: Check agent address and network connectivity

### Debug Mode

Enable debug logging by modifying the agent configuration in `agent.py`.
