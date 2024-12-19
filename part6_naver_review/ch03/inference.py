import os

from dotenv import load_dotenv
from openai import Client

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = Client(api_key=OPENAI_API_KEY)

def inference():
    prompt = """다음은 영화에 대한 리뷰입니다. 리뷰에서 긍정적인 키워드, 부정적인 키워드를 추출해주세요.

``` review
보는 내내 시간 가는줄 모르고 정말 재밌게 봤습니다.
```"""
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

if __name__ == '__main__':
    print(inference())