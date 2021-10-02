# CraftBeerPi4 FLowmeter Sensor / Step Plugin

This plugin has been ported from the craftbeerpi3 plugin version (https://github.com/nanab/Flowmeter)

The plugin includes sensor with action to reset the sensor and a custom step.
Use a 10k ohm resistor on sensors signal pin to protect your Pi or connect the hall type flow sensor to your Craftbeerpi extension board at the flowmeter ports.

Wire the sensor to the pi:
Red -> 5v.
Black -> GND.
Yellow -> 10k ohm resistor -> GPIO pin. (or data on the extension board. No extra resistor required here)

- Installation: 
    - sudo pip3 install cbpi4-Flowmeter
    --> or install from Repo
    - sudo pip3 install https://github.com/avollkopf/cbpi4-Flowmeter 

    - cbpi add cbpi4-Flowmeter

- Sensor Usage:
    - On the settings page, choose a unit for the Volume (e.g. L, qt, gal, ...)
    - Add Sensor under Hardware and choose Flowmeter as Type
    - Several parameters can be set:
        - GPIO defines the GPIO that is used for the signal of the sensor (connected to the yellow cable)
        - Display defines if the total volume or the flow per second is displayed
        - Hertz: Here you need to set the frequency of your sensor (Singals per Liter per minute). This should be documented in the sensor datasheet

![Flowsensor Settings](https://github.com/avollkopf/cbpi4-Flowmeter/blob/main/SensorConfig.png?raw=true)


- Once configured, you need to add the sensor to the Dashboard.
- Please select Yes for Action as this will add an additional menu on the right side of the sensor to reset the sensor to 0

![Flowsensor Action Setting](https://github.com/avollkopf/cbpi4-Flowmeter/blob/main/SensorActionSetting.png?raw=true)
![Flowsensor Action Button](https://github.com/avollkopf/cbpi4-Flowmeter/blob/main/SensorActionButton.png?raw=true)

    
- When you press the menu button on the right side of the sensor, a menu wil show up where you can reset the sensor.

![Flowsensor Action Menu](https://github.com/avollkopf/cbpi4-Flowmeter/blob/main/SensorAction.png?raw=true)

- Flowstep Usage:
    - The plugin provides a step where you can define a volume that should flow while the step is active.
    - You need to select your flowsensor as sensor.
    - An actor has to be defined that triggers the start and stop of the flow (e.g. magnetic valve)
    - You need to enter the volume that should flow while the step is active
    - When the step starts, the sensor will be set to 0.
    - You can select if the sensor should be set to 0 once the step is completed.

![Flowstep](https://github.com/avollkopf/cbpi4-Flowmeter/blob/main/FlowStep.png?raw=true)


- Changelog:

	- 02.10.21: Initial Release