from typing import List

from fastapi import FastAPI, Body
from pydantic import BaseModel

from ch02.inference import inference_json
from ch03.inference import inference_function_calling
from ch04.inference import inference_langchain
from ch05.inference import inference_all_langchain

app = FastAPI()

class RequestBody(BaseModel):
    review: str

@app.post("/evaluate")
async def evaluate_review(body: RequestBody = Body()):

    return inference_json(body.review)

@app.post("/extract")
async def extract_review(body: RequestBody = Body()):

    return inference_function_calling(body.review)

class RequestBodyList(BaseModel):
    reviews: List[str]

@app.post("/summary")
async def summary_reviews(body: RequestBodyList = Body()):

    return inference_langchain(body.reviews)

class Review(BaseModel):
    id: int
    document: str

class RequestBodyAll(BaseModel):
    reviews: List[Review]

@app.post("/analyze")
async def analyze_reviews(body: RequestBodyAll = Body()):
    reviews = [review.model_dump() for review in body.reviews]

    return inference_all_langchain(reviews)