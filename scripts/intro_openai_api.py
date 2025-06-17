from openai import OpenAI
# from dotenv import load_dotenv
# import os

# load_dotenv()

client = OpenAI()


def summarize_text(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a summarization engine. \
            You take in content and you output a bullet point summary of that content."},
                {"role": "user", "content": text}]
    )
    return response.choices[0].message.content

def load_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    text = load_file("../notebooks/assets-resources/Reinventing-explanation.txt")
    print(summarize_text(text))