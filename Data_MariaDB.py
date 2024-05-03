import pymysql

conn = pymysql.connect(host='localhost', user='user1', password="12345", port=3306, charset='utf8')
cursor = conn.cursor()

sql = 'DROP DATABASE test1'

cursor.execute(sql)
conn.commit()
conn.close()