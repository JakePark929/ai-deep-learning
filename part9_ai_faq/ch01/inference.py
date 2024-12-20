import os

from dotenv import load_dotenv
from openai import Client
from sympy import product

from download_data import get_data
from prompt_template import prompt_template

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = Client(api_key=OPENAI_API_KEY)

def inference(product_detail):
    prompt = prompt_template.format(product_detail=product_detail)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )
    output = response.choices[0].message.content

    return output

if __name__ == "__main__":
    product_detail = get_data()
    print(inference(product_detail))