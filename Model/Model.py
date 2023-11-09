import sys
import time
import warnings
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import lightgbm as lgb

# 경고 메시지 무시
warnings.filterwarnings('ignore')

# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않는 옵션을 추가
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)  # 묵시적 대기, 활성화를 최대 15초까지 기다림

# 명령줄 인자 받기
Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel = sys.argv[1:6]

# 받은 인자를 사용하여 날짜 형식 만들기
formatted_date = f"{Get_year}-{Get_month.zfill(2)}-{Get_date.zfill(2)}"

# '서울(108)'을 선택하려면 첫 번째 체크박스 ID를 'ztree_65_check'로 설정
checkbox_ids = [
    "ztree_65_check",
    "ztree1_3_check",  # 평균기온
    "ztree1_14_check",  # 일강수량
    "ztree1_22_check",  # 평균 풍속
    "ztree1_29_check",  # 평균 상대습도
    "ztree1_43_check",  # 합계일사량
    "ztree1_49_check",  # 3시간 신적설
    "ztree1_54_check"   # 평균 지면온도
]

# 페이지에 접속
driver.get('https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36')

# "일 자료" 옵션을 선택
Select(driver.find_element(By.ID, "dataFormCd")).select_by_value("F00501")

# 날짜 입력
date_fields = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "hasDatepicker")))
for date_field in date_fields:
    date_field.clear()
    date_field.send_keys(formatted_date)

# 잠시 대기 후 '닫기' 버튼 클릭
time.sleep(1)
driver.find_element(By.CLASS_NAME, "ui-datepicker-close").click()

# 서울(108) 체크박스 클릭
checkbox_id = "ztree_65_check"  # 서울(108)을 선택하는 체크박스의 ID
try:
    # 체크박스 요소를 찾음
    checkbox = driver.find_element(By.ID, checkbox_id)
    
    # JavaScript를 이용하여 클릭 이벤트를 강제로 발생시킴
    driver.execute_script("arguments[0].click();", checkbox)
except Exception as e:
    print(f"An error occurred while trying to click the checkbox with ID '{checkbox_id}': {e}")

# 체크박스 클릭
for checkbox_id in checkbox_ids:
    try:
        checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, checkbox_id))
        )
        checkbox.click()  # 기다린 후 클릭
    except Exception as e:
        print(f"Error clicking checkbox {checkbox_id}: {e}")

# '조회' 버튼 클릭 대신 goSearch() 함수 직접 호출
driver.execute_script("goSearch();")
time.sleep(5) 

# 선택된 도시에 대한 데이터를 포함하는 행을 찾습니다.
city_name = '서울' if Get_selectedCity == '0' else '다른 도시 이름'  # 실제 도시 이름으로 대체 필요
city_xpath = f"//tr[td[contains(text(),'{city_name}')]]"
row_data = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, city_xpath)))
data_items = row_data.find_elements(By.TAG_NAME, "td")

# 크롤링한 데이터를 리스트에 저장합니다.
crawled_data = [item.text for item in data_items]

#리스트 0번째 도시이름 변경하기
crawled_data[0]=0

# 종료 전 대기
driver.quit()

# 사용자 입력 데이터 처리 함수
def process_user_data(data):
    year, mnth, day = map(int, data[1].split('-'))
    values = [float(val) if val != "" else np.nan for val in data[2:]]
    avg_tmp, day_p, avg_wind, avg_rhum, t_sd, snow, avg_gtmp = values

    if mnth in [12, 1, 2]:
        season = 3
    elif mnth in [3, 4, 5]:
        season = 0
    elif mnth in [6, 7, 8]:
        season = 1
    elif mnth in [9, 10, 11]:
        season = 2
    result=pd.DataFrame([{'year': year, 'mnth': mnth, 'day': day, 'avg_tmp': avg_tmp, 'day_p': day_p,
                          'avg_wind': avg_wind, 'avg_rhum': avg_rhum, 't_sd': t_sd, 'snow': snow,
                          'avg_gtmp': avg_gtmp, 'season': season}])
    result = result.fillna(result.mean())
    return result

def process_and_encode_data(data, df):
    # 사용자 데이터 처리
    result_df = process_user_data(data)

    # 원-핫 인코딩 처리
    result_df = pd.get_dummies(result_df, columns=['day', 'year', 'mnth', 'season'])

    # 기존 데이터에 존재하는 모든 컬럼을 포함하도록 처리 (누락된 컬럼은 0으로 채움)
    for col in df.columns:
        if col not in result_df.columns:
            result_df[col] = 0

    # 'day_p'와 'snow' 컬럼의 null 값을 0으로 대체
    result_df['day_p'].fillna(0, inplace=True)
    result_df['snow'].fillna(0, inplace=True)

    # 훈련 데이터에 있는 모든 feature를 포함하도록 예측 데이터를 조정
    for col in df.drop(['CNT'], axis=1).columns:
        if col not in result_df.columns:
            result_df[col] = 0  # 없는 feature는 0으로 채웁니다.

    # 예측 데이터에 있는 모든 feature가 훈련 데이터에도 있는지 확인하고, 그렇지 않은 경우 해당 feature를 제거
    columns_to_remove = [col for col in result_df.columns if col not in df.drop(['CNT'], axis=1).columns]
    result_df.drop(columns=columns_to_remove, inplace=True)

    return result_df

