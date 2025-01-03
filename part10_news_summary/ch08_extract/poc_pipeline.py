import os
import json
from datetime import datetime

from dotenv import load_dotenv
from openai import Client

from prompt_template import json_schema, prompt_template
from mongodb_manager import save_one

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = Client(api_key=OPENAI_API_KEY)

model = "gpt-3.5-turbo-0125"

def chatgpt_generate(query):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = openai_client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content

    return answer

def prompting(news: str):
    prompt = prompt_template.format(json_schema=json_schema, news=news.strip())

    return prompt

news = """삼성 전자는 최근 가전 사업 수익성이 크게 악화돼 반도체와 스마트폰 사업과 비교해 존재감이 낮아지고 있다. 냉난방공조는 성장성과 수익성 측면에서 기존 가전 사업의 약점을 보완해줄 수 있어 적극 인수를 고려하는 것으로 풀이된다.

31일 로이터와 블룸버그 등 해외언론 보도를 종합하면, 삼성 전자가 존슨 콘트롤즈가 최근 매물로 내놓은 HVAC(냉난방공조) 사업 인수를 타진 중인것으로 나타났다.
"""

def pipeline():
    query = prompting(news)
    answer = chatgpt_generate(query)

    try:
        answer_json = json.loads(answer)
        current_date = datetime.now().strftime('%Y-%m-%d')
        answer_json['company'] = "삼성전자"
        answer_json['date'] = current_date
        
    except json.JSONDecodeError as e:
        print("[JSON 파싱 오류] 원본 응답:", answer)

    if answer_json is not None:
        insert_id = save_one(json=answer_json)
        print(f"db에 저장되었습니다 - {insert_id}")
    else:
        print("유효한 JSON 응답이 아니므로 DB에 저장되지 않았습니다.")
        print("[JSON 오류] 원본:", json.dumps(answer_json, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    pipeline()