import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_PATH = os.getenv("INDEX_PATH")
directory = INDEX_PATH

def search(question):
    # OpenAI Embeddings 초기화
    embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    # FAISS 인덱스 로드
    db = FAISS.load_local(
        f"{directory}/qas.index", 
        embeddings=embedding, 
        allow_dangerous_deserialization=True
    )

    result = db.search(question, search_type="similarity")

    return result[0].metadata

if __name__ == "__main__":
    question = "페이백은 어디서 받나요?"
    qa = search(question)
    print(qa['question'])
    print(qa['answer'])