# Oh no.... not another home environment monitoring system

Designed for WIZnet WizFi360 contest.

https://maker.wiznet.io/russel2512/contest/oh-no-not-another-home-environment-monitoring-system/

**home environment monitoring system using WizFi360-EVB-Pico**

This project uses a WIZnet WizFi360-EVB-Pico and Seeed Studion Grove devices to monitor the inside home environment. The program displays logging information to a serial port , current time/temp to a LED alphanumeric display and publishes MQTT to a broker. I used a Raspberry Pi and Node Red for the broker. The monitor also loads current weather information from Undergroundmap.org. 

This project was created to be a proof of concept using the WIZnet WizFi360-EVB-Pico board. The POC is to see if the board works ok with MicroPython and Seeed Studio Grove boards. 

I created the project in 2 parts.

**Versions:**

Version 1 was created to test the WiFi connection and Internet connection. It also connects to a BME680 sensor, SDD1315 OLED to display the sensor data and an Alphanumeric display to display the current time.
The program will:
- Connect to an NPT server and sync the time to the onboard RTC (real time clock)
- Displays time on the TM1637 alphanumeric display
- Collects data from BME680
- Displays collected information on the serial monitor and SDD1315 OLED display
- Data is sent to a MQTT broker and displayed on a Node Red Dashboard

Version 2 adds current weather from openweathermap.org
- Node Red requests current weather data
- Node Red publishes to the WizFi360 
- Displays the current temputature on the TM1637 alphanumeric display
- Displays weather data on the serial monitor



**Design:**

**Hardware design:**

**Bill of materials:**
- WIZnet WizFi360-EVB-Pico
www.wiznet.io
- Grove Shield for Pi Pico
Grove Shield for Pi Pico v1
- Grove - Temperature, Humidity, Pressure and Gas Sensor for Arduino - BME680
BME680
- Grove - 4-Digit Display
TM1637
- Grove - OLED Yellow&Blue Display 0.96 (SSD1315)
SSD1315 
- Grove - Universal 4 Pin Buckled 20cm Cable
Grove Universal 4 Pin Buckled 20cm Cable 5 PCs pack
- Micro USB cable


Project build out:
- Insert the WizFi360-EVB-Pico in the Grove Shield for Pi Pico socket 
- Using a Grove - Universal 4 pin buckled 20cm cable, connect the Grove TM1637 to D18 on the shield
- Using a 20cm cable, connect the Grove SSD1315 to I2C0 on the shield
- Using a 20cm cable, connect the Grove BME680 to I2C1 on the shield 
![board - 1](https://user-images.githubusercontent.com/13513067/197628294-9901b1eb-f349-4855-babd-a2cea341b099.jpg)
D18 Grove TM1637 
![board - 2](https://user-images.githubusercontent.com/13513067/197628395-7908b9ed-a19d-4fc8-ad29-ac32a13e5b2e.jpg)
I2C0 Grove SSD1315    I2C1 Grove BME680 

**Circuit diagram**




**Deployment:**

This is an overview of the project deployment. You should have a general knowledge of RP2040. Information can be found at https://www.raspberrypi.com/products/raspberry-pi-pico/ and https://docs.wiznet.io/Product/Open-Source-Hardware/wizfi360-evb-pico. 

This project was developed with MicroPython v1.19.1 deployed on the wizfi360-evb-pico. A good reference can be found at https://learn.adafruit.com/welcome-to-circuitpython.   
Version 7.1.1 of CircuitPython (adafruit-circuitpython-raspberry_pi_pico-en_US-7.1.1.uf2) can be found here:
https://adafruit-circuit-python.s3.amazonaws.com/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-7.1.1.uf2

Install Thonny IDE to program the wizfi360-evb-pico. It can be found here: https://thonny.org/.

Test MicroPython with the wizfi360-evb-pico using the Blink example program. 

**Library deployment steps:**
- Create **lib** folder on the board.
- Download and copy the following libraries 
   - https://github.com/mcauser/micropython-tm1637 (tm1637.py)
	at line 186 make these changes:
	#self.write([_SEGMENTS[38], _SEGMENTS[12]], 2) # degrees C
     	self.write([_SEGMENTS[38], _SEGMENTS[15]], 2) # degrees F
   - https://randomnerdtutorials.com/micropython-esp32-esp8266-bme680-web-server/ (bme680.py)
   - https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py (ssd1306.py)

Copy the monitor code (WizFi360_design_ver1.py or WizFi360_design_ver2.py) from https://github.com/russel2512/environment.
- Rename program to code.py (autorun)

Connect the LEDs per the circuit diagram found in the GitHub project.

**Setup a Raspberry Pi (Node Red is needed).** 
- For information on Raspberry Pi deployment, see https://www.raspberrypi.com/.
- For information on Mosquitto MQTT broker, see https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi.
- For information on Node Red, see https://nodered.org/docs/getting-started/raspberrypi.
- Import the text from **NodeRed import.txt** into Node Red. You may need to modify MQTT broker information. Server - 'localhost' works ok in my configuration.Change the username and password.  These will need to be change in both the code and Node Red.
  - username="rpi-pico"
  - password="wiznet"
- Add your city and openweathermap.org key.
