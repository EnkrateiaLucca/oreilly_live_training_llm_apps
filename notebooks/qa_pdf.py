import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ChatVectorDBChain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
 


def setup_pdf_qa(pdf):
    st.session_state.pdf = pdf
    loader = PyPDFLoader(pdf)    
    pdf_doc = loader.load_and_split()
    return pdf_doc



def setup_qa_chain(pdf_doc):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 500)
    persist_directory = './persist_directory/'
    embedding = OpenAIEmbeddings()
    all_splits = text_splitter.split_documents(pdf_doc)
    vectordb = Chroma.from_documents(all_splits, embedding=embedding,\
            persist_directory=persist_directory)
    vectordb.persist()
    pdf_qa = ChatVectorDBChain.from_llm(ChatOpenAI(temperature=0,\
    model_name="gpt-4"), vectordb)
    return pdf_qa
 
def main():
    st.header("Q&A with PDF 💬")
    # upload a PDF file
    pdf = st.text_input("Copy the path to the PDF here:")
 
    # st.write(pdf)
    if st.button("Load PDF"):
        st.session_state.pdf_doc = setup_pdf_qa(pdf)
        st.write("PDF loaded!")
    # Accept user questions/query
    query = st.text_input("Ask questions about your PDF file:")
    # st.write(query)
    if query:
        pdf_qa = setup_qa_chain(st.session_state.pdf_doc)
        result = pdf_qa({"question": query, "chat_history": []})
        st.write(result["answer"])
 
if __name__ == '__main__':
    main()