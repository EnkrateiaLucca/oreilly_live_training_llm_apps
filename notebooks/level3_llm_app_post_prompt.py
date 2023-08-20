import streamlit as st
import openai

def llm_model(prompt_question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful research and programming assistant"},
            {"role": "user", "content": prompt_question}
        ]
    )
    return response["choices"][0]["message"]["content"]

st.title('ChatGPT Essay Writer')

# Text input for the user's question.
user_input = st.text_input('Enter the subject for the essay:', '')

# Button to submit the input.
if st.button('Ask ChatGPT'):
    full_prompt = f"Act as an expert writer and researcher. You will be prompted with a subject and you will output a one paragraph essay about it. Subject: {user_input}, Essay:"
    st.write("Full prompt for the model: ", full_prompt)
    # Get the response from the model.
    response = llm_model(full_prompt)
    # Correct the grammar of the response.
    prompt_grammar = "Correct any grammar mistakes in the following text and return the corrected text: " + response
    grammar_corrected_response = llm_model(prompt_grammar)
    st.markdown("Post prompt: " + prompt_grammar)
    st.text_area('Grammar Corrected ChatGPT response:', grammar_corrected_response, height=200)
