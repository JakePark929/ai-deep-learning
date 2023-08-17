# class Person:
#     def __init__(self):
#         print(self, 'is generated')
#         self.name = 'Kate'
#         self.age = 10


# p1 = Person()
# p2 = Person()

# print(p1.name, p1.age)

# p1.name = 'Aaron'
# p1.age = 20

# print(p1.name, p1.age)

class Person:
    def __init__(self, name, age=10):
        self.name = name
        self.age = age


p1 = Person('Bob', 30)
p2 = Person('Kate', 20)
p3 = Person('Aaron')

print(p1.name, p1.age)
print(p2.name, p2.age)
print(p3.name, p3.age)
