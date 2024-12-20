from pydoc import doc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_data():
    url = "https://fastcampus.co.kr/data_online_llmservice"

    # 크롬 옵션 설정 (헤드리스 모드)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # GUI 없이 실행
    chrome_options.add_argument("--disable-gpu")

    # 드라이버 자동 관리
    service = Service(ChromeDriverManager().install())

    # 크롬 웹드라이버 생성
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    # 페이지 내용 가져오기
    content = driver.find_element("tag name", "body").text
    driver.quit()  # 작업 후 드라이버 종료

    return content

if __name__ == "__main__":
    print(get_data())
