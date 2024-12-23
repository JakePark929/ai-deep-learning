import os
import pickle

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from ch01.download_data import get_data
from ch01.inference import inference_json
from ch02.download_data import get_urls
from ch02.inference import inference_many_json

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_PATH = os.getenv("INDEX_PATH")

def main():
    product_detail = get_data()
    result_text = inference_json(product_detail)

    url_list = get_urls()
    result_images = inference_many_json(url_list)

    result = result_text["qa_list"] + result_images["qa_list"]
    print(result)

    # 디렉토리가 없으면 생성
    directory = INDEX_PATH
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f"{directory}/qas.pkl", "wb") as f:
        pickle.dump(result, f)

    result_questions = [row['question'] for row in result]

    # OpenAI API 임베딩 준비
    embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    # FAISS 객체 생성 (from_texts 사용)
    faiss_index = FAISS.from_texts(
        result_questions,  # 텍스트 데이터
        embedding,  # OpenAI 임베딩
        metadatas=result  # 메타데이터
    )

    # FAISS 인덱스를 파일로 저장
    faiss_index.save_local(f"{directory}/qas.index")

if __name__ == "__main__":
    main()