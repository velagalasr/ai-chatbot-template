# Complete Setup Guide

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [First Run](#first-run)
5. [Advanced Configuration](#advanced-configuration)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required

- Python 3.9 or higher
- pip package manager
- Git (for version control)
- At least one LLM API key (OpenAI, Anthropic, etc.)

### Optional

- Docker (for containerized deployment)
- AWS/Azure CLI (for cloud deployment)
- CUDA-capable GPU (for local LLM inference)

## Installation

### 1. Clone or Download Repository

If using as a template:
```bash
# On GitHub, click "Use this template" button
# Or clone:
git clone <your-template-repo-url>
cd chatbot-template
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env file with your API keys
```

Required variables:
```env
OPENAI_API_KEY=sk-...
```

Optional variables (depending on your configuration):
```env
ANTHROPIC_API_KEY=...
COHERE_API_KEY=...
PINECONE_API_KEY=...
HUGGINGFACE_API_KEY=...TAVILY_API_KEY=...  # For web search tool

# For email tool (SMTP - FREE)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# OR for email tool (SendGrid - FREE 100/day)
SENDGRID_API_KEY=SG.your-key-here```

### 2. Main Configuration

Edit `config/config.yaml`:

#### Choose LLM Provider

```yaml
llm:
  provider: "openai"  # or anthropic, cohere, azure_openai, huggingface
  model: "gpt-4"      # or gpt-3.5-turbo, claude-3-sonnet, etc.
  temperature: 0.7
  max_tokens: 2000
```

#### Configure RAG

```yaml
rag:
  enabled: true
  vector_db: "chromadb"  # or faiss, pinecone
  chunk_size: 1000
  chunk_overlap: 200
  top_k: 5
  document_path: "./data/documents"
```

#### Customize UI

```yaml
ui:
  title: "My AI Assistant"
  page_icon: "🤖"
  layout: "wide"
```

### 3. Agent Configuration

Edit `config/agents.yaml` to add custom agents:

```yaml
agents:
  my_custom_agent:
    name: "My Custom Agent"
    description: "Specialized for my use case"
    system_prompt: "You are a helpful assistant specialized in..."
    llm_override:
      temperature: 0.5
    use_rag: true
    max_history: 10
```

## First Run

### 1. Add Documents (for RAG)

Place your knowledge base documents in `data/documents/`:

```bash
# Supported formats: .txt, .pdf, .docx, .md
cp your_documents/* data/documents/
```

### 2. Initialize Vector Database

```bash
python scripts/init_vectordb.py
```

This will:
- Load all documents from `data/documents/`
- Split them into chunks
- Generate embeddings
- Store in your configured vector database

### 3. Start the Chatbot

```bash
streamlit run app.py
```

Open your browser to: `http://localhost:8501`

### 4. Test the Chatbot

**Public Access (No login):**
- Select an agent from the sidebar
- Ask questions in chat
- Clear your chat history

**Admin Access:**
- Click "🔐 Login as Admin to update settings"
- Enter admin code (default: `admin123`)
- Toggle individual tools (Calculator, RAG Search, Web Search, Email)
- Click example buttons to try features
- Upload documents (file uploader)
- Export chat history
- Click 🚺 to logout

**Setting Custom Admin Code:**
Add to `.env`:
```env
ADMIN_CODE=your_secure_password
```

## Advanced Configuration

### Multiple Agents

Create specialized agents for different tasks:

```yaml
# config/agents.yaml
agents:
  customer_support:
    name: "Customer Support"
    system_prompt: "You are a customer support agent..."
    use_rag: true
    
  technical_expert:
    name: "Technical Expert"
    system_prompt: "You are a technical expert..."
    llm_override:
      temperature: 0.3
      model: "gpt-4"
```

### Vector Database Options

#### ChromaDB (Default - Local)
```yaml
rag:
  vector_db: "chromadb"
  chromadb:
    persist_directory: "./data/chromadb"
    collection_name: "chatbot_docs"
```

#### FAISS (Fast - Local)
```yaml
rag:
  vector_db: "faiss"
  faiss:
    index_path: "./data/faiss/index"
    index_type: "FlatL2"
```

#### Pinecone (Cloud - Scalable)
```yaml
rag:
  vector_db: "pinecone"
  pinecone:
    api_key_env: "PINECONE_API_KEY"
    environment: "gcp-starter"
    index_name: "chatbot-index"
    dimension: 1536
```

### LLM Provider Setup

#### OpenAI
```yaml
llm:
  provider: "openai"
  model: "gpt-4"
  api_key_env: "OPENAI_API_KEY"
```

#### Anthropic (Claude)
```yaml
llm:
  provider: "anthropic"
  model: "claude-3-sonnet-20240229"
  api_key_env: "ANTHROPIC_API_KEY"
```

#### Azure OpenAI
```yaml
llm:
  provider: "azure_openai"
  model: "gpt-4"
  azure:
    endpoint: "https://your-resource.openai.azure.com/"
    deployment_name: "gpt-4"
    api_version: "2024-02-15-preview"
  api_key_env: "AZURE_OPENAI_API_KEY"
```

## Evaluation

### Run Evaluation Suite

```bash
python scripts/evaluate.py
```

This will:
- Load test cases from `data/evaluation/test_set.json`
- Run each test case through the chatbot
- Calculate performance metrics
- Save results to `data/evaluation/results/`

### Create Custom Test Cases

Edit `data/evaluation/test_set.json`:

```json
[
  {
    "question": "Your test question?",
    "expected_keywords": ["keyword1", "keyword2"],
    "context": "Test description",
    "category": "test_type"
  }
]
```

## Deployment

### Local/Development

```bash
streamlit run app.py
```

### Docker

```bash
# Build image
docker build -t chatbot:latest .

# Run container
docker run -p 8501:8501 --env-file .env chatbot:latest
```

### HuggingFace Spaces

See: [deployment/huggingface/README.md](deployment/huggingface/README.md)

### AWS

See: [deployment/aws/README.md](deployment/aws/README.md)

### Azure

See: [deployment/azure/README.md](deployment/azure/README.md)

## Troubleshooting

### Import Errors

```bash
# Make sure you're in the project root and virtual environment is activated
pip install -r requirements.txt
```

### API Key Errors

Check:
1. `.env` file exists and contains your keys
2. Keys are valid and active
3. No extra spaces or quotes around keys

### Vector Database Issues

```bash
# Clear and reinitialize
rm -rf data/chromadb/  # or data/faiss/
python scripts/init_vectordb.py
```

### Streamlit Issues

```bash
# Clear cache
streamlit cache clear

# Use different port
streamlit run app.py --server.port 8502
```

### Out of Memory

- Use smaller models (gpt-3.5-turbo instead of gpt-4)
- Reduce chunk size in RAG config
- Limit document set size
- Use FAISS instead of ChromaDB for better memory efficiency

### Slow Performance

- Use faster models
- Reduce top_k in RAG config
- Cache embeddings
- Consider cloud vector databases (Pinecone)
- Use GPU for embeddings

## Testing

### Run Unit Tests

```bash
pytest tests/
```

### Run Specific Tests

```bash
pytest tests/test_config.py
pytest tests/test_agents.py -v
```

## Maintenance

### Update Documents

```bash
# Add new documents to data/documents/
cp new_docs/* data/documents/

# Reinitialize vector database
python scripts/init_vectordb.py
```

### Update Configuration

1. Edit `config/config.yaml`
2. Restart application
3. Test changes

### Monitor Logs

Logs are saved to `logs/chatbot.log`:

```bash
tail -f logs/chatbot.log
```

### Backup Important Data

Regularly backup:
- `config/` - Your configurations
- `data/documents/` - Your knowledge base
- `.env` - Your API keys (securely!)
- `data/chromadb/` or `data/faiss/` - Vector database

## Getting Help

1. Check [README.md](README.md) for overview
2. Check [QUICKSTART.md](QUICKSTART.md) for quick setup
3. Review configuration files for options
4. Check logs for error messages
5. Open an issue on GitHub

## Next Steps

- ✅ Customize agents for your use case
- ✅ Add your own documents
- ✅ Adjust LLM parameters
- ✅ Run evaluations
- ✅ Deploy to production
- ✅ Set up monitoring
- ✅ Create custom UI themes

Happy building! 🚀
