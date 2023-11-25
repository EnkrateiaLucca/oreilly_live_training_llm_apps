import streamlit as st
from openai import OpenAI
import os

# Function to query the language model.
def llm_model(prompt,openai_api_key):
    if openai_api_key != "":
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return
    client = OpenAI()
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", 
                             messages=
                             [
                                 {"role": "system", "content": "You are helpful assistant."},
                                 {"role": "user", "content": prompt}   
                             ])
    return response.choices[0].message.content

# Streamlit app
st.title('Chat with ChatGPT')

# Text input for the user's question.
openai_api_key = st.sidebar.text_input('__Enter your OpenAI API key:__', type='password')
prompt_question = st.text_input('__Enter the prompt for the model:__', '')

# Button to submit the question.
if st.button('Ask ChatGPT'):
    response = llm_model(prompt_question, openai_api_key)
    st.text_area('__ChatGPT response:__', response, height=200)
