import serial
def serialInit():
    COM=raw_input("Enter COM Port to open\n")
    global robot
    robot=serial.Serial("COM"+COM,baudrate=115200,timeout=1)

def sendByte(x):
    robot.write(chr(x))

def m(l,r):
    robot.write('-')
    robot.write(l)
    robot.write('+')
    robot.write(r)
