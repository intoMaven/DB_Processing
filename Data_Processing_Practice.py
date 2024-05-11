import numpy as np

#파일 불러오기
path = 'C:/Users/yesye/OneDrive/바탕 화면/데이터베이스/프로젝트 자료/데이터베이스(raw data)/지역별_전력거래량_20240430113715.csv'
data = np.loadtxt(path, skiprows=1, delimiter=',', usecols=(0,1,2), dtype='str')
#파일 확인하기
print(data)