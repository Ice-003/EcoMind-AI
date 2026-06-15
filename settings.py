import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_settings():
    """Initialize default settings in session state."""
    if 'groq_api_key' not in st.session_state:
        st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")
    
    if 'cost_per_1m_tokens_usd' not in st.session_state:
        # Default cost for LLaMA 3 8B is typically around $0.05 - $0.10 per 1M tokens
        st.session_state.cost_per_1m_tokens_usd = 0.05
    
    if 'usd_to_inr_rate' not in st.session_state:
        st.session_state.usd_to_inr_rate = 83.50
        
    if 'carbon_grams_per_kwh' not in st.session_state:
        # Global average carbon intensity of grid
        st.session_state.carbon_grams_per_kwh = 475.0
        
    if 'kwh_per_token' not in st.session_state:
        # Estimated energy consumption per token generated/processed
        st.session_state.kwh_per_token = 0.000003

def get_setting(key):
    return st.session_state.get(key)

def update_setting(key, value):
    st.session_state[key] = value
