import pandas as pd
from pandas import DataFrame
from pandas import Series
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

#데이터 불러오기(차례대로 지역별 전력거래량, 행정구역별 용도별 판매전력량, 지역별 신-재생에너지 생산량, 지역별 신-재생에너지 발전량, 지역별 부문별 소비실적)
energyTrading = pd.read_csv('지역별_전력거래량_20240502173346.csv', encoding='cp949')
salesPower = pd.read_csv('행정구역별_용도별_판매전력량_20240501132320.csv', encoding='cp949')
renewEnergyProduction = pd.read_csv('지역별_신·재생에너지_생산량_비재생폐기물_제외_20240501132022.csv', encoding='cp949')
renewEnergyGeneration = pd.read_csv('지역별_신·재생에너지_발전량_비재생폐기물_제외_20240501132124.csv', encoding='cp949')
comsumptPower = pd.read_csv('지역별_부문별_소비실적_20240501180330.csv', encoding='cp949')

# 지역별 전력거래량
#연도로 인덱스 설정
energyTrading2 = energyTrading.set_index('연도')
energyTrading3 = energyTrading2.T
#stack으로 데이터 처리
energyTrading4 = energyTrading3.stack().reset_index()
#2020, 2021, 2022년 데이터 전력거래량/전력거래량 비율로 구분
Divided1_et = energyTrading4.iloc[0:18].reset_index()
Divided2_et = energyTrading4.iloc[19:38].reset_index()
Divided3_et = energyTrading4.iloc[38:57].reset_index()
Divided4_et = energyTrading4.iloc[57:76].reset_index()
Divided5_et = energyTrading4.iloc[76:95].reset_index()
Divided6_et = energyTrading4.iloc[95:].reset_index()
#옆으로 데이터 2개 합치기
resultET_2020 = pd.concat([Divided1_et, Divided2_et], axis=1)
resultET_2021 = pd.concat([Divided3_et, Divided4_et], axis=1)
resultET_2022 = pd.concat([Divided5_et, Divided6_et], axis=1)
#열 이름 변경, 필요없는 데이터 삭제
dtZero1_et = resultET_2020.set_axis(['index', '연도', '지역', '전력거래량(GWh)', '3', '1', '2', '전력거래량 비율(%)'], axis=1)
dtZero2_et = dtZero1_et.drop(['1','2','3'], axis=1)
dtZero3_et = dtZero2_et.drop(dtZero2_et.index[[18, 0]])
#부산 데이터 처리
dtZero3_et.loc['18'] = ['18.0', '2021', '부산','-1', '7.2']
#데이터 타입 설정
dtZero3_et['연도_datetime'] = pd.to_datetime(dtZero3_et['연도']).dt.year
dtZero3_et['전력거래량(GWh)']= dtZero3_et['전력거래량(GWh)'].astype(int) 
dtZero3_et['전력거래량 비율(%)'] = dtZero3_et['전력거래량 비율(%)'].astype(float)
dtZero4_et = dtZero3_et.set_index('index')
#2021 자료 처리
dtOne1_et = resultET_2021.set_axis(['index', '연도', '지역', '전력거래량(GWh)', '1', '2', '3', '전력거래량 비율(%)'], axis=1)
dtOne2_et = dtOne1_et.drop(['1','2','3'], axis=1)
dtOne3_et = dtOne2_et.drop(dtOne2_et.index[0])
dtOne3_et['연도_datetime'] = pd.to_datetime(dtOne3_et['연도']).dt.year
dtOne3_et['전력거래량(GWh)']= dtOne3_et['전력거래량(GWh)'].astype(int) 
dtOne3_et['전력거래량 비율(%)'] = dtOne3_et['전력거래량 비율(%)'].astype(float)
dtOne4_et = dtOne3_et.set_index('index')
#2022 자료 처리
dtTwo1_et = resultET_2022.set_axis(['index', '연도', '지역', '전력거래량(GWh)', '1', '2', '3', '전력거래량 비율(%)'], axis=1)
dtTwo2_et = dtTwo1_et.drop(['1','2','3'], axis=1)
dtTwo3_et = dtTwo2_et.drop(dtTwo2_et.index[0])
dtTwo3_et['연도_datetime'] = pd.to_datetime(dtTwo3_et['연도']).dt.year
dtTwo3_et['전력거래량(GWh)']= dtTwo3_et['전력거래량(GWh)'].astype(int) 
dtTwo3_et['전력거래량 비율(%)'] = dtTwo3_et['전력거래량 비율(%)'].astype(float)
dtTwo4_et = dtTwo3_et.set_index('index')
#전체 통합
totalEnergyTrading = pd.concat([dtZero4_et, dtOne3_et, dtTwo3_et])
totalEnergyTrading2 = totalEnergyTrading.reset_index()
totalEnergyTrading3 = totalEnergyTrading2.drop(['level_0','index'], axis=1)
column_seq2 = ['지역', '연도','전력거래량(GWh)','전력거래량 비율(%)','연도_datetime']
totalEnergyTrading4 = totalEnergyTrading3[column_seq2]
#print(totalEnergyTrading4)
#totalEnergyTrading4.to_csv('result_EnergyTrading_V2.csv')

