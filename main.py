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
from your_header import YourTwilioAccount
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
        return SafeDht(gpio_pin)

def reply(i,bod):#use this function to reply to message i with string bod as text message
    message = client.messages.create(
        from_=TwilioAccount.phone_number,
        body=bod,
        to=i.from_
         )
    safe_del(message)
def safe_del(i):#call this function to safely delete a message it takes whole messages
    mes =client.messages(i.sid).fetch()

    while(not(mes.status =="delivered") and not(mes.status =="received")):
        mes =client.messages(i.sid).fetch()
        print(mes.status)
        time.sleep(.001)
    client.messages(i.sid).delete()
def parse_in(i,s):#checks if s is in body of i
    if(s in i.body):
        return True
    else:
        return False




# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = TwilioAccount.account_sid
auth_token = TwilioAccount.auth_token
client = Client(account_sid, auth_token)

#Note this is basic on off code for relay
#Do not exceed 10 amps @ 120V per relay if using our parts guide!
sensor_pin = board.D18#pin for the humidity and temp sensor
relay = OutputDevice(20)#relay for switch connected to gpio 20 aka relay ch 2
relay2 = OutputDevice(21)#relay for switch connected to gpio 21 aka relay ch 3
ldr = LightSensor(23)#light sensor on gpio 23
#safety check switch relay devices to default off position with switch off for both outlets to go off.
relay.off()
relay2.off()








#debug variables
count=0
mybool=False



while True:
    print("loop start")#debug
    for i in client.messages.list():
        if(i.direction=="inbound"):
            #this is where your commands go
            #message is deleted at end of if statement
            print("inbound")
            if (i.body.lower()=="is light"):
                if(not(ldr.light_detected)):
                    reply(i,"it's light out!")
                else:
                    reply(i,"darkness is here.")
                #print("light done")
            elif(i.body.lower()=="temperature"):
                temperature, humidity =SafeDht(sensor_pin)#call function to get temp and hum
                reply(i,"the temperature is: "+str(temperature)+"farenheight")
            elif(i.body.lower()=="humidity"):
                temperature, humidity =SafeDht(sensor_pin)#call function to get temp and hum
                reply(i,"the humidity is: "+str(humidity))
            #OUTLET SWITCHING
            elif(i.body.lower() == "switch 1 off"):
                if(relay.value == 1):
                    relay.off()
                    reply(i,"Outlet 1 switched off")
                else:
                    reply(i,"Outlet 1 is already off")
            elif(i.body.lower() == "switch 1 on"):
                if(relay.value == 0):
                    relay.on()
                    reply(i,"Outlet 1 switched on")
                else:
                    reply(i,"Outlet 1 is already on")
            #OUTLET 2 SWITCHING
            elif(i.body.lower() == "switch 2 off"):
                if(relay2.value == 1):
                    relay2.off()
                    reply(i,"Outlet 2 switched off")
                else:
                    reply(i,"Outlet 2 is already off")
            elif(i.body.lower() == "switch 2 on"):
                if(relay.value == 0):
                    relay.on()
                    reply(i,"Outlet 1 switched on")
                else:
                    reply(i,"Outlet 1 is already on")
            elif(i.body.lower() == "help"):
                reply(i,"Here are the following commands:\n'is light': returns status of the light\n'temperature': returns the temperature\n'humidity': returns the humidity\n'switch {1,2} {on,off}': Switches the outlet to the desired setting\n 'Status': returns status")
            else:
                reply(i,"bad command please type 'help' for list of commands")
            safe_del(i)
            #client.messages(i.sid).delete()
        else:
            print(i.sid)
            safe_del(i)
        time.sleep(2)
        #client.messages(i.sid).delete()

    print("loop end")#debug
    time.sleep(.5)#keeping loop to once per .5 second to reduce power?





#todo switch on and off outlets via text
#find way to secure account sid and token using git ignore and separate file?
#demo environment for presentation.
#parse messages for correct one and commands have proper responses and error messages for wrong commands.
x='''
        if( i.body.lower() =="echo"):
            wow="wow"
            reply(i,"echooooooo")
            client.messages(i.sid).delete()

            #client.messages(i.sid).delete()


    temperature, humidity =SafeDht(sensor_pin)#call function to get temp and hum
    print(humidity," : ",temperature)
    time.sleep(5)#wait 5 seconds #debug

    #print(message.sid)
    if mybool:#debug
        relay.on()
        relay2.on()'''
