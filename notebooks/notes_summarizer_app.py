from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.schema import Document
import os
import requests
import streamlit as st

def load_text_file(uploaded_file):
    content = uploaded_file.read().decode("utf-8")
    content = Document(page_content=content)
    return content


def setup_summarization_chain(docs,openai_api_key):
    if openai_api_key != "":
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return
    llm = ChatOpenAI()
    prompt_template = """Write a concise summary of the following text:

    {text}

    The summary should be in this style: {style}.
    Let's think step by step.

    SUMMARY:"""

    prompt_summarization = PromptTemplate(template=prompt_template,
                            input_variables=["text", "style"])

    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt_summarization)
    return chain

def summarize_content(docs, chain, summary_option):
    """
    Runs the summarization chain with 
    the option specificed by the user.
    """
    summary = chain.run({"input_documents": docs, "style": summary_option})
    return summary

def main():
    st.title('Notes Summarizer using ChatGPT')
    # Option to upload a file or input text directly
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    option = st.sidebar.radio("Choose an input method:", ["Upload a .txt file", "Input text directly"])
    if option == "Upload a .txt file":
        uploaded_file = st.file_uploader("Choose a .txt file", type=['txt'])
        docs = ""
        if uploaded_file:
            docs = load_text_file(uploaded_file)
    else:
        docs_text = st.text_area("Enter your text here")
        docs = [Document(page_content=docs_text)]

    summary_option = st.sidebar.selectbox(
        'How do you want your summary?',
        ('Simple', 'Bullet points', 'Introduction, Argument, Conclusion')
    )

    if docs:
        chain = setup_summarization_chain(docs,openai_api_key)

    if st.sidebar.button('Summarize'):
        st.session_state.summary = summarize_content(docs, chain, summary_option)

    if 'summary' in st.session_state and st.session_state.summary:
        st.write('Your Summary: \n', st.session_state.summary)
        if st.sidebar.button('Download Summary'):
            with open('summary.txt', 'w') as f:
                f.write(st.session_state.summary)
            
            st.write("Your summary was downloaded to summary.txt")


if __name__ == "__main__":
    main()