import os

from openai import OpenAI
from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from langchain_openai import OpenAIEmbeddings

import streamlit as st

from faiss_manager import FAISSIndexManager

### DB 경로 설정 ###
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_PATH = os.getenv("INDEX_PATH")
index_path = INDEX_PATH

### 임베딩 모델 초기화 ###
embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
# embedding = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v1")

### FAISS 인덱스 매니저 초기화 ###
faiss_manager = FAISSIndexManager(index_path, embedding)

### 모델 선언 ###
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
model="gpt-3.5-turbo-0125"

### OpenAI API 생성 ###
def chatgpt_generate(query):
    message = [
        {
            "role": "system",
            "content": """당신은 연구원입니다. 연구에 관한 질문이 주어졌을 때, 질문에 첨부된 문서를 기반으로 답변하는 것이 목표입니다.
            답변 결과는 다음 조건들을 충족해야 합니다:
            1. 모든 문장은 항상 존댓말로 끝나야 합니다.
            """
        },
        {
            "role": "user",
            "content": query
        },
    ]
    response = client.chat.completions.create(model=model, messages=message)
    answer = response.choices[0].message.content

    return answer

### 프롬프트 생성 ###
def prompt_and_generate(query):
    docs = [doc for doc in faiss_manager.search(query)]
    prompt = f"""아래 질문을 기반으로 검색된 질문에 첨부된 문서 내용을 참고하여 질문에 대한 답변을 생성하시오. 문서에 있는 출처도 명시합니다.
        질문: {query}\n"""

    for i in range(len(docs)):
        prompt += f"문서{i + 1}\n"
        prompt += f"내용: {docs[i].page_content}\n"  # page_content로 문서 내용 접근
        prompt += f"출처: {docs[i].metadata['source']}, 페이지: {docs[i].metadata['page']}\n"  # metadata에서 출처와 페이지 정보 접근
        prompt += "\n"  # 문서 간 구분을 위한 줄바꿈

    prompt += "답변: "
    # print(f"prompt: {prompt}\n")
    answer = chatgpt_generate(prompt)

    return answer

### Client 구현 ###
st.title("🧑‍🔬Wisebot: AI Research Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("궁금한 점을 물어보세요."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"bot: {prompt_and_generate(prompt.strip())}"

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})