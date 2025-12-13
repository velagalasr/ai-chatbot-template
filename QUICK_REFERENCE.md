# 🚀 Quick Reference Card

**AI Chatbot Template - Cheat Sheet**

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Setup
make setup

# 2. Add API key to .env
OPENAI_API_KEY=sk-your-key-here

# 3. Initialize database
make init-db

# 4. Run
make run
```

Access at: **http://localhost:8501**

---

## 📋 Common Commands

| Command | Purpose |
|---------|---------|
| `make setup` | First-time setup |
| `make run` | Start chatbot |
| `make test` | Run tests |
| `make eval` | Run evaluation |
| `make verify` | Check environment |
| `make docker` | Build Docker image |
| `make docker-up` | Start with Docker |
| `make clean` | Clean temp files |
| `make help` | Show all commands |

---

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `.env` | API keys & secrets |
| `config/config.yaml` | Main settings |
| `config/agents.yaml` | Agent definitions |
| `.streamlit/config.toml` | UI customization |

---

## 🤖 Supported LLM Providers

| Provider | Model Examples | API Key |
|----------|----------------|---------|
| **OpenAI** | gpt-4, gpt-3.5-turbo | `OPENAI_API_KEY` |
| **Anthropic** | claude-3-opus, claude-3-sonnet | `ANTHROPIC_API_KEY` |
| **Cohere** | command, command-light | `COHERE_API_KEY` |
| **Azure OpenAI** | Same as OpenAI | `AZURE_OPENAI_API_KEY` |
| **HuggingFace** | llama-2, mistral, etc. | `HUGGINGFACE_API_KEY` |

---

## 💾 Vector Databases

| Database | Type | Best For | Setup |
|----------|------|----------|-------|
| **ChromaDB** | Local | Development | Auto-created |
| **FAISS** | Local | Fast search | Auto-created |
| **Pinecone** | Cloud | Production | Needs API key |

---

## 🛠️ Available Tools

| Tool | Purpose | Required Config |
|------|---------|-----------------|
| **RAG Search** | Search knowledge base | Enable RAG |
| **Calculator** | Math operations | Always available |
| **Web Search** | Internet search | `TAVILY_API_KEY` |
| **Email** | Send emails | SMTP or SendGrid |

---

## 📧 Email Tool Setup

### Gmail (FREE)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### SendGrid (FREE tier)
```env
SENDGRID_API_KEY=SG.your-key-here
```

### Enable in config.yaml
```yaml
email:
  enabled: true
  allowed_recipients:
    - "user@example.com"
```

---

## 🎨 Agent Configuration

```yaml
agents:
  my_agent:
    name: "My Custom Agent"
    description: "What this agent does"
    system_prompt: "You are a helpful assistant."
    use_rag: true           # Enable RAG
    use_tools: true         # Enable ReAct tools
    enable_web_search: true # Enable web search
    max_history: 10         # Conversation memory
```

---

## 🐳 Docker Commands

```bash
# Build image
docker build -t ai-chatbot:latest .

# Run container
docker run -p 8501:8501 --env-file .env ai-chatbot:latest

# Or use docker-compose
docker-compose up -d
docker-compose down
docker-compose logs -f
```

---

## 📁 Project Structure

```
chatbot-template/
├── app.py                 # Main app
├── requirements.txt       # Dependencies
├── Dockerfile            # Container
├── docker-compose.yml    # Orchestration
├── Makefile             # Commands
├── .env                 # Secrets (create from .env.example)
│
├── config/              # Configuration
│   ├── config.yaml
│   └── agents.yaml
│
├── src/                 # Source code
│   ├── agents/         # Agent system
│   ├── llm/           # LLM providers
│   ├── rag/           # RAG system
│   ├── ui/            # UI components
│   └── utils/         # Utilities
│
├── data/               # Data storage
│   ├── documents/     # Your documents
│   ├── chromadb/      # Vector DB
│   └── evaluation/    # Test data
│
├── scripts/            # Utility scripts
├── tests/             # Unit tests
└── deployment/        # Cloud configs
```

---

## 🚀 Deployment Quick Start

### HuggingFace Spaces
```bash
cd deployment/huggingface
# Follow README.md
```

### AWS ECS
```bash
cd deployment/aws
# Configure AWS CLI first
# Follow README.md
```

### Azure Container Instances
```bash
cd deployment/azure
# Configure Azure CLI first
# Follow README.md
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_agents.py -v

# Run with coverage
pytest --cov=src tests/

# Skip slow tests
pytest -m "not slow" tests/
```

---

## 📊 Evaluation

```bash
# Run evaluation
python scripts/evaluate.py

# Results saved to:
data/evaluation/results/
```

---

## 🔍 Troubleshooting

### Can't import modules
```bash
# Ensure you're in project root
cd "c:\Gen AI\Chatbot template"

# Reinstall dependencies
make install
```

### API key errors
```bash
# Verify .env file exists
dir .env

# Check API key format
# OpenAI: sk-...
# Anthropic: sk-ant-...
```

### Port already in use
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Vector DB errors
```bash
# Reinitialize database
python scripts/init_vectordb.py

# Or delete and recreate
rmdir /s data\chromadb
python scripts/init_vectordb.py
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview |
| `GETTING_STARTED.md` | First steps |
| `QUICKSTART.md` | 5-minute guide |
| `SETUP.md` | Complete setup |
| `USAGE.md` | Detailed usage |
| `TECH_STACK.md` | Technology docs |
| `PROJECT_REVIEW.md` | Completion report |

---

## 🔗 Important Links

- **LangChain Docs**: https://python.langchain.com/docs
- **LangGraph Guide**: https://langchain-ai.github.io/langgraph/
- **Streamlit Docs**: https://docs.streamlit.io
- **OpenAI API**: https://platform.openai.com/docs
- **Tavily Search**: https://tavily.com/
- **SendGrid**: https://sendgrid.com/

---

## 💡 Pro Tips

1. **Start Simple**: Disable tools initially, test basic chat first
2. **Use ChromaDB**: Fastest to get started for development
3. **Test API Keys**: Run `make verify` after adding keys
4. **Monitor Costs**: Check LLM usage regularly
5. **Chunk Carefully**: 500-1000 chars works well for most docs
6. **Version Control**: Use git for config changes
7. **Log Everything**: Check `logs/chatbot.log` for debugging
8. **Docker First**: Test in Docker before cloud deployment

---

## ⚠️ Common Mistakes

❌ Forgetting to copy `.env.example` to `.env`  
❌ Not initializing vector database before use  
❌ Using wrong API key format  
❌ Enabling tools without required API keys  
❌ Putting large files in documents without chunking  
❌ Not reading the logs when errors occur  
❌ Hardcoding values instead of using config  
❌ Skipping the verify step after installation

---

## ✅ Pre-Production Checklist

- [ ] All API keys in `.env`
- [ ] Documents indexed with `make init-db`
- [ ] Tests pass with `make test`
- [ ] Evaluation run with `make eval`
- [ ] Custom agents configured
- [ ] Tools tested individually
- [ ] Docker build successful
- [ ] Logs reviewed for errors
- [ ] Cost limits set on LLM providers
- [ ] Backup strategy for vector DB

---

## 📞 Support

- **Documentation**: See `docs/` folder
- **Issues**: Check logs first (`logs/chatbot.log`)
- **Config Problems**: Run `make verify`
- **API Errors**: Check `.env` file

---

**Quick Reference Version 1.0 | December 2025**
