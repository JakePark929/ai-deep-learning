import os
from service.faiss_manager import FAISSIndexManager

import torch
from transformers import pipeline
from openai import OpenAI
from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from langchain_openai import OpenAIEmbeddings

class ResearchService:
    def __init__(self):
        """
        ResearchAssistantService를 초기화하는 생성자입니다.
        환경 변수와 FAISS, OpenAI 클라이언트를 설정합니다.
        """
        # 환경 변수 로드 (이미 로드되지 않은 경우)
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        INDEX_PATH = os.getenv("INDEX_PATH")

        # FAISS 매니저 초기화
        self.embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        self.faiss_manager = FAISSIndexManager(INDEX_PATH, self.embedding)

        # OpenAI 모델 초기화
        self.model = "gpt-3.5-turbo-0125"
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        # 42dot 모델 파이프라인 초기화
        self.kslm_id = "42dot/42dot_LLM-SFT-1.3B"
        self.pipeline = pipeline(
            "text-generation",
            model=self.kslm_id,
            model_kwargs={"torch_dtype": torch.float16}
        )
        self.pipeline.model.eval()

    def chatgpt_generate(self, query: str) -> str:
        """
        Communicates with OpenAI API to generate a response based on the provided query.
        """
        message = [
            {
                "role": "system",
                "content": """당신은 연구원입니다. 연구에 관한 질문이 주어졌을 때, 질문에 첨부된 문서를 기반으로 답변하는 것이 목표입니다.
                답변 결과는 다음 조건들을 충족해야 합니다:
                1. 모든 문장은 항상 존댓말로 끝나야 합니다.
                2. 첨부된 문서에 답변할 내용이 없으면 답변을 할 수 없다고 합니다.
                3. 첨부된 문서에 해당 내용이 있으면 해당 출처를 반환합니다. 
                """
            },
            {
                "role": "user",
                "content": query
            },
        ]
        response = self.client.chat.completions.create(model=self.model, messages=message)

        return response.choices[0].message.content
    
    def kslm_generate(self, query: str) -> str:
        """
        SLLM 모델을 사용하여 응답을 생성하는 함수입니다.
        """
        answer = self.pipeline(
            query,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.5,
            top_p=0.9
        )

        return answer[0]['generated_text'][len(query):]

    def prompt_and_generate(self, query: str, model_name: str = "openai") -> str:
        """
        Generates a prompt from FAISS search results and queries OpenAI to generate a response.
        """
        # Perform a search using FAISS
        docs = [doc for doc in self.faiss_manager.search(query)]
        
        # Build the prompt from the search results
        prompt = f"""아래 질문을 기반으로 검색된 질문에 첨부된 문서 내용을 참고하여 질문에 대한 답변을 생성하시오.
        질문: {query}\n"""

        for i, doc in enumerate(docs):
            prompt += f"문서{i + 1}\n"
            prompt += f"내용: {doc.page_content}\n"  # page_content로 문서 내용 접근
            prompt += f"출처: {doc.metadata['source']}, 페이지: {doc.metadata['page']}\n"  # metadata에서 출처와 페이지 정보 접근
            prompt += "\n"  # 문서 간 구분을 위한 줄바꿈

        prompt += "답변: "
        
        # model_name에 따라 다르게 실행 (기본값: "openai")
        if model_name.lower() == "openai":
            return self.chatgpt_generate(prompt)
        elif model_name.lower() == "42dot":
            return self.kslm_generate(prompt)
        else:
            raise ValueError(f"지원하지 않는 모델 이름: {model_name}")