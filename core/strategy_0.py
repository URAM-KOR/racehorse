
if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from interface.upbit import buycoin_mp, sellcoin_mp
from entity.balance import krw_balance
from entity.ticker_list import buy_list

# wallet 점검
for my_ticker in krw_balance.keys():
	print("------------------")
	print("1. my_ticker:", my_ticker)
	try:
		if my_ticker not in buy_list.keys():
			sellcoin_mp(my_ticker, str(krw_balance[my_ticker]['balance']))
			print("2. successed sell ", buy_ticker)
	except Exception as e:
		print("2. sellcoin_mp err:", e)
		continue

# 차액 체크
for buy_ticker in buy_list.keys():
	print("------------------")
	print("1. buy_ticker:", buy_ticker)
	try:
		difference_balance = krw_balance['total'] * buy_list[buy_ticker] - krw_balance.get(buy_ticker, {}).get('balance_krw', 0)
		print("2. difference_balance:", difference_balance)
		if difference_balance > 0:
			buycoin_mp(buy_ticker, str(difference_balance))
			print("3. successed buy ", buy_ticker)
		if difference_balance < 0:
			difference_balance = difference_balance/krw_balance.get(buy_ticker, {}).get('trade_price', 1)
			sellcoin_mp(buy_ticker, str(-difference_balance))
			print("3. successed sell ", buy_ticker)
	except Exception as e:
		print("difference_balance err:", e)
		continue