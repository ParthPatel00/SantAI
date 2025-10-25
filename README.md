# 🎁 Gift Expert Agent

A sophisticated AI-powered gift recommendation agent built on the uAgents framework that helps users find the perfect gift for any occasion. The agent uses advanced LLM capabilities with Groq API and integrates with real-time Amazon product search to provide personalized gift recommendations.

## 🎯 Purpose

The Gift Expert Agent is designed to solve the common problem of finding the right gift by:

- **Intelligently collecting user preferences** through natural conversation
- **Understanding context** like occasion, recipient, interests, and budget
- **Providing personalized recommendations** from real Amazon products
- **Guiding users through the entire gift selection process** with an intuitive chat interface

## ✨ Key Functionalities

### 🧠 Intelligent Conversation Management

- **Context-aware parameter extraction** using advanced LLM prompts
- **Global parameter store** that maintains conversation context across interactions
- **Smart parameter validation** that only updates missing information
- **Natural language processing** for understanding user intent and preferences

### 🎯 Preference Collection & Validation

- **Occasion detection**: Birthday, anniversary, wedding, promotion, graduation, etc.
- **Recipient identification**: Mother, father, friend, boss, girlfriend, boyfriend, etc.
- **Interest extraction**: Hobbies, preferences, interests, lifestyle choices
- **Budget parsing**: Handles ranges ($50-100), minimums (under $50), maximums ($100+)

### 🛍️ Real-time Product Search

- **OpenWeb Ninja Amazon Data API integration** for live product data
- **Intelligent search query building** from user preferences
- **Price filtering** based on user budget constraints
- **Product ranking** by relevance and user preferences

### 💬 Dynamic Conversation Flow

- **State management** across conversation stages
- **Category suggestions** based on occasion and preferences
- **Interactive selection** with numbered options
- **Follow-up questions** for missing information
- **Error handling** with graceful fallbacks

### 🎁 Gift Recommendation Engine

- **Top 5 personalized recommendations** with detailed reasoning
- **Product information** including price, rating, availability, and links
- **Category-based filtering** for relevant gift types
- **Budget-optimized suggestions** within user's price range

## 🏗️ Architecture

### Core Components

```
├── agent.py                          # Main uAgent implementation
├── conversation_flow.py              # Conversation state management
├── llm_service.py                    # Groq LLM integration & prompts
├── global_parameters.py              # Global parameter store
├── global_memory.py                  # Conversation memory system
├── shopping_agent_interface.py       # Amazon API integration
├── models.py                         # Data models & structures
├── requirements.txt                  # Python dependencies
└── env_template.txt                  # Environment configuration
```

### Data Flow

1. **User Input** → Conversation Flow Manager
2. **Parameter Extraction** → LLM Service (Groq)
3. **Validation** → Global Parameter Store
4. **Product Search** → Shopping Agent Interface
5. **Recommendations** → User Display
6. **Selection** → Memory Storage

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key
- OpenWeb Ninja API key (for Amazon product search)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd SantAI
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r Gift-expert/requirements.txt
   ```

4. **Configure environment**

   ```bash
   cp Gift-expert/env_template.txt .env
   # Edit .env with your API keys
   ```

5. **Run the agent**
   ```bash
   cd Gift-expert
   python agent.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required API Keys
GROQ_API_KEY=your-groq-api-key-here
OPENWEB_NINJA_API_KEY=your-openweb-ninja-api-key-here

# Agent Configuration
AGENT_SEED=agent-seed-2025-parth-sakshi-devam-new
AGENT_PORT=8000
AGENT_NAME=Gift-Expert

# LLM Configuration
GROQ_MODEL=llama-3.1-8b-instant

# Optional Settings
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### API Keys Setup

