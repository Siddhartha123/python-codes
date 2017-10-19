import time
from serial import Serial

def sendCmd(pwmR,pwmL):
    if(sendByte(pwmR)):
        return sendByte(pwmL)
    else:
        return False
def sendByte(b):
    global robot
    robot.write(b)
    while robot.inWaiting()==0:
        pass
    if robot.read()==b:
        print b
        return True
    else:
        return False
COM=raw_input("Enter COM Port to open\n")
robot=Serial("COM"+COM,baudrate=115200,timeout=1)
time.sleep(1)
print time.time()
sendCmd('a','b')
print time.time()