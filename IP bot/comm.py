import requests

url='http://192.168.43.47'
def sendCommand(left,right,stat):

    data={'pwml':chr(left),'pwmr':chr(right),'stat':stat,'d':chr(50)}
    headers = {'content-type': 'application/json'}
    r=requests.get(url,data=data,headers=headers)
    if r.status_code==200:
        print r.text
        return True
