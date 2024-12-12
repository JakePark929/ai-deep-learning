import time

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# 모델 ID 설정
model_id = "meta-llama/Llama-3.2-3B"

# 토크나이저 및 모델 로드
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,  # 메모리 절약을 위한 float16 사용
    device_map="auto"          # 자동으로 GPU/CPU 매핑
)

# 모델 평가 모드 전환
model.eval()

# Hugging Face pipeline 생성
text_gen_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer
)

# 프롬프트 입력
prompt = (
    "아래 질문을 기반으로 검색된 질문에 첨부된 뉴스를 참고하여 질문에 대한 답변을 생성하시오.\n"
    "질문: 삼성전자가 인수하려고 하는 사업분야는?\n"
    "문서: 삼성전자가 HVAC(냉난방공조) 사업 인수를 타진 중이며, 이는 기존 가전 사업의 약점 보완을 목적으로 한다.\n"
    "답변: "  # 힌트
)

print(f"프롬프트: {prompt}")

# 생성 시간 측정 시작
start_time = time.time()

# 텍스트 생성 실행
outputs = text_gen_pipeline(
    prompt,
    max_new_tokens=100,  # 생성할 최대 토큰 수
    do_sample=True,      # 샘플링 활성화
    temperature=0.3,     # 출력 다양성 조절
    top_p=0.9            # Top-p 샘플링
)

# 생성 시간 측정 끝
end_time = time.time()

# 결과 출력
generated_text = outputs[0]['generated_text']
answer = generated_text[len(prompt):]

print("=====")
print("AI 답변:")
print(answer)
print(f"생성 시간: {end_time - start_time:.3f}초")