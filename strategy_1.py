import pickle
import sys
import os

# 실행 환경에 따른 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from interface import upbit
from interface.upbit import buycoin_mp, sellcoin_mp
from entity.balance import get_my_balance


def event_buy(top_5_items):
    # rate 계산
    buy_list = {}
    
    buy_list[list(top_5_items)[0]]=(1)/(1)
    # buy_list[list(top_5_items)[1]]=(1)/(5)
    # buy_list[list(top_5_items)[2]]=(1)/(12)
    # buy_list[list(top_5_items)[3]]=(2)/(2*15)
    # buy_list[list(top_5_items)[4]]=(1)/(2*15)
    
    # wallet 점검
    krw_balance = get_my_balance()
    print(krw_balance)
    for my_ticker in krw_balance.keys():
        print("------------------")
        try:
            print("1. my_ticker:", my_ticker, krw_balance[my_ticker]['balance'])
            if my_ticker not in buy_list.keys():
                if my_ticker == 'KRW-KRW' or my_ticker == 'KRW-VTHO' or my_ticker == 'KRW-APENFT':
                    continue
                print('my_ticker not in buy_list:', my_ticker)
                sellcoin_mp(my_ticker, str(krw_balance[my_ticker]['balance']))
                print("2. successed sell ", my_ticker)
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
            if difference_balance > 5000:
                buycoin_mp(buy_ticker, str(difference_balance))
                print("3. successed buy ", buy_ticker)
            if difference_balance < -5000:
                difference_balance = difference_balance/krw_balance.get(buy_ticker, {}).get('trade_price', 1)
                sellcoin_mp(buy_ticker, str(-difference_balance))
                print("3. successed sell ", buy_ticker)
        except Exception as e:
            print("difference_balance err:", e)
            continue
            logging.info(buy_list)
            
file_path = 'top_5_items.pkl'

while True:
    if os.path.exists(file_path):
        print(f'The file "{file_path}" exists.')
        # 파일에서 변수 읽어오기
        with open(file_path, 'rb') as file:
            try:
                top_5_items = pickle.load(file)
                print(top_5_items)
                event_buy(top_5_items)
            except EOFError:
                # print('EOFError: Ran out of input. Skipping...')
                pass
            
    else:
        print(f'The file "{file_path}" does not exist.')
        pass