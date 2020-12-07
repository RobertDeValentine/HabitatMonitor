#dependencies
#pip3 install adafruit-circuitpython-dht
#pip3 install board
#pip3 install gpiozero
#pip3 install twilio
from gpiozero import *
import time
import csv
import sys
import board
import adafruit_dht
from your_header import YourTwilioAccount
from twilio.rest import Client
from signal import pause
from header import *
from datetime import datetime
from datetime import timedelta


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
#writes array ti file with each element as line
def toFile(fname,mylist):
    with open(fname, 'w') as f:
        for item in mylist:
            f.writelines(item)
            f.writelines('\n')
#reads to list with each line as single element
def readtol(name):
    lines = list()
    with open(name) as f:
        for i in f:
            lines.append(i)
    return lines

def reply(i,bod):#use this function to reply to message i with string bod as text message
    message = client.messages.create(
        from_=TwilioAccount.phone_number,
        body=bod,
        to=i.from_
         )
    time.sleep(1)#to no reply too quickly and violate trial liscense comment out at own risk
    #print("replied to ",i.from_)#debug
def safe_del(i):#call this function to safely delete a message it takes whole messages
    time.sleep(.1)
    mes =client.messages(i.sid).fetch()
    if (mes.direction=="inbound" and mes.price is None):
        #print("choice 1")#debug
        bad_sid.add(i.sid)
        return
    elif (mes.sid in bad_sid):
        #print("choice 2")#debug
        bad_sid.remove(mes.sid)
    elif (mes.price is None):
        #print("choice 3")#debug
        return
    #print(mes.status,mes.price, "before deletion")#debug
    #print(i.body)#debug
    client.messages(mes.sid).delete()
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

bad_sid = set()#blacklist of sid

#Note this is basic on off code for relay
#Do not exceed 10 amps @ 120V per relay if using our parts guide!
sensor_pin = board.D18#pin for the humidity and temp sensor
relay = OutputDevice(20)#relay for switch connected to gpio 20 aka relay ch 2
relay2 = OutputDevice(21)#relay for switch connected to gpio 21 aka relay ch 3
ldr = LightSensor(23)#light sensor on gpio 23
#safety check switch relay devices to default off position with switch off for both outlets to go off.
relay.off()
relay2.off()

bad_sid = set(readtol("bl.txt"))
temp_sid = bad_sid
#clean up old messages 
for i in temp_sid:
    #print(i, "deletion attempt")#debug
    safe_del(client.messages(i).fetch())
for i in client.messages.list(from_=TwilioAccount.phone_number):
    #print(i, "deletion attempt")#debug
    safe_del(i)



#debug variables
count=0
mybool=False
ss1 = datetime.now()+timedelta(seconds=5)
ss2 = datetime.now()+timedelta(seconds=5)

while True:
    #print("loop start: ", count)#debug
    for i in client.messages.list(to=TwilioAccount.phone_number,date_sent_after=(datetime.now())):
        if(i.direction=="inbound" and (i.sid not in bad_sid)):
            #this is where your commands go
            #message is deleted at end of if statement
            print("inbound")
            print(i.body,"inbound 1")
            command = (i.body.lower()).strip()
            print(command,"inbound 2")
            if (command=="is light"):
                if(not(ldr.light_detected)):
                    reply(i,"It's light out!")
                else:
                    reply(i,"Darkness is here.")
                #print("light done")
            elif(command=="temperature"):
                temperature, humidity =SafeDht(sensor_pin)#call function to get temp and hum
                reply(i,"The temperature is: "+str(temperature)+" Celsius")
            elif(command=="humidity"):
                temperature, humidity =SafeDht(sensor_pin)#call function to get temp and hum
                reply(i,"The humidity is: "+str(humidity))
            #OUTLET SWITCHING
            elif(command == "switch 1 off"):
                if(relay.value == 1 ):
                    if(datetime.now()>ss1):
                        relay.off()
                        ss1 = datetime.now()+timedelta(seconds=5)
                        reply(i,"Outlet 1 switched off")
                    else:
                        reply(i,"Outlet 1 not switched off. 5 second cooldown not met.")
                else:
                    reply(i,"Outlet 1 is already off")
            elif(command == "switch 1 on"):
                if(relay.value == 0 ):
                    if(datetime.now()>ss1):
                        relay.on()
                        ss1 = datetime.now()+timedelta(seconds=5)
                        reply(i,"Outlet 1 switched on")
                    else:
                        reply(i,"Outlet 1 not switched on. 5 second cooldown not met.")
                else:
                    reply(i,"Outlet 1 is already on")
            #OUTLET 2 SWITCHING
            elif(command == "switch 2 off"):
                if(relay2.value == 1):
                    if(datetime.now()>ss2):
                        relay2.off()
                        ss2 = datetime.now()+timedelta(seconds=5)
                        reply(i,"Outlet 2 switched off")
                    else:
                        reply(i,"Outlet 2 not switched off. 5 second cooldown not met.")
                else:
                    reply(i,"Outlet 2 is already off")
            elif(command == "switch 2 on"):
                if(relay2.value == 0):
                    if(datetime.now()>ss2):
                        relay2.on()
                        ss1 = datetime.now()+timedelta(seconds=5)
                        reply(i,"Outlet 2 switched on")
                    else:
                        reply(i,"Outlet 2 not switched on. 5 second cooldown not met.")
                else:
                    reply(i,"Outlet 2 is already on")
            elif(command == "help"):
                reply(i,"Here are the following commands:\n'is light': returns status of the light\n'temperature': returns the temperature\n'humidity': returns the humidity\n'switch {1,2} {on,off}': Switches the outlet to the desired setting\n 'Status': returns status")
            else:
                reply(i,"bad command: '"+command+"'  please type 'help' for list of commands")
            safe_del(i)

    #print("loop end: ",count)#debug
    toFile("bl.txt",list(bad_sid))#backup current bad sid in case of power loss
    time.sleep(1)#keeping loop to once per 1 second to reduce power?
    #print(bad_sid)#debug
    count= count+1





#todo switch on and off outlets via text
#find way to secure account sid and token using git ignore and separate file?
#demo environment for presentation.
#parse messages for correct one and commands have proper responses and error messages for wrong commands.
