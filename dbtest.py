import pymysql
import datetime
import json


# DB 연결
dust_db = pymysql.connect(
    user='luvdduk', 
    passwd='alrkd4535', 
    host='127.0.0.1', 
    db='air-cleaner', 
    charset='utf8'
)
cursor = dust_db.cursor(pymysql.cursors.DictCursor)



NowDate = datetime.datetime.now()
left24h = NowDate - datetime.timedelta(days=1)
# NowDate = datetime.datetime.strftime(NowDate, '%Y-%m-%d %H:%M:%S')
# left24h = datetime.datetime.strftime(left24h, '%Y-%m-%d %H:%M:%S')
print("%s 부터 %s 까지"%(left24h, NowDate))

cursor.execute("SELECT * FROM status WHERE TIMESTAMP(timestamp) BETWEEN '%s' AND '%s';"%(left24h, NowDate))
result = cursor.fetchall()
print(result['timestamp': '2020-11-05 04:47:10'])



