# Russ Terrell
# 09-28-2022
# WizFi360-EVB-Pico
# Stand alone weather info from BME60 sensor
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

# Define LED display (digital)
tm = tm1637.TM1637(clk=Pin(18), dio=Pin(19))

# Define oled (I2C)
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
    
# AT commands
sendCMD_waitResp('AT\r\n') #AT
sendCMD_waitResp('AT+GMR\r\n') #AT ver

sleep(.25)
sendCMD_waitResp('AT+CWMODE_CUR=1\r\n') #Station Mode
sendCMD_waitResp('AT+CWDHCP_CUR=1,1\r\n') #DHCP on

sendCMD_waitResp('AT+CWHOSTNAME="WizFi360_1"\r\n') #Set Host name
#sendCMD_waitResp('AT+CWHOSTNAME?\r\n') #Display Host name

# Log into the network
sleep(.25)
sendCMD_waitResp('AT+CWJAP_CUR="netword id","password"\r\n') #AP connecting
sendCMD_waitResp('AT+CIPSTA_CUR?\r\n') #Display network connection
led.value(1) #connected

# Get network time
sendCMD_waitResp('AT+CIPSNTPCFG=1,-5,"time.google.com"\r\n')
sendCMD_waitResp('AT+CIPSNTPTIME?\r\n') #Display time

# Set real time clock
rtc = machine.RTC()
#print(rtc.datetime())
#(year,month,day,hour,minute,second,wday,yday)=utime.localtime(utime.time())
#print("%d-%02d-%02d %02d:%02d:%02d %s, day %d of the year" %
#         (year,month,day,hour,minute,second,str(days[wday]),yday))

while True:
    #display BME680 sensor information in the console
    temp = ((bme.temperature) * (9/5) + 32) + temperature_offset
    temp = str(round(temp)) + '˚F'
    hum = str(round(bme.humidity)) + '%'
    pres = str(round(bme.pressure)) + ' hPa'
    gas = str(round(bme.gas/1000, 2)) + ' KOhms'
    
    (year,month,day,hour,minute,second,wday,yday)=utime.localtime(utime.time())
    dhour = hour
    if hour < 1:
        dhour = 12
    if hour > 12:
        dhour = dhour - 12
    tm.numbers(dhour, minute)
    sleep(30)

    print(" ")
    if minute <10:
        print(str(dhour) + ":" + "0" + str(minute))
    else:
        print(str(dhour) + ":" + str(minute))
    print('Temperature:', temp)
    print('Humidity:', hum)
    print('Pressure:', pres)
    print('Gas:', gas)
    print('----------------------')
    
    #display BME680 info on SSD1306 OLED
    temp_d = 'Temp: '+ str(round(((bme.temperature) * (9/5) + 32) + temperature_offset)) + ' F'
    hum_d='Hum: ' + hum
    pres_d='Pres: ' + pres
    gas_d='Gas: ' + gas
    oled.fill(0)
    oled.text(temp_d, 0, 0)
    oled.text(hum_d, 0, 16)
    oled.text(pres_d, 0, 32)
    oled.text(gas_d, 0, 48)
    oled.show()
    
# log out of the network
sendCMD_waitResp('AT+CWQAP\r\n')
sleep(0.5)
led.value(0)
