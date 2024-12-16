import time
from datetime import datetime

import transformers
import torch

def formatted_time(timestamp: float) -> str:

    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

model_id = "42dot/42dot_LLM-SFT-1.3B"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.float16}
)

pipeline.model.eval()

prompt = "아래 질문을 기반으로 검색된 질문에 첨부된 뉴스를 참고하여 질문에 대한 답변을 생성하시오.\n"
prompt += "질문: 삼성전자가 인수하려고 하는 사업분야는?\n"
prompt += "문서: 삼성전자가 HVAC(냉난방공조) 사업 인수를 타진 중이며, 이는 기존 가전 사업의 약점 보완을 목적으로 한다.\n"
prompt += "답변: " # hint

print(f"프롬프트: {prompt}")

# 생성 시간 측정 시작
start_time = time.time()
print(f"===== 답변 생성을 시작합니다. {formatted_time(start_time)} =====")

outputs = pipeline(
    prompt,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.3,
    top_p=0.9
)

# 생성 시간 측정 끝
end_time = time.time()
print(f"===== 답변 생성을 시작합니다. {formatted_time(end_time)} =====")

print("=====")
print("AI 답변:")
print(outputs[0]['generated_text'][len(prompt):])
print(f"생성 시간: {end_time - start_time:.3f}초")