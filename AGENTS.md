# 🤖 Agent Guide - Understanding Your AI Assistants

This template comes with **6 pre-configured agents**, each with a unique personality and specialization. This guide explains what each agent does, when to use them, and how they work under the hood.

## 📋 Quick Overview

| Agent | Temperature | Best For | Memory | Max Tokens |
|-------|-------------|----------|--------|------------|
| General Assistant | 0.7 | General questions, casual chat | 10 exchanges | 2000 |
| Technical Support | 0.3 | Technical problems, debugging | 15 exchanges | 2000 |
| Code Assistant | 0.5 | Programming help, code examples | 10 exchanges | 2000 |
| Customer Service | 0.6 | Customer inquiries, support | 20 exchanges | 1500 |
| Sales Assistant | 0.7 | Product recommendations, sales | 15 exchanges | 2000 |
| Research Assistant | 0.4 | Research, complex topics | 10 exchanges | 3000 |

---

## 🎯 The 6 Pre-Configured Agents

### 1. **General Assistant** (default)

**Configuration File:** `config/config.yaml` → `agents.default`

**Personality:** Helpful, general-purpose AI assistant

**Best For:**
- General questions
- Casual conversation
- When you're not sure which agent to use
- Quick answers

**Key Settings:**
- **Temperature:** 0.7 (balanced creativity)
- **Memory:** Remembers last 10 exchanges
- **RAG:** ✅ Enabled (searches knowledge base)
- **Tools:** ❌ Disabled (no calculator, web search)

**Example Use Cases:**
- "What is artificial intelligence?"
- "Explain the concept of machine learning"
- "Help me understand this topic"

**System Prompt:**
```
You are a helpful AI assistant. Answer questions accurately and concisely.
```

---

### 2. **Technical Support Agent**

**Configuration File:** `config/config.yaml` → `agents.technical_support`

**Personality:** Methodical troubleshooter, technical expert

**Best For:**
- Technical problems
- Step-by-step guides
- Debugging issues
- Software/hardware troubleshooting
- Error message explanations

**Key Settings:**
- **Temperature:** 0.3 (very precise, consistent)
- **Memory:** Remembers last 15 exchanges (more context for complex issues)
- **RAG:** ✅ Enabled
- **Tools:** ❌ Disabled

**Example Use Cases:**
- "My application keeps crashing, how do I debug it?"
- "Walk me through setting up a database"
- "What does this error message mean?"

**System Prompt:**
```
You are a technical support specialist. Help users troubleshoot issues with clear, 
step-by-step instructions.
```

---

### 3. **Code Assistant**

**Configuration File:** `config/config.yaml` → `agents.code_assistant`

**Personality:** Expert programmer, clear explainer

**Best For:**
- Programming help
- Code examples
- Code explanations
- Best practices
- Algorithm design

**Key Settings:**
- **Temperature:** 0.5 (balanced - creative but precise)
- **Memory:** Remembers last 10 exchanges
- **RAG:** ✅ Enabled (can search code documentation)
- **Tools:** ❌ Disabled

**Example Use Cases:**
- "How do I implement a binary search in Python?"
- "Explain this code snippet"
- "What's the best way to handle authentication?"

**System Prompt:**
```
You are an expert programming assistant. Provide clear code examples and explanations.
```

---

### 4. **Customer Service Agent**

**Configuration File:** `config/agents.yaml` → `agents.customer_service`

**Personality:** Friendly, professional, empathetic

**Best For:**
- Customer inquiries
- Support tickets
- Product information
- Issue resolution
- Complaints handling

**Key Settings:**
- **Temperature:** 0.6 (warm and personable)
- **Memory:** Remembers last 20 exchanges (longest memory for detailed conversations)
- **Max Tokens:** 1500
- **RAG:** ✅ Enabled
- **Tools:** ❌ Disabled

**Example Use Cases:**
- "I have a problem with my order"
- "What features does this product have?"
- "Can you help me with a refund?"

**System Prompt:**
```
You are a friendly and professional customer service representative.
Help customers with their inquiries, provide product information, and resolve issues.
Always maintain a positive and helpful tone.
```

---

### 5. **Sales Assistant**

**Configuration File:** `config/agents.yaml` → `agents.sales_agent`

**Personality:** Knowledgeable product expert, consultative

