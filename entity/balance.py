
if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from interface.upbit import get_balance, get_ticker
import pickle
import os

def _update_profit_dict(current_total):
	file_path = 'saved_profit_dict.pkl'

	if os.path.exists(file_path):
		# print(f'The file "{file_path}" exists.')
		# 파일에서 변수 읽어오기
		with open(file_path, 'rb') as file:
			loaded_profit_dict = pickle.load(file)

			if loaded_profit_dict['max_total'] is None:
				loaded_profit_dict['max_total'] = current_total
						
			if current_total > loaded_profit_dict['max_total']:
				loaded_profit_dict['profit'] += current_total - loaded_profit_dict['max_total']
				loaded_profit_dict['net_profit'] = loaded_profit_dict['profit']/2
				loaded_profit_dict['max_total'] = current_total

			if current_total < loaded_profit_dict['max_total']:
				loaded_profit_dict['current_total'] = current_total
    
			with open(file_path, 'wb') as file:
				pickle.dump(loaded_profit_dict, file, protocol=pickle.HIGHEST_PROTOCOL)
			
		return loaded_profit_dict

	else:
		print(f'The file "{file_path}" does not exist.')

		profit_dict = {
			"max_total": None,
			"current_total": None,
			"profit": 0
		}

		profit_dict['current_total'] = current_total

		with open(file_path, 'wb') as file:
			pickle.dump(profit_dict, file)
		print(f'The file "{file_path}" saved.')
		
		return profit_dict

# # 함수 호출
# current_total_value = 100  # 예시로 100을 사용하였으나 실제 데이터에 맞게 설정
# result_profit_dict = _update_profit_dict(current_total_value)
# print(result_profit_dict)

def get_my_balance():
	balance = get_balance('KRW')
	krw_balance = {'total':float(next(item['balance'] for item in balance if item['currency'] == 'KRW'))}
	print(balance)
	for ticker in balance:
		if ticker['currency'] == 'KRW' or ticker['currency'] == 'VTHO' or ticker['currency'] == 'APENFT':
			continue
		# print(ticker['currency'])
		try:
			krw_ticker = get_ticker(f"KRW-{ticker['currency']}")[0]['trade_price'] * float(ticker['balance'])
			krw_balance['total'] += krw_ticker
			krw_balance[f"KRW-{ticker['currency']}"]={}
			krw_balance[f"KRW-{ticker['currency']}"]['balance_krw']=krw_ticker
			krw_balance[f"KRW-{ticker['currency']}"]['balance']=float(ticker['balance'])
			krw_balance[f"KRW-{ticker['currency']}"]['trade_price']=get_ticker(f"KRW-{ticker['currency']}")[0]['trade_price']
		except Exception as e:
			# print(e)
			continue

	profit_dict = _update_profit_dict(krw_balance['total'])
	print(profit_dict)
	krw_balance['total'] -= profit_dict['profit']/2
	return krw_balance

# krw_balance = get_my_balance()
# print(krw_balance)