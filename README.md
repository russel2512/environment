# Oh no.... not another home environment monitoring system

Designed for WIZnet WizFi360 contest.

https://maker.wiznet.io/russel2512/contest/oh-no-not-another-home-environment-monitoring-system/

**Home environment monitoring system using WizFi360-EVB-Pico**

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
https://www.seeedstudio.com/Grove-Shield-for-Pi-Pico-v1-0-p-4846.html?queryID=32c8874c38648d638876b7be5b5925aa&objectID=4846&indexName=bazaar_retailer_products
- Grove - Temperature, Humidity, Pressure and Gas Sensor for Arduino - BME680
https://www.seeedstudio.com/Grove-Temperature-Humidity-Pressure-and-Gas-Sensor-for-Arduino-BME680.html?queryID=323612fcdd044071b3abf9a28df4285f&objectID=100&indexName=bazaar_retailer_products
- Grove - 4-Digit Display
https://www.seeedstudio.com/Grove-4-Digit-Display.html?queryID=2875cfcd585f27ccc4190f6e032d17f4&objectID=1651&indexName=bazaar_retailer_products
- Grove - OLED Yellow&Blue Display 0.96 (SSD1315)
https://www.seeedstudio.com/Grove-OLED-Yellow-Blue-Display-0-96-SSD1315-V1-0-p-5010.html?queryID=f0746a190f7b5dcfe94963f483aaa663&objectID=5010&indexName=bazaar_retailer_products 
- Grove - Universal 4 Pin Buckled 20cm Cable
https://www.seeedstudio.com/Grove-Universal-4-Pin-Buckled-20cm-Cable-5-PCs-pack.html?queryID=1fc11df743882664d0ef0971b70f6ee8&objectID=1693&indexName=bazaar_retailer_products
- Micro USB cable


Project build out:
- Insert the WizFi360-EVB-Pico in the Grove Shield for Pi Pico socket 
- Using a Grove - Universal 4 pin buckled 20cm cable, connect the Grove TM1637 to D18 on the shield
- Using a 20cm cable, connect the Grove SSD1315 to I2C0 on the shield
- Using a 20cm cable, connect the Grove BME680 to I2C1 on the shield 
  
**D18  Grove TM1637**
![board - 1 small](https://user-images.githubusercontent.com/13513067/197630484-c06a4dcc-ff9a-449a-95fa-c06c870a8ece.jpg)

![board - 2](https://user-images.githubusercontent.com/13513067/197628395-7908b9ed-a19d-4fc8-ad29-ac32a13e5b2e.jpg)
**I2C0  Grove SSD1315     
I2C1  Grove BME680**

**Circuit diagram**
![image](https://user-images.githubusercontent.com/13513067/198863437-f55ce294-c906-491c-b505-6e9d20845711.png)


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

**Proof of concept results:**
The board uses AT commands which are sometimes confusing to understand without examples. Note that you need to update the board firmware. I spent days trying to troubleshoot an MQTT issue that was fixed with an update.
- The board connects easily to a router. 
- The board works well with MicroPython. The board can use a standard Pico build and the libraries I used worked ok. 
- The Grove Pico shield worked well. It's convent that WIZnet kept the Pico pinouts. 
All requirements for ++Versions 1 and 2** were meet.

**Issues:**
- The firmware needed to be updated. (I included a small program to update it. WizFi360_AT_update.py)
- Documentation of the AT commands were confusing. I had to experiment with them to figure out how they worked. They do seem to be similar to ESP32 commands. 
- I could not get GET commands to work. I would have liked to pull weather data directly off the site.
- MQTT isn't fully implemented. I couldn't get multiple Topics to work. Again, this could be my fault with not fully understanding the documentation. 

**Future enhancements:**
These are just ‘blue sky’ ideas. Some may not be valid or work. The biggest ‘got ya’ was not getting GET to work and MQTT implementation not being complete.
- Break up data for better data handling (ie, filling JASON fields and adding to databases).
- Send BME680 sensor data to a database or an external site (i.e. ThingSpeak).
- Quantify the gas data from the BME680. 
- Design a circuit board for the project.
- Design a 3D printed case.
