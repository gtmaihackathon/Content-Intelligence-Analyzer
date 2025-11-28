import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Content Intelligence Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .funnel-awareness {
        background-color: #e3f2fd;
        padding: 1rem;
        border-left: 4px solid #2196f3;
        margin: 0.5rem 0;
    }
    .funnel-consideration {
        background-color: #fff3e0;
        padding: 1rem;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
    }
    .funnel-decision {
        background-color: #e8f5e9;
        padding: 1rem;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .improvement-box {
        background-color: #fff9c4;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #fbc02d;
        margin: 0.5rem 0;
    }
    .strength-box {
        background-color: #c8e6c9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'saved_analyses' not in st.session_state:
    st.session_state.saved_analyses = []
if 'competitor_analyses' not in st.session_state:
    st.session_state.competitor_analyses = []
if 'personas' not in st.session_state:
    st.session_state.personas = []
if 'persona_analyses' not in st.session_state:
    st.session_state.persona_analyses = []
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        'openai': '',
        'gemini': '',
        'claude': ''
    }

# Directory setup for saving data
DATA_DIR = Path("analyzer_data")
DATA_DIR.mkdir(exist_ok=True)

# Helper functions
def load_saved_data():
    """Load previously saved data from disk"""
    try:
        if (DATA_DIR / "analyses.json").exists():
            with open(DATA_DIR / "analyses.json", 'r') as f:
                st.session_state.saved_analyses = json.load(f)
        
        if (DATA_DIR / "competitor_analyses.json").exists():
            with open(DATA_DIR / "competitor_analyses.json", 'r') as f:
                st.session_state.competitor_analyses = json.load(f)
        
        if (DATA_DIR / "personas.json").exists():
            with open(DATA_DIR / "personas.json", 'r') as f:
                st.session_state.personas = json.load(f)
        
        if (DATA_DIR / "persona_analyses.json").exists():
            with open(DATA_DIR / "persona_analyses.json", 'r') as f:
                st.session_state.persona_analyses = json.load(f)
        
        if (DATA_DIR / "api_keys.json").exists():
            with open(DATA_DIR / "api_keys.json", 'r') as f:
                st.session_state.api_keys = json.load(f)
    except Exception as e:
        st.error(f"Error loading saved data: {str(e)}")

def save_data(data_type, data):
    """Save data to disk"""
    try:
        filename = f"{data_type}.json"
        with open(DATA_DIR / filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

# Load saved data on startup
load_saved_data()

# Main app
st.markdown('<h1 class="main-header">📊 Content Intelligence Analyzer</h1>', unsafe_allow_html=True)

# Sidebar for API Keys Configuration
with st.sidebar:
    st.header("⚙️ API Configuration")
    
    with st.expander("🔑 API Keys Setup", expanded=False):
        openai_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_keys.get('openai', ''),
            type="password",
            help="Enter your OpenAI API key for GPT models"
        )
        
        gemini_key = st.text_input(
            "Google Gemini API Key",
            value=st.session_state.api_keys.get('gemini', ''),
            type="password",
            help="Enter your Google Gemini API key"
        )
        
        claude_key = st.text_input(
            "Anthropic Claude API Key",
            value=st.session_state.api_keys.get('claude', ''),
            type="password",
            help="Enter your Anthropic Claude API key"
        )
        
        if st.button("💾 Save API Keys"):
            st.session_state.api_keys = {
                'openai': openai_key,
                'gemini': gemini_key,
                'claude': claude_key
            }
            if save_data('api_keys', st.session_state.api_keys):
                st.success("✅ API keys saved successfully!")
    
    st.header("📋 Quick Stats")
    st.metric("Saved Analyses", len(st.session_state.saved_analyses))
    st.metric("Competitor Analyses", len(st.session_state.competitor_analyses))
    st.metric("Personas Created", len(st.session_state.personas))
    st.metric("Persona Analyses", len(st.session_state.persona_analyses))

# Main tabs
tab1, tab2, tab3 = st.tabs([
    "🎯 Own Content Analysis",
    "🔍 Competitor Analysis",
    "👥 Persona-Based Analysis"
])

# Import analysis modules
from analysis_modules import (
    render_own_content_tab,
    render_competitor_tab,
    render_persona_tab
)

with tab1:
    render_own_content_tab()

with tab2:
    render_competitor_tab()

with tab3:
    render_persona_tab()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Content Intelligence Analyzer v1.0 | Built with Streamlit</p>
        <p>💡 Analyze, Optimize, and Improve Your Content Strategy</p>
    </div>
    """,
    unsafe_allow_html=True
)
