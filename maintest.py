import serial
import time
import sqlite3



# port= "/dev/ttyACM1"
# serialArduino = serial.Serial(port, 9600, timeout=1)
# serialArduino.flushInput()
# dust=0
# state=0

# def loop():
#     global dust
#     global state


#     while True:
#         if serialArduino.in_waiting > 0:

#             dust = serialArduino.readline().decode('utf-8').rstrip()
#             if "PowerOn" in dust :
#                 state=1
#                 print("전원 켜짐" + state)

#             elif "PowerOff" in dust :
#                 state=0
#                 print("전원 꺼짐" + state)

#             else:
#                 print(dust)


    # time.sleep(1)

power_state=1
fan_state="MID"


pm1=0
pm25=0
pm10=0
def loop():
    global pm1, pm25, pm10, power_state
    while True:
        pm1 += 1
        pm25 += 2
        pm10 += 3
        # print("파워상태: %d" %power_state)
        # print(pm1)
        # print(pm25)
        # print(pm10)
        time.sleep(3)



# def poweron():
#     serialArduino.write(b"1\n")

# def poweroff():
#     serialArduino.write(b"0\n")

if __name__ == "__main__":
    loop()