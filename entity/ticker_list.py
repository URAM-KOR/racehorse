from datetime import datetime, timedelta
import pandas as pd


def set_candles(candles):
    if len(candles) == 0: # 캔들이 없을 때
        all = []
        return all
    
    one_year_ago_candles = candles[2190] if 2190 <= len(candles) else candles[-1]
    six_month_ago_candles = candles[1107] if 1107 <= len(candles) else candles[-1] 
    three_month_ago_candles = candles[547] if 547 <= len(candles) else candles[-1]
    one_month_ago_candles = candles[188] if 188 <= len(candles) else candles[-1]
    one_week_ago_candles = candles[48] if 48 <= len(candles) else candles[-1]
    one_day_ago_candles = candles[0]

    all = [one_year_ago_candles, six_month_ago_candles, three_month_ago_candles, one_month_ago_candles, one_week_ago_candles]
    # 남길 키 지정
    keys_to_keep = ["market", "opening_price", "trade_price", "candle_date_time_kst"]
    output = {}
            
    output["market"] = one_day_ago_candles["market"]
    output["trade_price"] = one_day_ago_candles["trade_price"]
    output["candle_date_time_kst"] = one_day_ago_candles["candle_date_time_kst"]
    output["change_rate_1y"] = (one_day_ago_candles["trade_price"] - one_year_ago_candles["opening_price"]) / one_year_ago_candles["opening_price"]
    output["change_rate_6m"] = (one_day_ago_candles["trade_price"] - six_month_ago_candles["opening_price"]) / six_month_ago_candles["opening_price"]
    output["change_rate_3m"] = (one_day_ago_candles["trade_price"] - three_month_ago_candles["opening_price"]) / three_month_ago_candles["opening_price"]
    output["change_rate_1m"] = (one_day_ago_candles["trade_price"] - one_month_ago_candles["opening_price"]) / one_month_ago_candles["opening_price"]
    output["change_rate_1w"] = (one_day_ago_candles["trade_price"] - one_week_ago_candles["opening_price"]) / one_week_ago_candles["opening_price"]
    
    return output


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		print(path.dirname( path.dirname( path.abspath(__file__) ) ))
		sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from interface.upbit import get_items, get_candle
import time
start_time = time.time()

def ticker_list():
    """
    return: list of ticker
    """
    # 현재 시간 가져오기
    current_time = datetime.now()

    # 1년 전 계산
    one_year_ago = current_time - timedelta(hours=8760)
    one_year_ago_string = one_year_ago.strftime("%Y-%m-%dT%H:%M:%SZ")

    # 데이터를 담을 리스트
    items = get_items(market='KRW', except_item='')

    all_candles = []
    buy_list = {}
    candles = [True]

    for ticker in items[:]:
        candles = get_candle(ticker['market'], '240', int(2274))[:]
        candles = set_candles(candles)
        print(candles)
        all_candles.append(candles)
        
    top_change_rate_1w = sorted(all_candles, key=lambda x: x['change_rate_1w'], reverse=True)[:5]
    top_change_rate_1m = sorted(all_candles, key=lambda x: x['change_rate_1m'], reverse=True)[:5]
    top_change_rate_3m = sorted(all_candles, key=lambda x: x['change_rate_3m'], reverse=True)[:5]
    top_change_rate_6m = sorted(all_candles, key=lambda x: x['change_rate_6m'], reverse=True)[:5]
    top_change_rate_1y = sorted(all_candles, key=lambda x: x['change_rate_1y'], reverse=True)[:5]

    print(top_change_rate_1w)
    print(top_change_rate_1m)
    print(top_change_rate_3m)
    print(top_change_rate_6m)
    print(top_change_rate_1y)

    # rate 계산
    for index, ticker in enumerate(top_change_rate_1w):
        buy_list[ticker['market']]=1 * index
        if buy_list.get(ticker['market'], False):
            print(buy_list)
    for index, ticker in enumerate(top_change_rate_1m):
        if ticker['market'] in buy_list.keys():
            buy_list[ticker['market']]+=1 * index
    for index, ticker in enumerate(top_change_rate_3m):
        if ticker['market'] in buy_list.keys():
            buy_list[ticker['market']]+=1 * index
    for index, ticker in enumerate(top_change_rate_6m):
        if ticker['market'] in buy_list.keys():
            buy_list[ticker['market']]+=1 * index
    for index, ticker in enumerate(top_change_rate_1y):
        if ticker['market'] in buy_list.keys():
            buy_list[ticker['market']]+=1 * index

    print(buy_list)
    return buy_list


# 잔고 조회 
def get_balance(ticker):
    """
    return: {ticker: volume}
    """
    pass 

# 매도
def sell(ticker, volume, price=1):
    "sell ticker with volume at price"
    pass

# 매수      
def buy(ticker, volume, price=1):
    "buy ticker with volume at price"
    pass

ticker_list()
        
end_time = time.time()
print("실행 시간 : ", end_time - start_time)                          