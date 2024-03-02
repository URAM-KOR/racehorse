import pickle
import os

def update_profit_dict(current_total):
    file_path = 'saved_profit_dict.pkl'

    if os.path.exists(file_path):
        print(f'The file "{file_path}" exists.')
        # 파일에서 변수 읽어오기
        with open(file_path, 'rb') as file:
            loaded_profit_dict = pickle.load(file)
            print(loaded_profit_dict)

        if loaded_profit_dict['max_total'] is None:
            loaded_profit_dict['max_total'] = current_total

        # update ----------
        
        # if current_total > loaded_profit_dict['max_total']:
        #     loaded_profit_dict['profit'] += current_total - loaded_profit_dict['max_total']
        #     loaded_profit_dict['max_total'] = current_total
        # loaded_profit_dict['net_profit'] = loaded_profit_dict['net_profit']/2

        print(loaded_profit_dict)

        # end ---------------
        
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
current_total_value = 100  # 예시로 100을 사용하였으나 실제 데이터에 맞게 설정
result_profit_dict = update_profit_dict(current_total_value)
# print(result_profit_dict)
