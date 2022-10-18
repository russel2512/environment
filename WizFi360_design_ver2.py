# Russ Terrell
# 10-14-2022
# WizFi360-EVB-Pico

# Remove '#' from command lines for troubleshooting

import uos
import utime
import tm1637
from machine import UART,Pin,I2C
from bme680 import *
from ssd1306 import SSD1306_I2C
from machine import RTC
from time import sleep

# System info
print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])
print("-------------------------------------------------------------")

# Online LED
led = machine.Pin(25, machine.Pin.OUT)
led.value(0)

# UART
uart = machine.UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
print("UART Setting...")
print(uart)
print(" ")

temperature_offset = -5
tp=0 # Outdoor temperature
hm=0 # Outdoor humidity
pr=0 # Outdoor pressure
days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

# Define LED display (digital)
tm = tm1637.TM1637(clk=Pin(18), dio=Pin(19))

# Define OLED (I2C)
i2c = I2C(0)
oled = SSD1306_I2C(128, 64, i2c)

# Define BME680 sensor (I2C)
i2c = I2C(1)
bme = BME680_I2C(i2c=i2c)

# Functions
def sendCMD_waitResp(cmd, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(timeout)
    print()
    
def waitResp(timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills) < timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print(resp)
    global myString
    myString=resp
    
# AT commands
sendCMD_waitResp('AT\r\n') #AT
sendCMD_waitResp('AT+GMR\r\n') #AT ver

sleep(.05)
sendCMD_waitResp('AT+CWMODE_CUR=1\r\n') #Station Mode
sendCMD_waitResp('AT+CWDHCP_CUR=1,1\r\n') #DHCP on

sendCMD_waitResp('AT+CWHOSTNAME="WizFi360_1"\r\n') #Set Host name
#sendCMD_waitResp('AT+CWHOSTNAME?\r\n') #Display Host name

# Log into the network
sleep(.05)
sendCMD_waitResp('AT+CWJAP_CUR="RTHomez","w1X2y3Z4Home2020cba"\r\n') #AP connecting
sendCMD_waitResp('AT+CIPSTA_CUR?\r\n') # Display network connection
led.value(1) # Connected

# Get network time (adjust for time zone -5 is CT)
sendCMD_waitResp('AT+CIPSNTPCFG=1,-5,"time.google.com"\r\n')
sendCMD_waitResp('AT+CIPSNTPTIME?\r\n')

# Set real time clock
rtc = machine.RTC()
#print(rtc.datetime())
#(year,month,day,hour,minute,second,wday,yday)=utime.localtime(utime.time())
#print("%d-%02d-%02d %02d:%02d:%02d %s, day %d of the year" %
#         (year,month,day,hour,minute,second,str(days[wday]),yday))

# Setup MQTT
# This is ID, Password and Host
sendCMD_waitResp('AT+MQTTSET="rpi-pico","wiznet","Wiznet",300\r\n')
sendCMD_waitResp('AT+MQTTSET?\r\n')
# Board only allows 1 Pub(publish) and upto 3 Subs(subscribes)
sendCMD_waitResp('AT+MQTTTOPIC="WIZnet","temper","humid","press"\r\n')
sendCMD_waitResp('AT+MQTTTOPIC?\r\n')
sendCMD_waitResp('AT+MQTTQOS=1\r\n')
# Change to IP address of Mosquitto Broker
sendCMD_waitResp('AT+MQTTCON=0,"192.168.68.127",1883\r\n')

while True:
    # Get BME680 sensor information 
    temp_m = str(round((bme.temperature) * (9/5) + 32) + temperature_offset)
    temp = temp_m + '˚F'
    temp_d='Temp: ' + temp_m + ' F'
    
    hum_m = str(round(bme.humidity))
    hum = hum_m + '%'
    hum_d='Hum: ' + hum
    
    pres_m = str(round(bme.pressure))
    pres = pres_m + ' hPa'
    pres_d = 'Pres: '+ pres
    
    gas_m = str(round(bme.gas/1000, 2))
    gas = gas_m + ' KOhms'
    gas_d='Gas: '+ gas
                
    # Display BME680 info on SSD1306 OLED
    oled.fill(0)
    oled.text(temp_d, 0, 0)
    oled.text(hum_d, 0, 16)
    oled.text(pres_d, 0, 32)
    oled.text(gas_d, 0, 48)
    oled.show()
    
    (year,month,day,hour,minute,second,wday,yday)=utime.localtime(utime.time())
    dhour = hour
    if hour < 1:
        dhour = 12
    if hour > 12:
        dhour = dhour - 12
    # Display time on LED display
    tm.numbers(dhour, minute)
    sleep(12)

    # Display temperature on LED display 
    tm.temperature(tp)
    sleep(3)
    
    print(" ")
    if minute <10:
        print(str(dhour) + ":" + "0" + str(minute))
    else:
        print(str(dhour) + ":" + str(minute))
        
    print('-----indoor------------')
    print('Temperature:', temp)
    print('Humidity:', hum)
    print('Pressure:', pres)
    print('Gas:', gas)
    
    print('-----outdoor-----------')
    print("Temperature:" + str(tp) + '˚F')
    print("Humidity:" + str(hm) + '%')
    print("Pressure:" + str(pr) + ' hPa')
    print(" ")
    
    sendCMD_waitResp('AT+MQTTPUB= ' + temp_m + ', ' + hum_m + ', ' + pres_m + ', ' + gas_m + '\r\n')
    String = myString.split()
    #print(String)
    counter = 0
    for i in String:
        #print(String[counter])
        #print(type(String[counter]))
        str_String=str(String[counter])
        #print(str_String)
        #print(type(str_String))
        if str_String == "b'temper'":
            tp=int(String[counter+2])
            #print(tp)            
        if str_String == "b'humid'":
            hm=int(String[counter+2])
            #print(hm)            
        if str_String == "b'press'":
            pr=int(String[counter+2])
            #print(pr)            
        counter = counter + 1
    
#log out of the network
sendCMD_waitResp('AT+CWQAP\r\n')
sleep(0.5)
led.value(0)