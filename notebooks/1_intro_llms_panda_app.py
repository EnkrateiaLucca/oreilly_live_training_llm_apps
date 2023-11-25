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
st.image("assets-resources/panda_letter.png", width=400)

if st.button("Write letter"):
    prompt = "Write a short love letter in 5 sentences from a 1700th century Panda who's been at war and is now returning to his lovely Panda Lady Pandesque."
    response = get_response(prompt)
    st.write(response)
    
    
    
