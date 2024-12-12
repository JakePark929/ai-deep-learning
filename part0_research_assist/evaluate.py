import time
from service.research_service import ResearchService

from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
from konlpy.tag import Okt

# KoNLPy의 Okt를 사용하여 토큰화
okt = Okt()

# ResearchService 인스턴스 초기화
research_service = ResearchService()

# BLEU와 ROUGE 점수 계산 함수
def calculate_bleu(reference, candidate):

    return sentence_bleu([reference], candidate)

def calculate_rouge(reference, candidate):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    return scorer.score(reference, candidate)

# 평가 함수
def evaluate(input_data, gold_data):
    # 시간 측정 시작
    start_time = time.time()

    # 연구 서비스로 답변 생성
    response = research_service.prompt_and_generate(input_data.strip())

    # 시간 측정 종료
    end_time = time.time()
    elapsed_time = end_time - start_time

    # KoNLPy Okt로 토큰화
    reference = okt.morphs(gold_data)  # 참조 문장
    candidate = okt.morphs(response)  # 생성된 응답을 후보 문장으로 사용

    # BLEU 점수 계산
    bleu_score = calculate_bleu(reference, candidate)
    
    # ROUGE 점수 계산
    rouge_scores = calculate_rouge(gold_data, response)

    # 출력 결과
    print(f"Response: {response}\n")
    print("=== evaluation ===")
    print(f"BLEU score: {bleu_score}")
    print(f"ROUGE scores: {rouge_scores}")
    print(f"Response Time(sec): {elapsed_time:.2f}")
    print("==================")

if __name__ == '__main__':
    input_data = "혁신활동지표인 우리나라 기업의 R&D 지출규모는 OECD 회원국중 몇 위인가?"
    gold_data = "2022년 우리나라의 R&D 지출규모는 OECD 회원국 중에서 이스라엘(6.0%)에 이어 2위에 해당한다. 출처 페이지"

    evaluate(input_data=input_data, gold_data=gold_data)