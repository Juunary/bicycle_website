import sys
if len(sys.argv) < 6:
    print("인수 부족")
    sys.exit(1)
year, month, date, selectedCity, selectedModel = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
# 받은 데이터 출력
print(f'Received data in Python: {year}, {month}, {date}, {selectedCity}, {selectedModel}')