# 행정구역별 용도별 판매전력량
#필요없는 열 제거
salesPower2 = salesPower.drop('용도별(2)', axis=1)
#행과 열을 바꾸고, 각각 연도별 합계 제거
salesPower3 = salesPower2.T.drop(['2020', '2021', '2022'])
#필요없는 제조업 10개 상세항목 제거
salesPower4 = salesPower3.iloc[1:, 0:8]
#행의 이름 변경
salesPower5 = salesPower4.set_axis(['지역', '합계', '가정용', '공공용', '서비스업', '농림어업' , '광업', '제조업'], axis=1)
#인덱스 행으로 바꾸기
salesPower6 = salesPower5.reset_index()
#다시 행의 위치 변경
column_seq = ['지역', 'index','가정용','공공용','서비스업','농림어업','광업','제조업', '합계']
salesPower7 = salesPower6[column_seq]
#또 다시 행의 이름 변경
salesPower8 = salesPower7.set_axis(['지역', '연도', '가정용', '공공용', '서비스업', '농림어업', '광업', '제조업', '합계'], axis=1)
#개성 데이터 없으므로 제거
cond1 = (salesPower8['지역'] == '개성')
salesPower9 = salesPower8.loc[~cond1]
#데이터 타입 설정
#salesPower9['연도_datetime'] = pd.to_datetime(salesPower9['연도']).dt.year
#salesPower9[['가정용', '공공용', '서비스업', '농림어업', '광업', '제조업', '합계']] = salesPower9[['가정용', '공공용', '서비스업', '농림어업', '광업', '제조업', '합계']].astype(int) 

# 지역별 신-재생에너지 생산량
#필요없는 데이터 제거
rep1 = renewEnergyProduction.drop('에너지원별(1)', axis=1)
rep2 = rep1.drop(rep1.index[[7, 8, 10, 11, 13, 14, 19, 20, 21, 22, 23, 24, 25, 26, 27,28, 29, 30, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42]])
rep3 = rep2.drop('에너지원별(3)', axis=1)
rep4 = rep3.set_index('에너지원별(2)')
rep5 = rep4.T
rep6 = rep5.reset_index()
#행의 이름 변경
rep7 = rep6.set_axis(['연도', '지역', '소계', '재생에너지', '신에너지', '공급비중', '태양열 (toe)', 
                    '태양광 (toe)', '풍력 (toe)', '수력 (toe)', '해양 (toe)', '지열 (toe)', 
                    '수열 (toe)', '바이오 (toe)', '폐기물 (toe)', '연료전지 (toe)'], axis=1)
#결측값 -1로 변경, 해양 데이터는 결측값이 많아서 제외할지 생각 중
rep8 = rep7.replace('-', '-1')
#데이터 타입 설정
rep8['연도_datetime'] = pd.to_datetime(rep8['연도']).dt.year
"""rep8[['소계', '재생에너지', '신에너지', '태양열 (toe)', '태양광 (toe)', '풍력 (toe)', '수력 (toe)', 
        '해양 (toe)', '지열 (toe)', '수열 (toe)', '바이오 (toe)', '폐기물 (toe)', '연료전지 (toe)']]= rep8[['소계', 
        '재생에너지', '신에너지', '태양열 (toe)', '태양광 (toe)','풍력 (toe)', '수력 (toe)', '해양 (toe)', '지열 (toe)', 
        '수열 (toe)', '바이오 (toe)','폐기물 (toe)', '연료전지 (toe)']].astype(int)"""
rep8['공급비중'] = rep8['공급비중'].astype(float)
#rep8.to_csv('result_RenewEnergyProduction.csv')

# 지역별 신-재생에너지 발전량
#필요없는 데이터 제거
reg1 = renewEnergyGeneration.drop('에너지원별(1)', axis=1)
reg2 = reg1.drop(reg1.index[[2,3, 5, 6, 8, 9, 12, 13, 15, 16, 18, 19, 21]])
reg3 = reg2.drop(labels=range(23,49), axis=0)
reg4 = reg3.drop(labels=range(50,68), axis=0)
reg5 = reg4.drop(reg4.index[[12, 13, 15]])
reg6 = reg5.drop(['에너지원별(2)', '에너지원별(3)', '에너지원별(4)'], axis=1)
reg7 = reg6.T.reset_index()
#행의 이름 변경
reg8 = reg7.set_axis(['연도', '지역', '소계', '재생에너지', '신에너지', '발전비중', '태양광 (MWh)', 
                    '풍력 (MWh)', '수력 (MWh)', '해양 (MWh)', '바이오 (MWh)', '폐기물 (MWh)', 
                    '연료전지 (MWh)', 'IGCC (MWh)'], axis=1)
