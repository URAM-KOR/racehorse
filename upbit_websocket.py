import os
import sys
import time
import json
import datetime
import asyncio
import logging
import traceback
import websockets
import pickle

# 실행 환경에 따른 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from interface import upbit
from interface.upbit import buycoin_mp, sellcoin_mp
from entity.balance import get_my_balance

# 프로그램 정보
pgm_name = 'websocket'
pgm_name_kr = '업비트 Ticker 웹소켓'


# -----------------------------------------------------------------------------
# - Name : get_subscribe_items
# - Desc : 구독 대상 종목 조회
# -----------------------------------------------------------------------------
def get_subscribe_items(except_item: str = ''):
    try:
        subscribe_items = []

        # KRW 마켓 전 종목 추출
        items = upbit.get_items('KRW', except_item)

        # 종목코드 배열로 변환
        for item in items:
            subscribe_items.append(item['market'])

        return subscribe_items

    # ---------------------------------------
    # Exception 처리
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : upbit_ws_client
# - Desc : 업비트 웹소켓
# -----------------------------------------------------------------------------
async def upbit_ws_client():
    try:
        # 중복 실행 방지용
        seconds = 0

        # 순위 리셋용
        days = -1

        # 제외 종목
        except_item = ''

        # 구독 데이터 조회
        subscribe_items = get_subscribe_items(except_item)

        logging.info('제외 종목 : ' + str(except_item))
        logging.info('구독 종목 개수 : ' + str(len(subscribe_items)))
        logging.info('구독 종목 : ' + str(subscribe_items))

        # 구독 데이터 조립
        subscribe_fmt = [
            {"ticket": "test-websocket"},
            {
                "type": "ticker",
                "codes": subscribe_items,
                "isOnlyRealtime": True
            },
            {"format": "DEFAULT"}
        ]

        subscribe_data = json.dumps(subscribe_fmt)

        async with websockets.connect(upbit.ws_url) as websocket:

            await websocket.send(subscribe_data)

            # broadcast
            not_speaked = True

            # broadcast
            broadcast={}

            # selected_data
            selected_data = {}

            # pre_top_5_keys
            pre_top_5_keys = []

            # buy function condition
            start_time = time.time()  # 메인 루프가 시작된 시간 기록
            rest_time = time.time()  # 메인 루프가 시작된 시간 기록

            while True:
                period = datetime.datetime.utcnow()

                data = await websocket.recv()
                data = json.loads(data)

                # 가져오고자 하는 키들
                desired_keys = ['code', 'change', 'change_rate']

                # 딕셔너리 컴프리헨션을 사용하여 새로운 딕셔너리 생성
                if data.get('change') == 'RISE':
                    selected_data = {key: data[key] for key in desired_keys if key in data}

                # 순위 중계
                broadcast[selected_data['code']] = selected_data['change_rate']

                # 딕셔너리의 값들을 내림차순으로 정렬
                sorted_items = sorted(broadcast.items(), key=lambda x: x[1], reverse=True)

                # 상위 5개 값만 선택
                top_5_items = dict(sorted_items[:5])
                
                # broadcast 딕셔너리에서 상위 5개 키만 남기기
                broadcast = top_5_items
                # logging.info(list(top_5_items))

                if len(top_5_items) == 5:
                    # 이전 값 비교
                    if pre_top_5_keys != list(top_5_items):
                        logging.info(data)
                        logging.info(list(top_5_items))
                        not_speaked = True
                
                # 10초가 지났으면 이벤트 발생
                if time.time() - start_time >= 10:
                    # logging.info("Time to event!")
                    file_path = 'top_5_items.pkl'                    
                    with open(file_path, 'wb') as file:
                        pickle.dump(top_5_items, file, protocol=pickle.HIGHEST_PROTOCOL)
                        # await event_buy(top_5_items)
                
                pre_top_5_keys = list(top_5_items)

                # 매일마다 순위 측정 다시 시작
                if (period.day) != days:
                    # 중복 실행 방지
                    days = period.day

                    logging.info('\n\n')
                    logging.info('*************************************************')
                    logging.info(f'{period.year}.{period.month}.{period.day} 업비트 오늘의 경주 힘차게 출발했습니다!')
                    logging.info('*************************************************')
                    logging.info('\n\n')

                    # 순위 리셋
                    broadcast = {}

                # # 5초마다 종목 정보 재 조회 후 추가된 종목이 있으면 웹소켓 다시 시작
                # if (period.second % 5) == 0 and seconds != period.second:
                #     # 중복 실행 방지
                #     seconds = period.second

                #     # 종목 재조회
                #     re_subscribe_items = get_subscribe_items(except_item)
                #     # logging.info('\n\n')
                #     # logging.info('*************************************************')
                #     # logging.info('제외 종목 : [' + str(except_item) + ']')
                #     # logging.info('기존 종목[' + str(len(subscribe_items)) + '] : ' + str(subscribe_items))
                #     # logging.info('종목 재조회[' + str(len(re_subscribe_items)) + '] : ' + str(re_subscribe_items))
                #     # logging.info('*************************************************')
                #     # logging.info('\n\n')

                #     # 현재 종목과 다르면 웹소켓 다시 시작
                #     if subscribe_items != re_subscribe_items:
                #         logging.info('종목 달리짐! 웹소켓 다시 시작')
                #         await websocket.close()
                #         time.sleep(1)
                #         await upbit_ws_client()

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception as e:
        logging.error('Exception Raised!')
        logging.error(e)
        logging.error('Connect Again!')

        # 웹소켓 다시 시작
        await upbit_ws_client()


# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
async def main():
    try:
        # 웹소켓 시작
        await upbit_ws_client()

    except Exception as e:
        logging.error('Exception Raised!')
        logging.error(e)


# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # noinspection PyBroadException
    try:
        print("***** USAGE ******")
        print("[1] 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)")

        if sys.platform.startswith('win32'):
            # 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)
            log_level = 'I'
            upbit.set_loglevel(log_level)
        else:
            # 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)
            log_level = 'I'
            upbit.set_loglevel(log_level)

        if log_level == '':
            logging.error("입력값 오류!")
            sys.exit(-1)

        logging.info("***** INPUT ******")
        logging.info("[1] 로그레벨(D:DEBUG, E:ERROR, 그외:INFO):" + str(log_level))

        # ---------------------------------------------------------------------
        # Logic Start!
        # ---------------------------------------------------------------------
        # 웹소켓 시작
        asyncio.run(main())

    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)