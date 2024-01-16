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

st.title('ChatGPT Essay Writer')
openai_api_key = st.sidebar.text_input('__Enter your OpenAI API key:__', type='password')
# Text input for the user's question.
user_input = st.text_input('Enter the subject for the essay:', '')

# Button to submit the input.
if st.button('Ask ChatGPT'):
    full_prompt = f"Act as an expert writer and researcher. You will be prompted with a subject and you will output a one paragraph essay about it. Subject: {user_input}, Essay:"
    st.write("Full prompt for the model: ", full_prompt)
    # Get the response from the model.
    response = llm_model(full_prompt,openai_api_key)
    # Correct the grammar of the response.
    prompt_grammar = "Correct any grammar mistakes in the following text and return the corrected text: " + response
    grammar_corrected_response = llm_model(prompt_grammar, openai_api_key)
    st.markdown("Post prompt: " + prompt_grammar)
    st.text_area('Grammar Corrected ChatGPT response:', grammar_corrected_response, height=200)
