import os

from dotenv import load_dotenv
from openai import Client

from prompt_template import prompt_template

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

if __name__ == '__main__':
    print(inference("재미없게 봤습니다~"))