import streamlit as st
from openai import OpenAI
st.session_state["translated_text"] = ""
# Initialize your OpenAI client
client = OpenAI()

# Define your language options
languages = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Portuguese": "pt"
}

def translate_text(input_text, target_language):
    # Here, you'll need to tailor the prompt to instruct ChatGPT to translate
    # Adjust the prompt according to your needs and the capabilities of the model
    prompt = f"Translate this into {target_language}: {input_text}"
    
    # Make the API call to OpenAI (adjust as per the actual API requirements)
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", 
                             messages=
                             [
                                 {"role": "system", "content": "You are a helpful assistant."},
                                 {"role": "user", "content": prompt}   
                             ],
                             temperature=0.0,
                             n = 1
                             )

    # Extract the translated text from the response
    # This may need to be adjusted based on the actual response structure
    translated_text = response.choices[0].message.content.strip()

    return translated_text

def main():
    st.title("Simple Translation App")

    # User inputs
    input_text = st.text_area("Enter text to translate", height=150)
    target_language = st.selectbox("Select target language", list(languages.keys()))

    # Translate button
    if st.button("Translate"):
        # Perform the translation
        st.session_state["translated_text"] = translate_text(input_text, languages[target_language])
        
        # Display the translated text
    
    if st.session_state["translated_text"]!="":
        st.write(st.session_state["translated_text"])

if __name__ == "__main__":
    main()