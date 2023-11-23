import streamlit as st
# source for this code mostly from: https://towardsdatascience.com/run-interactive-sessions-with-chatgpt-in-jupyter-notebook-87e00f2ee461
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from datetime import datetime

st.title("Q&A")
st.image("./assets-resources/owl.png", width=400)

# loader = DirectoryLoader("./docs/", glob="*.txt")
# txt_docs = loader.load_and_split()

# embeddings = OpenAIEmbeddings()
# txt_docsearch = Chroma.from_documents(txt_docs, embeddings)

# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

# chat_history = []
# qa = ConversationalRetrievalChain.from_llm(llm, retriever=txt_docsearch.as_retriever())
st.session_state["chat_history"] = []

question = st.text_input("What is your question?")

if question!="":
    try:
        response = qa({"question": f"{question}", "chat_history": st.session_state["chat_history"]})
        answer = response["answer"]
        st.session_state["chat_history"].append((question, answer))
    except Exception as e:
        answer = "<b>Error:</b> " + str(e)
    
    st.write(answer)
