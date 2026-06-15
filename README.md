# 🧠 EcoMind AI - Sustainable Intelligence Starts Here

**EcoMind AI** is an AI Sustainability Intelligence Platform. It analyzes prompts, measures efficiency, estimates token waste, predicts cost impact, estimates carbon emissions, and generates optimized prompts that achieve the exact same objective with lower computational and environmental costs.

This project was built to demonstrate full-stack AI product development, featuring an intuitive, premium, dark-mode Streamlit UI, integrated with the ultra-fast Groq API and LLaMA 3 8B.

---

## 🌟 Features

- **Prompt Intelligence Engine:** Analyzes your prompt across three modes: Concise, Balanced, and Maximum Efficiency.
- **Token Intelligence:** Calculates original vs. optimized tokens and displays savings.
- **Cost Intelligence:** Real-time cost estimation in USD and INR.
- **Carbon Intelligence:** Estimates Energy Usage (kWh) and Carbon Emissions (gCO2).
- **Smart Dashboard:** Interactive Plotly charts for tracking total tokens, cost, and carbon saved over time.
- **Prompt Memory:** SQLite-powered history to search, view, and replay past prompt optimizations.
- **PDF Reports:** One-click beautiful PDF generation of your sustainability intelligence metrics.
- **Settings Configuration:** Fully customizable Cost Rates, Carbon Factors, and API keys.

---

## 📸 Screenshots

*(Add screenshots of the Optimizer, Dashboard, and Memory tabs here!)*

---

## 🏗️ Architecture

The project is structured into modular components:

- `app.py`: The main Streamlit entry point handling UI, routing, and custom CSS.
- `optimizer.py`: Handles API interactions with Groq and LLM prompt engineering.
- `database.py`: SQLite wrapper for persisting prompt memory.
- `analytics.py`: Data aggregation and metric calculations for the Dashboard.
- `carbon.py` & `cost.py`: Core logic for environmental and financial impact estimations.
- `pdf_generator.py`: Custom PDF builder using `fpdf2`.
- `settings.py`: Session state manager for user configurations.

---

## 🚀 Installation

1. **Clone the repository** (or download the files).
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**
   Rename `.env.example` to `.env` and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

---

## 💻 Usage

Run the Streamlit application:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

1. Go to **Settings** and ensure your Groq API key is present.
2. Go to **Optimizer**, paste a long, inefficient prompt, and select an optimization mode.
3. Click **✨ Optimize Prompt** to see the magic.
4. Download your **PDF Report** or visit the **Dashboard** to see your lifetime impact!

---

## 🤝 Interview Explanation

If you are a hiring manager or recruiter reading this, here is why EcoMind AI stands out:
- **Clean Code & Modularity:** I avoided writing a massive monolithic `app.py`. Instead, logic is separated by domain (`optimizer`, `carbon`, `cost`, `analytics`).
- **Real-World Value:** It solves a real problem—token waste in LLM applications, which translates directly to API cost overhead and carbon footprint.
- **UX/UI Obsession:** The Streamlit default UI was completely overridden with custom CSS to provide a 'Vercel/Linear' startup feel. 
- **Error Resilience:** The app gracefully handles missing API keys, empty prompts, and prevents crashes.

---

## 🔮 Future Scope

- Support for OpenAI, Anthropic, and Gemini models.
- Enterprise SSO Integration.
- Batch prompt optimization (CSV upload).
- Integration with CI/CD pipelines to analyze prompt efficiency in production codebases.

---

*Built with ❤️ for a more sustainable AI future.*