**Best For:**
- Product recommendations
- Features and pricing questions
- Needs assessment
- Product comparisons
- Sales inquiries

**Key Settings:**
- **Temperature:** 0.7 (engaging and persuasive)
- **Memory:** Remembers last 15 exchanges
- **RAG:** ✅ Enabled (can access product catalogs)
- **Tools:** ❌ Disabled

**Example Use Cases:**
- "What product would you recommend for my needs?"
- "Compare these two products for me"
- "What's included in the premium package?"

**System Prompt:**
```
You are a knowledgeable sales assistant.
Help customers find the right products based on their needs.
Provide detailed product information and answer questions about features and pricing.
```

---

### 6. **Research Assistant**

**Configuration File:** `config/agents.yaml` → `agents.research_assistant`

**Personality:** Academic researcher, detail-oriented

**Best For:**
- Research questions
- Complex topics
- Academic explanations
- Citations and sources
- In-depth analysis

**Key Settings:**
- **Temperature:** 0.4 (very factual and accurate)
- **Memory:** Remembers last 10 exchanges
- **Max Tokens:** 3000 (can give longer, detailed responses)
- **RAG:** ✅ Enabled
- **Tools:** ❌ Disabled

**Example Use Cases:**
- "Research the history of neural networks"
- "Explain quantum computing in detail"
- "What are the latest findings on this topic?"

**System Prompt:**
```
You are a research assistant with expertise in finding and synthesizing information.
Provide well-researched, accurate answers with citations when possible.
Break down complex topics into understandable explanations.
```

---

## 📊 Detailed Comparison

### Temperature Settings (Creativity Level)

| Temperature | Agents | Behavior |
|-------------|--------|----------|
| **0.3** | Technical Support | Very consistent, deterministic, precise answers |
| **0.4** | Research Assistant | Factual, accurate, minimal creativity |
| **0.5** | Code Assistant | Balanced - creative problem solving with precision |
| **0.6** | Customer Service | Warm, personable, slightly varied responses |
| **0.7** | General, Sales | Creative, conversational, engaging |

### Memory (Context Window)

| Memory | Agents | Use Case |
|--------|--------|----------|
| **10 exchanges** | General, Code, Research | Standard conversations |
| **15 exchanges** | Technical Support, Sales | Moderate complexity, multi-step interactions |
| **20 exchanges** | Customer Service | Long, detailed customer interactions |

### Response Length

| Max Tokens | Agents | Purpose |
|------------|--------|---------|
| **1500** | Customer Service | Concise, focused responses |
| **2000** | General, Technical, Code, Sales | Standard detailed answers |
| **3000** | Research Assistant | Long-form, comprehensive explanations |

---

## 🔧 How Agent Selection Works

### Code Flow

```
User Selects Agent in UI
         ↓
src/ui/components.py (Line 32-44)
├── Dropdown selection changes
└── Calls agent_manager.set_current_agent()
         ↓
src/agents/agent_manager.py (Line 114-119)
├── Switches current_agent_name
└── Next message uses new agent
         ↓
src/agents/agent_manager.py (Line 139-145)
├── agent_manager.chat() calls
└── Forwards to current agent
         ↓
src/agents/base_agent.py (Line 118-134)
├── Builds message history with system_prompt
├── Adds conversation context (max_history)
└── Invokes LLM with agent's temperature
         ↓
OpenAI API Response
└── Shaped by system_prompt + temperature
```

### What Makes Each Agent Unique?

| Component | Configuration | Code Location | Effect |
|-----------|--------------|---------------|--------|
| **System Prompt** | `config/agents.yaml` → `system_prompt` | `src/agents/base_agent.py#L60` | Sets personality, role, and behavior |
| **Temperature** | `config/agents.yaml` → `llm_override.temperature` | `src/llm/llm_factory.py#L48` | Controls creativity (0.3 = precise, 0.7 = creative) |
| **Max History** | `config/agents.yaml` → `max_history` | `src/agents/base_agent.py#L62` | How many past exchanges to remember |
| **Max Tokens** | `config/agents.yaml` → `llm_override.max_tokens` | `src/llm/llm_factory.py#L48` | Maximum length of responses |

---

## 🎨 Creating Custom Agents

### Step 1: Define Your Agent

Edit `config/agents.yaml`:

