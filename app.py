# app.py
from flask import Flask, render_template, jsonify, request
# import mainsys
import asyncio
import time
from threading import Thread
import maintest
import database

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
  # mainsys.fan_speed_ctrl(mainsys.SLOW)
  return ("nothing")

@app.route('/fanmid')
def fanmid():
  print ("fanmid")
  # mainsys.fan_speed_ctrl(mainsys.MID)
  return ("nothing")

@app.route('/fanfull')
def fanfull():
  print ("fanfull")
  # mainsys.fan_speed_ctrl(mainsys.FULL)
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
  return jsonify(database.oneday_hours_mean)

@app.route('/days_graph', methods = ['GET'])
def days_graph():
  return jsonify(database.oneweek_days_mean)

@app.route('/stuff', methods = ['GET'])
def stuff():
  # dust=ardu.dust
  
  return jsonify(pm1=maintest.pm1, pm25= maintest.pm25, pm10=maintest.pm10, power_state=maintest.power_state, fan_speed=maintest.fan_speed)

if __name__=="__main__":
  # Thread(target=mainsys.Button_Ctrl).start()
  Thread(target=maintest.loop).start()
  app.run(debug=True)
  
  
  
  
  
  
  # host 등을 직접 지정하고 싶다면
  # app.run(host="0.0.0.0", port="5000", debug=True)