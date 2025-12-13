# Deploying to HuggingFace Spaces

This guide will help you deploy your chatbot to HuggingFace Spaces.

## Prerequisites

- HuggingFace account
- Git installed
- HuggingFace CLI installed: `pip install huggingface_hub`

## Steps

### 1. Login to HuggingFace

```bash
huggingface-cli login
```

### 2. Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - Space name: your-chatbot-name
   - License: MIT
   - Space SDK: **Streamlit**
   - Space hardware: CPU basic (upgrade if needed)

### 3. Clone Your Space Repository

```bash
git clone https://huggingface.co/spaces/<your-username>/<space-name>
cd <space-name>
```

### 4. Copy Project Files

Copy these files from your chatbot template:

```bash
# Core files
cp -r ../chatbot-template/src ./
cp ../chatbot-template/app.py ./
cp ../chatbot-template/requirements.txt ./
cp -r ../chatbot-template/config ./

# Optional: Include sample documents
cp -r ../chatbot-template/data ./
```

### 5. Create `.env` for Secrets

Don't commit `.env` file. Instead, add secrets in HuggingFace Space settings:

1. Go to your Space settings
2. Navigate to "Repository secrets"
3. Add your API keys:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY` (if using)
   - `PINECONE_API_KEY` (if using)
   - etc.

### 6. Modify Configuration (if needed)

Edit `config/config.yaml` to:
- Disable any features that won't work in HF Spaces
- Use appropriate model sizes
- Adjust memory settings

### 7. Create README.md for Space

```markdown
---
title: Your Chatbot Name
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.29.0"
app_file: app.py
pinned: false
---

# Your Chatbot

Description of your chatbot...

## Features

- Feature 1
- Feature 2

## Usage

Simply type your question and get answers!
```

### 8. Push to HuggingFace

```bash
git add .
git commit -m "Initial deployment"
git push
```

### 9. Wait for Build

Your Space will automatically build and deploy. Check the logs in the Space interface.

## Tips

1. **Performance**: Use lighter models for free tier
2. **Persistence**: HF Spaces have limited persistence. Consider:
   - Using Pinecone for vector storage
   - Rebuilding vector DB on startup (with cached documents)
3. **Secrets**: Always use HF Secrets, never commit API keys
4. **Memory**: Free tier has 16GB RAM limit
5. **Sleep Mode**: Free Spaces sleep after inactivity

## Troubleshooting

### Space Won't Start

Check:
- All dependencies in requirements.txt
- API keys are set correctly
- No file path issues (use relative paths)

### Out of Memory

- Reduce model size
- Use smaller embedding models
- Limit vector DB size
- Consider upgrading Space tier

### Slow Performance

- Use CPU-optimized models
- Cache embeddings
- Consider GPU upgrade

## Upgrading Space

For better performance:
1. Go to Space settings
2. Change hardware to GPU (paid)
3. Restart Space
