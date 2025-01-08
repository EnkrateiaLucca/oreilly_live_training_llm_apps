# source: https://python.langchain.com/docs/tutorials/llm_chain/#:~:text=Server%E2%80%8B,with%20langserve.add_routes
#!/usr/bin/env python
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
# os.environ["LANGCHAIN_API_KEY"] = "YOUR API KEY"
os.environ["LANGCHAIN_PROJECT"] = "langchain-chatgpt-course-test"

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(title="LangChain Server",
              version="1.0",
              description="A simple API server using LangChain's Runnable interfaces for translation.",)
# 5. Adding chain route
add_routes(app,chain,path="/chain",)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)