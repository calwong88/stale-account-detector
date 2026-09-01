from src.loader import load_accounts

accounts = load_accounts("data/users_sample.csv")
print(len(accounts))
print(accounts[2].upn, accounts[2].last_sign_in)
print(accounts[3].enabled, type(accounts[3].enabled))