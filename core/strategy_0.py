
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
	try:
		if my_ticker not in buy_list.keys():
			sellcoin_mp(my_ticker, str(krw[my_ticker]['balance']))
	except Exception as e:
		print(e)

# 차액 체크
for buy_ticker in buy_list.keys():
	print("buy_ticker:", buy_ticker)
	time.sleep(0.1)
	try:
		difference_balance = krw_balance['total'] * buy_list[buy_ticker] - krw_balance.get(buy_ticker, {}).get('balance_krw', 0)
		print("difference_balance:", difference_balance)
		if difference_balance > 0:
			buycoin_mp(buy_ticker, str(difference_balance))
			print("successed buy ", buy_ticker)
		if difference_balance < 0:
			difference_balance = difference_balance/krw_balance.get(buy_ticker, {}).get('trade_price', 1)
			sellcoin_mp(buy_ticker, str(-difference_balance))
			print("successed sell ", buy_ticker)
	except Exception as e:
		print(e)