# AI Chatbot Template

A production-ready, configurable chatbot template with RAG capabilities, multiple LLM support, and multi-cloud deployment options.

## 🚀 Features

- **LangGraph + ReAct Framework**: State-based orchestration with reasoning and acting capabilities
- **Intelligent Tool System**: RAG search, web search (Tavily), email sending (SMTP/SendGrid), and calculator
- **Streamlit UI**: Clean and intuitive chat interface
- **Agent-Based Architecture**: Configure multiple specialized agents
- **Multiple LLM Support**: OpenAI, Anthropic, Cohere, Azure OpenAI, HuggingFace
- **RAG System**: Retrieval-Augmented Generation with document support
- **Multiple Vector DBs**: ChromaDB (primary), FAISS (optional), or Pinecone (cloud)
- **Configuration-Driven**: No hardcoding, all settings in YAML
- **Multi-Cloud Deployment**: Deploy to HuggingFace, AWS, or Azure
- **Evaluation Framework**: Built-in scripts for LLM performance testing

## 📋 Prerequisites

- Python 3.9+
- API keys for your chosen LLM provider
- (Optional) API keys for vector database services

## 🔧 Quick Start

### 1. Clone this repository

```bash
git clone <your-repo-url>
cd chatbot-template
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Configure your chatbot

Edit `config/config.yaml` to customize:
- LLM provider and model
- Agent behaviors
- RAG settings
- Vector database choice
- UI preferences

### 5. Add your documents (for RAG)

Place your documents in the `data/documents/` folder. Supported formats:
- `.txt`
- `.pdf`
- `.docx`
- `.md`

### 6. Initialize vector database

```bash
python scripts/init_vectordb.py
```

### 7. Run the chatbot

```bash
streamlit run app.py
```

### 8. Access the UI

Open http://localhost:8501 in your browser.

**Default Access:**
- Chat with AI agents (no login required)
- Select different agents
- Clear chat history

**Admin Access:**
- Click **"🔐 Login as Admin to update settings"** in sidebar
- Default admin code: `admin123`
- Set custom code via `ADMIN_CODE` in `.env`

**Admin Features:**
- Toggle individual tools (Calculator, RAG Search, Web Search, Email)
- Try pre-built example prompts for each tool
- Export chat history
- Advanced configuration controls

## 📁 Project Structure

```
chatbot-template/
├── app.py                          # Main Streamlit application
├── config/
│   ├── config.yaml                 # Main configuration file
│   └── agents.yaml                 # Additional agent configurations
├── src/
│   ├── agents/
│   │   ├── base_agent.py          # LangGraph + ReAct agent implementation
│   │   ├── agent_manager.py       # Agent management system
│   │   └── tools.py               # Tool definitions (RAG, web search, calculator)
│   ├── llm/
│   │   └── llm_factory.py         # LLM provider factory
│   ├── rag/
│   │   ├── rag_manager.py         # RAG pipeline management
│   │   └── vectordb/              # Vector database implementations
│   └── utils/                     # Configuration and logging utilities
├── scripts/                       # Utility scripts
├── evaluation/                    # Evaluation framework
├── data/                          # Documents and databases
└── deployment/                    # Multi-cloud deployment configs
```

## 🏗️ Architecture

### LangGraph + ReAct Framework

The chatbot uses **LangGraph** for state-based orchestration and the **ReAct (Reasoning + Acting)** pattern:

1. **Think**: Agent analyzes the question
2. **Act**: Agent decides which tool to use (if any)
3. **Observe**: Agent processes tool results
4. **Repeat**: Until it has the answer

### Available Tools

Each tool can be toggled independently in the admin UI:

- **\ud83e\uddee Calculator**: Performs mathematical operations
  - Example: "I bought 3 items at $45.99 each with 15% discount. What's the total?"
  - No configuration needed
- **\ud83d\udcda RAG Search**: Queries your indexed documents
  - Example: "What is artificial intelligence according to the knowledge base?"
  - Requires documents to be indexed
- **\ud83c\udf10 Web Search**: Searches the internet (optional, requires Tavily API)
  - Example: "What are the latest developments in artificial intelligence?"
  - Requires `TAVILY_API_KEY` in `.env`
- **\ud83d\udce7 Email Sender**: Sends emails via SMTP or SendGrid (optional, configurable whitelist)
  - Example: "Send email to test@example.com about Meeting Reminder"
  - Requires email configuration in `config.yaml`

**UI Features:**
- Individual toggles for each tool (admin mode)
- 2 clickable example prompts per tool
- Real-time tool status indicators

### Agent Modes

**Without Tools** (`use_tools: false`):
- Direct LLM responses
- Faster, simpler
- Good for general Q&A

**With Tools** (`use_tools: true`):
- ReAct reasoning framework
- Tool orchestration
- Better for complex tasks
│   ├── config.yaml                 # Main configuration file
│   └── agents.yaml                 # Additional agent configurations
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Base agent class
│   │   └── agent_manager.py       # Agent management system
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── llm_factory.py         # LLM provider factory
│   │   └── providers/             # Individual LLM providers
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── document_loader.py     # Document loading and processing
│   │   ├── embeddings.py          # Embedding generation
│   │   └── vectordb/              # Vector database implementations
│   ├── ui/
│   │   ├── __init__.py
│   │   └── components.py          # Streamlit UI components
│   └── utils/
│       ├── __init__.py
│       ├── config_loader.py       # Configuration loading utilities
│       └── logger.py              # Logging setup
├── scripts/
│   ├── init_vectordb.py           # Initialize vector database
│   ├── evaluate.py                # Run evaluation suite
│   └── export_chat.py             # Export chat history
├── evaluation/
│   ├── __init__.py
│   ├── evaluator.py               # Evaluation framework
│   └── metrics.py                 # Custom metrics
├── deployment/
│   ├── huggingface/
│   │   ├── Dockerfile
│   │   └── README.md
│   ├── aws/
│   │   ├── cloudformation.yaml
│   │   ├── Dockerfile
│   │   └── README.md
│   └── azure/
│       ├── arm_template.json
│       ├── Dockerfile
│       └── README.md
├── data/
│   ├── documents/                 # Place your documents here
│   ├── evaluation/                # Evaluation datasets and results
│   └── chromadb/                  # ChromaDB persistence (auto-generated)
├── tests/
│   └── test_*.py                  # Unit tests
├── .env.example                   # Environment variables template
├── .gitignore
├── requirements.txt
└── README.md
```

