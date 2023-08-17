class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self, food):
        print('{}은 {}를 먹습니다.'.format(self.name, food))

    def sleep(self, minute):
        print('{}은 {}분 동안 잡니다.'.format(self.name, minute))

    def work(self, minute):
        print('{}은 {}분 동안 준비를 합니다.'.format(self.name, minute))


class Student(Person):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def work(self, minute):  # method overriding
        super().work(minute)
        print('{}은 {}분 동안 공부합니다.'.format(self.name, minute))


class Employee(Person):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def work(self, minute):  # method overriding
        super().work(minute)
        print('{}은 {}분 동안 업무합니다.'.format(self.name, minute))


# bob = Person('Bob', 25)
bob = Student('Bob', 25)
# bob = Employee('Bob', 25)
bob.eat('BBQ')
bob.sleep(30)
bob.work(60)
