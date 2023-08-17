import re
import requests
from bs4 import BeautifulSoup

# 아래 뉴스 원문에서 이메일 주소만 출력하기


def get_news_content(url):
    response = requests.get(url)
    content = response.text

    soup = BeautifulSoup(content, 'html5lib')

    div = soup.find('div', attrs={'class': 'article_view'})

    content = ''
    for paragraph in div.find_all('p'):
        content += paragraph.get_text()

    return content


news1 = get_news_content('https://news.v.daum.net/v/20190617073049838')
print(news1)

mail = re.search(r'\b[\w-]+@[A-Za-z0-9.-]+\.[A-Za-z]+', news1)

print(mail.group(0))


# 다음 중 올바른 주소만 출력

webs = [
    'http://www.test.co.kr',
    'https://www.test1.com',
    'http://www.test.com',
    'ftp://www.test.com',
    'http:://www.test.com',
    'htp://www.test.com',
    'http://www.google.com',
    # 'http://ww.google.com',
    # 'http://.google.com',
    'https://www.homepage.com.',
]

# for web in webs:
# address = re.search(r'\bhttps?://[A-Za-z0-9.-]+\.[^\.][A-Za-z]+\b', web)
# address = re.search(r'^https?://(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]+$', web)
# address = re.search(r'^https?://[A-Za-z0-9.-]+\.[A-Za-z]+$', web)
# print(address)
# adress = re.findall(r'https?://', webs)
# print(adress)

pattern = r'^https?://[A-Za-z0-9.-]+\.[A-Za-z]+$'
valid_urls = [web for web in webs if re.match(pattern, web)]
print(valid_urls)


# 문제 풀이

# 1번
email_reg = re.compile(r'[\w-]+@[\w.]+\w+')
# mail = email_reg.search('test@gmail.com.')
mail = email_reg.search(news1)
print(mail)

# 2번
web_reg = re.compile(r'https?:/{2}[\w.]+\w+$')
print(list(map(lambda w: web_reg.search(w) != None, webs)))
