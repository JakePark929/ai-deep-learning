import os
import json
from typing import List

from dotenv import load_dotenv
from openai import Client
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

from download_data import get_urls
from prompt_template import prompt_template

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = Client(api_key=OPENAI_API_KEY)

def inference(url_list):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": "다음 사진의 내용을 읽고 FAQ를 한국어로 만들어 주세요."
                    },
                    {
                        "type": "image_url", 
                        "image_url": {
                            "url": url_list[0]
                        }
                    }
                ]
            }
        ],
        max_tokens=1000,
    )
    print(url_list[0])
    output = response.choices[0].message.content

    return output

def inference_many(url_list):
    content = [
        {"type": "text", "text": "다음 사진들의 내용을 읽고 FAQ를 한국어로 만들어 주세요."}
    ]
    for url in filter_image_urls(url_list):
        content.append({"type": "image_url", "image_url": {"url": url}})
    print(content)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=1000,
    )

    output = response.choices[0].message.content

    return output

def filter_image_urls(url_list, max_count=5):
    valid_extensions = ['png', 'jpeg', 'gif', 'webp']

    filtered_urls = [
        url for url in url_list
        if url.split('?')[0].split('.')[-1].lower() in valid_extensions
    ]
    
    return filtered_urls[:max_count]

class QA(BaseModel):
    question: str
    answer: str

class Output(BaseModel):
    qa_list: List[QA]

output_parser = PydanticOutputParser(pydantic_object=Output)

def inference_many_json(url_list):
    prompt = prompt_template.format(format_instruction=output_parser.get_format_instructions())
    content = [
        {"type": "text", "text": prompt}
    ]
    for url in filter_image_urls(url_list):
        content.append({"type": "image_url", "image_url": {"url": url}})
    print(content)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": content}
        ],
        max_tokens=1000,
        response_format={"type": "json_object"}
    )
    output = response.choices[0].message.content
    output_json = json.loads(output)   

    return output_json

if __name__ == "__main__":
    url_list = get_urls()
    result = inference_many_json(url_list)

    print(json.dumps(result, indent=2, ensure_ascii=False))