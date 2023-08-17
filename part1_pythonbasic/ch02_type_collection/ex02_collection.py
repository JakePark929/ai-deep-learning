print("\n==== 1. list ====")
a = []
print(a)

a = [1, 2, 3, 5, 10]
print(a)

a = ['korea', 'canada', 1, 23, [34, 56]]
print(a)

print("\n=== list() ===")
a = 'hello world'
b = list(a)
print(b)

print("\n=== str.split() ===")
a = 'hello world nice weather'
b = a.split()
print(b)

print("\n=== list indexing ===")
a = [1, 2, 3, 4, 5, 6]
print(a[2])
print(a[5])
print(a[-1])

print("\n=== string slicing, immutable ===")
a = 'hello world'
print(a[0])
# a[0] = 'j'  # string 은 불변 객체

b = 'jello world'
c = 'j' + a[1:]

d = a.replace('h', 'j')  # 치환함
print(d, a)  # a 는 바뀌지 않음
print(b, c)

print("\n=== list mutable ===")
a = [1, 2, 3, 4, 5]
a[0] = 100

print(a)

print("\n=== list slicing ===")
a = [1, 2, 3, 4, 5, 6, 7, 8]
print(a[4:7])  # idx 4 ~ 6
print(a[:7])  # idx 0 ~ 6
print(a[3:])  # idx 3 ~ last
print(a[:])  # all

# slicing
# start:end:increment
print(a[1:7:1])  # idx 1 ~ 6 1 칸씩
print(a[1:7:2])  # idx 1 ~ 6 2 칸씩
print(a[1:7:6])  # idx 1 ~ 6 2 칸씩

print("\n=== list append() ===")
a = [1, 2, 3, 4, 5]
a.append(10)

print(a)

print("\n==== 2. list member ====")
print("\n=== list extend() ===")
a = [1, 2, 3, 4, 5]
b = [6, 7, 8, 9, 10]

# a.append(b)
# print(a[5])

# a.extend(b)
a += b
print(a)

print("\n=== list insert() ===")
a = [1, 3, 4, 5, 6]
a.insert(1, 40)

print(a)

print("\n=== list remove() ===")
a = [1, 2, 30, 30, 4, 5]
a.remove(30)

print(a)

print("\n=== list pop() ===")
a = [1, 2, 3, 4, 5]
# a.pop()
# a.pop(2)
d = a.pop(2)

print(a)
print(d)

print("\n=== list index() ===")
a = [2, 6, 7, 9, 10]
print(a.index(10))

print("\n=== in keyword ===")
a = [1, 2, 3, 4, 5, 10]
b = 7
# b = 10

c = b in a  # False
print(c)

print("\n=== list sort() ===")
a = [9, 10, 7, 19, 1, 2, 20, 21, 7, 8]
# a.sort() # asc
# a.sort(reverse=True)  # desc

d = sorted(a)

print(a)
print(d)

print("\n==== 3. tuple ====")
a = [1, 2, 3]
b = (1, 2, 3)

print(type(a))
print(type(b))

a[0] = 100
print(a)

# b[0] = 100 # error
# print(b) # error

print("\n=== tuple unpacking ===")
a = 100, 200
print(type(a))

print("\n=== swap ===")
a = 5
b = 4

print(a, b)

# swap logic
# temp = a
# a = b
# b = temp

a, b = b, a

print(a, b)

print("\n==== 4. dictionary ====")
# a = [0, 1, 2, 3, 4, 10, 100, 200, 300]
# print(a[0])
# print(a[4])

a = {
    'Korea': 'Seoul',
    'Canada': 'Ottawa',
    'USA': 'Wasington D.C'
}
# b = {}
b = {
    0: 1,
    1: 6,
    7: 9,
    8: 10
}

print(a)
print(type(b))
print(type(a))
print(a['Korea'])

print(b[0])

print("\n=== dict add element and update ===")
a = {
    'Korea': 'Seoul',
    'Canada': 'Ottawa',
    'USA': 'Wasington D.C'
}

a['Japan'] = 'Tokyo'
a['Japan'] = 'Kyoto'  # update
a['Japan2'] = 'Kyoto'
a['China'] = 'Beijing'

print(a)

print("\n=== dict update() ===")
a = {'a': 1, 'b': 2, 'c': 3}
b = {'a': 2, 'd': 4, 'e': 5}

a.update(b)

print(a)

print("\n=== dict pop() ===")
a = {'a': 1, 'b': 2, 'c': 3}
print(a)

# a.pop('b')
del a['b']

print(a)

print("\n=== del keyword ===")
# c = 100
# del c

# print(c)

print("\n=== dict clear() ===")
print(a)
a.clear()
print(a)

print("\n=== dict * in keyword * ===")
a = {'a': 1, 'b': 2, 'c': 3}
# print(a)
b = [1, 2, 3, 4, 5, 6, 7, 9, 10, 100]

# print('b' in a)
# print('d' in a)
print(100 in b)  # 성능 저하를 일으킬 수 있음(전체 리스트 조회)
print('b' in a)  # 빠른 시간에 가져옴(키를 바로 찾음)
print(2 in a)

print("\n=== dict value access ===")
# print(a['d']) # 프로그램이 죽음
print(a.get('d'))  # None 반환

if 'd' in a:
    print(a['d'])

print("\n=== dict access all keys and values ===")
print(a)
# print(a.keys())
# print(a.values())
print(list(a.keys()))
print(list(a.values()))
print(list(a.items()))

print("\n==== 5. set ====")
a = {1, 1, 2, 3, 3, 4, 1, 5}
print(a)

a = set()
print(type(a))

print("\n=== list to set ===")
a = [1, 1, 2, 3, 3, 4, 1, 5]
print(a)

b = set(a)
print(b)

print("\n=== set operations ===")
a = {1, 2, 3}
b = {2, 3, 4}

print(a)
print(b)
print("\n== union() ==")
print(a.union(b))
print("\n== intersection() ==")
print(a.intersection(b))
print("\n== difference() ==")
print(a.difference(b))
print("\n== issubset() ==")
print(a.issubset(b))
