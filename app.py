# app.py
from flask import Flask, render_template, jsonify, request
import time
from threading import Thread
import database
import pandas as pd
import json

#Flask 객체 인스턴스 생성
app = Flask(__name__)

state = {
  "power_on" : False,
  "power_off" : False,
  "auto_mode" : False,
  "fan_slow" : False,
  "fan_mid" : False,
  "fan_full" : False
}
power_state = 0
fan_state = 0
pm1 = 0
pm25 = 0
pm10 = 0



@app.route('/') # index.html 렌더링
def index():
  return render_template('index.html')

@app.route('/graph') # graph.html 렌더링
def graph():
  return render_template('graph.html')

@app.route('/dustinfo') # dustinfo.html 렌더링
def dustinfo():
  return render_template('dustinfo.html')

@app.route('/fan_speed') # fan_speed.html 렌더링
def fan_speed():
  return render_template('fan_speed.html')

@app.route('/info') # info.html 렌더링
def info():
  return render_template('info.html')

@app.route('/poweron') # main 전원변수 0으로
def poweron():
  global state
  print ("poweron")
  state["power_on"] = True
  return ("nothing")

@app.route('/poweroff') # main 전원변수 1로
def poweroff():
  global state
  print ("poweroff")
  state['power_off'] = True
  return ("nothing")

@app.route('/modeauto') # main 전원변수 2로
def modeauto():
  global state
  print ("automode")
  state['auto_mode'] = True
  return ("nothing")

@app.route('/fanslow') # main 팬 PWM Value값 0.3으로 변경
def fanslow():
  global state
  print ("fanslow")
  state['fan_slow'] = True
  return ("nothing")

@app.route('/fanmid') # main 팬 PWM Value값 0.65으로 변경
def fanmid():
  global state
  print ("fanmid")
  state['fan_mid'] = True
  return ("nothing")

@app.route('/fanfull') # main 팬 PWM Value값 1로 변경
def fanfull():
  global state
  print ("fanfull")
  state['fan_full'] = True
  return ("nothing")


@app.route('/hours_graph', methods = ['GET']) # 1시간별 데이터 반환, GET요청만 허용
def hours_graph():
  #database.py의 list변수를 데이터프레임으로 변환
  df = pd.DataFrame(database.oneday_hours_mean())
  df = df.set_index("hours") # index를 Hours 변수로 지정 (1~24)
  return df.to_json() # json타입으로 변환하여 리턴

@app.route('/days_graph', methods = ['GET']) # 1일별 데이터 반환, GET요청만 허용
def days_graph():
  #database.py의 list변수를 데이터프레임으로 변환
  df = pd.DataFrame(database.oneweek_days_mean())
  df = df.set_index("days_ago")# index를 Days_ago 변수로 지정 (1~7)
  return df.to_json() # json타입으로 변환하여 리턴




@app.route('/receivedata', methods = ['GET', 'POST'])
def receivedata():
  global data, power_state, fan_state, pm1, pm25, pm10
  data = request.get_json(force=True)
  print(data)
  # data =  json.load(data)
  power_state = data["power_state"]
  fan_state = data["fan_state"]
  pm1 = data["pm1"]
  pm25 = data["pm25"]
  pm10 = data["pm10"]

  if (state["power_on"] == True) & (power_state == 1):
    state["power_on"] = False
  if (state["power_off"] == True) & (power_state == 0):
    state["power_off"] = False
  if (state["auto_mode"] == True) & (power_state == 2):
    state["auto_mode"] = False
  if (state["fan_slow"] == True) & (fan_state == "SLOW"):
    state["fan_slow"] = False
  if (state["fan_mid"] == True) & (fan_state == "MID"):
    state["fan_mid"] = False
  if (state["fan_full"] == True) & (fan_state == "FULL"):
    state["fan_full"] = False
  return ("data received")

@app.route('/senddata', methods = ['GET', 'POST'])
def senddata():
  global state
  return jsonify(state)


@app.route('/stuff', methods = ['GET']) # 실시간 데이터 반환, GET요청만 허용
def stuff():
  print(state)
  try:
    return jsonify(data)
  except:
    return ("no data")



if __name__=="__main__":
  app.run(host="0.0.0.0", debug=True) # 쓰레드2
  
  
  # host 등을 직접 지정하고 싶다면
  # app.run(host="0.0.0.0", port="5000", debug=True)