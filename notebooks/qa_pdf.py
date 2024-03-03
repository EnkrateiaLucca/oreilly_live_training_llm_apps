import streamlit as st
from langchain.document_loaders import PyPDFLoader
import PyPDF2
from io import BytesIO
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
import pysqlite3 as sqlite3
from langchain.vectorstores import Chroma
from langchain.chains import ChatVectorDBChain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
 
def setup_pdf(file):
    """Read a PDF file and return its content as text."""
    reader = PyPDF2.PdfReader(BytesIO(file.read()))
    docs = []
    for page in range(len(reader.pages)):
        docs.append(Document(page_content=reader.pages[page].extract_text()))
    return docs


def setup_qa_chain(pdf_doc, openai_api_key):
    if openai_api_key != "":
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 500)
    persist_directory = './persist_directory/'
    embedding = OpenAIEmbeddings()
    all_splits = text_splitter.split_documents(pdf_doc)
    vectordb = Chroma.from_documents(all_splits, embedding=embedding,\
            persist_directory=persist_directory)
    vectordb.persist()
    # use ConversationalRetrievalChain
    pdf_qa = ChatVectorDBChain.from_llm(ChatOpenAI(temperature=0,\
    model_name="gpt-4"), vectordb)
    return pdf_qa


def main():
    st.header("Q&A with PDF 💬")
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # To read file as string:
        pdf_docs = setup_pdf(uploaded_file)
        pdf_qa = setup_qa_chain(pdf_docs,openai_api_key)
        st.write("Pdf Loaded!")
    
    # Accept user questions/query
    query = st.text_input("Ask questions about your PDF file:")
    st.write(f"Question: {query}")
    if query:
        result = pdf_qa({"question": query, "chat_history": []})
        answer = result["answer"]
        st.write(f"Answer: {answer}")
 
if __name__ == '__main__':
    main()