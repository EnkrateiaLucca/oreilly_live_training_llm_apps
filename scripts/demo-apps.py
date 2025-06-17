import streamlit as st

st.set_page_config(
    page_title="Educational Demo Apps",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Educational Demo Applications")
st.sidebar.success("Select a demo from the sidebar above.")

st.markdown("""
## Welcome to the AI-Powered Educational Tools Collection!

This collection showcases various applications of AI in education and content management.

### Available Demos:

#### 📊 Quiz App
- AI-powered quiz generation from any content
- Multiple-choice question format
- Score tracking and performance visualization
- Export results to CSV

#### 🌎 Translation Hub
- Multi-language translation capabilities
- Support for 6 different languages
- Parallel translation viewing
- Professional-grade translations using AI

#### 📚 PDF Summarizer
- Multi-level text summarization
- Various summary styles (Narrative, Bullet Points, etc.)
- Interactive length adjustment
- Summary statistics and visualization
- PDF document support

#### 💬 Q&A System
- Interactive question-answering
- Context-aware responses
- Document-based knowledge base
- Customer support simulation

### Getting Started
1. Select any demo from the sidebar menu 👈
2. Each app will require an OpenAI API key
3. Follow the in-app instructions for specific features

### Note
These demos are educational tools designed to showcase the capabilities of AI in various educational contexts. They're built using Streamlit and powered by OpenAI's language models.
""")

# Add a footer with additional information
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <i>Built with Streamlit and OpenAI • For Educational Purposes</i>
</div>
""", unsafe_allow_html=True)