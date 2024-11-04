import streamlit as st
# source for this code mostly from: https://towardsdatascience.com/run-interactive-sessions-with-chatgpt-in-jupyter-notebook-87e00f2ee461
import os
import glob
import requests
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from datetime import datetime
import glob
import chromadb

chromadb.api.client.SharedSystemClient.clear_system_cache()

st.session_state["chat_history"] = []


DATA_DIR = "./customer-tickets"

def qa_over_docs_setup(openai_api_key):
    if openai_api_key != "":
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return
    
    loader = DirectoryLoader(DATA_DIR, glob="*.txt")
    txt_docs = loader.load_and_split()
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(txt_docs, embeddings)
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0)
    system_prompt = (
    "You are a customer support assistant that answers questions about tickets. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}")

    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # prompt
    qa_chain = create_stuff_documents_chain(llm, prompt)
    qa = create_retrieval_chain(vectordb.as_retriever(), qa_chain)
    
    return qa

def show_documents():
    st.subheader("Documents")
    for doc in glob.glob("./customer-tickets/*.txt"):    
        with open(doc, "r") as f:
            st.write(doc)
            st.write(f.read())

def main():
    st.title("Q&A")
    st.image("./assets-resources/owl-customer-support.png", width=400)
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    show_docs = st.sidebar.checkbox("Show documents")
    chat_history = []
    qa = qa_over_docs_setup(openai_api_key)
    question = st.text_input("What is your question?")

    if question!="":
        try:
            response = qa.invoke({"input": f"{question}"})
            answer = response["answer"]
            st.session_state["chat_history"].append((question, answer))
        except Exception as e:
            answer = "<b>Error:</b> " + str(e)
        
        st.write(answer)
    
    if show_docs:
        show_documents()

if __name__ == "__main__":
    main()