def load_and_process_data():
    # 데이터 로딩
    df = pd.read_csv('https://raw.githubusercontent.com/rich-hyun/Battle-of-the-Strongest-Statisticians/main/18-23%20Seoul_day.csv')

    # 'date' 컬럼을 날짜 형식으로 변환하고 연, 월, 일 정보 추출
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['mnth'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    # 필요한 컬럼 선택
    selected_columns = ['day', 'year', 'mnth', 'avg_tmp', 'day_p', 'avg_wind', 'avg_rhum', 't_sd', 'snow', 'avg_gtmp', 'season', 'CNT']
    df = df[selected_columns]

    # 'CNT' 컬럼의 쉼표 제거하고 실수형으로 변환
    df['CNT'] = df['CNT'].str.replace(',', '').astype(float)

    # 범주형 데이터 원-핫 인코딩 처리 (필요한 컬럼에 대해서만 실행)
    df = pd.get_dummies(df, columns=['day', 'year', 'mnth', 'season'])

    # 결측치 처리 (평균값으로 대체)
    df = df.fillna(df.mean())

    # X와 y 데이터 설정
    X = df.drop(['CNT'], axis=1).values.astype(np.float32)
    y = df['CNT'].values.astype(np.float32)

    return X, y, df

# 모델 훈련 및 예측 함수
def train_and_predict_model(model, X_train, X_test, y_train, y_test, data, df, model_name):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)    
    result_df = process_and_encode_data(data, df)
    predicted_CNT = model.predict(result_df.values.astype(np.float32))
    predicted_CNT_rounded = round(predicted_CNT[0])
    print(f"{model_name} {predicted_CNT_rounded}")

# 모델별 훈련 및 예측 함수 정의
def train_and_predict_lgbm(X_train, X_test, y_train, y_test, data, df):
    model = lgb.LGBMRegressor(max_depth=30, random_state=42, verbose=-1)
    train_and_predict_model(model, X_train, X_test, y_train, y_test, data, df, "LightGBM")

def train_and_predict_xgboost(X_train, X_test, y_train, y_test, data, df):
    model = xgb.XGBRegressor(learning_rate=0.2, max_depth=3, n_estimators=100, random_state=42)
    train_and_predict_model(model, X_train, X_test, y_train, y_test, data, df, "XGBoost")

def train_and_predict_rf(X_train, X_test, y_train, y_test, data, df):
    model = RandomForestRegressor(n_estimators=300, max_features='sqrt', max_depth=20, random_state=42)
    train_and_predict_model(model, X_train, X_test, y_train, y_test, data, df, "Random Forest")

def train_and_predict_gb(X_train, X_test, y_train, y_test, data, df):
    model = GradientBoostingRegressor(max_depth=4, n_estimators=200, random_state=42)
    train_and_predict_model(model, X_train, X_test, y_train, y_test, data, df, "Gradient Boosting")

def train_and_predict_dt(X_train, X_test, y_train, y_test, data, df):
    model = DecisionTreeRegressor(max_depth=20, min_samples_split=10, random_state=42)
    train_and_predict_model(model, X_train, X_test, y_train, y_test, data, df, "Decision Tree")

def train_and_predict_lr(X_train, X_test, y_train, y_test, data, df):
    model = LinearRegression()
    train_and_predict_model(model, X_train, X_test, y_train, y_test, data, df, "Linear Regression")

data = crawled_data
result_df = process_user_data(data)

# 데이터 로딩 및 처리
X, y, df = load_and_process_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 선택에 따라 해당 모델 훈련 및 예측
if Get_vselectedModel == '1':
    train_and_predict_lgbm(X_train, X_test, y_train, y_test, data, df)

elif Get_vselectedModel == '2':
    train_and_predict_xgboost(X_train, X_test, y_train, y_test, data, df)

elif Get_vselectedModel == '3':
    train_and_predict_rf(X_train, X_test, y_train, y_test, data, df)

elif Get_vselectedModel == '4':
    train_and_predict_gb(X_train, X_test, y_train, y_test, data, df)

elif Get_vselectedModel == '5':
    train_and_predict_dt(X_train, X_test, y_train, y_test, data, df)

elif Get_vselectedModel == '6':
    train_and_predict_lr(X_train, X_test, y_train, y_test, data, df)

else:
    print("error_wrong_number",Get_vselectedModel)