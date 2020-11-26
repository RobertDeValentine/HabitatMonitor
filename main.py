from gpiozero import *
import time
from twilio.rest import Client

from signal import pause

#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
relay = OutputDevice(20)
relay2 = OutputDevice(21)
relay.off()
relay2.off()




# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'AC4718a993b32ee4a3da3a5f4b0ad8856d'
auth_token = '43ef9aff6f02fd33c750146a7de19029'
client = Client(account_sid, auth_token)



#pir = MotionSensor(4)
count=0
mybool=False

while True:
    print("loop start")
    for message in client.messages.list():
        t = time.localtime()
        ct = time.strftime("%H:%M:%S" , t)
        print("attempt ",count,ct)
        print(message.from_)
        #message = client.messages.create(
        #                          from_='+12183664277',
        #                          body='sensor tripped'+str(count)+' at '+ct,
        #                          to='+15305037021'
        #                      )
    time.sleep(10)

    #print(message.sid)
    if mybool:
        relay.on()
        relay2.on()
    print("loop end")
