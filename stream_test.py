import requests
with open('http://192.168.43.1:8080/video/x.mjpeg','r') as f:
    requests.post('http://192.168.43.210',data=f)