from serialCom import *
serialInit()
while True:
    r=int(raw_input("right speed:"))
    sendByte(r)
