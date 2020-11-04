from gpiozero import Button, LED, RGBLED, OutputDevice, DigitalOutputDevice, PWMOutputDevice
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
fan_pin2 = DigitalOutputDevice(6) # 모터드라이버 IN1
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
    # 설정파일 로드
    conf = ConfigParser()
    conf.read('config.ini')
    # 팬속 로드
    fanspeed = conf['FAN']['fan_speed']
    fanspeed = float(fanspeed)
    print("설정파일 팬속도: %f" %fanspeed)
    fan_pwm.value = fanspeed
except:
    print("설정파일 로드 오류")

if fanspeed == FULL:
    fan_state = "FULL"
elif fanspeed == MID:
    fan_state = "MID"
elif fanspeed == SLOW:
    fan_state = "SLOW"
else:
    print("설정파일 로드 오류")


# lcd초기화
lcd.lcd_init()



# 버튼 제어
def Button_Ctrl():
    global power_state
    powersw.when_pressed = powerctrl
    fansw.when_pressed = fan_speedsw
    pause()


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

# 팬 on/off
def fan_power(state):
    if state:
        fan_pin1.on()
        fan_pin2.off()
    else:
        fan_pin1.off()
        fan_pin2.off()

# 팬 스피드
def fan_speedsw():
    if fan_state == "SLOW":
        fan_speed_ctrl(MID)
        return
    if fan_state == "MID":
        fan_speed_ctrl(FULL)
        return
    if fan_state == "FULL":
        fan_speed_ctrl(SLOW)
        return

def fan_speed_ctrl(speed):
    if speed == SLOW:
        fan_pwm.value = speed
        # conf['FAN']['fan_speed'] = speed
        fan_state = "MID"
        print("팬속도 : 느리게")
        return
    elif speed == MID:
        fan_pwm.value = speed
        # conf['FAN']['fan_speed'] = speed
        fan_state = "MID"
        print("팬속도 : 중간")
        return
    elif speed == FULL:
        fan_pwm.value = speed
        # conf['FAN']['fan_speed'] = speed
        fan_state = "FULL"
        print("팬속도 : 최고")
        return





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
            fan_speed_ctrl(SLOW)
    # 나쁨
    elif duststate3 <= 150 and (duststate1 + duststate2) <= 75:
        lcd.lcd_string("      BAD      ", lcd.LCD_LINE_1)
        led.color = Color("yellow")
        if power_state == 2:
            fan_speed_ctrl(MID)
    # 매우나쁨
    elif duststate3 > 150 or (duststate1 + duststate2) > 75:
        lcd.lcd_string("    VERY BAD   ", lcd.LCD_LINE_1)
        led.color = Color("red")
        if power_state == 2:
            fan_speed_ctrl(FULL)
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

            global pm1
            global pm25
            global pm10
            pm1 = int(data[dustlib.DUST_PM1_0_ATM])
            pm25 = int(data[dustlib.DUST_PM2_5_ATM])
            pm10 = int(data[dustlib.DUST_PM10_0_ATM])
            print ("PMS 7003 dust data")
            print ("PM 1.0 : %d" % (pm1))
            print ("PM 2.5 : %d" % (pm25))
            print ("PM 10.0 : %d" % (pm10))
        else:
            print ("data read Err")
        
        # db에 먼지농도 저장
        cursor.execute("INSERT INTO status(powerstate, PM1, PM25, PM10) VALUES ('%d', '%d','%d','%d')"%(power_state, pm1, pm25, pm10))
        dust_db.commit()
        
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
            if pm10 <= 30 and (pm1 + pm25) <= 15 :
                fan_power(OFF)
            else:
                fan_power(ON)
            
            display_dust(pm1, pm25, pm10)
        # powersw.wait_for_press(timeout=2)
        time.sleep(1)



if __name__ == "__main__":
    # 쓰레딩
    Thread(target=Button_Ctrl).start()
    Thread(target=loop).start()
    
