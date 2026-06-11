# /// script
# requires-python = ">=3.11"
# dependencies = ["streamlit==1.37.0", "openai"]
# ///
#
# NOTE: streamlit is pinned to 1.37.0 on purpose. Streamlit's newer
# uvicorn/ASGI server (>=~1.55, incl. 1.58) fails to initialize the
# websocket session on this machine -> the app loads but is stuck on
# the gray skeleton placeholders ("Connection error" / never hydrates).
# 1.37.0 uses the proven Tornado server and works. Don't unpin without
# re-testing that the page actually renders.
#
# Run with (the --with flags ensure the pinned deps are used for the
# `streamlit` command itself, not just the script import):
#   uv run --with streamlit==1.37.0 --with openai streamlit run demo-app-panda-letters.py
import streamlit as st
from openai import OpenAI
import os
import urllib.request

if os.environ.get("OPENAI_API_KEY") is None:
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key

if not os.environ.get("OPENAI_API_KEY"):
    st.info("Please enter your OpenAI API key in the sidebar to continue.")
    st.stop()

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
        size=size,  # Must be one of 1024x1024 , 1792x1024 , or 1024x1792 for dall-e-3 models.
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    urllib.request.urlretrieve(image_url, filename)

    abs_path = os.path.abspath(filename)
    print(f'Saved image to {abs_path}')
    return abs_path


def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are the most insanely creative writer of all times."},
            {"role": "user", "content": prompt}
        ])
    return response.choices[0].message.content


st.title("The Panda Warrior")
cover_image_character = st.sidebar.selectbox(
    "Select your prefered character",
    ["Panda Warrior", "Punk Elmo", "Drunk OWL", "Funky Penguin"],
    index=0,
)


def get_character_info(character: str) -> str:
    """Display the image for the selected character and return its backstory."""
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
    if prompt_background.strip():
        prompt = f"{prompt_background}. Write a super short story using the 3 act structure for about this character:"
        response = get_response(prompt)
        st.write(response)
    else:
        st.warning("Please provide a background story first.")
