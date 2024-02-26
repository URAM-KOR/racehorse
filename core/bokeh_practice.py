from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
import pandas as pd
import random
from datetime import timedelta, datetime
from time import time

from racehorse.interface.mongo_handler import MongoDBHandler
from racehorse.interface.upbit import get_items, get_candle, get_max



# print(get_items('KRW',''))
# candle = get_candle('KRW-BTC','1',200)
# print(len(candle))
# max = get_max(candle,'high_price', 'low_price')
# print(max)

# MongoDBHandler 인스턴스 생성
mongo_handler = MongoDBHandler()
documents = mongo_handler.find_documents("rise_top_3", query={}, projection={"_id": 0})

# 데이터를 담을 리스트
all_candles = []

for idx, event_log in enumerate(documents):
    # print(event_log)
    # print(event_log['trade_utc'].strftime("%Y-%m-%dT%H:%M:%SZ"))

    # 이전 거래 시간과 현재 거래 시간 사이의 분 차이 계산
    if idx > 0:
        time_difference = (event_log['trade_utc'] - documents[idx - 1]['trade_utc']).total_seconds() / 60
        # print(int(time_difference))
        # 분 차이를 기반으로 데이터 가져오기
        for ticker in event_log['top_3_items'].keys():
            candles = get_candle(ticker, 'D', int(365), event_log['trade_utc'].strftime("%Y-%m-%dT%H:%M:%SZ"))[:]
            all_candles.extend(candles)

print(all_candles)
df = pd.DataFrame(all_candles)

from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.plotting import figure, show, output_file


# 파일 생성
output_file('plot.html')

inc = df.trade_price >= df.opening_price
dec = df.opening_price > df.trade_price

# 데이터프레임을 'market' 기준으로 groupby
grouped_df = df.groupby('market')
from bokeh.palettes import Category20  # Bokeh에서 제공하는 색상 팔레트 사용

# Bokeh 그래프 설정
p = figure(title="Change Rate over Time", x_axis_label='Timestamp', y_axis_label='change_rate')


# 각 마켓에 대해 서로 다른 랜덤 색상 할당
colors = ['#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(len(grouped_df))]

for i, (market, group) in enumerate(grouped_df):
    # 각 'market' 별로 Bokeh의 ColumnDataSource로 변환
    group = group.set_index('timestamp').reset_index()  # 인덱스 설정 및 'candle_date_time_kst'를 열로 변환

    # 'change_rate' 열 추가
    day_candles = get_candle(market, 'D', int(1), event_log['trade_utc'].strftime("%Y-%m-%dT%H:%M:%SZ"))[0]

    group['change_rate'] = ((group['trade_price'] - day_candles['opening_price']) / day_candles['opening_price']) * 100

    # ColumnDataSource 생성 시 명시적으로 열 지정
    source = ColumnDataSource(group).stream

    # figure 에 그릴 그래프 그리기
    # p.line(x='timestamp', y='change_rate', legend_label=market, line_width=2, line_color=colors[i], source=source)

    # 거래대금을 각 색상에 맞게 바 형태로 표시
    p.vbar(x='timestamp', width=4, bottom=0, top='change_rate', color=colors[i], alpha=0.2, source=source,
           legend_label=market)

# 레전드 위치 설정 (선택적)
p.legend.location = "top_left"

# x-축 눈금 방향 및 개수 설정
p.xaxis.major_label_orientation = "vertical"
p.xaxis.ticker.desired_num_ticks = 10

# x-축의 datetime 형식 설정
p.xaxis.formatter = DatetimeTickFormatter(days="%m-%d %H:%M", months="%m-%d %H:%M", years="%m-%d %H:%M")

# Hover 도구 생성
hover = HoverTool(tooltips=[
    ("Timestamp", "@trade_utc"),
    ("Change Rate", "@change_rate"),
    ("Market", "@market"),
], formatters={'@timestamp': 'datetime'})

# 그래프에 Hover 도구 추가
p.add_tools(hover)

# 새 브라우저 탭에 출력!
show(p)
