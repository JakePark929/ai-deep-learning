import os
import json

from dotenv import load_dotenv
from openai import Client

from prompt_template import prompt_template, prompt_template_json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = Client(api_key=OPENAI_API_KEY)

def inference(review):
#     prompt = """다음은 영화에 대한 리뷰입니다. 영화에 대해 긍정적이면 1, 부정적이면 0으로 평가해주세요.
# ```review
# 보는 내내 시간 가는 중 모르고 정말 재밌게 봤습니다~
# ```"""

#     prompt = """다음은 영화에 대한 리뷰입니다. 영화에 대해 긍정적이면 1, 부정적이면 0으로 평가해주세요.
# ```review
# 진짜 최악의 영화
# ```"""

    prompt = prompt_template.format(review=review)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0 # 0 ~ 2.0
    )

    output = response.choices[0].message.content

    return output

def inference_json(review):
    prompt = prompt_template_json.format(review=review)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0, # 0 ~ 2.0
        response_format={"type": "json_object"}
    )

    cost = calculate_cost(response.usage.prompt_tokens, response.usage.completion_tokens)

    output = response.choices[0].message.content
    output_json = json.loads(output)

    return output_json, cost

def calculate_cost(prompt_tokens, completion_tokens):

    return (prompt_tokens / 1000000 * 0.5 + completion_tokens / 1000000 * 1.5) * 1400

if __name__ == '__main__':
    # print(inference("진짜 쓰레기 영화"))
    output, cost = inference_json("진짜 돈 아까움..")
    print(output)
    print(f"비용: {cost:.3f} 원")
    