from account.account import SavingAccount, CheckingAccount
from user.user import BankUser

user2 = BankUser("Brian", 900)

# 입출금 계좌에 $800
user2.deduct_money(800)
checking_account = CheckingAccount(user2.get_name(), 800)
user2.add_account(checking_account)

# 6% 예금 계좌 $100
user2.deduct_money(100)
saving_account = SavingAccount(user2.get_name(), 100, 0.06)
user2.add_account(saving_account)

try:
    # 예금계좌에서 $800 출금
    checking_account.withdraw(800)
except ValueError:
    checking_account.update_withdraw_limit(800)
    checking_account.withdraw(800)
finally:
    user2.add_money(800)

# 결과 출력
user2.get_assets()