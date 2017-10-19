from serialCom import *

#serialInit()

def go(pwml,pwmr):
    sendByte(pwml)
    sendByte(pwmr)
