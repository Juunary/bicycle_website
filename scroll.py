#Ch_selenium/example/tutorial1.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

# 웹드라이버 초기화
driver = webdriver.Chrome()  # 여기서 Chrome 드라이버의 경로를 명시해야 할 수도 있습니다.
driver.implicitly_wait(15)  # 묵시적 대기, 15초 동안 요소가 로드될 때까지 기다립니다.

# 페이지 가져오기(이동)
url = "https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36"
driver.get(url)

data_form_select = Select(driver.find_element(By.ID, "dataFormCd"))

# "일 자료" 옵션을 선택
data_form_select.select_by_value("F00501")

checkbox_ids = [
    "ztree_65_check",  # 서울
    "ztree1_3_check",  # 평균기온
    "ztree1_14_check",  # 일강수량
    "ztree1_22_check",  # 평균 풍속
    "ztree1_29_check",  # 평균 상대습도
    "ztree1_43_check",  # 합계일사량
    "ztree1_49_check",  # 3시간 신적설
    "ztree1_54_check"   # 평균 지면온도
]

# 모든 체크박스를 클릭
for checkbox_id in checkbox_ids:
    checkbox_element = driver.find_element(By.ID, checkbox_id)
    if not checkbox_element.is_selected():
        checkbox_element.click()

# 사용자의 입력을 기다리거나, 무한 대기 설정
#input("브라우저를 닫기 전에 엔터를 누르세요...")
#time.sleep(600)  # 10분간 대기
while True:
    time.sleep(1)

