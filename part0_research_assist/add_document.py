import os

from dotenv import load_dotenv
from service.faiss_manager import FAISSIndexManager
# from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from langchain_openai import OpenAIEmbeddings

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_PATH = os.getenv("INDEX_PATH")
index_path = INDEX_PATH

# 임베딩 모델 초기화
embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
# embedding = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v1")

# FAISS 인덱스 매니저 초기화
manager = FAISSIndexManager(index_path, embedding)

def add_documents(pdf_files):
    """
    문서를 FAISS 인덱스에 추가하는 함수
    :param pdf_files: PDF 파일 경로 리스트
    """
    manager.add_documents(pdf_files)
    print("Documents added and FAISS index updated.")

# 새로 추가할 문서 리스트 예시
if __name__ == "__main__":
    pdf_files = ["./src/bok_sample.pdf"]
    add_documents(pdf_files)