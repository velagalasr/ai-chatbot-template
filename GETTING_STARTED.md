# 🚀 Getting Started - First Steps

Welcome! Follow these steps to get your chatbot running in minutes.

## Step 1: Install Python Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Streamlit (UI framework)
- LangGraph (State-based orchestration)
- LangChain (LLM wrappers and tools)
- ChromaDB (vector database)
- OpenAI client
- And more...

## Step 2: Configure API Keys

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in a text editor

3. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

   Get a key from: https://platform.openai.com/api-keys

4. **(Optional)** For web search capabilities, add Tavily API key:
   ```
   TAVILY_API_KEY=tvly-your-key-here
   ```

   Get a free key from: https://tavily.com/
   
   > **Note**: Web search is optional and disabled by default. The chatbot works fine without it.

5. **(Optional)** For email sending capabilities:
   ```
   # For SMTP (Gmail, Outlook - FREE)
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   
   # OR for SendGrid (FREE tier available)
   SENDGRID_API_KEY=SG.your-key-here
   ```
   
   > **Note**: Email tool is optional and disabled by default. Both SMTP and SendGrid have free tiers!

## Step 3: Review Configuration (Optional)

The default configuration in `config/config.yaml` is ready to use, but you can customize:

- **LLM Model**: Change from `gpt-4` to `gpt-3.5-turbo` for faster/cheaper responses
- **Agent Behavior**: Edit agent personalities in `config/agents.yaml`
- **ReAct Tools**: Enable `use_tools: true` for reasoning + acting capabilities
  - RAG search tool (searches your knowledge base)
  - Calculator tool (for math operations)
  - Web search tool (requires Tavily API key)
  - Email sending tool (requires SMTP or SendGrid - both FREE)
- **UI Settings**: Modify title, colors, etc.

### UI Features

The chatbot interface includes:

- **Public Mode**: Anyone can chat with agents
- **Admin Mode**: Protected settings access
  - Login with admin code (default: `admin123`)
  - Configure tools individually (4 separate toggles)
  - Try pre-built example prompts (2 per tool)
  - Access advanced controls

To set a custom admin password:
```env
ADMIN_CODE=your_secure_password
```

## Step 4: Initialize Knowledge Base

The template includes sample documents. To index them:

```bash
python scripts/init_vectordb.py
```

You'll see output like:
```
INFO - Loading and processing documents...
INFO - Split 2 documents into 15 chunks
INFO - Successfully indexed 15 document chunks
✅ Vector database initialization complete!
```

## Step 5: Start the Chatbot

```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501`

## Step 6: Try It Out!

1. **Select an Agent**: Use the sidebar to choose different agents
2. **Ask a Question**: Type something like "What is artificial intelligence?"
3. **Upload Documents**: Use the file uploader to add more knowledge
4. **Export Chat**: Save your conversation history

## What's Next?

### Add Your Own Documents

1. Place files in `data/documents/` folder
2. Supported formats: `.txt`, `.pdf`, `.docx`, `.md`
3. Run: `python scripts/init_vectordb.py`

### Create Custom Agents

Edit `config/agents.yaml`:

```yaml
agents:
  my_expert:
    name: "Domain Expert"
    description: "Expert in [your domain]"
    system_prompt: "You are an expert in..."
    use_rag: true
```

### Test Performance

```bash
python scripts/evaluate.py
```

### Deploy to Cloud

See deployment guides in:
- `deployment/huggingface/README.md` - Easiest option
- `deployment/aws/README.md` - AWS deployment
- `deployment/azure/README.md` - Azure deployment

## Common Issues

### "No module named 'streamlit'"

Make sure you installed requirements:
```bash
pip install -r requirements.txt
```

### "API key not found"

Check that:
1. `.env` file exists (copy from `.env.example`)
2. Your API key is correct
3. No extra spaces around the key

### "No documents found"

Add documents to `data/documents/` folder before running `init_vectordb.py`

### Port 8501 already in use

Use a different port:
```bash
streamlit run app.py --server.port 8502
```

## Getting Help

- 📖 Read [README.md](README.md) for full documentation
- 🚀 Check [QUICKSTART.md](QUICKSTART.md) for quick reference
- ⚙️ See [SETUP.md](SETUP.md) for detailed configuration
- 💬 Open an issue on GitHub for support

## Tips for Success

1. **Start Simple**: Use default configuration first
2. **Test Locally**: Make sure everything works before deploying
3. **Add Documents Gradually**: Start with a few, then expand
4. **Monitor Costs**: GPT-4 is expensive, consider GPT-3.5-turbo for testing
5. **Iterate**: Test, get feedback, improve

---

**You're all set! Start building amazing chatbots!** 🎉

Need help? Check the documentation or open an issue.
