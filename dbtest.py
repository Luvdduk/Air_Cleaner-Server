import pymysql
import datetime
import json
import pandas as pd


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
left24h = NowDate - datetime.timedelta(days=3)
# NowDate = datetime.datetime.strftime(NowDate, '%Y-%m-%d %H:%M:%S')
# left24h = datetime.datetime.strftime(left24h, '%Y-%m-%d %H:%M:%S')
print("%s 부터 %s 까지"%(left24h, NowDate))

cursor.execute("SELECT * FROM status WHERE TIMESTAMP(timestamp) BETWEEN '%s' AND '%s';"%(left24h, NowDate))
df = cursor.fetchall()
df = pd.DataFrame(df)


def get_1h_mean(start_time):
    end_time = start_time + datetime.timedelta(hours=1)
    one_hour = (df['timestamp']> start_time) & (df['timestamp']< end_time)
    df_1h = df.loc[one_hour]
    mean_1h = { "time": start_time, "PM1.0": df_1h['PM1'].mean(), "PM2.5": df_1h['PM25'].mean(), "PM10": df_1h['PM10'].mean()}
    return mean_1h



print(get_1h_mean(datetime.datetime(2020,11,5,4,47,0)))











# df47m = (result['timestamp']> '2020-11-05 04:47:00') & (result['timestamp']< '2020-11-05 04:48:00')


# print(result)
# print(result.loc[df47m])
# print(result.loc[(result['timestamp']> '2020-11-05 04:47:00') & (result['timestamp']< '2020-11-05 04:48:00')])

# m47=result.loc[df47m]
# mmean = m47['PM1'].mean()
# print(mmean)






















