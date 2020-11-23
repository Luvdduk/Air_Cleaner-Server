from gpiozero import Button, RGBLED, DigitalOutputDevice, PWMOutputDevice
from colorzero import Color
from signal import pause
from threading import Thread
import time
import serial
from PMS7003 import PMS7003
import lcd_i2c as lcd
from configparser import ConfigParser
import pymysql


# 핀 설정
powersw = Button(24) # 전원버튼
fansw= Button(26) # 팬속버튼
fan_pwm = PWMOutputDevice(12) # 모터드라이버 pwm
fan_pin1 = DigitalOutputDevice(5) # 모터드라이버 IN1
fan_pin2 = DigitalOutputDevice(6) # 모터드라이버 IN2
led = RGBLED(16, 20, 21) # rgb led

# 초기 전원
power_state=0

#먼지센서 오브젝트
dustlib = PMS7003()

# 시리얼
Speed = 9600
SERIAL_PORT = '/dev/ttyUSB0'

# DB 연결
dust_db = pymysql.connect(
    user='luvdduk', 
    passwd='alrkd4535', 
    host='127.0.0.1', 
    db='air-cleaner', 
    charset='utf8'
)
cursor = dust_db.cursor(pymysql.cursors.DictCursor)

# 팬 on/off
ON = 1
OFF = 0

# 팬속
FULL = 1.0
MID = 0.65
SLOW = 0.3


# config.ini 가 있으면 로드 없으면 에러
try:
    conf = ConfigParser()# 설정파일 로드
    conf.read('config.ini')
    fan_state = conf['FAN']['fan_speed']# 팬속 로드
    print("설정파일 팬속도: %s" %fan_state)
except:
    print("설정파일 로드 오류")

if fan_state == "FULL":
    fan_pwm.value = 1.0
elif fan_state == "MID":
    fan_pwm.value = 0.65
elif fan_state == "SLOW":
    fan_pwm.value = 0.3
else:
    print("설정파일 로드 오류")

# lcd초기화
lcd.lcd_init()

# 버튼 제어
def Button_Ctrl():
    global power_state
    global fan_state
    powersw.when_pressed = powerctrl #파워버튼 누르면 실행
    fansw.when_pressed = fan_speedsw #팬속도 조정버튼 누르면 실행
    pause() # 누를때까지 대기



# 파워 꺼짐: 0, 켜짐: 1, 자동: 2
def powerctrl():
    global power_state
    if power_state == 0:
        power_state = 1
        print("전원켬")
        return
    if power_state == 1:
        power_state = 2
        print("자동모드로 변경")
        return
    if power_state == 2:
        power_state = 0
        print("전원끔")
        return

# 팬 스피드
def fan_speedsw():
    global fan_state
    if power_state == 1:

        if fan_state == "SLOW":
            fan_pwm.value = 0.65
            fan_state = "MID"
            print("팬속도: %f"%fan_pwm.value)
            return
        if fan_state == "MID":
            fan_pwm.value = 1
            fan_state = "FULL"
            print("팬속도: %f"%fan_pwm.value)
            return
        if fan_state == "FULL":
            fan_pwm.value = 0.3
            fan_state = "SLOW"
            print("팬속도: %f"%fan_pwm.value)
            return
    else:
        print("일반모드에서만 동작")


# 팬 on/off
def fan_power(state):
    if state:
        fan_pin1.on()
        fan_pin2.off()
    else:
        fan_pin1.off()
        fan_pin2.off()








def display_dust(duststate1, duststate2, duststate3):
    # 좋음
    if duststate3 <= 30 and (duststate1 + duststate2) <= 15 :
        lcd.lcd_string("     GOOD      ", lcd.LCD_LINE_1)
        led.color = Color("blue")
    # 보통
    elif  duststate3 <= 80 and (duststate1 + duststate2) <= 35:
        lcd.lcd_string("     NORMAL    ", lcd.LCD_LINE_1)
        led.color = Color("green")
        if power_state == 2:
            fan_pwm.value = 0.3
    # 나쁨
    elif duststate3 <= 150 and (duststate1 + duststate2) <= 75:
        lcd.lcd_string("      BAD      ", lcd.LCD_LINE_1)
        led.color = Color("yellow")
        if power_state == 2:
            fan_pwm.value = 0.65
    # 매우나쁨
    elif duststate3 > 150 or (duststate1 + duststate2) > 75:
        lcd.lcd_string("    VERY BAD   ", lcd.LCD_LINE_1)
        led.color = Color("red")
        if power_state == 2:
            fan_pwm.value = 1
    else:
        print("LCD표기 오류 or 먼지센서 데이터 오류")
    
    # pm1.0 표시
    lcd.lcd_string("PM1.0: %dug/m3 " %duststate1, lcd.LCD_LINE_2)
    powersw.wait_for_press(timeout=2)
    if powersw.is_pressed:
        return
    # pm2.5 표시
    lcd.lcd_string("PM2.5: %dug/m3 " %duststate2, lcd.LCD_LINE_2)
    powersw.wait_for_press(timeout=2)
    if powersw.is_pressed:
        return
    # pm10 표시
    lcd.lcd_string("PM10: %dug/m3  " %duststate3, lcd.LCD_LINE_2)
    # powersw.wait_for_press(timeout=1.5)
    # if powersw.is_pressed:
    #     return



# 메인루프
def loop():
    global power_state

    while True:
        # 먼지센서 동작
        ser = serial.Serial(SERIAL_PORT, Speed, timeout = 1)
        buffer = ser.read(1024)

        if(dustlib.protocol_chk(buffer)):
            data = dustlib.unpack_data(buffer)
            global pm1, pm25, pm10
            pm1 = int(data[dustlib.DUST_PM1_0_ATM])
            pm25 = int(data[dustlib.DUST_PM2_5_ATM])
            pm10 = int(data[dustlib.DUST_PM10_0_ATM])

            # db에 데이터 저장
            cursor.execute("INSERT INTO status(powerstate, PM1, PM25, PM10) VALUES ('%d', '%d','%d','%d')"%(power_state, pm1, pm25, pm10))
            dust_db.commit()

            print ("PMS 7003 dust data")
            print ("PM 1.0 : %d" % (pm1))
            print ("PM 2.5 : %d" % (pm25))
            print ("PM 10.0 : %d" % (pm10))
        else:
            print ("먼지센서 데이터 read 오류")
        
        # 전원 상태에 따른 동작
        if power_state == 0:
            print("전원꺼짐")
            fan_power(OFF)
            lcd.LCD_BACKLIGHT = 0x00
            lcd.lcd_string("   Power Off   ", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            led.off()
        if power_state == 1:
            print("전원켜짐")
            lcd.LCD_BACKLIGHT = 0x08
            lcd.lcd_string("   Power On    ", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            time.sleep(1)
            fan_power(ON)
            display_dust(pm1, pm25, pm10)
        if power_state == 2:
            print("자동모드")
            lcd.LCD_BACKLIGHT = 0x08
            lcd.lcd_string("   Auto Mode   ", lcd.LCD_LINE_1)
            lcd.lcd_string("", lcd.LCD_LINE_2)
            time.sleep(1)
            
            display_dust(pm1, pm25, pm10)
        time.sleep(1)



if __name__ == "__main__":
    # 쓰레딩
    Thread(target=Button_Ctrl).start()
    Thread(target=loop).start()