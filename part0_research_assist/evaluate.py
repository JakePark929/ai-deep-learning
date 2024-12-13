import os
import sys
import json
import time
from datetime import datetime
from service.research_service import ResearchService

from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
from konlpy.tag import Okt

# KoNLPy의 Okt를 사용하여 토큰화
okt = Okt()

# BLEU와 ROUGE 점수 계산 함수
def calculate_bleu(reference, candidate):

    return sentence_bleu([reference], candidate)

def calculate_rouge(reference, candidate):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    return scorer.score(reference, candidate)

# 평가 함수
def evaluate(input_data, gold_data, research_service: ResearchService, model_name: str="openai"):
    # 시간 측정 시작
    start_time = time.time()
    print(f"===== {model_name} 답변 생성을 시작합니다. {formatted_time(start_time)} =====")

    # 연구 서비스로 답변 생성
    response = research_service.prompt_and_generate(input_data.strip(), model_name)

    # 시간 측정 종료
    end_time = time.time()
    print(f"===== {model_name} 답변 생성을 종료합니다. {formatted_time(end_time)} =====")
    elapsed_time = end_time - start_time

    # KoNLPy Okt로 토큰화
    reference = okt.morphs(gold_data)  # 참조 문장
    candidate = okt.morphs(response)  # 생성된 응답을 후보 문장으로 사용

    # BLEU 점수 계산
    bleu_score = calculate_bleu(reference, candidate)
    
    # ROUGE 점수 계산
    rouge_scores = calculate_rouge(gold_data, response)

    # 출력 결과
    print(f"\nResponse: {response}\n")
    print("=== evaluation ===")
    print(f"BLEU score: {bleu_score}")
    print(f"ROUGE scores: {rouge_scores}")
    print(f"Response Time(sec): {elapsed_time:.2f}")
    print("==================\n")

    return {
        "input_data": input_data,
        "gold_data": gold_data,
        "response": response,
        "bleu_score": bleu_score,
        "rouge_scores": {
            metric: {
                "precision": score.precision,
                "recall": score.recall,
                "fmeasure": score.fmeasure
            } 
            for metric, score in rouge_scores.items()
        },
        "response_time_sec": round(elapsed_time, 2)
    }

def generate_report(input_datas, gold_datas, model_name: str="openai", num_evaluations=1):
    # ResearchService 인스턴스 초기화
    research_service = ResearchService(model_list=[model_name])

    evaluation_results = []

    for i in range(num_evaluations):
        print(f"\n##### {model_name.upper()} TEST {i + 1} #####")
        for j in range(len(input_datas)):
            result = evaluate(input_data=input_datas[j], gold_data=gold_datas[j], research_service=research_service, model_name=model_name)
            evaluation_results.append(result)

    # 평균 계산
    avg_bleu_score = sum(result["bleu_score"] for result in evaluation_results) / len(evaluation_results)
    avg_rouge_score = {
        "rouge1": sum(result["rouge_scores"]['rouge1']['fmeasure'] for result in evaluation_results) / len(evaluation_results),
        "rouge2": sum(result["rouge_scores"]['rouge2']['fmeasure'] for result in evaluation_results) / len(evaluation_results),
        "rougeL": sum(result["rouge_scores"]['rougeL']['fmeasure'] for result in evaluation_results) / len(evaluation_results)
    }
    avg_response_time = sum(result["response_time_sec"] for result in evaluation_results) / len(evaluation_results)

    # 보고서 작성
    title = f"{model_name}_report"
    current_date = datetime.now().strftime("%Y-%m-%d")
    report = {
        "title": title,
        "num_evaluations": num_evaluations,
        "date": current_date,
        "evaluation_results": evaluation_results,
        "average_scores": {
            "bleu_score": avg_bleu_score,
            "rouge_scores": avg_rouge_score,
            "response_time_sec": avg_response_time
        }
    }

    # './report/' 디렉토리 존재 여부 확인
    os.makedirs('./report', exist_ok=True)

    # json 파일 생성
    filepath = f"./report/{title}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    print(f"평가 결과가 '{title}' 파일로 저장되었습니다.")

def formatted_time(timestamp: float) -> str:

    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def validate_num(args):
    if len(args) > 1:
        try:
            num = int(args[1])
            if 0 < num and num < 10:
                return num
            else:
                print("The number of evaluations must be a positive integer less than or equal to 10.")
                sys.exit(1)
        except ValueError:
            print("Please provide a valid integer for the number of evaluations.")
            sys.exit(1)

    return 1

if __name__ == '__main__':
    num_evaluations = validate_num(sys.argv)

    input_datas = [
        "혁신활동지표인 우리나라 기업의 R&D 지출규모는 OECD 회원국 중 몇 위인가?",
        # "2022년 현재 우리나라 국내 총 생산대비 R&D 지출 규모는?"
    ]
    gold_datas = [
        "2022년 우리나라의 R&D 지출규모는 OECD 회원국 중, 이스라엘 (6.0%)에 이어 2위에 해당한다. 출처, 페이지",
        # "2022년 현재 우리나라 국내 총 생산대비 R&D 지출 규모는 전체 R&D 지출의 79%를 차지한다. 출처, 페이지"
    ]

    generate_report(input_datas=input_datas, gold_datas=gold_datas, model_name="openai", num_evaluations=num_evaluations)
    # generate_report(input_datas=input_datas, gold_datas=gold_datas, model_name="llama", num_evaluations=num_evaluations)
    # generate_report(input_datas=input_datas, gold_datas=gold_datas, model_name="42dot", num_evaluations=num_evaluations)
    