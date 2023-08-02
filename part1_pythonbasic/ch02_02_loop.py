print("\n==== 1. while ====")
a = [1, 10, 9, 24]

i = 0
sum = 0
while i < len(a):
    # print(a[i])
    print('value: ', a[i], ', index: ', i)
    sum += a[i]
    i += 1

print(sum)
print('haahah')

print("\n== grater than 20 ==")
a = [1, 10, 9, 24, 25, 26]

i = 0
while i < len(a):
    if a[i] > 20:  # 20보다 큰 경우만 출력
        print(a[i])
    i += 1

print("\n== odd case ==")
a = [1, 10, 9, 24, 25, 26]

i = 0
while i < len(a):
    if a[i] % 2:  # 홀수인 경우만 출력
        print(a[i])
    else:
        print(a[i] / 2)
    i += 1

print("\n== break ==")
a = [1, 10, 9, 24, 25, 26]

i = 0
while i < len(a):
    if a[i] > 20:
        break
    print(a[i])
    i += 1

print('hahaha')

print("\n== continue ==")
a = 7
while a > 0:
    a -= 1
    if a == 5:
        continue
    print(a)

print("\n== sum 1 to 100 ==")
num = 1
_sum = 0
while num <= 100:
    _sum += num
    num += 1

print(_sum, num)


print("\n==== 2. for ====")
a = [1, 2, 3, 4, 5]
for i in a:
    print(i, i * 2)
print('hahaha')

print("\n== string items ==")
a = 'hello world'
for ch in a:
    print(ch)

print("\n== dictionary items ==")
a = {
    'Korea': 'Seoul',
    'Canada': 'Ottawa',
    'USA': 'Wasington D.C'
}
for key in a:
    # print(key, a[key])
    print(key)

for value in a.values():
    print(value)

print(list(a.items()))
for k, v in a.items():  # tuple
    print(k, v)

print("\n== enumerate() ==")
a = [1, 2, 4, 3, 5]
for idx, val in enumerate(a):
    if idx > 3:
        print(idx, val)
print('haha')

print("\n== for break ==")
a = [100, 90, 80, 70, 60, 50]
for num in a:
    if num < 80:
        break
    print(num)

print("\n== for continue ==")
a = [100, 90, 80, 70, 60, 50]
for num in a:
    if num >= 60 and num <= 70:
        continue
    print(num)

print("\n== gugudan ==")
x = [2, 3, 4, 5, 6, 7, 8, 9]
y = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in x:
    for j in y:
        print(i, ' x ', j, ' = ', i * j)

print("\n== range() ==")
print(list(range(10)))  # 0 부터 10 미포함
print(list(range(1, 101)))  # 1부터 101 미포함
print(list(range(1, 101, 5)))  # 1부터 101 미포함, 5씩 건너뜀

print("\n== 1 <= ~ < 100, multiple 5 ==")
print(list(range(5, 100, 5)))

print("\n=== practice ===")
print("\n== 1. gugudan ==")
for i in range(2, 10):
    for j in range(1, 10):
        print(i, ' x ', j, ' = ', i * j)

print("\n== 2. 1 - 100, multiple 2 or 11 ==")
for i in range(1, 101):
    if i % 2 == 0 or i % 11 == 0:
        print(i)

print("\n== 3. max and min in list ==")
a = [22, 1, 3, 4, 7, 98, 21, 55, 87, 99, 19, 20, 45]
a.sort()
print(a[0], a[-1])

max = -9999
min = 9999

for i in a:
    if i > max:
        max = i
    if i < min:
        min = i

print('max: ', max, ', min: ', min)

print("\n== 4. get avg in list ==")
a = [22, 1, 3, 4, 7, 98, 21, 55, 87, 99, 19, 20, 45]

sum = 0
for i in a:
    sum += i

print(sum / len(a))
