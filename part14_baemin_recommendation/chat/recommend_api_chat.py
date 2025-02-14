import logging
import os
import sys
sys.path.insert(0, "..")
from dotenv import load_dotenv
from collections.abc import MutableMapping
from pydantic import BaseModel
from typing import Union

from fastapi import FastAPI
from pymongo import MongoClient

from utils import extract_keywords
from utils import get_embedding, get_most_relevant_indices


load_dotenv()
MONGO_INITDB_HOST = os.getenv('MONGO_INITDB_HOST')
MONGO_INITDB_PORT = int(os.getenv('MONGO_INITDB_PORT'))
MONGO_INITDB_ROOT_USERNAME  = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD  = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

# 몽고DB 연결
client = MongoClient(
    host=MONGO_INITDB_HOST, 
    port=MONGO_INITDB_PORT,
    username=MONGO_INITDB_ROOT_USERNAME,
    password=MONGO_INITDB_ROOT_PASSWORD,
    authSource='admin'
)

db = client['menu_db']
collection = db['menu_info']

menu_db = list(collection.find({}))

app = FastAPI()

class QueryModel(BaseModel):
    query_text: str


@app.get("/health")
def health():
    return "OK"


@app.post("/recommend")
def recommend(query: QueryModel):
    query = extract_keywords(query.query_text)
    if query == []:
        return []

    query_embedding = get_embedding(query, model='text-embedding-3-large')
    context_embeddings = [menu["embeddings"] for menu in menu_db]
    indices, scores = get_most_relevant_indices(query_embedding, context_embeddings)

    result = []
    top_k = min(10, len(indices)) # 상위 10개 메뉴 추천
    for i in range(top_k):
        result.append({
            "_id": menu_db[indices[i]]["_id"],
            "score": scores[indices[i]],
            "menu": menu_db[indices[i]]["menu"],
            "restaurant": menu_db[indices[i]]["restaurant"],
            "url": menu_db[indices[i]]["url"]
        })
    return result