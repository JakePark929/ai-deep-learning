import random
from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, holder_name, balance):
        self._account_number = random.randint(100000, 999999)
        self._holder_name = holder_name
        self.__balance = balance

    def get_account_number(self):
        return self._account_number

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("잔액이 부족합니다.")
        else:
            self.__balance -= amount
            return self.__balance

    @abstractmethod
    def info(self):
        return f"{self._holder_name}님의 계좌 잔액은 {self.__balance}원 입니다."
    
# 적금 계좌
class SavingAccount(BankAccount):
    def __init__(self, holder_name, balance, interest_rate):
        super().__init__(holder_name, balance)
        self.__interest_rate = interest_rate
        self.__is_locked = True

    def withdraw(self, amount):
        if self.__is_locked:
            raise AttributeError("잠긴 계좌입니다.")
        else:
            super().withdraw(amount)

    def unlock(self):
        self.__is_locked = False
        interest = self.get_balance() * self.__interest_rate
        self.deposit(interest)

    def info(self):
        print(f"[예금/{self.get_account_number()}] 잔액 ${self.get_balance()}, 이율: {self.__interest_rate}%, 출금 제한 여부: {self.__is_locked}")

# 예금 계좌
class CheckingAccount(BankAccount):
    def __init__(self, holder_name, balance, withdraw_limit = 500):
        super().__init__(holder_name, balance)
        self.withdraw_limit = withdraw_limit

    def withdraw(self, amount):
        if amount > self.withdraw_limit:
            raise ValueError("출금 한도를 초과했습니다.")
        else:
            super().withdraw(amount)

    def update_withdraw_limit(self, new_limit):
        self.withdraw_limit = new_limit

    def info(self):
        print(f"[입출금/{self.get_account_number()}] 잔액 ${self.get_balance()}, 출금 한도: {self.withdraw_limit}")