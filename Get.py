# -*- coding: utf-8 -*- 이게 없애도 되려나
# Get.py
import sys
import subprocess
from datetime import datetime, timedelta

# 커맨드 라인 인수의 개수 확인
if len(sys.argv) == 6:
    # 인수 부족할 경우 기본 값 할당
    Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel = sys.argv[1:6]
else:
    # 커맨드 라인 인수 사용
    Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel = '2023', '10', '11', 'Seoul', 'Random_Forest'
# 입력받은 날짜를 datetime 객체로 변환
input_date = datetime(int(Get_year), int(Get_month), int(Get_date))

# 현재 날짜를 구하고 하루를 뺀 날짜를 계산
yesterday = datetime.now() - timedelta(days=1)

# 입력받은 날짜가 어제보다 이후인지 확인

if input_date > yesterday:
    current_date = datetime.now().strftime('%Y-%m-%d')  # Format the current date as a string
    print(f"We only provide data for dates in the past, not beyond yesterday. Today's date is {current_date}.")
    sys.exit(1)

# "도시 선택" 또는 "모델 선택"인 경우 안내 메시지 출력
# 이부분 catch 에러로 바꿀 수 있을듯
if Get_selectedCity == "도시 선택" or Get_vselectedModel == "모델 선택":
    print("You must select the date, city, and model.")
    sys.exit(1)

# 서울 여부를 숫자로 변환
Get_selectedCity = '0' if Get_selectedCity == 'Seoul' else '1'

# 모델 선택을 숫자로 변환
if Get_vselectedModel == 'LightGBM':
    Get_vselectedModel = '1'
elif Get_vselectedModel == 'XGBOOST':
    Get_vselectedModel = '2'
elif Get_vselectedModel == 'Random_Forest':
    Get_vselectedModel = '3'
elif Get_vselectedModel == 'Gradient_Boosting':
    Get_vselectedModel = '4'
elif Get_vselectedModel == 'Decision_Tree':
    Get_vselectedModel = '5'
elif Get_vselectedModel == 'Linear_Regression':
    Get_vselectedModel = '6'
else :
    pass

# Model\Random.py 스크립트 실행
subprocess.run(['python', 'Model\\Model.py', Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel])