import streamlit as st
from openai import OpenAI
import os

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

st.title('ChatGPT Quiz Maker')

# Text input for the user's question.
user_input = st.text_input('Enter the subject or topic for the quiz:', '')
openai_api_key = st.sidebar.text_input('__Enter your OpenAI API key:__', type='password')

# Button to submit the input.
if st.button('Ask ChatGPT'):
    full_prompt = f"Act as an expert quiz maker and tutor. \
    You will help students create instructive quizzes on any subject matter,\
        the students will input a topic and you will output a quiz and the responses at the end.\
        Topic: {user_input},\
        Quiz:"
    st.markdown("__Topic:__ " + user_input)
    st.write("__Full prompt for the model:__ ", full_prompt)
    response = llm_model(full_prompt, openai_api_key)
    st.text_area('__ChatGPT response:__', response, height=200)