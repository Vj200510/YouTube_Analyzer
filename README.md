# Agentic Agno - YouTube Analyzer & Multi-Agent Framework

## 🚀 Quick Start (Local)

1. Clone repo
2. `pip install -r requirements.txt`
3. Create `api_keys.env`:
   ```
   GROQ_API_KEY=your_groq_key_here
   ```
4. Run YouTube Analyzer:
   ```
   streamlit run ui.py
   ```

## ☁️ Streamlit Cloud Deployment

1. Push to GitHub (requirements.txt auto-installs deps)
2. Deploy on [share.streamlit.io](https://share.streamlit.io)
3. In app settings → Secrets: Add `GROQ_API_KEY=your_key`
4. App live! Paste YouTube URL to analyze.

## 📁 Project Structure
- `ui.py`: Streamlit UI for YouTube Analyzer
- `youtube_analyzer.py`: Core agent + YouTube tools
- `agent.py`, `finance.py`, `memory.py`, `team.py`: Example agents

## 🔧 Dependencies
Handled by `requirements.txt`:
- streamlit
- python-dotenv
- groq + agno-agi framework
- Tools: yfinance, duckduckgo-search, yt-dlp

## Notes
- API keys ignored via `.gitignore`
- Built with [agno-agi](https://github.com/agno-agi/agno) for agentic workflows.

Enjoy analyzing! 🎥
