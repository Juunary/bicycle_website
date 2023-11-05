import warnings
warnings.filterwarnings('ignore')
import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
import lightgbm as lgb
import sys

# 사용자 입력 데이터 처리 함수
def process_user_data(data):
    data_parts = data.split()
    year, mnth, day = map(int, data_parts[0].split('-'))
    values = [float(val) if val != "NULL" else np.nan for val in data_parts[5:12]]
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

    # 연도, 월, 일 컬럼 추출
    result_df['year'] = Get_year
    result_df['mnth'] = Get_month
    result_df['day'] = Get_date

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

Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel = sys.argv[1:6]

data = f"{Get_year}-{Get_month}-{Get_date} 서울 랜덤포레스트 서울(108) {Get_year}-{Get_month}-{Get_date} 15.7 NULL 1.9 71.1 10.07 NULL 16.5"

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