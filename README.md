# O'Reilly Live Trainining - Building Text Based Applications with the ChatGPT API and Langchain

## Setup

**Conda**

- Install [anaconda](https://www.anaconda.com/download)
- This repo was tested on a Mac with python=3.10.
- Create an environment: `conda create -n oreilly-env python=3.10`
- Activate your environment with: `conda activate oreilly-env`
- Install requirements with: `pip install -r requirements.txt`
- Setup your openai [API key](https://platform.openai.com/)

**Pip**


1. **Create a Virtual Environment:**
    Navigate to your project directory. Make sure you hvae python3.10 installed! 
    If using Python 3's built-in `venv`:
    ```bash
    python -m venv oreilly-env
    ```
    If you're using `virtualenv`:
    ```bash
    virtualenv oreilly-env
    ```

2. **Activate the Virtual Environment:**
    - **On Windows:**
      ```bash
      .\oreilly-env\Scripts\activate
      ```
    - **On macOS and Linux:**
      ```bash
      source oreilly-env/bin/activate
      ```

3. **Install Dependencies from `requirements.txt`:**
    ```bash
    pip install python-dotenv
    pip install -r requirements.txt
    ```

4. Setup your openai [API key](https://platform.openai.com/)

Remember to deactivate the virtual environment once you're done by simply typing:
```bash
deactivate
```

## Setup your .env file

- Change the `.env.example` file to `.env` and add your OpenAI API key.

## To use this Environment with Jupyter Notebooks:

- ```pip install jupyter```
- ```python3 -m ipykernel install --user --name=oreilly-env```

## Notebooks

Here are the notebooks available in the `notebooks/` folder:

1. [Intro to ChatGPT API & Prompt Basics](notebooks/1.0-Intro-ChatGPT-API-prompt-basics.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/1.0-Intro-ChatGPT-API-prompt-basics.ipynb)

2. [Applying Prompt Engineering Strategies](notebooks/2.0-applying-prompt-engineering-strategies.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/2.0-applying-prompt-engineering-strategies.ipynb)

3. [Prompt Engineering Guide](notebooks/2.1-prompt-engineering-guide.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/2.1-prompt-engineering-guide.ipynb)

4. [Fine-tuning ChatGPT API](notebooks/3.0-fine-tuning-chatgpt-api.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/3.0-fine-tuning-chatgpt-api.ipynb)

5. [Intro to LangChain](notebooks/4.0-intro-to-langchain.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/4.0-intro-to-langchain.ipynb)

6. [Q&A with LangChain](notebooks/4.1-qa-with-langchain.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/4.1-qa-with-langchain.ipynb)

7. [Quiz Generator App](notebooks/5-quiz_generator_app.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/5-quiz_generator_app.ipynb)

8. [Notes Summarizer App](notebooks/6-notes_summarizer_app.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/6-notes_summarizer_app.ipynb)

9. [General Intro to LLMs](notebooks/general-intro-to-llms.ipynb)
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/general-intro-to-llms.ipynb)

10. [Prompt Engineering Techniques: Knowledge Generation](notebooks/prompt-engineering-techniques-knowledge-generation.ipynb)
    
    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/prompt-engineering-techniques-knowledge-generation.ipynb)

11. [Prompt Engineering Techniques](notebooks/prompt-engineering-techniques.ipynb)
    
    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/EnkrateiaLucca/oreilly_live_training_llm_apps/blob/main/notebooks/prompt-engineering-techniques.ipynb)
