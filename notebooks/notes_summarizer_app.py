from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
import streamlit as st

def load_text_file(text_file):
    docs = TextLoader(text_file).load()
    return docs


def setup_summarization_chain(docs):
    llm = ChatOpenAI()
    prompt_template = """Write a concise summary of the following text:

    {text}

    The summary should be in this style: {style}.
    Let's think step by step.

    SUMMARY:"""

    PROMPT = PromptTemplate(template=prompt_template,
                            input_variables=["text", "style"])

    chain = load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT)
    return chain


def summarize_content(docs, chain, summary_option):
    """
    Runs the summarization chain with 
    the option specificed by the user.
    """
    summary = chain.run({"input_documents": docs, "style": summary_option})
    return summary



st.title('Notes Summarizer using ChatGPT')
uploaded_file = st.text_input("Choose a .txt file")

summary_option = st.selectbox(
    'How do you want your summary?',
    ('Simple', 'Bullet points', 'Introduction, Argument, Conclusion', 'Custom Summary')
)

if uploaded_file!="":
    docs = load_text_file(uploaded_file)
    chain = setup_summarization_chain(docs)

if st.button('Summarize'):
    st.session_state.summary = summarize_content(docs, chain, summary_option)

if 'summary' in st.session_state and st.session_state.summary:
    st.write('Your Summary: ', st.session_state.summary)
    if st.button('Download Summary'):
        with open('summary.txt', 'w') as f:
            f.write(st.session_state.summary)
        
        st.write("Your summary was downloaded to summary.txt")
