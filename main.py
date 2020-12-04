#dependencies
#pip3 install adafruit-circuitpython-dht
#pip3 install board
#pip3 install gpiozero
#pip3 install twilio
from gpiozero import *
import time
import board
#pip3 install board
import adafruit_dht
from your_header.py import YourTwilioAccount
from header.py import TwilioAccount
from twilio.rest import Client
from signal import pause
from header import *

#dht sensors are unreliable and thus this function is needed
#uses try except and recursion to sweep under the rug errors
# and keep trying sensor until a correct reading occurs.
def SafeDht(gpio_pin):
    dht_device = adafruit_dht.DHT22(gpio_pin,use_pulseio=False)
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return temperature, humidity
    except RuntimeError as error:
        return SafeDht()

#Note this is basic on off code for relay
#Do not exceed 10 amps @ 120V per relay if using our parts guide!
sensor_pin = board.D18#pin for the humidity and temp sensor 
relay = OutputDevice(20)#relay for switch connected to gpio 20 aka relay ch 2
relay2 = OutputDevice(21)#relay for switch connected to gpio 21 aka relay ch 3
#safety check switch relay devices to default off position with switch off for both outlets to go off.
relay.off()
relay2.off()




# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = TwilioAccount.account_sid
auth_token = TwilioAccount.auth_token
client = Client(account_sid, auth_token)



#debug variables
count=0
mybool=False

while True:
    print("loop start")#debug
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
    temperature, humidity =SafeDht(sensor_pin)#call function to get temp and hum
    print(humidity," : ",temperature)
    time.sleep(5)#wait 5 seconds #debug

    #print(message.sid)
    if mybool:#debug
        relay.on()
        relay2.on()
    print("loop end")#debug




#todo switch on and off outlets via text
#find way to secure account sid and token using git ignore and separate file?
#demo environment for presentation.
#parse messages for correct one and commands have proper responses and error messages for wrong commands.