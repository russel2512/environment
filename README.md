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
- Connect to an NPT server and sync the time to the onboard RTC 
- Displays time on the TM1637 alphanumeric display
- Collect data from BME680
- Display collected information on the serial monitor and SDD1315 OLED display
- Data is sent to a MQTT broker and displayed on a Node Red Dashboard

Version 2 adds current weather from openweathermap.org
- Node Red requests current weather data
- Node Red publishes to the WizFi360 
- Displays the current temputature on the TM1637 alphanumeric display
- Displays weather data on the serial monitor



**Design:**

Hardware used
- WIZnet WizFi360-EVB-Pico
  - www.wiznet.io
- Grove Shield for Pi Pico
  - https://www.seeedstudio.com/Grove-Shield-for-Pi-Pico-v1-0-p-4846.html?queryID=32c8874c38648d638876b7be5b5925aa&objectID=4846&indexName=bazaar_retailer_products
- Grove - Temperature, Humidity, Pressure and Gas Sensor for Arduino - BME680
  - https://www.seeedstudio.com/Grove-Temperature-Humidity-Pressure-and-Gas-Sensor-for-Arduino-BME680.html?queryID=323612fcdd044071b3abf9a28df4285f&objectID=100&indexName=bazaar_retailer_products
- Grove - 4-Digit Display
  - https://www.seeedstudio.com/Grove-4-Digit-Display.html?queryID=2875cfcd585f27ccc4190f6e032d17f4&objectID=1651&indexName=bazaar_retailer_products
- Grove - OLED Yellow&Blue Display 0.96 (SSD1315)
  - https://www.seeedstudio.com/Grove-OLED-Yellow-Blue-Display-0-96-SSD1315-V1-0-p-5010.html?queryID=f0746a190f7b5dcfe94963f483aaa663&objectID=5010&indexName=bazaar_retailer_products
- Grove - Universal 4 Pin Buckled 20cm Cable
  - https://www.seeedstudio.com/Grove-Universal-4-Pin-Buckled-20cm-Cable-5-PCs-pack.html?queryID=1fc11df743882664d0ef0971b70f6ee8&objectID=1693&indexName=bazaar_retailer_products
- Micro USB cable


- The program is written in MicroPython. Thonny was used as the editor.
- Program file name is code.py. This allows the program to autostart on powerup. 
- 
