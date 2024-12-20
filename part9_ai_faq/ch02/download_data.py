import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_urls():
    # 크롬 옵션 설정 (헤드리스 모드)
    options = Options()
    options.add_argument("--headless")  # GUI 없이 실행
    options.add_argument("--disable-gpu")
    
    # WebDriver Manager를 사용해 ChromeDriver 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = "https://fastcampus.co.kr/data_online_llmservice"
        driver.get(url)
        time.sleep(5)  # 페이지 로딩 및 JavaScript 실행 대기

        # 페이지 소스 가져오기
        soup = BeautifulSoup(driver.page_source, "html.parser")
        img_list = soup.find_all("img")

        # 이미지 URL 추출
        url_list = [tag.get('src') for tag in img_list if tag.get('src')]

        return url_list
    finally:
        driver.quit()  # 웹드라이버 종료

if __name__ == "__main__":
    urls = get_urls()
    print(urls)