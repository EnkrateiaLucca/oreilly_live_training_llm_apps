import streamlit as st
from pypdf import PdfReader
import openai
from openai import OpenAI
import numpy as np
import plotly.graph_objects as go
import os

MODEL = "gpt-4o-mini"

# Add this after the imports
SUMMARY_TYPES = {
    "Narrative": "Create a flowing narrative summary",
    "Bullet Points": "Create a bullet-point summary with key points",
    "Structure": "Create a structured summary with sections and subsections",
    "Key Concepts": "Focus on main concepts and their relationships",
    "Executive": "Create an executive summary style with context and recommendations"
}

st.set_page_config(page_title="PDF Summarizer", layout="wide")
st.title("Multi-Level PDF Summarizer")

# Initialize OpenAI client
@st.cache_resource
def load_client():
    api_key = os.environ.get("OPENAI_API_KEY") or st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if not api_key:
        st.error("Please enter your OpenAI API key")
        st.stop()
    return OpenAI(api_key=api_key)

client = load_client()


def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



def generate_summaries(text, summary_type, num_levels=5):
    target_lengths = np.geomspace(50, len(text.split()), num=num_levels).astype(int)
    summaries = []
    
    system_prompts = {
        "Bullet Points": "Produce a basic bullet-point summary of main ideas. For each section, expand with detailed bullet points highlighting specific information. Begin each main point with a • symbol, ensuring consistency across sections.",
        "Narrative": "Generate a concise narrative summary that begins with a basic overview. For each subsequent section, provide a more detailed narrative summary, maintaining flow and including critical information.",
        "Structure": "Start with a high-level structured summary, introducing the main sections (e.g., Introduction, Main Points, Conclusion). For each section, develop a detailed summary under clear headers, preserving structured consistency.",
        "Key Concepts": "Begin with a compressed overview of core concepts. For each section, elaborate on the main concepts and their relationships, sorted by importance within each section. Ensure organized conceptual clarity across levels.",
        "Executive": "Create a high-level executive summary that includes context and key findings. For each section, provide a more detailed executive-style summary, covering additional insights and, when relevant, recommendations, maintaining clarity throughout."
    }
    
    for target_length in target_lengths:
        prompt = f"Summarize the following text in approximately {target_length} words using a {summary_type.lower()} style:\n\n{text}"
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompts[summary_type]},
                {"role": "user", "content": prompt}
            ]
        )
        summaries.append(response.choices[0].message.content)
    return summaries

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if 'summaries_dict' not in st.session_state:
        st.session_state.summaries_dict = {}
        
    with st.spinner('Extracting text from PDF...'):
        if 'text' not in st.session_state:
            st.session_state.text = extract_text_from_pdf(uploaded_file)
    
    # Add summary type selector
    summary_type = st.selectbox(
        "Select Summary Type",
        list(SUMMARY_TYPES.keys()),
        help="Choose the style of summary you want to generate"
    )
    
    if summary_type not in st.session_state.summaries_dict:
        with st.spinner(f'Generating {summary_type.lower()} summaries at different levels...'):
            num_levels = st.sidebar.slider("Number of Summary Levels", 5, 10, 5)
            st.session_state.summaries_dict[summary_type] = generate_summaries(
                st.session_state.text,
                summary_type,
                num_levels
            )
    
    summaries = st.session_state.summaries_dict[summary_type]
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Summary Level")
        level = st.slider("Adjust summary detail level", 1, len(summaries), len(summaries)//2)
        
        st.write("Summary Statistics:")
        original_length = len(st.session_state.text.split())
        summary_length = len(summaries[level-1].split())
        st.write(f"Original text: {original_length} words")
        st.write(f"Summary: {summary_length} words")
        st.write(f"Compression ratio: {summary_length/original_length:.2%}")
        
        if st.sidebar.checkbox("Show Original Text"):
            st.subheader("Original Text")
            st.write(st.session_state.text)
        
    with col2:
        st.subheader("Summary")
        summary = summaries[level-1]
        st.markdown(summary)
        st.download_button("Download Summary", summary)
        
        # Plot summary lengths
        if st.sidebar.checkbox("Show Summary Lengths"):
            lengths = [len(summary.split()) for summary in summaries]
            fig = go.Figure(data=go.Scatter(
                x=list(range(1, num_levels+1)),
                y=lengths,
                mode='lines+markers',
                name='Summary Length'
            ))
            fig.update_layout(
                title="Summary Length by Level",
            xaxis_title="Summary Level",
            yaxis_title="Word Count"
            )
            st.plotly_chart(fig)
else:
    st.info("Please upload a PDF file to begin.")
