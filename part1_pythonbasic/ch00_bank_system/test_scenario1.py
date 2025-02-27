from account import SavingAccount, CheckingAccount
from user import BankUser

user1 = BankUser("박중언", 1000)

# $200를 입출금 계좌에
user1.deduct_money(200)
checking_account = CheckingAccount(user1.get_name(), 200)
user1.add_account(checking_account)

# $800를 예금 계좌에
user1.deduct_money(800)
saving_account = SavingAccount(user1.get_name(), 800, 0.05)
user1.add_account(saving_account)

# 예금계좌 출금 가능
saving_account.unlock()

# 예금계좌에서 $400 출금한 다음, 사용자에게 지급
saving_account.withdraw(400)
user1.add_money(400)

# $400를 차감하여, 입출금 계좌로 입금
user1.deduct_money(400)
checking_account.deposit(400)

# 보유 현금 및 계좌목록 출력
user1.get_assets()