from gpiozero import *
import time


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers


from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACb89f0c0970056db56a8c7c913086f222'
auth_token = 'f347093ec0d27816142411df5361c491'
client = Client(account_sid, auth_token)



pir = MotionSensor(4)
count=0
relay = OutputDevice(20)
relay2 = OutputDevice(21)
from signal import pause
while True:
    #pir.wait_for_motion()
    t = time.localtime()
    ct = time.strftime("%H:%M:%S" , t)
    print(" you moved ",count,ct)
    #message = client.messages.create(
    #                          from_='+12183664277',
    #                          body='sensor tripped'+str(count)+' at '+ct,
    #                          to='+15305037021'
    #                      )

    #print(message.sid)
    relay.on()
    relay2.on()
    time.sleep(10)
    count+=1
    relay.off()
    relay2.off()
    time.sleep(10)
