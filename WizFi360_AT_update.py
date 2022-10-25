import os, sys
import utime
from machine import UART,Pin

#system info
print(os.uname())

#LED
led = machine.Pin(25, machine.Pin.OUT)
led.value(0)
utime.sleep(0.5)
led.value(1)

#UART
uart = machine.UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
print("UART Setting...")
print(uart)

#Functions
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

#AT command Test
sendCMD_waitResp('AT\r\n') #AT
sendCMD_waitResp('AT+GMR\r\n') #AT ver

utime.sleep(.5)
#sendCMD_waitResp('AT+RST\r\n') #reset
sendCMD_waitResp('AT+CWMODE_CUR=1\r\n') # Station Mode
sendCMD_waitResp('AT+CWDHCP_CUR=1,1\r\n') #DHCP on

#log into the network
utime.sleep(.5)
sendCMD_waitResp('AT+CWJAP_CUR="RTHomez","w1X2y3Z4Home2020cba"\r\n') #AP connecting
sendCMD_waitResp('AT+CIPSTA_CUR?\r\n') #network chk

sendCMD_waitResp('AT+CIUPDATE="http://wiki.wiznet.io/download/WizFi360/O11/WizFi360_SDK.img"\r\n')

sendCMD_waitResp('AT+GMR\r\n') #AT ver