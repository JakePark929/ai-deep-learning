import os

from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
model="gpt-3.5-turbo-0125"

doc_list = [
    "우리나라는 2022년에 코로나가 유행했다.",
    "우리나라의 2024년 GDP 전망은 3.0%이다.",
    "우리나라 2022년 국내총생산 중 연구개발 예산은 약 5%이다.",
    "삼성전자 2024년 1분기 매출액은 약 7조원으로 잠정 추정됩니다.",
    "2024년 7월 19일 삼성전자 주가는 64,500원 입니다."
]

bm25_retriever = BM25Retriever.from_texts(
    doc_list, metadatas=[{"source": i} for i in range(len(doc_list))]
)
bm25_retriever.k = 1

embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
faiss_vectorstore = FAISS.from_texts(
    doc_list, embedding, metadatas=[{"source": i} for i in range(len(doc_list))]
)
faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k":1})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever], weights=[0.2, 0.8]
)

def search(query):
    ensemble_docs = ensemble_retriever.invoke(query)

    return ensemble_docs

def chatgpt_generate(query):
    message = [
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": query
        },
    ]
    response = client.chat.completions.create(model=model, messages=message)
    answer = response.choices[0].message.content

    return answer

def prompt_and_generate(query, docs):
    prompt = f"""아래 질문을 기반으로 검색된 질문에 첨부된 문서를 참고하여 질문에 대한 답변을 생성하시오.
        질문: {query}"""

    for i in range(len(docs)):
        prompt += f"문서{i + 1}: " + docs[i]

    print(prompt)
    answer = chatgpt_generate(prompt)

    return answer

query = "삼성전자의 올해 매출액은?"
retrieved = [doc.page_content for doc in search(query)]
answer = prompt_and_generate(query, retrieved)
print(answer)