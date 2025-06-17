import streamlit as st
from openai import OpenAI
import os
import wget

if os.environ.get("OPENAI_API_KEY") is None:
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    os.environ["OPENAI_API_KEY"] = openai_api_key

client = OpenAI()


def generate_image(prompt: str, filename: str = "output_image.png", size: str = "1024x1024"):
    """
    Generates an image using the DALL·E 3 model and saves it to a file.

    Args:
    prompt (str): The text prompt to generate the image.
    filename (str): The output filename for saving the image.
    size (str): The size of the generated image (default: 1024x1024).
    
    Returns:
    str: The path to the saved image file.
    """
    # Check if file already exists
    if os.path.exists(filename):
        abs_path = os.path.abspath(filename)
        print(f'Using existing image at {abs_path}')
        return abs_path
        
    # Generate the image using the DALL·E 3 model
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size, # Must be one of 1024x1024 , 1792x1024 , or 1024x1792 for dall-e-3 models.
        quality="standard",
        n=1
    )
    
    image_url = response.data[0].url
    wget.download(image_url, filename)
    
    abs_path = os.path.abspath(filename)
    print(f'Saved image to {abs_path}')
    return abs_path

def get_response(prompt):
    response = client.chat.completions.create(model="gpt-4o-mini", 
                             messages=
                             [
                                 {"role": "system", "content": "You are the most insanely creative writer of all times."},
                                 {"role": "user", "content": prompt}   
                             ])
    return response.choices[0].message.content


st.title("The Panda Warrior")
cover_image_character = st.sidebar.selectbox("Select your prefered character", ["Panda Warrior", "Punk Elmo", "Drunk OWL", "Funky Penguin"], index=0)


def get_character_info(character: str) -> None:
    """Display the image for the selected character."""
    if character == "Panda Warrior":
        image_path = "../notebooks/assets-resources/panda_letter.png"
    else:
        st.write(f"Generating cover image for {character}...")
        prompt = f"Generate a creative outside the box like cover image for this character of a story: {character}."
        image_path = generate_image(prompt, filename=f"{character}_cover_image.png")
    
    st.image(image_path, width=400)
    
    prompt = f"Generate a funny and creative short backstory for this character: {character}. Make it one paragraph max."
    backstory = get_response(prompt)
    return backstory    

backstory = get_character_info(cover_image_character)

if cover_image_character == "Panda Warrior":
    default_background = "A mighty panda warrior who trained in the bamboo forests of ancient China, mastering both martial arts and meditation. This noble creature now protects the forest and teaches young pandas the way of inner peace and outer strength."
    prompt_background = st.sidebar.text_area("Write a different background story for the panda", value=default_background)
else:
    prompt_background = st.sidebar.text_area("Write a different background story for the panda", value=backstory)

if st.button("Write Story"):
    if prompt_background != "":
        prompt = f"{prompt_background}. Write a super short story using the 3 act structure for about this character:"
    response = get_response(prompt)
    st.write(response)
    
    
    
