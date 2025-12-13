"""
Streamlit UI Components
Reusable UI components for the chatbot interface.
"""

import streamlit as st
from typing import Dict, Any, List
from datetime import datetime


def render_sidebar(agent_manager, rag_manager, config: Dict[str, Any]):
    """
    Render the sidebar with agent selection and settings.
    
    Args:
        agent_manager: AgentManager instance
        rag_manager: RAGManager instance
        config: UI configuration
    """
    ui_config = config.get('sidebar', {})
    
    with st.sidebar:
        st.title("⚙️ Settings")
        
        # Agent selection
        if ui_config.get('show_agent_selector', True):
            agents = agent_manager.list_agents()
            agent_names = list(agents.keys())
            agent_labels = [agents[name]['name'] for name in agent_names]
            
            selected_index = agent_names.index(agent_manager.current_agent_name)
            
            selected_label = st.selectbox(
                "Select Agent",
                agent_labels,
                index=selected_index,
                help="Choose an AI agent specialized for different tasks"
            )
            
            # Get agent name from label
            selected_name = agent_names[agent_labels.index(selected_label)]
            
            if selected_name != agent_manager.current_agent_name:
                agent_manager.set_current_agent(selected_name)
                st.rerun()
            
            # Show agent description
            current_agent = agent_manager.get_current_agent()
            st.info(f"**{current_agent.description}**")
        
        st.divider()
        
        # Admin Authentication
        if 'admin_logged_in' not in st.session_state:
            st.session_state.admin_logged_in = False
        
        # Initialize tool states in session state if not exists (needed for both admin and non-admin)
        if 'enable_calculator' not in st.session_state:
            st.session_state.enable_calculator = True
        if 'enable_rag_search' not in st.session_state:
            st.session_state.enable_rag_search = True
        if 'enable_web_search' not in st.session_state:
            st.session_state.enable_web_search = False
        if 'enable_email' not in st.session_state:
            st.session_state.enable_email = False
        
        if not st.session_state.admin_logged_in:
            # Show login link and form
            if st.button("🔐 Login as Admin to update settings", use_container_width=True):
                st.session_state.show_admin_login = True
            
            if st.session_state.get('show_admin_login', False):
                with st.form("admin_login_form"):
                    st.caption("Enter admin code to access settings")
                    admin_code = st.text_input("Admin Code", type="password")
                    login_button = st.form_submit_button("Login")
                    
                    if login_button:
                        # Check admin code (can be set in environment or use default)
                        import os
                        correct_code = os.getenv('ADMIN_CODE', 'admin123')
                        
                        if admin_code == correct_code:
                            st.session_state.admin_logged_in = True
                            st.session_state.show_admin_login = False
                            st.success("✅ Logged in as Admin")
                            st.rerun()
                        else:
                            st.error("❌ Invalid admin code")
            
            st.divider()
        else:
            # Admin is logged in - show logout button
            col1, col2 = st.columns([3, 1])
            with col1:
                st.success("👤 Admin Mode")
            with col2:
                if st.button("🚪", help="Logout"):
                    st.session_state.admin_logged_in = False
                    st.rerun()
            
            st.divider()
            
            # Tools Configuration (only visible when logged in as admin)
            st.subheader("🛠️ Agent Tools")
            
            current_agent = agent_manager.get_current_agent()
            
            # Individual tool toggles
            enable_calculator = st.toggle(
                "🧮 Calculator",
                value=st.session_state.enable_calculator,
                help="Enable calculator for mathematical operations"
            )
            
            enable_rag_search = st.toggle(
                "📚 RAG Search",
                value=st.session_state.enable_rag_search,
                help="Enable knowledge base search"
            )
            
            enable_web_search = st.toggle(
                "🌐 Web Search",
                value=st.session_state.enable_web_search,
                help="Enable web search. Requires TAVILY_API_KEY environment variable"
            )
            
            enable_email = st.toggle(
                "📧 Email",
                value=st.session_state.enable_email,
                help="Enable email sending. Requires email configuration in config.yaml"
            )
            
            # Check if any tool settings changed
            tools_changed = (
                enable_calculator != st.session_state.enable_calculator or
                enable_rag_search != st.session_state.enable_rag_search or
                enable_web_search != st.session_state.enable_web_search or
                enable_email != st.session_state.enable_email
            )
            
            if tools_changed:
                st.session_state.enable_calculator = enable_calculator
                st.session_state.enable_rag_search = enable_rag_search
                st.session_state.enable_web_search = enable_web_search
                st.session_state.enable_email = enable_email
                
                # Update agent tools with individual settings
                agent_manager.update_agent_tools_individual(
                    enable_calculator=enable_calculator,
                    enable_rag_search=enable_rag_search,
                    enable_web_search=enable_web_search,
                    enable_email=enable_email
                )
                st.rerun()
            
            # Show active tools
            active_tools = []
            if st.session_state.enable_calculator:
                active_tools.append("calculator")
            if st.session_state.enable_rag_search:
                active_tools.append("rag_search")
            if st.session_state.enable_web_search:
                active_tools.append("web_search")
            if st.session_state.enable_email:
                active_tools.append("send_email")
            
            if active_tools:
                st.caption(f"🟢 Active: {', '.join(active_tools)}")
            else:
                st.caption("🔴 No tools active")
            
            st.divider()
            
            # Tool Examples Section
            st.subheader("💡 Try Examples")
            
            # Calculator examples
            if st.session_state.enable_calculator:
                st.caption("**🧮 Calculator Examples:**")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📊 Calculate discount", key="calc_ex1", use_container_width=True):
                        st.session_state.example_prompt = "I bought 3 items at $45.99 each with 15% discount. What's the total?"
                        st.rerun()
                with col2:
                    if st.button("🔢 Complex math", key="calc_ex2", use_container_width=True):
                        st.session_state.example_prompt = "What is (25 * 8 + 150) / 5 - 20?"
                        st.rerun()
            
            # RAG Search examples
            if st.session_state.enable_rag_search:
                st.caption("**📚 RAG Search Examples:**")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📖 Search docs", key="rag_ex1", use_container_width=True):
                        st.session_state.example_prompt = "What is artificial intelligence according to the knowledge base?"
                        st.rerun()
                with col2:
                    if st.button("🔍 Find info", key="rag_ex2", use_container_width=True):
                        st.session_state.example_prompt = "Search for information about machine learning in the documents"
                        st.rerun()
            
            # Web Search examples
            if st.session_state.enable_web_search:
                st.caption("**🌐 Web Search Examples:**")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🌍 Current events", key="web_ex1", use_container_width=True):
                        st.session_state.example_prompt = "What are the latest developments in artificial intelligence?"
                        st.rerun()
                with col2:
                    if st.button("💹 Market info", key="web_ex2", use_container_width=True):
                        st.session_state.example_prompt = "Search the web for today's technology news"
                        st.rerun()
            
            # Email examples
            if st.session_state.enable_email:
                st.caption("**📧 Email Examples:**")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✉️ Meeting reminder", key="email_ex1", use_container_width=True):
                        st.session_state.example_prompt = "Send an email to test@example.com with subject 'Meeting Reminder' and message 'Don't forget our 2pm meeting tomorrow'"
                        st.rerun()
                with col2:
                    if st.button("📝 Status update", key="email_ex2", use_container_width=True):
                        st.session_state.example_prompt = "Send an email to team@example.com about Project Update with message: The AI chatbot is now ready for testing"
                        st.rerun()
        
        # General controls and info (visible to everyone)
            
            st.divider()
            
            # RAG System Status (admin view with tool status)
            if ui_config.get('show_rag_status', True) and rag_manager:
                st.subheader("📚 RAG System")
                rag_stats = rag_manager.get_stats()
                
                # Show vector database status
                if rag_stats.get('enabled'):
                    st.caption(f"Vector DB: {rag_stats.get('vector_db', 'N/A')} ✅")
                    if 'document_count' in rag_stats:
                        st.caption(f"Documents: {rag_stats['document_count']}")
                else:
                    st.caption("Vector DB: Not initialized ⚠️")
                
                # Show RAG tool status (whether agent can use it)
                if st.session_state.enable_rag_search:
                    st.caption("RAG Search Tool: Active 🟢")
                else:
                    st.caption("RAG Search Tool: Inactive 🔴")
            
            st.divider()
            
            # Additional admin settings
            if ui_config.get('show_settings', True):
                st.subheader("🔧 Admin Controls")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("♻️ Reset All", use_container_width=True):
                        st.session_state.clear()
                        agent_manager.clear_all_histories()
                        st.rerun()
                
                with col2:
                    # Export chat option
                    if config.get('enable_chat_export', True):
                        if st.button("💾 Export Chat", use_container_width=True):
                            export_chat_history(st.session_state.get('messages', []))
        
        # General controls (visible to everyone)
        st.divider()
        st.subheader("🔧 Controls")
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            agent_manager.clear_history()
            st.rerun()
        
        # Basic RAG info (visible to everyone)
        if ui_config.get('show_rag_status', True) and rag_manager and not st.session_state.admin_logged_in:
            st.divider()
            st.subheader("📚 RAG System")
            rag_stats = rag_manager.get_stats()
            
            if rag_stats.get('enabled'):
                st.caption(f"Vector DB: {rag_stats.get('vector_db', 'N/A')} ✅")
                if 'document_count' in rag_stats:
                    st.caption(f"Documents: {rag_stats['document_count']}")
            else:
                st.caption("Vector DB: Not initialized ⚠️")


