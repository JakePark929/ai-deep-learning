import os

from dotenv import load_dotenv
from openai import Client

from prompt_template import prompt_template

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

if __name__ == '__main__':
    print(inference("진짜 쓰레기 영화"))
    