import os
import pandas as pd
import pymysql

# pandas 데이터 유형을 MySQL 데이터 유형으로 변환하는 함수
def map_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_object_dtype(dtype):
        return "TEXT"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    else:
        return "TEXT"

# 테이블 이름과 열 이름을 안전하게 처리하는 함수
def safe_column_name(name):
    return f"`{name}`"

def create_table_from_csv(cursor, table_name, df):
    # 데이터 유형 매핑
    column_definitions = ", ".join([f"{safe_column_name(col)} {map_dtype(dtype)}" for col, dtype in zip(df.columns, df.dtypes)])
    # 테이블 생성 쿼리
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {safe_column_name(table_name)} (
        {column_definitions}
    )
    '''
    cursor.execute(create_table_query)

def insert_data_from_csv(cursor, table_name, df):
    # 데이터 삽입 쿼리
    cols = "`,`".join([str(i) for i in df.columns.tolist()])
    for i, row in df.iterrows():
        sql = f"INSERT INTO `{table_name}` (`{cols}`) VALUES {tuple(row)}"
        cursor.execute(sql)


fileNameList = ['result_EnergyConsumption', 'result_EnergyGeneration', 'result_EnergyTrading', 'result_RenewEnergyGeneration', 'result_RenewEnergyProduction', 'result_SalesPower']

for fileName in fileNameList:
    # MySQL 연결 설정
    conn = pymysql.connect(host='localhost', user='user1', password="12345", db=fileName, charset='utf8')
    cursor = conn.cursor()

    # CSV 파일이 저장된 디렉토리 경로 설정
    csv_directory = './data_csv/' + fileName

    # CSV 파일 목록 가져오기
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

    for csv_file in csv_files:
        # CSV 파일의 데이터프레임 생성
        df = pd.read_csv(os.path.join(csv_directory, csv_file))

        # 파일 이름에서 테이블 이름 생성
        table_name = os.path.splitext(csv_file)[0]

        # 테이블 생성
        create_table_from_csv(cursor, table_name, df)

        # 데이터 삽입
        insert_data_from_csv(cursor, table_name, df)

    # 커밋 및 연결 종료
    conn.commit()
    conn.close()
