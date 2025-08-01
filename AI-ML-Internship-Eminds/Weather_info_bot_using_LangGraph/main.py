import streamlit as st
from src.langgraph_app import graph, validate_city_and_get_weather, get_friendly_weather_response
from src.memory import memory

# Professional UI setup
st.set_page_config(
    page_title="Weather Info Bot",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional styling with proper color contrast
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        border-bottom: 2px solid #e5e7eb;
    }
    .conversation-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        color: #1f2937;
    }
    .user-message {
        background: #f3f4f6;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #3b82f6;
        color: #1f2937;
    }
    .bot-message {
        background: #f9fafb;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #10b981;
        color: #1f2937;
    }
    .status-box {
        background: #dbeafe;
        border: 1px solid #3b82f6;
        border-radius: 6px;
        padding: 0.75rem;
        margin: 1rem 0;
        color: #1e40af;
    }
    .input-container {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1f2937;
    }
    .stTextInput > div > div > input {
        color: #1f2937 !important;
        background-color: #ffffff !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #6b7280 !important;
    }
    .stButton > button {
        color: #ffffff !important;
        background-color: #3b82f6 !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #2563eb !important;
    }
    .stMarkdown {
        color: #1f2937 !important;
    }
    .stSubheader {
        color: #1f2937 !important;
    }
    .stCaption {
        color: #6b7280 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<h1 class="main-header">🌤️ Weather Information System</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 Quick Actions")
    
    if st.button("🔄 Reset Session", type="primary"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    st.subheader("📍 Popular Cities")
    popular_cities = ["Chennai", "Delhi", "Bangalore", "Mumbai", "Kolkata", "Hyderabad"]
    
    for city in popular_cities:
        if st.button(f"🌍 {city}", key=f"city_{city}"):
            st.session_state.state = {"user_input": "", "message": "", "next": "ask_city"}
            st.session_state.node = "validate_city"
            st.session_state.state["user_input"] = city
            st.rerun()
    
    st.markdown("---")
    st.subheader("ℹ️ System Info")
    st.info("Powered by LangGraph & Groq LLM")
    st.caption("Real-time weather data via Open-Meteo API")

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Initialize session state
    if "state" not in st.session_state:
        st.session_state.state = {"user_input": "", "message": "", "next": "ask_city"}
        st.session_state.node = "ask_city"
        st.session_state.conversation_history = []

    # Conversation container
    with st.container():
        st.markdown('<div class="conversation-container">', unsafe_allow_html=True)
        
        # Display conversation history
        for i, (role, message) in enumerate(st.session_state.conversation_history):
            if role == "user":
                st.markdown(f'<div class="user-message"><strong>You:</strong> {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message"><strong>Weather Bot:</strong> {message}</div>', unsafe_allow_html=True)
        
        # Current conversation flow
        if st.session_state.node == "ask_city":
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            st.subheader("📍 Enter City Name")
            st.caption("Please provide a city name to get current weather information")
            
            user_input = st.text_input(
                "City Name:",
                placeholder="e.g., Chennai, Delhi, Bangalore...",
                key="input_ask",
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔍 Get Weather", type="primary", use_container_width=True):
                    if user_input:
                        st.session_state.state["user_input"] = user_input
                        st.session_state.node = "validate_city"
                        st.session_state.conversation_history.append(("user", user_input))
                        st.rerun()
                    else:
                        st.error("Please enter a city name")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.node == "validate_city":
            city = st.session_state.state.get("user_input", "").strip()
            is_valid, message = validate_city_and_get_weather(city)
            
            if not is_valid:
                st.error(f"❌ {message}")
                st.session_state.node = "retry"
                st.rerun()
            else:
                st.session_state.node = "respond"
                st.rerun()

        elif st.session_state.node == "retry":
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            st.warning("⚠️ Invalid city name. Please try again.")
            st.subheader("📍 Enter City Name")
            
            user_input = st.text_input(
                "City Name:",
                placeholder="e.g., Chennai, Delhi, Bangalore...",
                key="input_retry",
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔍 Get Weather", type="primary", use_container_width=True):
                    if user_input:
                        st.session_state.state["user_input"] = user_input
                        st.session_state.node = "validate_city"
                        st.session_state.conversation_history.append(("user", user_input))
                        st.rerun()
                    else:
                        st.error("Please enter a city name")
            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.node == "respond":
            last_city = memory.get("last_location", "Unknown")
            last_weather = memory.get("last_weather", "No data")
            
            # Get friendly response from LLM
            friendly_message = get_friendly_weather_response(last_city, last_weather)
            st.session_state.conversation_history.append(("bot", friendly_message))
            
            # Display the response
            st.markdown(f'<div class="bot-message"><strong>Weather Bot:</strong> {friendly_message}</div>', unsafe_allow_html=True)
            
            # Status information
            st.markdown('<div class="status-box">', unsafe_allow_html=True)
            st.markdown("**System Status:**")
            st.markdown(f"• 📍 Last queried city: **{last_city}**")
            st.markdown(f"• 🌡️ Weather data: **{last_weather}**")
            st.markdown("• 🤖 LLM: **Groq (llama3-8b-8192)**")
            st.markdown("• 🔗 Framework: **LangGraph**")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Reset option
            if st.button("🔄 New Query", type="secondary"):
                st.session_state.node = "ask_city"
                st.session_state.conversation_history = []
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
