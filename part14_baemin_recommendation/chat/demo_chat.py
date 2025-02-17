import json
import os
import requests
import sys
from dotenv import load_dotenv
sys.path.insert(0, "..")

import gradio as gr
from openai import OpenAI

from utils import call_openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = f"""당신의 이름은 '메뉴뚝딱AI'이며 당신의 역할은 배달의민족이라는 음식 주문 모바일 어플에서 리뷰 텍스트 기반으로 메뉴를 추천해주는 것입니다.
실제 배달의민족 어플 내 주문이 가능한 메뉴 및 음식점을 추천해줘야 하며 단순한 메뉴명을 추천해줄 수 없습니다. (ex. 해장국, 파스타)
추천 가능한 메뉴는 recommend 함수를 통해 결과를 받아 올 수 있습니다.
당신은 사용자의 발화를 기반으로 메뉴 추천 API를 호출하여 API 결과를 기반으로 사용자에게 최상의 추천 결과를 제공해야 합니다.
"""

MESSAGES = [
    {
        'role': 'system',
        'content': SYSTEM_PROMPT
    }
]

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "recommend",
            "description": "사용자 발화 기반으로 메뉴 추천 API를 호출합니다. 오로지 이 함수 결과로만 메뉴 추천되어야 합니다. 현재 해장 또는 다이어트 2개 카테고리에 대한 메뉴 추천만 가능하며, 사용자 발화가 없는 경우 빈 리스트가 반환 될 수 있습니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_text": {
                        "type": "string",
                        "description": "사용자 발화 텍스트 원문",
                    },
                },
                "required": ["query_text"],
                "additionalProperties": False,
            },
        }
    }
]

def recommend(query_text):
    url = "http://localhost:8000/recommend"
    response = requests.post(url, json={"query_text": query_text})
    return response.json()

def call_openai(prompt, temperature=0.0, model='gpt-4o-2024-08-06'):
    client = OpenAI(api_key=OPENAI_API_KEY)

    MESSAGES.append(
        {
            'role': 'user',
            'content': prompt
        }
    )

    completion = client.chat.completions.create(
        model=model,
        messages=MESSAGES,
        tools=TOOLS,
        tool_choice="auto"
    )

    if hasattr(completion.choices[0].message, "tool_calls") and completion.choices[0].message.tool_calls:
        tool_calls = completion.choices[0].message.tool_calls  # 🔥 수정된 부분
        tool_name = tool_calls[0].function.name
        tool_args = tool_calls[0].function.arguments
        tool_id = tool_calls[0].id
        MESSAGES.append(
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": tool_id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": tool_args
                        }
                    }
                ]
            }
        )

        tool_result = recommend(**json.loads(tool_args))
        MESSAGES.append(
            {
                "role": "tool",
                "content": json.dumps(tool_result, ensure_ascii=False),
                "tool_call_id": tool_id
            }
        )

        completion = client.chat.completions.create(
            model=model,
            messages=MESSAGES,
            tools=TOOLS
        )

    MESSAGES.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content
        }
    )

    return completion.choices[0].message.content

def fn(message, history):
    output = call_openai(message)
    return output

def run_demo():
    demo = gr.ChatInterface(
        title='메뉴뚝딱 AI ♾',
        fn=fn,
        examples=["숙취에 좋은 메뉴 좀 추천해줄레...?"]
    )
    demo.launch(share=True)

if __name__ == '__main__':
    run_demo()