import streamlit as st
import pandas as pd
import plotly.express as px
from time import sleep

# Import our custom modules
from settings import init_settings, get_setting, update_setting
from database import init_db, save_optimization_result, get_all_history, clear_history, delete_record
from optimizer import optimize_prompt, count_tokens
from carbon import calculate_carbon_gco2, format_carbon
from cost import calculate_cost_usd, format_currency, usd_to_inr
from analytics import get_dashboard_metrics, get_trend_data
from pdf_generator import generate_pdf_report

# Initialize configuration
st.set_page_config(
    page_title="EcoMind AI | Sustainable Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State & Database
init_settings()
init_db()

# --- CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""
<style>
    /* Global Background and Fonts */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-weight: 700;
    }
    
    /* Text Inputs and Areas */
    .stTextArea textarea {
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 8px;
        font-size: 16px;
    }
    .stTextArea textarea:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 1px #58a6ff;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2ea043 0%, #238636 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3fb950 0%, #2ea043 100%);
        box-shadow: 0 4px 15px rgba(46, 160, 67, 0.4);
        transform: translateY(-2px);
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #58a6ff !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
        color: #3fb950 !important;
    }
    
    /* Custom Card Style for Containers */
    .premium-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🧠 EcoMind AI")
st.sidebar.caption("Sustainable Intelligence Starts Here.")
st.sidebar.markdown("---")

