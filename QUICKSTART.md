# Quick Start Guide

Get your chatbot running in 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Setup Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API keys
# At minimum, you need:
# - OPENAI_API_KEY=your_key_here
```

## 3. Configure Your Chatbot

Edit `config/config.yaml`:

```yaml
llm:
  provider: "openai"
  model: "gpt-4"
  
rag:
  enabled: true
  vector_db: "chromadb"

agents:
  default:
    use_tools: false           # Set true for ReAct reasoning
    enable_web_search: false   # Set true + add TAVILY_API_KEY for web search
```

**Tool System**: 
- `use_tools: false` (default) - Fast, direct responses
- `use_tools: true` - ReAct framework with reasoning + tools:
  - RAG search (knowledge base)
  - Calculator (math operations)
  - Web search (optional, needs Tavily API)
  - Email sender (optional, needs SMTP/SendGrid - both FREE)

## 4. (Optional) Add Documents for RAG

Place your documents in `data/documents/`:

```bash
# Supported formats: .txt, .pdf, .docx, .md
cp your_document.pdf data/documents/
```

## 5. Initialize Vector Database

```bash
python scripts/init_vectordb.py
```

## 6. Run the Chatbot

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

## What's Next?

- **Add more agents**: Edit `config/agents.yaml`
- **Customize UI**: Modify `config/config.yaml` under `ui` section
- **Upload documents**: Use the UI file uploader
- **Run evaluation**: `python scripts/evaluate.py`
- **Deploy**: See deployment guides in `deployment/`

## Troubleshooting

### "No module named 'src'"

Make sure you're running from the project root directory.

### "API key not found"

Check that your `.env` file exists and contains the required keys.

### "No documents to index"

Add documents to `data/documents/` folder before running init_vectordb.py

### Port 8501 already in use

Kill the existing process or use a different port:
```bash
streamlit run app.py --server.port 8502
```

## Need Help?

Check the full README.md or open an issue on GitHub!
