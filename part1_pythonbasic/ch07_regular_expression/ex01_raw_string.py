import re

a = 'abcdef\n'  # escape 문자열
print(a)

b = r'abcdef\n'
print(b)

print('\n ==== 1. search method() ====')
# m = re.search(r'abc', 'abcdef')  # search(정규표현식 패턴, 찾을 대상)
m = re.search(r'abc', '123abcdef')  # search(정규표현식 패턴, 찾을 대상)
# m = re.search(r'abc', '123abdef')  # search(정규표현식 패턴, 찾을 대상)

print(m.start())  # 해당 패턴의 시작 위치
print(m.end())  # 해당 패턴의 끝 위치 -1
print(m.group())  # 검색된 패턴 자체
print(m)

print('\n == 1. search method() - \d, \w ==')
m = re.search(r'\d\d\d', '112abcdef119')
m = re.search(r'\d\d\d\w', '112abcdef119')

print(m)

m = re.search(r'..\w\w', '@#$%ABCDabcd')  # 아무문자 두개 영문자2개

print(m)

print('\n == 2. [] ==')
m = re.search(r'[cbm]at', 'cat')
m = re.search(r'[cbm]at', 'bat')
m = re.search(r'[cbm]at', 'mat')
m = re.search(r'[cbm]at', 'aat')  # None
print(m)

m = re.search(r'[0-9]haha', '1hahah')
m = re.search(r'[0-4]haha', '7hahah')  # Node
print(m)

m = re.search(r'[abc.^]aron', 'caron')
m = re.search(r'[abc.^]aron', '^aron')
m = re.search(r'[abc.^]aron', 'daron')  # None
m = re.search(r'[^abc]aron', 'aaron')  # None, ^ 부정
m = re.search(r'[^abc]aron', '#aron')  # None, ^ 부정
m = re.search(r'[^abc]aron', '0aron')  # None
print(m)

print('\n == 3. \ ==')
m = re.search(r'\sand', 'apple and banana')
m = re.search(r'\Sand', 'apple and banana')  # None
print(m)

m = re.search(r'.and', 'pand')
m = re.search(r'\.and', '.and')
print(m)

m = re.search(r'p.g', 'pig')
print(m)

print('\n == 4. +*? ==')
m = re.search(r'a[bcd]*b', 'abcbdccb')
print(m)

m = re.search(r'b\w+a', 'banana')  # 문자가 한번이상 반복
print(m)

m = re.search(r'i+', 'piigiii')  # + 는 처음것만 찾음
print(m)

m = re.search(r'pi+g', 'pg')
print(m)
m = re.search(r'pi*g', 'pg')
print(m)

m = re.search(r'https?', 'https://www.naver.com')
print(m)
m = re.search(r'https?', 'httpk://www.naver.com')
print(m)

print('\n == 5. ^*, ^$ ==')
m = re.search(r'b\w+a', 'cabana')
print(m)

m = re.search(r'^b\w+a', 'cabana')  # 문자열 시작부터 했어?
print(m)

m = re.search(r'b\w+a$', 'cabana')  # 문자열 뒤부터 했어?
m = re.search(r'b\w+a$', 'cabanap')  # 문자열 뒤부터 했어?
print(m)

print('\n == 6. grouping ==')
m = re.search(r'(\w+)@(.+)', 'test@gmail.com')
print(m)
print(m.group())
print(m.group(1))
print(m.group(2))
print(m.group(0))

print('\n == 7. {} ==')
m = re.search(r'pi{3}g', 'piiig')
m = re.search(r'pi{3,5}g', 'piiiiiig')  # 최소 3, 최대 5
print(m)

print('\n == 8. non greedy way ==')
m = re.search(r'<.+>', '<html>haha</html>')
print(m)

m = re.search(r'<.+?>', '<html>haha</html>')
print(m)

m = re.search(r'a{3,5}', 'aaaaa')  # greedy
print(m)

m = re.search(r'a{3,5}?', 'aaaaa')  # non greedy
print(m)

print('\n == 9. match() ==')
m = re.match(r'\d\d\d', 'my number is 123')
print(m)

m = re.search(r'\d\d\d', '123 is my number')
print(m)

re.search(r'^\d\d\d', '123 is my number')  # 동일동작

print('\n == 10. findall() ==')
ms = re.findall(r'[\w-]+@[\w.]+',
                'test@gmail.com haha test2@gmail.com nice test test')

print(ms)

print('\n == 11. sub() ==')
ms = re.sub(r'[\w-]+@[\w.]+', 'great',
            'test@gmail.com haha test2@gmail.com nice test test')

ms = re.sub(r'[\w-]+@[\w.]+', 'great',
            'test@gmail.com haha test2@gmail.com nice test test', count=1)

print(ms)

print('\n == 12. compile() ==')
email_reg = re.compile(r'[\w-]+@[\w.]+')

com = email_reg.search('test@gmail.com haha good')
com = email_reg.findall('test@gmail.com haha good')
print(com)
