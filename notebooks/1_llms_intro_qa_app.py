import streamlit as st
# source for this code mostly from: https://towardsdatascience.com/run-interactive-sessions-with-chatgpt-in-jupyter-notebook-87e00f2ee461
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from datetime import datetime
import os
import glob

st.session_state["chat_history"] = []

def qa_over_docs_setup(openai_api_key):
    if openai_api_key != "":
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return
    
    loader = DirectoryLoader("./docs/", glob="*.txt")
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
