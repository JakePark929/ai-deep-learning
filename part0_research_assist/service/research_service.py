import os
from service.faiss_manager import FAISSIndexManager

from openai import OpenAI
from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from langchain_openai import OpenAIEmbeddings

class ResearchService:
    def __init__(self):
        """
        Initializes the ResearchAssistantService with necessary configurations.
        """
        # Load environment variables (if not already loaded)
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        INDEX_PATH = os.getenv("INDEX_PATH")

        # Initialize OpenAI and FAISS manager
        self.embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        self.faiss_manager = FAISSIndexManager(INDEX_PATH, self.embedding)
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo-0125"

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
                """
            },
            {
                "role": "user",
                "content": query
            },
        ]
        response = self.client.chat.completions.create(model=self.model, messages=message)
        return response.choices[0].message.content

    def prompt_and_generate(self, query: str) -> str:
        """
        Generates a prompt from FAISS search results and queries OpenAI to generate a response.
        """
        # Perform a search using FAISS
        docs = [doc for doc in self.faiss_manager.search(query)]
        
        # Build the prompt from the search results
        prompt = f"""아래 질문을 기반으로 검색된 질문에 첨부된 문서 내용을 참고하여 질문에 대한 답변을 생성하시오. 문서에 있는 출처도 명시합니다.
        질문: {query}\n"""

        for i, doc in enumerate(docs):
            prompt += f"문서{i + 1}\n"
            prompt += f"내용: {doc.page_content}\n"  # page_content로 문서 내용 접근
            prompt += f"출처: {doc.metadata['source']}, 페이지: {doc.metadata['page']}\n"  # metadata에서 출처와 페이지 정보 접근
            prompt += "\n"  # 문서 간 구분을 위한 줄바꿈

        prompt += "답변: "
        
        # Generate the response using OpenAI
        return self.chatgpt_generate(prompt)