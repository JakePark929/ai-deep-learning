import os
import re
import json
from typing import List

from dotenv import load_dotenv
from openai import Client
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

from ch01.download_data import get_data
from ch01.prompt_template import prompt_template, prompt_template_json

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

class QA(BaseModel):
    question: str
    answer: str

class Output(BaseModel):
    qa_list: List[QA]

output_parser = PydanticOutputParser(pydantic_object=Output)

def inference_json(product_detail):
    prompt = prompt_template_json.format(
        format_instruction=output_parser.get_format_instructions(),
        product_detail=process_text(product_detail)
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    cost = calculate_cost(response.usage.prompt_tokens, response.usage.completion_tokens)
    print(f"cost: {cost:.3f} 원")
    output = response.choices[0].message.content
    output_json = json.loads(output)   

    return output_json

def calculate_cost(prompt_tokens, completion_tokens):

    return (prompt_tokens / 1000000 * 0.15 + completion_tokens / 1000000 * 0.6) * 1400

def process_text(text):
    text = re.sub(r'\n+', '\n', text) # 연속된 개행 문자를 하나의 개행 문자로 줄이기
    text = re.sub(r' +', ' ', text) # 연속된 공백을 하나의 공백으로 줄이기
    
    return text.strip()

if __name__ == "__main__":
    product_detail = get_data()
    result = inference_json(product_detail)

    print(json.dumps(result, indent=2, ensure_ascii=False))