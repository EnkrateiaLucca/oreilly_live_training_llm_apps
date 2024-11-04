import streamlit as st
from openai import OpenAI
import os

st.session_state["translated_text"] = ""
# Initialize your OpenAI client


# Define your language options
languages = {
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Portuguese": "pt",
    "Hindi": "hi",
    "Chinese": "zh"
}

def translate_text(input_text, target_language, openai_api_key):
    if openai_api_key != "":
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return
    
    client = OpenAI()
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
    st.set_page_config(layout="wide")  # Make the app full-width
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    st.title("🌎 Multi-Language Translation Hub")

    # User input
    input_text = st.text_area("Enter text to translate", height=150)

    # Create a button to translate to all languages
    if st.button("Translate to Multiple Languages 🚀"):
        # Create two columns with 3 translations each
        col1, col2 = st.columns(2)
        
        # Dictionary to store translations
        translations = {}
        
        with st.spinner('Translating to all languages...'):
            # Generate all translations
            for lang_name, lang_code in languages.items():
                translations[lang_name] = translate_text(input_text, lang_code, openai_api_key)
        
        # Display translations in columns
        with col1:
            for lang in list(languages.keys())[:4]:
                with st.expander(f"🔤 {lang}", expanded=True):
                    st.text_area(
                        label="Translation",
                        value=translations.get(lang, ""),
                        height=150,
                        key=f"translation_{lang}",
                        disabled=True
                    )

        with col2:
            for lang in list(languages.keys())[4:]:
                with st.expander(f"🔤 {lang}", expanded=True):
                    st.text_area(
                        label="Translation",
                        value=translations.get(lang, ""),
                        height=150,
                        key=f"translation_{lang}",
                        disabled=True
                    )

if __name__ == "__main__":
    main()