menu = ["🚀 Optimizer", "📊 Dashboard", "💾 Memory", "⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

st.sidebar.markdown("---")
st.sidebar.markdown("<small>Powered by Groq & LLaMA 3 8B</small>", unsafe_allow_html=True)

# --- OPTIMIZER PAGE ---
if choice == "🚀 Optimizer":
    st.title("Prompt Intelligence Engine")
    st.markdown("Transform your prompts to maximize efficiency and minimize carbon footprint.")
    
    if not get_setting('groq_api_key'):
        st.warning("⚠️ Please configure your Groq API Key in the Settings tab first.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        original_prompt = st.text_area("Enter your original prompt:", height=200, placeholder="E.g., Write a very long and detailed explanation of how quantum physics works using simple words, please and thank you very much.")
    
    with col2:
        st.markdown("### Optimization Mode")
        mode = st.radio("Select Strategy:", ["Concise", "Balanced", "Maximum Efficiency"], index=1)
        
        st.markdown("### Current Footprint")
        if original_prompt:
            temp_tokens = count_tokens(original_prompt)
            temp_cost = calculate_cost_usd(temp_tokens)
            temp_carbon = calculate_carbon_gco2(temp_tokens)
            st.metric("Tokens", temp_tokens)
            st.metric("Cost Est.", format_currency(temp_cost))
            st.metric("Carbon Est.", format_carbon(temp_carbon))
        else:
            st.info("Start typing to see estimates.")
            
        optimize_btn = st.button("✨ Optimize Prompt", disabled=not original_prompt or not get_setting('groq_api_key'))

    if optimize_btn:
        with st.spinner("Analyzing and optimizing your prompt..."):
            try:
                # Actual optimization logic
                result = optimize_prompt(original_prompt, mode)
                
                # Calculations
                orig_tokens = count_tokens(original_prompt)
                opt_tokens = result['optimized_tokens']
                tokens_saved = max(0, orig_tokens - opt_tokens)
                
                orig_cost = calculate_cost_usd(orig_tokens)
                opt_cost = calculate_cost_usd(opt_tokens)
                cost_saved = max(0, orig_cost - opt_cost)
                
                orig_carbon = calculate_carbon_gco2(orig_tokens)
                opt_carbon = calculate_carbon_gco2(opt_tokens)
                carbon_saved = max(0, orig_carbon - opt_carbon)
                
                # Save to DB
                db_data = {
                    'original_prompt': original_prompt,
                    'optimized_prompt': result['optimized_prompt'],
                    'optimization_mode': mode,
                    'original_tokens': orig_tokens,
                    'optimized_tokens': opt_tokens,
                    'tokens_saved': tokens_saved,
                    'original_cost': orig_cost,
                    'optimized_cost': opt_cost,
                    'cost_saved': cost_saved,
                    'original_carbon': orig_carbon,
                    'optimized_carbon': opt_carbon,
                    'carbon_saved': carbon_saved,
                    'efficiency_score': result['efficiency_score']
                }
                save_optimization_result(db_data)
                
                st.success("Optimization Complete!")
                
                # Results Display
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                st.subheader("✅ Optimized Prompt")
                st.code(result['optimized_prompt'], language="markdown")
                
                if result['suggestions']:
                    st.markdown("**Optimization Notes:**")
                    for s in result['suggestions']:
                        st.markdown(f"- {s}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Efficiency Score", f"{result['efficiency_score']}/100", f"+{result['efficiency_score'] - 50}%" if result['efficiency_score'] > 50 else None)
                m2.metric("Tokens Saved", tokens_saved, f"{(tokens_saved/orig_tokens)*100:.1f}%" if orig_tokens > 0 else "0%")
                m3.metric("Cost Saved", format_currency(cost_saved), f"₹{usd_to_inr(cost_saved):.4f}")
                m4.metric("CO₂ Saved", format_carbon(carbon_saved), "Green Impact")
                
                # PDF Generation
                if st.button("📄 Generate PDF Report"):
                    with st.spinner("Generating beautiful PDF report..."):
                        pdf_path = generate_pdf_report(db_data)
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=pdf_file,
                                file_name=f"EcoMind_Report_{int(pd.Timestamp.now().timestamp())}.pdf",
                                mime="application/pdf"
                            )
                            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# --- DASHBOARD PAGE ---
elif choice == "📊 Dashboard":
    st.title("Smart Dashboard")
    
    metrics = get_dashboard_metrics()
    
    # Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Prompts", metrics['total_prompts'])
    with col2:
        st.metric("Tokens Saved", f"{metrics['total_tokens_saved']:,}")
    with col3:
        st.metric("Total Saved", format_currency(metrics['total_cost_saved_usd']))
    with col4:
        st.metric("CO₂ Prevented", format_carbon(metrics['total_carbon_saved_gco2']))
        
    st.markdown("---")
    
    # Charts
    df_trend = get_trend_data()
    
    if not df_trend.empty:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Token Savings Over Time")
            fig_tokens = px.area(df_trend, x='date', y='tokens_saved', template='plotly_dark',
                                 color_discrete_sequence=['#58a6ff'])
            st.plotly_chart(fig_tokens, use_container_width=True)
            
        with col_chart2:
            st.subheader("Carbon Prevented Over Time")
            fig_carbon = px.bar(df_trend, x='date', y='carbon_saved', template='plotly_dark',
                                color_discrete_sequence=['#3fb950'])
            st.plotly_chart(fig_carbon, use_container_width=True)
            
    else:
        st.info("No data available yet. Optimize some prompts to see your impact!")

# --- MEMORY PAGE ---
elif choice == "💾 Memory":
    st.title("Prompt Memory")
    st.markdown("Review your past optimizations and environmental impact.")
    
    df = get_all_history()
    
    if df.empty:
        st.info("No history found. Go to the Optimizer to get started.")
    else:
        # Display as a dataframe for simplicity and power
        display_df = df[['timestamp', 'optimization_mode', 'original_tokens', 'optimized_tokens', 'tokens_saved', 'efficiency_score']]
        st.dataframe(display_df, use_container_width=True)
        
        st.markdown("### Search & View Detailed Record")
        record_idx = st.selectbox("Select a record to view details:", df.index, format_func=lambda x: f"{df.loc[x, 'timestamp']} - Mode: {df.loc[x, 'optimization_mode']} - Score: {df.loc[x, 'efficiency_score']}")
        
        if record_idx is not None:
            record = df.loc[record_idx]
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.markdown("**Original Prompt:**")
            st.info(record['original_prompt'])
            st.markdown("**Optimized Prompt:**")
            st.success(record['optimized_prompt'])
            st.markdown("</div>", unsafe_allow_html=True)
            
        if st.button("🗑️ Clear All History", type="secondary"):
            clear_history()
            st.rerun()

# --- SETTINGS PAGE ---
elif choice == "⚙️ Settings":
    st.title("Platform Settings")
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("API Configuration")
    api_key = st.text_input("Groq API Key", value=get_setting('groq_api_key'), type="password")
    if st.button("Save API Key"):
        update_setting('groq_api_key', api_key)
        st.success("API Key saved securely in session!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("Cost & Impact Rates")
    
    col1, col2 = st.columns(2)
    with col1:
        cost_rate = st.number_input("Cost per 1M Tokens (USD)", value=float(get_setting('cost_per_1m_tokens_usd')), format="%.4f")
        inr_rate = st.number_input("USD to INR Conversion Rate", value=float(get_setting('usd_to_inr_rate')), format="%.2f")
    
    with col2:
        carbon_rate = st.number_input("Carbon Intensity (gCO2 per kWh)", value=float(get_setting('carbon_grams_per_kwh')), format="%.2f")
        energy_rate = st.number_input("Energy per Token (kWh)", value=float(get_setting('kwh_per_token')), format="%.6f")
        
    if st.button("Save Rates"):
        update_setting('cost_per_1m_tokens_usd', cost_rate)
        update_setting('usd_to_inr_rate', inr_rate)
        update_setting('carbon_grams_per_kwh', carbon_rate)
        update_setting('kwh_per_token', energy_rate)
        st.success("Rates updated successfully!")
    st.markdown("</div>", unsafe_allow_html=True)