def render_chat_message(role: str, content: str, timestamp: datetime = None):
    """
    Render a chat message.
    
    Args:
        role: Message role ('user' or 'assistant')
        content: Message content
        timestamp: Optional timestamp
    """
    avatar = "🧑‍💻" if role == "user" else "🤖"
    
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)
        if timestamp:
            st.caption(f"_{timestamp.strftime('%H:%M:%S')}_")


def render_file_uploader(rag_manager):
    """
    Render file upload widget for adding documents to RAG.
    
    Args:
        rag_manager: RAGManager instance
    """
    with st.expander("📤 Upload Documents"):
        uploaded_files = st.file_uploader(
            "Add documents to knowledge base",
            type=['txt', 'pdf', 'docx', 'md'],
            accept_multiple_files=True,
            help="Upload documents to enhance the chatbot's knowledge"
        )
        
        if uploaded_files and st.button("Process Documents"):
            with st.spinner("Processing documents..."):
                import tempfile
                import os
                
                temp_files = []
                try:
                    # Save uploaded files temporarily
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=os.path.splitext(uploaded_file.name)[1]
                        ) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            temp_files.append(tmp_file.name)
                    
                    # Process documents
                    count = rag_manager.initialize_documents(temp_files)
                    st.success(f"Successfully processed {count} document chunks!")
                
                except Exception as e:
                    st.error(f"Error processing documents: {e}")
                
                finally:
                    # Clean up temp files
                    for temp_file in temp_files:
                        try:
                            os.unlink(temp_file)
                        except:
                            pass


