import os
from openai import OpenAI
from pydantic import BaseModel, Field
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ProductInfo(BaseModel):
    product_description: str = Field(description="The description title of the product")
    product_price: str = Field(description="The price of the product")
    product_rating: str = Field(description="The rating of the product")
    product_brand: str = Field(description="The brand of the product")

def load_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

def extract_product_info_with_chatgpt(product_page_raw_text: str) -> ProductInfo:
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
             You are a helpful assistant that extracts product information from an amazon page text.
             You will be given a raw product page text and you will need to extract the product information:
             - product description
             - product price
             - product rating
             - product brand
             """},
            {"role": "user", "content": product_page_raw_text}
        ],
        temperature=0,
        response_format=ProductInfo
    )
    
    return response.choices[0].message.parsed

def transform_product_info_to_table(product_info: ProductInfo) -> str:
    columns = ["product_description", "product_price", "product_rating", "product_brand"]
    data = [[
        product_info.product_description,
        product_info.product_price,
        product_info.product_rating,
        product_info.product_brand
    ]]
    df = pd.DataFrame(data, columns=columns)
    return df

file_path = "/Users/greatmaster/Desktop/projects/oreilly-live-trainings/oreilly_live_training_llm_apps/notebooks/assets-resources/shoes_product_page_raw.txt"

product_page_text = load_file(file_path)

product_info = extract_product_info_with_chatgpt(product_page_text)
print(transform_product_info_to_table(product_info))

