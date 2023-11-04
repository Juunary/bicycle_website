# Get.py
import sys
import subprocess

if len(sys.argv) < 6:
    print("인수 부족")
    sys.exit(1)

# 인자로 받은 값들을 변수에 저장
Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel = sys.argv[1:6]

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
#subprocess.run(['python', 'Scroll.py', Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel])