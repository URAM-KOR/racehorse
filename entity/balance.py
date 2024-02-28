
if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		print(path.dirname( path.dirname( path.abspath(__file__) ) ))
		sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from interface.upbit import get_balance, get_ticker, get_items

balance = get_balance('KRW')
def get_my_balance(balance):
	krw_balance = {'total':float(balance[0]['balance'])}
	for ticker in balance:
		try:
			krw_ticker = get_ticker(f"KRW-{ticker['currency']}")[0]['trade_price'] * float(ticker['balance'])
			krw_balance['total'] += krw_ticker
			krw_balance[f"KRW-{ticker['currency']}"]={}
			krw_balance[f"KRW-{ticker['currency']}"]['balance_krw']=krw_ticker
			krw_balance[f"KRW-{ticker['currency']}"]['balance']=float(ticker['balance'])
			krw_balance[f"KRW-{ticker['currency']}"]['trade_price']=get_ticker(f"KRW-{ticker['currency']}")[0]['trade_price']
		except Exception as e:
			print(e)
			continue

	return krw_balance

krw_balance = get_my_balance(balance)
print(krw_balance)