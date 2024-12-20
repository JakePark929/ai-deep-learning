import os

from dotenv import load_dotenv
from openai import Client

from prompt_template import prompt_template

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = Client(api_key=OPENAI_API_KEY)

def inference_all(reviews):
    reviews = "\n".join([f"review_no: {review['id']}\tcontent: {review['document']}" for review in reviews])
    prompt = prompt_template.format(reviews=reviews)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system", "content": "You are a helpful assistant."},
            {"role":"user", "content": prompt}
        ],
        temperature=0,
    )
    output = response.choices[0].message.content

    return output
    
if __name__ == "__main__":
    print(inference_all([
        {"id": 1, "document": "뭐야 이 평점들은.... 나쁘진 않지만 10점 짜리는 더더욱 아니잖아"},
        {"id": 2, "document": "지루하지는 않은데 완전 막장임"},
        {"id": 3, "document": "3D만 아니었어도 별 다섯개 줬을텐데.."},
        {"id": 4, "document": "진짜 최악"},
        {"id": 5, "document": "너무 재밌어요."},
    ]))