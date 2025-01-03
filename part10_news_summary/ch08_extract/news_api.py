import concurrent.futures
import pandas as pd
import time
from gdeltdoc import GdeltDoc, Filters
from newspaper import Article
from datetime import datetime, timedelta
import threading

# GDELT 객체 초기화
gd = GdeltDoc()

# URL을 받아오는 함수
def get_urls(keyword: str, start_date: str, end_date: str):
    f = Filters(
        start_date=start_date,
        end_date=end_date,
        num_records=100,
        keyword=keyword,
        domain='nytimes.com',
        country='US'
    )

    # GDELT에서 기사 검색
    articles = gd.article_search(f)

    return articles

# 기사 파싱 및 중복 처리 함수
def parse_article(row, seen_urls, lock):
    url = row['url']
    
    # 이미 처리한 URL은 건너뜀 (동기화된 접근)
    with lock:
        if url in seen_urls:
            return None
        seen_urls.add(url)

    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            'title': row['title'],
            'date': row['seendate'],
            'text': article.text,
            'url': url
        }

    except Exception as e:
        print(f"Error processing article at {url}: {e}")
        return None

# 텍스트 파싱 함수 (순차 처리)
def parse_text_sequential(article_df: pd.DataFrame, lock):
    seen_urls = set()  # 중복 방지 set
    result = []

    for _, row in article_df.iterrows():
        parsed_article = parse_article(row, seen_urls, lock)
        if parsed_article:
            result.append(parsed_article)

    return result

# 텍스트 파싱 함수 (병렬 처리 포함)
def parse_text_parallel(article_df: pd.DataFrame, max_workers=10, lock=None):
    seen_urls = set()  # 중복 방지 set
    result = []

    # 내부 병렬 처리 (멀티스레딩)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(parse_article, row, seen_urls, lock) for _, row in article_df.iterrows()]

        # 완료된 작업의 결과를 받아옴
        for future in concurrent.futures.as_completed(futures):
            parsed_article = future.result()
            if parsed_article:
                result.append(parsed_article)

    return result

# 순차 처리용 메인 실행부
def main_sequential(keywords, start_date=None, end_date=None):
    total_list_sequential = []  # 전체 기사 리스트 (순차 처리)

    # 시작 날짜 처리
    if not start_date:
        start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')  # 기본값: 오늘부터 한 달 전

    # 종료 날짜 처리
    if not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d')  # 기본값: 오늘 날짜
    
    print(f"Fetching articles from {start_date} to {end_date}")

    # 락 객체 생성 (URL 중복 방지를 위한 동기화)
    lock = threading.Lock()

    # 전체 순차 처리 시간 측정
    start_time = time.time()

    for keyword in keywords:
        df = get_urls(keyword, start_date, end_date)

        # 순차 처리
        print(f"키워드 '{keyword}'에 대해 {len(df)}개의 기사를 가져왔습니다.")
        result_list_sequential = parse_text_sequential(df, lock)  # 순차 처리
        total_list_sequential.extend(result_list_sequential)  # 결과 리스트에 추가

    sequential_time = time.time() - start_time
    print(f"\n전체 순차 처리 시간: {sequential_time:.2f}초")

    # 결과 출력
    print(f"\n총 {len(total_list_sequential)}개의 기사를 순차 처리 완료.")

# 병렬 처리용 메인 실행부
def main_parallel(keywords, start_date=None, end_date=None):
    total_list_parallel = []  # 전체 기사 리스트 (병렬 처리)

    # 시작 날짜 처리
    if not start_date:
        start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')  # 기본값: 오늘부터 한 달 전

    # 종료 날짜 처리
    if not end_date:
        end_date = datetime.today().strftime('%Y-%m-%d')  # 기본값: 오늘 날짜
    
    print(f"Fetching articles from {start_date} to {end_date}")

    # 락 객체 생성 (URL 중복 방지를 위한 동기화)
    lock = threading.Lock()

    # 전체 병렬 처리 시간 측정
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_urls, keyword, start_date, end_date) for keyword in keywords]

        for future in concurrent.futures.as_completed(futures):
            df = future.result()

            # 병렬 처리
            print(f"키워드 '{keywords[futures.index(future)]}'에 대해 {len(df)}개의 기사를 가져왔습니다.")
            result_list_parallel = parse_text_parallel(df, max_workers=10, lock=lock)  # 병렬 처리
            total_list_parallel.extend(result_list_parallel)  # 병렬 처리 결과 리스트에 추가

    parallel_time = time.time() - start_time
    print(f"\n전체 병렬 처리 시간: {parallel_time:.2f}초")

    # 결과 출력
    print(f"\n총 {len(total_list_parallel)}개의 기사를 병렬 처리 완료.")

if __name__ == "__main__":
    keywords = ["inflation", "economy", "recession"]  # 여러 키워드를 동시에 처리
    start_date, end_date = "2024-01-01", "2024-12-24"

    # 순차 처리 메인 함수 실행
    print("==== 순차 처리 시작 ====")
    main_sequential(keywords=keywords, start_date=start_date, end_date=end_date)

    # 병렬 처리 메인 함수 실행
    print("==== 병렬 처리 시작 ====")
    main_parallel(keywords=keywords, start_date=start_date, end_date=end_date)