1. **Groq API Key**: Get from [Groq Console](https://console.groq.com/keys)
2. **OpenWeb Ninja API Key**: Get from [OpenWeb Ninja](https://openwebninja.com/)

## 💬 Usage Guidelines

### Starting a Conversation

The agent welcomes users with a friendly greeting and asks for:

- **Occasion**: Birthday, anniversary, wedding, etc.
- **Recipient**: Who the gift is for
- **Preferences**: Interests, hobbies, likes
- **Budget**: Price range or specific amount

### Example Conversation Flow

```
User: "I need help finding a gift for my friend's birthday"
Agent: "Perfect! A birthday gift for your friend - that's thoughtful! 🎁
        I'm getting a good sense of what you're looking for! Just need a couple more details:
        • What are their preferences? (hobbies, interests, favorite things, etc.)
        • What's your budget? (e.g., 50-100, under $50, $100+)"

User: "She likes hiking, and my budget is around $50 - $100"
Agent: "Perfect! I'll keep your budget of $50-100 in mind! 💵
        Based on hiking and your budget, here are the categories I think would work best:
        1. Outdoor Gear & Equipment
        2. Hiking Accessories
        3. Adventure Books & Guides
        4. Fitness & Wellness
        5. Nature Photography
        What would you like to do?"
```

### Interaction Options

- **Select by number**: Choose from numbered category options
- **Say "surprise me"**: Let the agent pick a random category
- **Ask for "more options"**: Get additional category suggestions
- **Provide more details**: Share additional preferences or constraints

## 🔍 Advanced Features

### Smart Parameter Extraction

- **Context preservation**: Maintains conversation history across interactions
- **Incremental updates**: Only asks for truly missing information
- **Validation logic**: Prevents overwriting already-collected data
- **Natural language understanding**: Handles various input formats

### Real-time Product Integration

- **Live Amazon data**: Real product availability and pricing
- **Intelligent filtering**: Budget and preference-based product selection
- **Product details**: Complete information including ratings and reviews
- **Direct purchase links**: Seamless transition to Amazon for purchase

### Error Handling & Recovery

- **API failure handling**: Graceful degradation when services are unavailable
- **Input validation**: Robust parsing of user preferences and budget ranges
- **Conversation recovery**: Ability to restart or modify preferences mid-conversation
- **Debug logging**: Comprehensive logging for troubleshooting

## 🛠️ Development

### Project Structure

```
Gift-expert/
├── agent.py                    # Main agent with uAgent framework
├── conversation_flow.py        # Conversation state management
├── llm_service.py             # Groq LLM integration
├── global_parameters.py       # Global parameter store
├── global_memory.py           # Memory management
├── shopping_agent_interface.py # Amazon API integration
├── models.py                  # Data models
├── requirements.txt           # Dependencies
├── env_template.txt           # Environment template
└── README.md                  # Documentation
```

### Key Classes

- **`ConversationFlowManager`**: Manages conversation states and user interactions
- **`LLMService`**: Handles all Groq API interactions and prompt management
- **`GlobalParameters`**: Maintains persistent conversation context
- **`ShoppingAgentInterface`**: Integrates with OpenWeb Ninja Amazon API
- **`UserPreferences`**: Data model for user preferences and gift requirements

### Adding New Features

1. **New Gift Categories**: Modify `get_gift_categories()` in `llm_service.py`
2. **Additional APIs**: Extend `shopping_agent_interface.py`
3. **New Conversation States**: Update `ConversationState` enum in `models.py`
4. **Enhanced Prompts**: Modify prompts in `llm_service.py`

## 🧪 Testing

### Manual Testing

1. Start the agent: `python agent.py`
2. Connect via ASI:One or another agent
3. Follow conversation flow with test inputs
4. Verify parameter extraction and product recommendations

### Debug Mode

Enable debug logging by setting `DEBUG_MODE=true` in your `.env` file.

## 🚨 Troubleshooting

### Common Issues

1. **"GROQ_API_KEY not found"**

   - Ensure `.env` file exists with valid Groq API key
   - Check file permissions and location

2. **"403 Forbidden" from Amazon API**

   - Verify OpenWeb Ninja API key is correct
   - Check API key permissions and quotas

3. **"Address already in use"**

   - Kill existing processes: `lsof -ti:8000 | xargs kill -9`
   - Or change port in agent configuration

4. **Import errors**
   - Ensure virtual environment is activated
   - Install all dependencies: `pip install -r requirements.txt`

### Debug Steps

1. Check environment variables are loaded correctly
2. Verify API keys are valid and have proper permissions
3. Review debug logs for specific error messages
4. Test individual components (LLM, API calls) separately

## 🔮 Future Enhancements

### Planned Features

- **Multi-language support** for global accessibility
- **User authentication** and gift history tracking
- **Advanced filtering** with more sophisticated algorithms
- **Payment integration** for seamless purchase completion
- **Social features** for sharing and collaborative gift selection

### Integration Opportunities

- **Payment agents** for complete purchase flow
- **Calendar integration** for occasion reminders
- **Social media APIs** for preference learning
- **Inventory management** for real-time availability

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contact Information

- **Developer**: Parth Patel
- **Project**: CalHacks SantAI
- **Repository**: [GitHub Repository URL]
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)

## 🙏 Acknowledgments

- **uAgents Framework** for the robust agent infrastructure
- **Groq** for high-performance LLM inference
- **OpenWeb Ninja** for real-time Amazon product data
- **CalHacks** for the hackathon platform and inspiration
- **OpenAI** for foundational LLM research and development

## 📊 Technical Specifications

- **Framework**: uAgents (Python)
- **LLM Provider**: Groq (llama-3.1-8b-instant)
- **Product Data**: OpenWeb Ninja Amazon Data API
- **Architecture**: Microservices with agent-based communication
- **Deployment**: Local development with Agentverse integration
- **Memory**: Thread-safe global parameter store
- **API Integration**: RESTful with async/await patterns

---

**Built with ❤️ for CalHacks 2025**
