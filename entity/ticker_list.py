from datetime import datetime, timedelta

def set_candles(candles):
    if len(candles) == 0: # 캔들이 없을 때
        all = []
        return all
    # print(candles)
    # one_year_ago_candles = candles[5]
    six_month_ago_candles = candles[4]
    three_month_ago_candles = candles[3]
    one_month_ago_candles = candles[2]
    one_week_ago_candles = candles[1]
    one_day_ago_candles = candles[0]
    
    output = {}

    output["market"] = one_day_ago_candles["market"]
    output["trade_price"] = one_day_ago_candles["trade_price"]
    output["candle_date_time_kst"] = one_day_ago_candles["candle_date_time_kst"]
    # output["change_rate_1y"] = (one_day_ago_candles["trade_price"] - one_year_ago_candles["opening_price"]) / one_year_ago_candles["opening_price"]
    output["change_rate_6m"] = (one_day_ago_candles["trade_price"] - six_month_ago_candles["opening_price"]) / six_month_ago_candles["opening_price"]
    output["change_rate_3m"] = (one_day_ago_candles["trade_price"] - three_month_ago_candles["opening_price"]) / three_month_ago_candles["opening_price"]
    output["change_rate_1m"] = (one_day_ago_candles["trade_price"] - one_month_ago_candles["opening_price"]) / one_month_ago_candles["opening_price"]
    output["change_rate_1w"] = (one_day_ago_candles["trade_price"] - one_week_ago_candles["opening_price"]) / one_week_ago_candles["opening_price"]
    output["change_rate_1d"] = one_day_ago_candles["change_rate"]
    
    return output


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

from interface.upbit import get_items, get_candle
# import time
# start_time = time.time()

def ticker_list():
    """
    return: list of ticker
    """
    # 현재 시간 (UTC)
    now_utc = datetime.utcnow()

    # 1주 전
    one_week_ago = now_utc - timedelta(weeks=1)

    # 한 달 전 (30일로 계산)
    one_month_ago = now_utc - timedelta(days=30)

    # 3달 전 (90일로 계산)
    three_months_ago = now_utc - timedelta(days=90)

    # 6달 전 (180일로 계산)
    six_months_ago = now_utc - timedelta(days=180)

    # 1년 전 (365일로 계산)
    # one_year_ago = now_utc - timedelta(days=365)

    # 포맷 지정
    date_format = "%Y-%m-%dT%H:%M:%S"

    # 결과 출력
    print("1주 전:", one_week_ago.strftime(date_format))
    print("한 달 전:", one_month_ago.strftime(date_format))
    print("3달 전:", three_months_ago.strftime(date_format))
    print("6달 전:", six_months_ago.strftime(date_format))
    # print("1년 전:", one_year_ago.strftime(date_format))

    period = [one_week_ago.strftime(date_format), one_month_ago.strftime(date_format), three_months_ago.strftime(date_format), six_months_ago.strftime(date_format)] # one_year_ago.strftime(date_format)

    # 데이터를 담을 리스트
    items = get_items(market='KRW', except_item='')
    all_candles = []
    buy_list = {}
    candles = [True]

    for ticker in items[:]:
        all_candle = []
        all_candle.extend(get_candle(ticker['market'], 'D', int(1), to=""))
        for to in period:
            candles = get_candle(ticker['market'], '10', int(1), to=to)
            if not candles:
                candles = get_candle(ticker['market'], '10', int(1), to="")
            all_candle.extend(candles)
        candles = set_candles(all_candle)
        all_candles.append(candles)

    top_change_rate_1d = sorted(all_candles, key=lambda x: x['change_rate_1d'], reverse=True)[:5]
    top_change_rate_1w = sorted(all_candles, key=lambda x: x['change_rate_1w'], reverse=True)[:5]
    top_change_rate_1m = sorted(all_candles, key=lambda x: x['change_rate_1m'], reverse=True)[:5]
    top_change_rate_3m = sorted(all_candles, key=lambda x: x['change_rate_3m'], reverse=True)[:5]
    top_change_rate_6m = sorted(all_candles, key=lambda x: x['change_rate_6m'], reverse=True)[:5]
    # top_change_rate_1y = sorted(all_candles, key=lambda x: x['change_rate_1y'], reverse=True)[:5]

    print(top_change_rate_1d)
    print(top_change_rate_1w)
    print(top_change_rate_1m)
    print(top_change_rate_3m)
    print(top_change_rate_6m)
    # print(top_change_rate_1y) 

    # rate 계산
    for index, ticker in enumerate(reversed(top_change_rate_1d)):
        buy_list[ticker['market']]=(index+1)*(5)*5/(75*15)
    for index, ticker in enumerate(reversed(top_change_rate_1w)):
        if ticker['market'] in buy_list.keys():
            buy_list[ticker['market']]+=(index+1)*(4)*5/(75*15)
    for index, ticker in enumerate(reversed(top_change_rate_1m)):
        if ticker['market'] in buy_list.keys():
            buy_list[ticker['market']]+=(index+1)*(3)*5/(75*15)
    for index, ticker in enumerate(reversed(top_change_rate_3m)):
        if ticker['market'] in buy_list.keys():
            buy_list[ticker['market']]+=(index+1)*(2)*5/(75*15)
    for index, ticker in enumerate(reversed(top_change_rate_6m)):
        if ticker['market'] in buy_list.keys():
            buy_list[ticker['market']]+=(index+1)*(1)*5/(75*15)
    # for index, ticker in enumerate(reversed(top_change_rate_1y)):
    #     if ticker['market'] in buy_list.keys():
    #         buy_list[ticker['market']]+=(index+1)*(1)*5/(75*15)
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

# buy_list = ticker_list()
        
# end_time = time.time()
# print("실행 시간 : ", end_time - start_time)                          