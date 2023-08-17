# Point
# 2차원 좌표평면 각 점 (x, y)
# 연산
# 두 점의 덧셈, 뺄셈 (1 + 2) + (3, 4) = (4, 6)
# 한 점과 숫자의 곱셈 (1, 2) * 3 = (3, 6)
# 그점의 길이 (0, 0) 부터의 거리
# (x, y) 값 가져오기
# 출력하기

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, pt):
        new_x = self.x + pt.x
        new_y = self.y + pt.y
        return Point(new_x, new_y)

    def __sub__(self, pt):
        new_x = self.x - pt.x
        new_y = self.y - pt.y
        return Point(new_x, new_y)

    def __mul__(self, factor):
        return Point(self.x * factor, self.y * factor)

    def __len__(self):
        return self.x ** 2 + self.y ** 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        else:
            return -1

    def get_y(self):
        return self.y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)


p1 = Point(3, 4)
p2 = Point(3, 7)

a = 1 + 2
# p3 = p1 + p2
# p3 = p1.add(p2)
p3 = p1 + p2
p4 = p1 - p2
# p5 = p1.multiply(3)
p5 = p1 * 3

# print(p1.length())
print(len(p1))

# p1[0] -> x
# p1[1] -> y
# print(p1.get_x())
# print(p1.get_y())
print(p1[0])
print(p1[1])
print(p1)
print(p2)
print(p3)
print(p4)
print(p5)
