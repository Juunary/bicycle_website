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
if Get_vselectedModel == 'Random':
    Get_vselectedModel = '1'
elif Get_vselectedModel == 'Time_series':
    Get_vselectedModel = '2'

# Model\Random.py 스크립트 실행
#subprocess.run(['python', 'Model\\Random.py', Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel])
subprocess.run(['python', 'Scroll.py', Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel])