# 🎯 Complete Usage Guide

This guide covers everything you need to know to use and customize your chatbot template.

## 📚 Table of Contents

1. [Basic Usage](#basic-usage)
2. [Configuration](#configuration)
3. [Agent Management](#agent-management)
4. [RAG System](#rag-system)
5. [Evaluation](#evaluation)
6. [Deployment](#deployment)
7. [Advanced Topics](#advanced-topics)

---

## Basic Usage

### Starting the Chatbot

```bash
# Activate virtual environment (if using)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Start the application
streamlit run app.py
```

### First-Time Setup Verification

```bash
# Verify your setup
python scripts/verify_setup.py
```

This will check:
- ✅ Python version
- ✅ Dependencies installed
- ✅ Environment variables configured
- ✅ Configuration files present
- ✅ Directory structure
- ✅ Module imports

### Using the UI

1. **Select Agent**: Choose from sidebar dropdown
2. **Ask Questions**: Type in chat input at bottom
3. **Upload Documents**: Use expander to add files
4. **View Stats**: Check statistics panel
5. **Clear Chat**: Use sidebar button
6. **Export History**: Save conversation to file

### Admin Authentication

The UI includes an authentication system to protect configuration changes:

**Accessing Admin Mode:**
1. Click **"🔐 Login as Admin to update settings"** in the sidebar
2. Enter admin code (default: `admin123`)
3. Click "Login"

**Admin Code Configuration:**
```env
# Add to .env file
ADMIN_CODE=your_secure_password
```

**Features Available in Admin Mode:**

#### Individual Tool Controls
Each tool can be toggled independently:

| Tool | Description | Requirements |
|------|-------------|-------------|
| 🧮 **Calculator** | Mathematical operations | None |
| 📚 **RAG Search** | Knowledge base search | Documents indexed |
| 🌐 **Web Search** | Internet search via Tavily | TAVILY_API_KEY |
| 📧 **Email** | Send emails | Email config in config.yaml |

#### Tool Examples
Each enabled tool shows 2 clickable example prompts:

**Calculator Examples:**
- "📊 Calculate discount" → Calculates 3 items at $45.99 with 15% discount
- "🔢 Complex math" → Evaluates (25 * 8 + 150) / 5 - 20

**RAG Search Examples:**
- "📖 Search docs" → Searches for AI definition in knowledge base
- "🔍 Find info" → Searches for machine learning information

**Web Search Examples:**
- "🌍 Current events" → Latest AI developments
- "📈 Market info" → Today's technology news

**Email Examples:**
- "✉️ Meeting reminder" → Sends meeting notification
- "📝 Status update" → Sends project update email

**Clicking an example button** automatically sends that prompt through the chat interface.

#### Admin Controls
- **♻️ Reset All**: Clears all sessions and history
- 💾 **Export Chat**: Download conversation history
- **🚺 Logout**: Exit admin mode

### Public Features (No Login Required)

Users without admin access can still:
- Chat with the AI agents
- Select different agents
- Clear their own chat history
- View basic RAG system status

### RAG System Status

The sidebar shows two separate indicators:

**For Everyone:**
- **Vector DB Status**: Whether ChromaDB is available (✅/⚠️)
- **Documents Indexed**: Count of document chunks

**For Admins Only:**
- **RAG Search Tool Status**: Whether agents can use search tool (🟢/🔴)
- This changes when you toggle the RAG Search tool on/off

---

## Configuration

### Environment Variables (.env)

```env
# Required for OpenAI
OPENAI_API_KEY=sk-...

# Optional - Only if using
ANTHROPIC_API_KEY=sk-ant-...
COHERE_API_KEY=...
PINECONE_API_KEY=...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://...
# Optional - For web search tool (requires use_tools: true, enable_web_search: true)
TAVILY_API_KEY=tvly-...```

### Main Configuration (config/config.yaml)

#### LLM Settings

```yaml
llm:
  provider: "openai"          # openai, anthropic, cohere, azure_openai
  model: "gpt-4"              # Model name
  temperature: 0.7            # 0.0-1.0, higher = more creative
  max_tokens: 2000           # Maximum response length
  api_key_env: "OPENAI_API_KEY"  # Environment variable name
```

**Temperature Guide:**
- `0.0-0.3`: Factual, deterministic
- `0.4-0.7`: Balanced (recommended)
- `0.8-1.0`: Creative, diverse

#### RAG Settings

```yaml
rag:
  enabled: true
  vector_db: "chromadb"      # chromadb, faiss, pinecone
  chunk_size: 1000           # Characters per chunk
  chunk_overlap: 200         # Overlap between chunks
  top_k: 5                   # Number of relevant chunks to retrieve
  similarity_threshold: 0.7  # Minimum similarity score (0.0-1.0)
  document_path: "./data/documents"

#### Agent Tool Settings

```yaml
agents:
  default:
    name: "General Assistant"
    use_rag: true              # Use RAG for document retrieval
    use_tools: false           # Enable/disable ReAct framework with tools
    enable_web_search: false   # Enable web search tool (requires TAVILY_API_KEY)
    max_history: 10
```

**Tool System (ReAct Framework):**

When `use_tools: true`, agents use LangGraph + ReAct for reasoning:
- **RAG Search Tool**: Searches your knowledge base (always available if `use_rag: true`)
- **Calculator Tool**: Performs mathematical calculations (always available)
- **Web Search Tool**: Searches the internet via Tavily (requires `enable_web_search: true` and `TAVILY_API_KEY`)

**When to use tools:**
- Set `use_tools: true` for complex reasoning tasks
- Set `use_tools: false` for simple Q&A (faster, more direct responses)

**Tool Configuration:**
```yaml
use_tools: true               # Enable ReAct framework
enable_web_search: true       # Enable web search
```

#### Email Tool Settings

```yaml
email:
  enabled: false  # Set to true to enable email sending
  provider: "smtp"  # Options: smtp, sendgrid
  from_email: "chatbot@example.com"
  from_name: "AI Chatbot Assistant"
  
  # Recipient whitelist
  allowed_recipients:
    - "user1@example.com"
    - "admin@company.com"
  
  allow_any_email: false  # Set true to allow any email address
  
  # SMTP settings (for provider: smtp)
  smtp_host: "smtp.gmail.com"
  smtp_port: 587
```

**Email Tool Features:**
- **Whitelist Mode**: Restrict emails to specific recipients only
- **Open Mode**: Set `allow_any_email: true` to send to any valid email
- **SMTP Support**: Use Gmail, Outlook, or any SMTP server (FREE)
- **SendGrid Support**: Use SendGrid API (100 emails/day FREE)
- **Natural Language**: Agent understands requests like "Send email to john@example.com about Meeting with message: See you at 2pm"

**Environment Variables:**
```env
# For SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# For SendGrid
SENDGRID_API_KEY=SG.your-key-here
```

**Gmail Setup (FREE):**
1. Enable 2-Step Verification in Google Account
2. Generate App Password: Security → 2-Step Verification → App passwords
3. Use app password as SMTP_PASSWORD

**SendGrid Setup (FREE 100 emails/day):**
1. Sign up at https://sendgrid.com/
2. Create API key in Settings → API Keys
3. Add to SENDGRID_API_KEY
```

**Chunk Size Guide:**
- Small (500): Better precision, more chunks
- Medium (1000): Balanced (recommended)
- Large (2000): Better context, fewer chunks

#### UI Settings

```yaml
ui:
  title: "AI Chatbot Assistant"
  page_icon: "🤖"
  layout: "wide"              # wide or centered
  sidebar:
    show_agent_selector: true
    show_rag_status: true
    show_settings: true
  theme:
    primary_color: "#FF4B4B"
```

---

## Agent Management

### Understanding Agents

Agents are specialized AI personalities with:
- **Name**: Display name
- **Description**: What the agent does
- **System Prompt**: Instructions for behavior
- **LLM Override**: Optional custom LLM settings
- **RAG Usage**: Whether to use RAG
- **Max History**: Conversation context length

### Creating a New Agent

Edit `config/agents.yaml`:

```yaml
agents:
  customer_service:
    name: "Customer Service Agent"
    description: "Handles customer inquiries professionally"
    system_prompt: |
      You are a professional customer service representative.
      Be friendly, helpful, and empathetic.
      Always try to resolve issues effectively.
      If you don't know something, admit it honestly.
    llm_override:
      temperature: 0.6        # Slightly lower for consistency
      max_tokens: 1500
    use_rag: true            # Use knowledge base
    max_history: 20          # Remember last 20 messages
```

### Agent Templates

#### Technical Support Agent

```yaml
technical_support:
  name: "Technical Support"
  description: "Troubleshoots technical issues"
  system_prompt: |
    You are a technical support specialist.
    Provide step-by-step troubleshooting instructions.
    Ask clarifying questions when needed.
    Be patient and thorough.
  llm_override:
    temperature: 0.3        # Very deterministic
  use_rag: true
  max_history: 15
```

#### Sales Agent

```yaml
sales_agent:
  name: "Sales Assistant"
  description: "Helps with product information and recommendations"
  system_prompt: |
    You are a knowledgeable sales assistant.
    Help customers find the right products.
    Ask about needs and preferences.
    Provide honest recommendations.
  llm_override:
    temperature: 0.7
  use_rag: true
  max_history: 15
```

#### Creative Writer

```yaml
creative_writer:
  name: "Creative Writer"
  description: "Helps with creative writing tasks"
  system_prompt: |
    You are a creative writing assistant.
    Help brainstorm ideas, develop characters, and craft stories.
    Be imaginative and encouraging.
  llm_override:
    temperature: 0.9        # High for creativity
    max_tokens: 3000
  use_rag: false           # Don't need RAG for creative tasks
  max_history: 10
```

---

## RAG System

### Adding Documents

#### Supported Formats

- `.txt` - Plain text
- `.pdf` - PDF documents
- `.docx` - Word documents
- `.md` - Markdown files

#### Adding via File System

```bash
# Copy files to documents folder
cp my_document.pdf data/documents/

# Or organize in subdirectories
mkdir data/documents/product_docs
cp *.pdf data/documents/product_docs/

# Initialize/update vector database
python scripts/init_vectordb.py
```

#### Adding via UI

1. Click "📤 Upload Documents" expander
2. Select files (can select multiple)
3. Click "Process Documents"
4. Wait for confirmation

### Vector Database Options

#### ChromaDB (Recommended for Starting)

**Pros:**
- Easy setup, no configuration needed
- Fast for small to medium datasets
- Local, no API keys required
- Good for development

**Cons:**
- Not suitable for very large datasets
- No built-in scalability

**Configuration:**
```yaml
rag:
  vector_db: "chromadb"
  chromadb:
    persist_directory: "./data/chromadb"
    collection_name: "chatbot_docs"
```

#### FAISS (Fast, Facebook AI)

**Pros:**
- Very fast similarity search
- Efficient memory usage
- Good for large datasets
- Local, no API keys

**Cons:**
- Slightly more complex
- Manual saving required

**Configuration:**
```yaml
rag:
  vector_db: "faiss"
  faiss:
    index_path: "./data/faiss/index"
    index_type: "FlatL2"    # or HNSW for large datasets
```

#### Pinecone (Cloud-based)

**Pros:**
- Highly scalable
- Managed service
- Great for production
- Global availability

**Cons:**
- Requires API key
- Costs money (has free tier)
- Network latency

**Configuration:**
```yaml
rag:
  vector_db: "pinecone"
  pinecone:
    api_key_env: "PINECONE_API_KEY"
    environment: "gcp-starter"
    index_name: "chatbot-index"
    dimension: 1536          # Must match embedding model
```

### RAG Best Practices

1. **Chunk Size**: 
   - Technical docs: 500-800
   - General content: 1000-1500
   - Long-form: 1500-2000

2. **Overlap**:
   - Use 10-20% of chunk size
   - Prevents context loss at boundaries

3. **Top-K**:
   - Start with 3-5
   - Increase for broader context
   - Decrease for focused responses

4. **Document Organization**:
   - Group related documents
   - Use clear file names
   - Update regularly

---

## Evaluation

### Running Evaluations

```bash
# Run evaluation suite
python scripts/evaluate.py
```

### Creating Test Cases

Edit `data/evaluation/test_set.json`:

```json
[
  {
    "question": "What is your return policy?",
    "expected_keywords": ["return", "days", "refund", "policy"],
    "expected_answer": "Brief expected answer",
    "context": "Customer service question",
    "category": "policy"
  }
]
```

### Understanding Metrics

- **Keyword Score**: Presence of expected terms
- **Coherence Score**: Response structure and quality
- **Relevance Score**: Alignment with question
- **Length Score**: Appropriate response length
- **Overall Score**: Weighted average

### Interpreting Results

```
Average Overall Score: 0.85 (85%)
```

- **0.9-1.0**: Excellent
- **0.7-0.9**: Good
- **0.5-0.7**: Acceptable
- **< 0.5**: Needs improvement

---

## Deployment

### Local Development

```bash
streamlit run app.py
```

### Docker

```bash
# Build
docker build -t my-chatbot .

# Run
docker run -p 8501:8501 --env-file .env my-chatbot
```

### Cloud Deployment

See detailed guides:
- [HuggingFace Spaces](deployment/huggingface/README.md)
- [AWS](deployment/aws/README.md)
- [Azure](deployment/azure/README.md)

---

## Advanced Topics

### Custom Embeddings

```yaml
rag:
  embeddings:
    provider: "huggingface"
    huggingface:
      model_id: "sentence-transformers/all-mpnet-base-v2"
```

### Agent-Specific LLM Settings

```yaml
agents:
  precise_agent:
    name: "Precise Agent"
    llm_override:
      model: "gpt-4"
      temperature: 0.2
      max_tokens: 1000
```

### Multiple Vector Databases

Switch easily by changing one line:

```yaml
rag:
  vector_db: "faiss"    # Just change this
```

### Logging

Configure in `config/config.yaml`:

```yaml
logging:
  level: "INFO"          # DEBUG, INFO, WARNING, ERROR
  file: "./logs/chatbot.log"
  max_bytes: 10485760    # 10MB
  backup_count: 5
```

View logs:
```bash
tail -f logs/chatbot.log
```

---

## Troubleshooting

### Common Issues

#### "Module not found"
```bash
pip install -r requirements.txt
```

#### "API key invalid"
- Check `.env` file
- Verify key is correct
- Check API key status on provider website

#### "No documents found"
- Add files to `data/documents/`
- Run `python scripts/init_vectordb.py`

#### "Out of memory"
- Use smaller model
- Reduce chunk_size
- Limit document set

### Getting Help

1. Check documentation
2. Review configuration
3. Check logs
4. Run verify_setup.py
5. Open GitHub issue

---

## Tips & Best Practices

1. **Start Simple**: Use defaults, then customize
2. **Test Locally**: Before deploying
3. **Monitor Costs**: Track API usage
4. **Update Regularly**: Keep dependencies current
5. **Backup Data**: Save configurations and documents
6. **Use Git**: Track changes
7. **Document Changes**: Note customizations
8. **Test Agents**: Use evaluation framework

---

**Need more help?** Check other documentation files or open an issue!
