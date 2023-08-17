# 1. 숫자를 하나 증가
# 2. 숫자를 0으로 초기화
class Counter:
    def __init__(self):
        self.num = 0

    def increment(self):
        self.num += 1

    def reset(self):
        self.num = 0

    def printCurrentValue(self):
        print('현재값은:', self.num)


class Math:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b


c1 = Counter()
print(c1.num)
c1.printCurrentValue()
c1.increment()
c1.increment()
c1.increment()
c1.printCurrentValue()

c1.reset()
c1.printCurrentValue()

c2 = Counter()
c2.printCurrentValue()

c2.increment()
c2.printCurrentValue()

# m = Math()
# print(m.add(10, 20))
# print(m.multiply(10, 20))

print(Math.add(10, 20))
print(Math.multiply(10, 20))
