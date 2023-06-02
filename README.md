# CraftBeerPi4 FLowmeter Sensor / Step Plugin

*For recently added VolumeSensor functionality scroll down*

This plugin has been ported from the craftbeerpi3 plugin version (https://github.com/nanab/Flowmeter)

The plugin includes sensor with action to reset the sensor and a custom step.
Use a 10k ohm resistor on sensors signal pin to protect your Pi or connect the hall type flow sensor to your Craftbeerpi extension board at the flowmeter ports.

Wire the sensor to the pi:
Red -> 5v.
Black -> GND.
Yellow -> 10k ohm resistor -> GPIO pin. (or data on the extension board. No extra resistor required here)

- Installation: 
    - pypi release: sudo pip3 install cbpi4-Flowmeter
    - PiBrewing release: sudo pip3 install https://github.com/avollkopf/cbpi4-Flowmeter/archive/main.zip
	- prash3r VolumeSensor testing branch: sudo pip3 install https://github.com/prash3r/cbpi4-Flowmeter/archive/VolumeSensor.zip

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

## VolumeSensor functionality

The recently added *very simple* VolumeSensor functionality can be used like this:

Parameters:
 - GPIO: The GPIO Pin number in BCM numbering
 - impulsesPerVolumeUnit: the amount of impulses that should be displaying the volume of 1 of whatever Unit. This is unit agnostic. Just use the same unit in your FlowStep if you use it.

The VolumeSensor does nothing more then to count impulses and calculate the volume the number of impulses represent.

Actions:
 - Reset Sensor: resets the countet impulses and volume to 0
 - Fake Impulse: fakes the detection of an impulse (i used this for testing because i dont have a flow sensor)



## Changelog:
- 14.05.23: (0.0.6) added simple VolumeSensor
- 14.04.23: (0.0.5.a2) fixed bug in parameter generation
- 08.04.23: (0.0.5.a1) added test support for plugin settings selection branch
- 11.05.22: (0.0.4) Updated README (removed cbpi add)
- 10.05.22: (0.0.3) removed cbpi dependency
- 27.04.22: (0.0.2) Added MQTT based flowsensor with reset topic
- 02.10.21: (0.0.1) Initial Release

