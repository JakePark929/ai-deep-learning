import os
import time
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

def formatted_time(timestamp: float) -> str:

    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 모델 ID 설정 및 모델 로드드
model_id = "gpt-3.5-turbo-0125"
client = OpenAI(api_key=OPENAI_API_KEY)

prompt = "아래 질문을 기반으로 검색된 질문에 첨부된 뉴스를 참고하여 질문에 대한 답변을 생성하시오.\n"
prompt += "질문: 삼성전자가 인수하려고 하는 사업분야는?\n"
prompt += "문서: 삼성전자가 HVAC(냉난방공조) 사업 인수를 타진 중이며, 이는 기존 가전 사업의 약점 보완을 목적으로 한다.\n"
prompt += "답변: "

print(f"프롬프트: {prompt}")

message = [
    {
        "role": "system",
        "content": ""
    },
    {
        "role": "user",
        "content": prompt
    },
]

# 생성 시간 측정 시작
start_time = time.time()
print(f"===== 답변 생성을 시작합니다. {formatted_time(start_time)} =====")

response = client.chat.completions.create(model=model_id, messages=message)

# 생성 시간 측정 끝
end_time = time.time()
print(f"===== 답변 생성을 종료합니다. {formatted_time(end_time)} =====")

# 결과 출력
answer = response.choices[0].message.content

print("=====")
print("AI 답변:")
print(answer)
print(f"생성 시간: {end_time - start_time:.3f}초")