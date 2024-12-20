import os

from dotenv import load_dotenv
from openai import Client

from download_data import get_urls

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

if __name__ == "__main__":
    url_list = get_urls()
    print(inference_many(url_list))