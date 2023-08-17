# 내장 함수
import functools
print("\n==== 1. embeded function ====")
a = [1, 2, 3, 4]
length = len(a)
print(length)

summation = sum(a)
print(summation)

print("\n=== def keyword ===")


def add(x, y):
    n = x + y
    return n


l = len([1, 2, 3])
print(l)
c = add(30, 300)
print(c)

# c = add(30)  # error


def substract(x, y):
    sub = x - y
    return sub


print(substract(4, 3))


def test():
    print('haha')
    print('good')

    return 100


a = test()
print(a)

print("\n=== default parameter ===")


def newAdd(x, y, z=5):
    a = x + y + z
    return a


# print(newAdd(10, 20, 30))
print(newAdd(10, 20))

print("\n=== print() default parameter ===")
print(1, 2, 3, sep='!', end='%%%')
print(2, 3, 4, sep='p')

print("\n=== default parameter caution ===")
# def test(a, b=3, c):
#     print(a, b, c) # syntax error

print("\n=== keywaord parameter ===")


def test(x, y, z):
    a = x + y + z
    return a


print(test(x=10, z=3, y=50))

print("\n=== return keyword ===")


def weird_multiply(x, y):
    if x > 10:
        return x * y
    print(x + y)
    return (x + 2) * y
    print(x + y)


print(weird_multiply(1, 5))
print(weird_multiply(12, 5))

print("\n=== no return ===")


def weird_multiply(x, y):
    if x > 10:
        return
    print(x + y)
    return (x + 2) * y


c = weird_multiply(12, 5)
print(c)

print("\n=== none return ===")


def weird_multiply(x, y):
    if x > 10:
        return x * y


c = weird_multiply(2, 5)
print(c)

print("\n=== multiple return ===")


def add_mul(x, y):
    s = x + y
    m = x + y
    return s, m


# c = add_mul(20, 3)
# print(type(c))
# print(c)

a, b = add_mul(20, 3)
print(a, b)

print("\n=== variable scope ===")
num1 = 10
num2 = 30


def test(num1, num2):
    print(num1, num2)
    return num1 + num2


print(test(30, 40))
print(num1, num2)

print("\n=== variable length argument ===")
print()
print(1)
print(1, 2)
print(1, 2, 3)
print(1, 2, 3, 4)


def test(*x):  # *args
    # print(type(x))
    for item in x:
        print(item)


test(10, 20, 30, 40, 50)

print("\n=== keyword parameter argument ===")


def test2(**x):  # **kwargs = keyword arguments
    # print(type(x))
    for key, value in x.items():
        print('key', key, 'value', value)


# test2(a=1, b=2, c=3, d=4, name='Bob')
test2(a=1)

print("\n=== format() ===")
a = 'today\'s temperature: {today_temp}c, probability of rainfall : {today_prob}%, tomorrow\'s temperature: {tomorrow_temp}c'.format(
    today_temp=20, today_prob=50, tomorrow_temp=23)
print(a)

print("\n==== 2. lambda function ====")
def square(x): return x**2


# square = lambda x: x**2
print(type(square))
print(square(5))


def add(x, y):
    return x + y


# add = lambda x,y:x+y
add(10, 20)

strings = ['bob', 'charles', 'alexander3', 'teddy']
# strings.sort()
def str_len(s): return len(s)


print(str_len('goods'))

# strings.sort(key=str_len)  # custom sort
strings.sort(key=lambda s: len(s))  # custom sort with lambda

print(strings)

print("\n=== filter, map, reduce ===")
print("\n== filter() ==")
# filter(함수, 리스트)
def even(n): return n % 2 == 0


print(even(2))
print(even(3))

nums = [1, 2, 3, 6, 8, 9, 10, 11, 13, 15]
# print(list(filter(even, nums)))
print(list(filter(lambda n: n % 2 == 0, nums)))

print("\n== map() ==")
# map(함수, 리스트)
# 주어진 리스트, 리스트의 제곱을 한 숫자로 된 새로운 리스트
nums = [1, 2, 3, 6, 8, 9, 10, 11, 13, 15]
print(list(map(lambda n: n**2, nums)))

print(list(map(even, nums)))

print("\n== reduce() ==")
# functools.reduce(함수, 리스트) - 3부터 변경

# a = list(range(1, 11))
a = [1, 3, 5, 8]

# for loop 로 전체 합을 구함
# 리스트 내 모든 숫자합 구하기
# print(functools.reduce(lambda x, y: x + y, a))
print(functools.reduce(lambda x, y: x * y, a))

print("\n== practice 1 ==")


def avg(ls):
    # sum = functools.reduce(lambda x, y: x + y, ls)
    return functools.reduce(lambda x, y: x + y, ls) / len(ls)


a = [10, 10, 20]
b = [1, 2, 3]
# avg = lambda ls: functools.reduce(lambda x, y: x + y, ls) / len(ls)
print(avg(a))
print(avg(b))

print("\n== practice 2 ==")


def isPrime(n):
    if n == 1:
        return False
    # if n == 2:
    #     return True
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


print(isPrime(1))
print(isPrime(2))
print(isPrime(3))

print("\n== practice 3 ==")


def getCountPrime(n):
    count = 0
    for i in range(2, n):
        if isPrime(i):
            count += 1
    return count


print(getCountPrime(3))
