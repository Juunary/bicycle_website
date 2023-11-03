import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import sys
import pandas as pd

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

# 데이터를 훈련 세트와 테스트 세트로 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 최적의 하이퍼파라미터로 랜덤 포레스트 모델 생성 및 훈련
best_rf_model = RandomForestRegressor(n_estimators=300, max_features='sqrt', max_depth=20, random_state=42)
best_rf_model.fit(X_train, y_train)

# 테스트 데이터에 대한 예측 수행
y_pred = best_rf_model.predict(X_test)

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

    return pd.DataFrame([{'year': year, 'mnth': mnth, 'day': day, 'avg_tmp': avg_tmp, 'day_p': day_p,
                          'avg_wind': avg_wind, 'avg_rhum': avg_rhum, 't_sd': t_sd, 'snow': snow,
                          'avg_gtmp': avg_gtmp, 'season': season}])
Get_year, Get_month, Get_date, Get_selectedCity, Get_vselectedModel = sys.argv[1:6]
data = f"{Get_year}-{Get_month}-{Get_date} 서울 랜덤포레스트 서울(108) {Get_year}-{Get_month}-{Get_date} 15.7 NULL 1.9 71.1 10.07 NULL 16.5"
result_df = process_user_data(data)

# 원-핫 인코딩 처리
result_df = pd.get_dummies(result_df, columns=['day', 'year', 'mnth', 'season'])

# 기존 데이터에 존재하는 모든 컬럼을 포함하도록 처리 (누락된 컬럼은 0으로 채움)
for col in df.columns:
    if col not in result_df.columns:
        result_df[col] = 0

# 컬럼 순서를 맞춤
result_df = result_df[df.drop(['CNT'], axis=1).columns]

# 결측치 처리 (평균값으로 대체)
result_df = result_df.fillna(df.mean())

# 예측 수행
predicted_CNT = best_rf_model.predict(result_df.values.astype(np.float32))

# 예측 결과를 반올림
predicted_CNT_rounded = round(predicted_CNT[0])

# 예측 결과 출력
print(f"{predicted_CNT_rounded}")

