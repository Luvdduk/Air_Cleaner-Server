import pymysql
import datetime
import json
import pandas as pd
from random import randrange as rd


# DB 연결
dust_db = pymysql.connect(
    user='luvdduk', 
    passwd='alrkd4535', 
    host='127.0.0.1', 
    db='air-cleaner', 
    charset='utf8'
)
dust_db2 = pymysql.connect(
    user='luvdduk', 
    passwd='alrkd4535', 
    host='127.0.0.1', 
    db='air-cleaner', 
    charset='utf8'
)


def oneday_hours_mean():
    cursor1 = dust_db.cursor(pymysql.cursors.DictCursor)
    NowDate = datetime.datetime.now()
    left24h = NowDate - datetime.timedelta(days=1)
    cursor1.execute("SELECT * FROM status WHERE TIMESTAMP(timestamp) BETWEEN '%s' AND '%s';"%(left24h, NowDate))
    df = cursor1.fetchall()
    df = pd.DataFrame(df)
    hour = 1
    hours_mean = list()
    while hour <= 24:
        if hour > 0:
            start_time = datetime.datetime.now() - datetime.timedelta(hours=hour)
            end_time = start_time + datetime.timedelta(hours=1)
            one_hour = (df['timestamp']>= start_time) & (df['timestamp']< end_time)
            df_1h = df.loc[one_hour]
            mean_1h = { "hours" : hour, "time": start_time.strftime("%Y-%m-%d %H:%M:%S"), "pm1": df_1h['PM1'].mean(), "pm25": df_1h['PM25'].mean(), "pm10": df_1h['PM10'].mean()}
        hours_mean.append(mean_1h)
        hour += 1
    # hours_mean = json.dumps(hours_mean)
    return hours_mean


def oneweek_days_mean():
    cursor = dust_db2.cursor(pymysql.cursors.DictCursor)
    NowDate = datetime.datetime.now()
    left7d = NowDate - datetime.timedelta(days=8)
    cursor.execute("SELECT * FROM status WHERE TIMESTAMP(timestamp) BETWEEN '%s' AND '%s';"%(left7d, NowDate))
    df = cursor.fetchall()
    df = pd.DataFrame(df)
    days = 0
    days_mean = list()
    while days <= 7:
        day = datetime.date.today() - datetime.timedelta(days=days)
        day = datetime.datetime.combine(day, datetime.time())
        one_day = (df['timestamp']>= day) & (df['timestamp']< (day + datetime.timedelta(hours=24)))
        df_1d = df.loc[one_day]
        mean_1h = {"days_ago": days, "date":day.strftime("%Y-%m-%d"), "pm1": df_1d['PM1'].mean(), "pm25": df_1d['PM25'].mean(), "pm10": df_1d['PM10'].mean()}
        days_mean.append(mean_1h)
        days += 1
    # days_mean = json.dumps(days_mean)
    return days_mean



# def get_1h_mean(start_time):
#     end_time = start_time + datetime.timedelta(hours=1)
#     one_hour = (df['timestamp']> start_time) & (df['timestamp']< end_time)
#     df_1h = df.loc[one_hour]
#     mean_1h = { "time": start_time, "PM1.0": df_1h['PM1'].mean(), "PM2.5": df_1h['PM25'].mean(), "PM10": df_1h['PM10'].mean()}
#     return mean_1h

# # n시간전의 1시간동안의 데이터 평균(현재시간 기준) 반환
# def get_hours_ago_mean(t_hours):
#     if t_hours > 0:
#         start_time = datetime.datetime.now() - datetime.timedelta(hours=t_hours)
#         end_time = start_time + datetime.timedelta(hours=1)
#         one_hour = (df['timestamp']>= start_time) & (df['timestamp']< end_time)
#         df_1h = df.loc[one_hour]
#         mean_1h = { "hours" : t_hours, "time": start_time, "PM1.0": df_1h['PM1'].mean(), "PM2.5": df_1h['PM25'].mean(), "PM10": df_1h['PM10'].mean()}
#         return mean_1h
#     else:
#         print("1이상 가능")

# # n일전의 1일간의 데이터 평균(해당일 00:00~24:00) 반환
# def get_days_ago_mean(t_days):
#     if t_days > 0:
#         day = datetime.date.today() - datetime.timedelta(days=t_days)
#         one_day = (df['timestamp']== day)
#         df_1d = df.loc[one_day]
#         mean_1h = { "hours" : t_days, "day": day, "PM1.0": df_1d['PM1'].mean(), "PM2.5": df_1d['PM25'].mean(), "PM10": df_1d['PM10'].mean()}
#         return mean_1h
#     elif t_days == 0:
#         day = datetime.date.today()
#         one_day = (df['timestamp']== day)
#         df_1d = df.loc[one_day]
#         mean_1h = { "hours" : t_days, "day": day, "PM1.0": df_1d['PM1'].mean(), "PM2.5": df_1d['PM25'].mean(), "PM10": df_1d['PM10'].mean()}
#         return mean_1h
#     else:
#         print("1이상 가능")








# print(get_1h_mean(datetime.datetime(2020,11,5,4,47,0)))











# df47m = (result['timestamp']> '2020-11-05 04:47:00') & (result['timestamp']< '2020-11-05 04:48:00')


# print(result)
# print(result.loc[df47m])
# print(result.loc[(result['timestamp']> '2020-11-05 04:47:00') & (result['timestamp']< '2020-11-05 04:48:00')])

# m47=result.loc[df47m]
# mmean = m47['PM1'].mean()
# print(mmean)


def dummy_week():
    a = 0
    while a<8:
        start_date = datetime.datetime(2020,11,13,14,0) + datetime.timedelta(days=a)
        cursor.execute("INSERT INTO status(timestamp, powerstate, PM1, PM25, PM10) VALUES ('%s','%d','%d','%d','%d')"%(start_date, 1, rd(3,11), rd(5,21), rd(9,41)))
        dust_db.commit()
        a += 1

def dummy_day():
    a = 0
    while a<24:
        start_date = datetime.datetime(2020,11,19,0,0) + datetime.timedelta(hours=a)
        cursor.execute("INSERT INTO status(timestamp, powerstate, PM1, PM25, PM10) VALUES ('%s','%d','%d','%d','%d')"%(start_date, 1, rd(3,11), rd(5,21), rd(9,41)))
        dust_db.commit()
        a += 1








if __name__ == "__main__":
    # print(oneweek_days_mean())
    print(oneday_hours_mean())
    # dummy_day()


















