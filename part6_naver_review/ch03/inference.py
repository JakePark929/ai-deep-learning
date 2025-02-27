import os
import json

from dotenv import load_dotenv
from openai import Client

from ch03.prompt_template import prompt_template, prompt_template_function_calling

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = Client(api_key=OPENAI_API_KEY)

def inference(review):
    prompt = prompt_template.format(review=review)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    output = response.choices[0].message.content

    return output

def inference_function_calling(review): 
    prompt = prompt_template_function_calling.format(review=review)
    tools = [
       {
            "type": "function",
            "function": {
                "name": "extract_positive_and_negetive_keywords",
                "description": "Extract positive keywords and negative keywords in given movie review.",
                "parameters": {
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "type": "object",
                    "properties": {
                        "positive_keywords": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "negative_keywords": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["positive_keywords", "negative_keywords"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        response_format={"type": "json_object"},
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "extract_positive_and_negetive_keywords"}}
    )
    output = response.choices[0].message.tool_calls[0].function.arguments
    output_json = json.loads(output)

    return output_json

if __name__ == '__main__':
    print(inference_function_calling("보는 내내 시간 가는 줄 모르고 정말 재밌게 봤습니다 ㅎㅎㅎㅎㅎ"))
    # print(inference_function_calling("너무 너무 재미없습니다 ㅎㅎㅎ"))