```yaml
agents:
  data_analyst:
    name: "Data Analyst"
    description: "Analyzes data and provides insights"
    system_prompt: |
      You are an expert data analyst.
      Analyze data, identify patterns, and provide actionable insights.
      Use clear visualizations and statistical reasoning.
    llm_override:
      temperature: 0.4      # Precise for data work
      max_tokens: 2500
    use_rag: true
    use_tools: false
    enable_web_search: false
    max_history: 15
```

### Step 2: Restart the Application

```bash
python -m streamlit run app.py
```

Your new agent will appear in the dropdown!

---

## 🧪 Testing Different Agents

Try asking the **same question** to different agents to see how they respond differently:

**Question:** "What is machine learning?"

**General Assistant (0.7 temp):**
> "Machine learning is a fascinating field of AI where computers learn from data..."
> *(Conversational, engaging)*

**Technical Support (0.3 temp):**
> "Machine learning is a method of data analysis that automates analytical model building..."
> *(Precise, technical definition)*

**Research Assistant (0.4 temp):**
> "Machine learning (ML) is a subset of artificial intelligence that enables systems to learn and improve from experience. Key components include..."
> *(Academic, comprehensive, structured)*

---

## 💡 Best Practices

### Choosing the Right Agent

1. **General questions?** → Use **General Assistant**
2. **Technical problem?** → Use **Technical Support**
3. **Writing code?** → Use **Code Assistant**
4. **Customer issue?** → Use **Customer Service**
5. **Need recommendations?** → Use **Sales Assistant**
6. **Deep research?** → Use **Research Assistant**

### Temperature Guidelines

- **0.1-0.3**: Math, code generation, technical docs (needs consistency)
- **0.4-0.6**: Analysis, explanations, support (balanced accuracy)
- **0.7-0.9**: Creative writing, brainstorming, marketing (needs variety)

### Memory Considerations

- **Short conversations (10)**: Quick Q&A, general help
- **Medium conversations (15)**: Multi-step problems, sales conversations
- **Long conversations (20+)**: Complex customer support, ongoing projects

---

## 🔍 Under the Hood

### System Prompt Injection

Every message sent to the agent includes the system prompt:

```python
# src/agents/base_agent.py (Line 96-107)
def _build_messages_for_history(self) -> List[BaseMessage]:
    messages = []
    messages.append(SystemMessage(content=self.system_prompt))  # ← Agent personality
    
    # Add conversation history
    for msg in self.conversation_history[-self.max_history:]:
        if msg.role == 'user':
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == 'assistant':
            messages.append(AIMessage(content=msg.content))
    
    return messages
```

### LLM Configuration Override

Each agent can override global LLM settings:

```python
# src/llm/llm_factory.py (Line 35-48)
llm_config = config.get_llm_config().copy()

# Apply agent-specific overrides
if agent_config and agent_config.get('llm_override'):
    llm_config.update(agent_config['llm_override'])  # ← Temperature, max_tokens, etc.

return ChatOpenAI(
    model=llm_config.get('model', 'gpt-3.5-turbo'),
    temperature=llm_config.get('temperature', 0.7),  # ← Different per agent
    max_tokens=llm_config.get('max_tokens', 2000),
    # ...
)
```

---

## 📚 Configuration Files Reference

### Main Config: `config/config.yaml`
Contains: `default`, `technical_support`, `code_assistant`

### Agents Config: `config/agents.yaml`
Contains: `customer_service`, `sales_agent`, `research_assistant`

### Loading Priority
1. `config/config.yaml` agents loaded first
2. `config/agents.yaml` agents merged in
3. All agents available in dropdown

---

## 🚀 Advanced: Enable Tools

Want agents to use tools like calculator, web search, or email?

```yaml
agents:
  research_assistant:
    use_tools: true           # ← Enable ReAct tools
    enable_web_search: true   # ← Requires TAVILY_API_KEY
```

**Available Tools:**
- 🔍 **RAG Search** - Searches knowledge base
- 🧮 **Calculator** - Math operations
- 🌐 **Web Search** - Current information (requires Tavily API)
- 📧 **Email** - Send emails (requires SMTP/SendGrid)

See [USAGE.md](USAGE.md) for tool configuration details.

---

## 📖 Related Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Initial setup and first steps
- **[USAGE.md](USAGE.md)** - Detailed usage guide and configuration
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick command reference
- **[README.md](README.md)** - Complete project overview

---

**Need help?** Open an issue or check the documentation!
