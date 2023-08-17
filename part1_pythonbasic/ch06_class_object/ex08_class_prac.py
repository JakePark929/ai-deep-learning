import math

# 1) 복소수 클래스를 정의
# 2) 덧셈, 뺄셈, 곱셈 연산자 지원
# 3) 길이 (복소수의 크기) 지원
# 4) 복소수 출력 '1 + 4j'와 같이 표현
# 5) 비교연산 ==, != 지원
# 6) =, <=, <, > 연산 지원
# 7) 절대값 지원


class ComplexNumber:
    def __init__(self, real, img):
        self.real = real
        self.img = img

    def __add__(self, cn):
        return ComplexNumber(self.real + cn.real, self.img + cn.img)

    def __sub__(self, cn):
        return ComplexNumber(self.real - cn.real, self.img - cn.img)

    def __mul__(self, x):
        if type(x) == int:
            return ComplexNumber(self.real * x, self.img * x)
        elif type(x) == ComplexNumber:
            return ComplexNumber(self.real * x.real - self.img * x.img, self.real * x.img + self.img * x.real)
            # (a + bj) * (c + dj) = (ac - bd) + (ad + bc)j

    def __str__(self):
        if self.img > 0:
            return '{} + {}j'.format(self.real, self.img)
        else:
            return '{} - {}j'.format(self.real, abs(self.img))

    def __eq__(self, cn):
        return self.real == cn.real and self.img == cn.img

    def __ne__(self, cn):
        return not (self.real == cn.real and self.img == cn.img)

    def __abs__(self):
        return math.sqrt(self.real ** 2 + self.img ** 2)

    def __len__(self):
        # return int(math.sqrt(self.real ** 2 + self.img ** 2))
        return self.real ** 2 + self.img ** 2


a = ComplexNumber(1, 2)
b = ComplexNumber(3, 5)
print(a)
print(a + b)
print(a - b)
print(a * 3)
print(a * b)
b = ComplexNumber(1, 2)
print(a == b)
b = ComplexNumber(3, 2)
print(a != b)  # 자동으로 되긴 함

print(abs(a))
print(abs(-4))
print(len(a))
