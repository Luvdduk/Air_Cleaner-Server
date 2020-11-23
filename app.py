# app.py
from flask import Flask, render_template, jsonify, request
# import main
import time
from threading import Thread
import maintest
import database
import pandas as pd

#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
  return render_template('index.html')

@app.route('/poweron')
def poweron():
  print ("poweron")
  maintest.power_state = 1
  return ("nothing")

@app.route('/poweroff')
def poweroff():
  print ("poweroff")
  maintest.power_state = 0
  return ("nothing")

@app.route('/modeauto')
def modeauto():
  print ("automode")
  maintest.power_state = 2
  return ("nothing")

@app.route('/fanslow')
def fanslow():
  print ("fanslow")
  # main.fan_pwm.value = 0.3
  # main.fan_state = "SLOW"
  return ("nothing")

@app.route('/fanmid')
def fanmid():
  print ("fanmid")
  # main.fan_pwm.value = 0.65
  # main.fan_state = "MID"
  return ("nothing")

@app.route('/fanfull')
def fanfull():
  print ("fanfull")
  # main.fan_pwm.value = 1.0
  # main.fan_state = "FULL"
  return ("nothing")

@app.route('/graph')
def graph():
  return render_template('graph.html')

@app.route('/dustinfo')
def dustinfo():
  return render_template('dustinfo.html')

@app.route('/fan_speed')
def fan_speed():
  return render_template('fan_speed.html')


@app.route('/hours_graph', methods = ['GET'])
def hours_graph():
  df = pd.DataFrame(database.oneday_hours_mean())
  df = df.set_index("hours")
  print(df)
  return df.to_json()

@app.route('/days_graph', methods = ['GET'])
def days_graph():
  df = pd.DataFrame(database.oneweek_days_mean())
  df = df.set_index("days_ago")
  print(df)
  return df.to_json()

@app.route('/stuff', methods = ['GET'])
def stuff():
  return jsonify(pm1=maintest.pm1, pm25= maintest.pm25, pm10=maintest.pm10, power_state=maintest.power_state, fan_speed=maintest.fan_state)
  # return jsonify(pm1=main.pm1, pm25= main.pm25, pm10=main.pm10, power_state=main.power_state, fan_speed=main.fan_state)

if __name__=="__main__":
  # Thread(target=main.Button_Ctrl).start() # 쓰레드0
  Thread(target=maintest.loop).start() # 쓰레드1
  app.run(host="0.0.0.0", debug=True) # 쓰레드2
  
  
  # host 등을 직접 지정하고 싶다면
  # app.run(host="0.0.0.0", port="5000", debug=True)