from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, show
import pandas as pd
import random
from datetime import timedelta

from racehorse.interface.mongo_handler import MongoDBHandler

# MongoDBHandler 인스턴스 생성
mongo_handler = MongoDBHandler()
documents = mongo_handler.find_documents("rise_top_5", query={}, projection={"_id": 0})

df = pd.DataFrame(documents[20000:])

# timestamp를 datetime으로 변환
df['trade_timestamp'] = pd.to_datetime(df['trade_timestamp'], unit='ms')
df['trade_timestamp'] = df['trade_timestamp'] + timedelta(hours=9)

# 캔버스 크기 조절
plot_width = 1600
plot_height = 960

# 빈 캔버스 생성
p = figure(width=plot_width, height=plot_height, x_axis_type='datetime')  # x축을 datetime으로 설정

# 'code'로 그룹화하여 그룹마다 그래프 생성
for group_name, group_data in df.groupby('code'):
    source = ColumnDataSource(data=group_data)
    # 랜덤한 RGB 값 생성
    random_color = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 각 그룹마다 라인 그래프 추가
    line = p.line(x='trade_timestamp', y='change_rate', source=source, legend_label=group_name, line_color=random_color)

    # HoverTool 추가
    hover = HoverTool(tooltips=[
        ("Code", "@code"),
        ("timestamp", "@trade_timestamp{%Y-%m-%d %H:%M:%S}"),
        ("change_rate", "@change_rate")
    ], formatters={'@trade_timestamp': 'datetime'})
    p.add_tools(hover)

# 범례 위치 조절
p.legend.location = (0, -30)

# 범례 추가
p.legend.title = 'Code'
p.legend.label_text_font_size = '10pt'

# 결과 보여주기
show(p)