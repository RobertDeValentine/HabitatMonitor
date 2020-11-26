from gpiozero import *
import time
import board
import adafruit_dht
#pip3 install adafruit-circuitpython-dht

from twilio.rest import Client

from signal import pause


def SafeDht(gpio_pin):
    dht_device = adafruit_dht.DHT22(gpio_pin,use_pulseio=False)
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return temperature, humidity
    except RuntimeError as error:
        return SafeDht()

#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
sensor_pin = board.D18
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
    x = '''for i in client.messages.list():
        t = time.localtime()
        ct = time.strftime("%H:%M:%S" , t)
        print("attempt ",count,ct)
        print(i.from_)
        #message = client.messages.create(
        #                          from_='+12183664277',
        #                          body='sensor tripped'+str(count)+' at '+ct,
        #                          to='+15305037021'
        #                      )
    time.sleep(10)'''#string comment to disable checking messages
    temperature, humidity =SafeDht(sensor_pin)
    print(humidity," : ",temperature)
    time.sleep(5)

    #print(message.sid)
    if mybool:
        relay.on()
        relay2.on()
    print("loop end")
