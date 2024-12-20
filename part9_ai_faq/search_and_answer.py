import os

from dotenv import load_dotenv
from openai import Client
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from prompt_template import prompt_template

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_PATH = os.getenv("INDEX_PATH")
client = Client(api_key=OPENAI_API_KEY)
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

def generate_answer(context, question):
    context_join = f"""Q: {context['question']}
A: {context['answer']}"""
    prompt = prompt_template.format(context=context_join, question=question)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )

    output = response.choices[0].message.content

    return output

if __name__ == "__main__":
    question = "페이백은 어디서 받나요?"
    qa = search(question)
    print(qa['question'])
    print(qa['answer'])
    print("=====")
    print(question)
    print(generate_answer(qa, question))