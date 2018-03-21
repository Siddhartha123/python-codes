import time
from serial import Serial

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
