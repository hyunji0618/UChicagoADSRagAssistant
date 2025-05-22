import streamlit as st
import requests

# --- Page Config ---
st.set_page_config(
    page_title="MSADS RAG Chatbot",
    layout="wide",
    page_icon="🎓"
)

# --- Color & Style Constants ---
PRIMARY_COLOR = "#800000"  # Maroon
BACKGROUND_COLOR = "#f8f5f2"  # Light beige background
TEXT_COLOR = "#2b2b2b"

# --- CSS Styling ---
st.markdown(f"""
    <style>
    body {{
        background-color: {BACKGROUND_COLOR};
        margin: 0;
        padding-bottom: 80px;  /* space for input */
    }}
    .reportview-container {{
        font-family: 'Helvetica', sans-serif;
    }}
    .stButton>button {{
        color: white;
        background-color: {PRIMARY_COLOR};
        border-radius: 8px;
    }}
    .stTextInput>div>div>input {{
        border-radius: 6px;
        border: 1px solid #ccc;
        padding: 8px;
        font-size: 16px;
    }}
    .user-message {{
        background-color: #DCF8C6;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        max-width: 70%;
        margin-left: auto;
        text-align: right;
    }}
    .assistant-message {{
        background-color: #f1f0f0;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        max-width: 70%;
        margin-right: auto;
        text-align: left;
    }}
    .message-sender {{
        font-size: 14px;
        color: gray;
        margin-bottom: 4px;
    }}
    h1, h2, h3 {{
        font-size: 20px !important;
    }}
    .fixed-input {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        right: 20px;
        background-color: {BACKGROUND_COLOR};
        padding: 10px;
        border-top: 1px solid #ccc;
        z-index: 999;
    }}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🔍 About the Project")
    st.markdown(
        """
        This Retrieval-Augmented Generation (RAG) chatbot helps you explore the **MS in Applied Data Science** program at the University of Chicago.

        Ask questions like:
        - *What are the core courses?*
        - *What are the admission requirements?*
        - *Tell me about the capstone project.*
        """
    )

    st.caption("Made with ❤️ for Generative AI Principles")

# --- Header (Title) ---
st.markdown(f"""
    <div style='text-align: center; padding: 0px 0 30px 0; margin-top: -20px;'>
        <div style='font-size: 48px;'>🎓</div>
        <div style='font-size: 20px; font-weight: bold; color: {PRIMARY_COLOR}; line-height: 1.4;'>
            UChicago MS in Applied Data Science
        </div>
        <div style='font-size: 50px; font-weight: bold; color: {TEXT_COLOR};'>
            AI Chat Assistant
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# Display chat messages from history
for message in st.session_state.messages:
    with st.container():
        message_class = "user-message" if message['role'] == 'user' else "assistant-message"
        sender = "You" if message['role'] == 'user' else "Assistant"
        st.markdown(f"""
            <div class="{message_class}">
                <div class="message-sender">{sender}</div>
                <div style='font-size: 16px; color: {TEXT_COLOR};'>
                    {message['content']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- Input ---
query = st.text_input(
    "💬 Ask a question about the program (e.g., What is the capstone project about?)", 
    key="query_input"
)

if query and query != st.session_state.last_query:
    # Update last query
    st.session_state.last_query = query
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("🤖 Thinking..."):
        response = requests.post(
            "http://localhost:8000/query",
            json={"question": query}
        )
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "No response available.")
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # Keep only the last 4 messages
            if len(st.session_state.messages) > 4:
                st.session_state.messages = st.session_state.messages[-4:]
            
            # Rerun to update the display
            st.rerun()
        else:
            st.error("⚠️ Failed to retrieve an answer. Please try again later.")
elif not st.session_state.messages:
    st.markdown(
        """
        <div style="background-color:#f3e8e8; padding: 10px; border-left: 6px solid #800000; border-radius: 5px;">
            <span style="color:#800000; font-size: 15px;">
            <b>Enter a question above to get started.</b>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Footer ---
st.markdown("<div style='padding-bottom: 80px'></div>", unsafe_allow_html=True)
st.caption("---")
st.caption("© 2025 MSADS at The University of Chicago")