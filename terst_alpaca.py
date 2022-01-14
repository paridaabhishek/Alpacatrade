
import re
import requests
# import alpaca_trade_api as tradeapi
# base_url = 'https://paper-api.alpaca.markets'
# api_key_id = 'PK82SGIMO3NE8LBCE4P4'
# api_secret = 'bZcC4lWvDmnXmaekDudR99dHCnEYp0tBcZVNXZzi'

# api = tradeapi.REST(
#     key_id=api_key_id,
#     secret_key=api_secret,
#     base_url=base_url,
#     api_version='v2'
# )

# api1 = tradeapi.REST()

# account = api.get_account()
# print(account)


# payload = {'APCA-API-KEY-ID': 'PK82SGIMO3NE8LBCE4P4',
#            'APCA-API-SECRET-KEY': 'bZcC4lWvDmnXmaekDudR99dHCnEYp0tBcZVNXZzi'}


# print(payload)


base_url = 'https://paper-api.alpaca.markets'
account_url = '{}/v2/account'.format(base_url)
print(account_url)
r = requests.get(url=account_url, headers={'APCA-API-KEY-ID': 'PK82SGIMO3NE8LBCE4P4',
                 'APCA-API-SECRET-KEY': 'bZcC4lWvDmnXmaekDudR99dHCnEYp0tBcZVNXZzi'})
data = r.json()
print(data)

requests.post()

print('Tesing')