#결측값 -1로 변경, 해양 데이터는 결측값이 많아서 제외할지 생각 중
reg9 = reg8.replace('-', '-1')
#데이터 타입 설정
reg9['연도_datetime'] = pd.to_datetime(reg9['연도']).dt.year
"""reg9[['소계', '재생에너지', '신에너지', '태양광 (MWh)', '풍력 (MWh)', '수력 (MWh)', '해양 (MWh)', 
    '바이오 (MWh)', '폐기물 (MWh)', '연료전지 (MWh)', 'IGCC (MWh)']]= reg9[['소계', '재생에너지', 
    '신에너지', '태양광 (MWh)', '풍력 (MWh)', '수력 (MWh)', '해양 (MWh)',  '바이오 (MWh)', '폐기물 (MWh)', 
    '연료전지 (MWh)', 'IGCC (MWh)']].astype(int)"""
reg9['발전비중'] = reg9['발전비중'].astype(float)
#reg9.to_csv('result_RenewEnergyGeneration.csv')

# 지역별 부문별 소비실적
#지역별 전력거래량과 같은 방식으로 연도로 구분해 합침
comsumptPower2 = comsumptPower.set_index('연도').T
comsumptPower3 = pd.DataFrame(comsumptPower2.stack().reset_index())
Divided1_cp = comsumptPower3.iloc[1:19].reset_index()
Divided2_cp = comsumptPower3.iloc[20:38].reset_index()
Divided3_cp = comsumptPower3.iloc[39:57].reset_index()
Divided4_cp = comsumptPower3.iloc[58:76].reset_index()
Divided5_cp = comsumptPower3.iloc[77:95].reset_index()
result_2020 = pd.concat([Divided1_cp, Divided2_cp, Divided3_cp, Divided4_cp, Divided5_cp], axis= 1)
dtZero1_cp = result_2020.set_axis(['1', '연도', '지역', '총계', '2', '3', '4', '산업', '5', '6', '7', '건물', '8', '9', '10', '수송', '11', '12', '13', '발전'], axis=1)
dtZero2_cp = dtZero1_cp.drop(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'], axis=1)

Divided6_cp = comsumptPower3.iloc[115:133].reset_index()
Divided7_cp = comsumptPower3.iloc[134:152].reset_index()
Divided8_cp = comsumptPower3.iloc[153:171].reset_index()
Divided9_cp = comsumptPower3.iloc[172:190].reset_index()
Divided10_cp = comsumptPower3.iloc[191:209].reset_index()
result_2021 = pd.concat([Divided6_cp, Divided7_cp, Divided8_cp, Divided9_cp, Divided10_cp], axis= 1)
dtOne1_cp = result_2020.set_axis(['1', '연도', '지역', '총계', '2', '3', '4', '산업', '5', '6', '7', '건물', '8', '9', '10', '수송', '11', '12', '13', '발전'], axis=1)
dtOne2_cp = dtOne1_cp.drop(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'], axis=1)

Divided11_cp = comsumptPower3.iloc[229:247].reset_index()
Divided12_cp = comsumptPower3.iloc[248:266].reset_index()
Divided13_cp = comsumptPower3.iloc[267:285].reset_index()
Divided14_cp = comsumptPower3.iloc[286:304].reset_index()
Divided15_cp = comsumptPower3.iloc[305:323].reset_index()
result_2022 = pd.concat([Divided11_cp, Divided12_cp, Divided13_cp, Divided14_cp, Divided15_cp], axis= 1)
dtTwo1_cp = result_2022.set_axis(['1', '연도', '지역', '총계', '2', '3', '4', '산업', '5', '6', '7', '건물', '8', '9', '10', '수송', '11', '12', '13', '발전'], axis=1)
dtTwo2_cp = dtTwo1_cp.drop(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'], axis=1)

totalComsumptPower = pd.concat([dtZero2_cp, dtOne2_cp, dtTwo2_cp])
totalComsumptPower2 = totalComsumptPower.reset_index()
totalComsumptPower3 = totalComsumptPower2.drop(['index'], axis=1)
totalComsumptPower4 = totalComsumptPower3.replace('X', '-1')
totalComsumptPower5 = totalComsumptPower4.replace('-', '-1')
totalComsumptPower5['연도_datetime'] = pd.to_datetime(totalComsumptPower5['연도']).dt.year
totalComsumptPower5[['총계', '산업', '건물', '수송', '발전']] = totalComsumptPower5[['총계', '산업', '건물', '수송', '발전']].astype(int)
print(totalComsumptPower5.info())
#totalComsumptPower5.to_csv('result_ComsumptPower.csv')

