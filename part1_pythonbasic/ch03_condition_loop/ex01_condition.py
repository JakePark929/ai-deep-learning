print("\n==== 1. condition ====")

print("\n=== if basic1 ===")
if 6 >= 5:
    print('6 is greater than 5')
    print('Yeah, it is true')
    print('It is really trye')

print('This code is not belongs to if statements')

print("\n=== if basic2 ===")
if 6 == 5:
    print('6 is greater than 5')
    print('Yeah, it is true')
    print('It is really trye')

print('This code is not belongs to if statements')

print("\n=== NOT > AND > OR ===")
a = 10
b = 8
c = 11
if a == 10 or b == 9 and c == 12:
    print('that is true')

print("\n=== NOT ===")
if not a == 10:
    print('a is ten')

print("\n=== boolean ? ===")
# a = 0
# a = 10
a = []
if a:
    print('print')

print("\n=== if, else ===")
# 짝수인 경우에는 2로 나눈 값을 출력하고,
# 홀수인 경우에는 1을 더한 값을 출력해라
# a = 10
a = 9
if a % 2 == 0:
    print(a / 2)
else:
    print(a + 1)

print("\n=== if, elif, else ===")
a = 18
if a % 4 == 0:
    print('a is divisible by 4')
elif a % 4 == 1:
    print('a % 4 is 1')
elif a % 4 == 2:
    print('a % 4 is 2')
else:
    print('a % 4 is 3')