## 🎯 Configuration Guide

### Adding a New Agent

Edit `config/agents.yaml`:

```yaml
agents:
  my_custom_agent:
    name: "My Custom Agent"
    description: "Description of what this agent does"
    system_prompt: "Your custom system prompt here"
    llm_override:
      temperature: 0.7
    use_rag: true
    max_history: 10
```

### Changing LLM Provider

Edit `config/config.yaml`:

```yaml
llm:
  provider: "anthropic"  # Change to your provider
  model: "claude-3-sonnet-20240229"
  temperature: 0.7
  api_key_env: "ANTHROPIC_API_KEY"
```

### Switching Vector Database

Edit `config/config.yaml`:

```yaml
rag:
  vector_db: "chromadb"  # Primary option (also: faiss, pinecone)
  # Update the corresponding settings below
```

### Customizing UI

Edit `config/config.yaml`:

```yaml
ui:
  title: "Your Chatbot Name"
  page_icon: "🤖"
  theme:
    primary_color: "#FF4B4B"
```

## 🧪 Evaluation

Run evaluation on your chatbot:

```bash
python scripts/evaluate.py
```

Create test datasets in `data/evaluation/test_set.json`:

```json
[
  {
    "question": "What is the capital of France?",
    "expected_answer": "Paris",
    "context": "Geography question"
  }
]
```

## 🚀 Deployment

### HuggingFace Spaces

```bash
cd deployment/huggingface
# Follow instructions in deployment/huggingface/README.md
```

### AWS

```bash
cd deployment/aws
# Follow instructions in deployment/aws/README.md
```

### Azure

```bash
cd deployment/azure
# Follow instructions in deployment/azure/README.md
```

## 🧪 Testing

Run tests:

```bash
pytest tests/
```

## 📝 License

MIT License - feel free to use this template for your projects!

## 🤝 Contributing

This is a template repository. Fork it and customize it for your needs!

## 📧 Support

For issues and questions, please open an issue in the GitHub repository.
