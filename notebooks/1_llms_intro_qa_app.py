import streamlit as st
# source for this code mostly from: https://towardsdatascience.com/run-interactive-sessions-with-chatgpt-in-jupyter-notebook-87e00f2ee461
import os
import glob
import requests
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from datetime import datetime

st.session_state["chat_history"] = []

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def download_docs():
    # List of file URLs (raw GitHub content URLs)
    file_urls = [
        "https://raw.githubusercontent.com/EnkrateiaLucca/oreilly_live_training_llm_apps/main/notebooks/docs/james.txt",
        "https://raw.githubusercontent.com/EnkrateiaLucca/oreilly_live_training_llm_apps/main/notebooks/docs/maria.txt",
        "https://raw.githubusercontent.com/EnkrateiaLucca/oreilly_live_training_llm_apps/main/notebooks/docs/sofia.txt",
        "https://raw.githubusercontent.com/EnkrateiaLucca/oreilly_live_training_llm_apps/main/notebooks/docs/tom.txt",
        "https://raw.githubusercontent.com/EnkrateiaLucca/oreilly_live_training_llm_apps/main/notebooks/docs/robert.txt",
        # Add more file URLs as needed
    ]

    # Directory where files will be downloaded
    download_dir = "docs"
    os.makedirs(download_dir, exist_ok=True)

    txt_docs = []

    for url in file_urls:
        # Extract filename from URL
        filename = url.split("/")[-1]
        local_file_path = os.path.join(download_dir, filename)

        # Download and save the file
        download_file(url, local_file_path)

        # Load the content of the file
        with open(local_file_path, 'r') as file:
            content = file.read()
            txt_docs.append(content)


def qa_over_docs_setup(openai_api_key):
    if openai_api_key != "":
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return
    
    loader = DirectoryLoader("./docs", glob="*.txt")
    txt_docs = loader.load_and_split()
    embeddings = OpenAIEmbeddings()
    txt_docsearch = Chroma.from_documents(txt_docs, embeddings)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=txt_docsearch.as_retriever())
    
    return qa

def show_documents():
    st.subheader("Documents")
    for doc in glob.glob("./docs/*.txt"):    
        with open(doc, "r") as f:
            st.write(doc)
            st.write(f.read())

def main():
    st.title("Q&A")
    st.image("https://github.com/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/assets-resources/owl.png?raw=true", width=400)
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    show_docs = st.sidebar.checkbox("Show documents")
    with st.spinner():
        download_docs()
    
    chat_history = []
    qa = qa_over_docs_setup(openai_api_key)
    question = st.text_input("What is your question?")

    if question!="":
        try:
            response = qa({"question": f"{question}", "chat_history": st.session_state["chat_history"]})
            answer = response["answer"]
            st.session_state["chat_history"].append((question, answer))
        except Exception as e:
            answer = "<b>Error:</b> " + str(e)
        
        st.write(answer)
    
    if show_docs:
        show_documents()

if __name__ == "__main__":
    main()