def render_chat_input(agent_manager, config: Dict[str, Any]):
    """
    Render chat input and handle user messages.
    
    Args:
        agent_manager: AgentManager instance
        config: UI configuration
        
    Returns:
        User input or None
    """
    max_length = config.get('max_message_length', 4000)
    
    user_input = st.chat_input(
        "Type your message here...",
        max_chars=max_length
    )
    
    return user_input


def show_typing_indicator():
    """Show a typing indicator while generating response."""
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            pass


def export_chat_history(messages: List[Dict[str, Any]]):
    """
    Export chat history to a downloadable format.
    
    Args:
        messages: List of message dictionaries
    """
    if not messages:
        st.warning("No messages to export")
        return
    
    # Create text format
    export_text = "# Chat History Export\n\n"
    export_text += f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    export_text += "---\n\n"
    
    for msg in messages:
        role = msg['role'].upper()
        content = msg['content']
        timestamp = msg.get('timestamp', '')
        
        export_text += f"## {role}\n"
        if timestamp:
            export_text += f"*{timestamp}*\n\n"
        export_text += f"{content}\n\n"
        export_text += "---\n\n"
    
    # Provide download button
    st.download_button(
        label="Download Chat History",
        data=export_text,
        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )


def render_stats_panel(agent_manager, rag_manager):
    """
    Render statistics panel.
    
    Args:
        agent_manager: AgentManager instance
        rag_manager: RAGManager instance
    """
    with st.expander("📊 Statistics"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            message_count = len(st.session_state.get('messages', []))
            st.metric("Messages", message_count)
        
        with col2:
            agents_count = len(agent_manager.list_agents())
            st.metric("Available Agents", agents_count)
        
        with col3:
            if rag_manager and rag_manager.enabled:
                stats = rag_manager.get_stats()
                doc_count = stats.get('document_count', 0)
                st.metric("Documents", doc_count)


def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown("""
        <style>
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .stButton button {
            border-radius: 0.3rem;
        }
        
        .stTextInput input {
            border-radius: 0.3rem;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        </style>
    """, unsafe_allow_html=True)
