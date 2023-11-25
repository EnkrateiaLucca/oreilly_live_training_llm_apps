import streamlit as st
from openai import OpenAI

def get_response(prompt):
    client = OpenAI()
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", 
                             messages=
                             [
                                 {"role": "system", "content": "You are an expert writer poet."},
                                 {"role": "user", "content": prompt}   
                             ])
    return response.choices[0].message.content

st.title("The Panda Warrior")
prompt_background_panda = st.sidebar.text_area("Write a different background story for the panda")
st.image("assets-resources/panda_letter.png", width=400)



if st.button("Write letter"):
    if prompt_background_panda != "":
        prompt = f"{prompt_background_panda}. Write a short love letter in 5 sentences."
    else:
        prompt_background_panda = "You are a 1700th century Panda who's been at war and is now returning to his lovely Panda Lady Pandesque."
        prompt = f"{prompt_background_panda}. Write a short love letter in 5 sentences."
    
    response = get_response(prompt)
    st.write(response)
    
    
    
