import os
import json
import datetime
from pprint import pprint

from dotenv import load_dotenv
from openai import Client
from pymongo import MongoClient
from gdeltdoc import GdeltDoc, Filters
from newspaper import Article

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
gpt_client = Client(api_key=OPENAI_API_KEY)
model = "gpt-3.5-turbo-0125"

gd = GdeltDoc()

MONGO_INITDB_HOST = os.getenv('MONGO_INITDB_HOST')
MONGO_INITDB_PORT = int(os.getenv('MONGO_INITDB_PORT'))
MONGO_INITDB_ROOT_USERNAME  = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD  = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

mongo_client = MongoClient(
    host=MONGO_INITDB_HOST, 
    port=MONGO_INITDB_PORT,
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD,
    authSource='admin'
)

db = mongo_client['project1']
collection = db['NewsAnalysis']

def get_url(keyword):
    f = Filters(
        start_date="2024-11-19",
        end_date="2024-12-23",
        num_records=10,
        keyword=keyword,
        domain="nytimes.com",
        country="US"
    )

    articles = gd.article_search(f)

    return articles

def url_crawling(df):
    urls = df["url"]
    titles = df["title"]
    texts = []

    for url in urls:
        article = Article(url)
        article.download()
        article.parse()
        texts.append(article.text)

    return texts, titles

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

    response = gpt_client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content

    return answer

def analysis():
    prompt = """아래 텍스트에서 S&P 500에 상장된 기업명을 모두 추출하고, 기업에 해당하는 감성을 분석하시오.
    반드시 출력포맷만을 생성하고, 그 이외의 단어나 설명은 생성하지 마시오.

    출력 포맷은 다음과 같습니다.
    [
        {
            "company": <기업명>,
            "sentiment": [
                {
                    "positive": <probability>
                },
                {
                    "negative": <probability>
                },
                {
                    "neutral": <probability>
                }
            ]
        },
        {
            "company": <기업명>,
            "sentiment": [
                {
                    "positive": <probability>
                },
                {
                    "negative": <probability>
                },
                {
                    "neutral": <probability>
                }
            ]
        }
    ]

    텍스트: """

    orgs = ["apple", "microsoft"]

    # 각 기업에 대해 처리
    for org in orgs:
        df = get_url(org)
        texts, titles = url_crawling(df)

        for idx, text in enumerate(texts):
            # 각 뉴스 텍스트에 대해 GPT 모델에 요청
            current_prompt = prompt + text  # 각 뉴스에 대해 prompt를 설정
            print(current_prompt)

            news_item = {}
            answer = chatgpt_generate(current_prompt)

            # JSON 형식으로 처리하기
            try:
                parsed_answer = json.loads(answer)
                news_item["title"]  = titles[idx]
                news_item["text"]  = text
                news_item["analysis"] = parsed_answer
                news_item["date"] = datetime.datetime.now()
                insert_id = collection.insert_one(news_item)
                print(insert_id)
            except json.JSONDecodeError as e:
                print("[JSON 파싱 오류] 원본 응답:", answer)
                continue

analysis()