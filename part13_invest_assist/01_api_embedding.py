import os

from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SimilarityFunction

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
similarity_fn = SimilarityFunction.to_similarity_fn("cosine")

def get_embedding(text, model="text-embedding-3-small"):
    text = text.strip()

    return client.embeddings.create(input=[text], model=model).data[0].embedding

embedding_1 = get_embedding("일찍 학교에 갔다.")
embedding_2 = get_embedding("날씨가 화창하다.")
embedding_3 = get_embedding("일찍 초등학교로 등교했다.")

score_1_2 = similarity_fn(embedding_1, embedding_2)
score_1_3 = similarity_fn(embedding_1, embedding_3)
score_2_3 = similarity_fn(embedding_2, embedding_3)

print(score_1_2)
print(score_1_3)
print(score_2_3)


