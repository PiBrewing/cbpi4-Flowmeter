
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
import time
from cbpi.api.config import ConfigType
from cbpi.api.base import CBPiBase

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except Exception as e:
    print(e)
    pass

class Flowmeter_Config(CBPiExtension):

    def __init__(self,cbpi):
        self.cbpi = cbpi
        self._task = asyncio.create_task(self.init_sensor())

    async def init_sensor(self):
        unit = self.cbpi.config.get("flowunit", None)
        if unit is None:
            logging.info("INIT FLOW SENSOR CONFIG")
            try:
                await self.cbpi.config.add("flowunit", "L", ConfigType.SELECT, "Flowmeter unit", [{"label": "L", "value": "L"},
                                                                                            {"label": "gal(us)", "value": "gal(us)"},
                                                                                            {"label": "gal(uk)", "value": "gal(uk)"},
                                                                                            {"label": "qt", "value": "qt"}])
            except:
                logging.info("Flowmeter Error, Unable to update database.")



class FlowMeterData():
    SECONDS_IN_A_MINUTE = 60
    MS_IN_A_SECOND = 1000.0
    enabled = True
    clicks = 0
    lastClick = 0
    clickDelta = 0
    hertz = 0.0
    flow = 0  # in Liters per second
    pour = 0.0  # in Liters

    def __init__(self):
        self.clicks = 0
        self.lastClick = int(time.time() * FlowMeterData.MS_IN_A_SECOND)
        self.clickDelta = 0
        self.hertz = 0.0
        self.flow = 0.0
        self.pour = 0.0
        self.enabled = True

    def update(self, currentTime, hertzProp):
        #print hertzProp
        self.clicks += 1
        # get the time delta
        self.clickDelta = max((currentTime - self.lastClick), 1)
        # calculate the instantaneous speed
        if self.enabled is True and self.clickDelta < 1000:
            self.hertz = FlowMeterData.MS_IN_A_SECOND / self.clickDelta
            self.flow = self.hertz / (FlowMeterData.SECONDS_IN_A_MINUTE * hertzProp)  # In Liters per second
            instPour = self.flow * (self.clickDelta / FlowMeterData.MS_IN_A_SECOND)  
            self.pour += instPour
        # Update the last click
        self.lastClick = currentTime

    def clear(self):
        self.pour = 0
        return str(self.pour)


@parameters([Property.Select(label="GPIO", options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],description="GPIO that is used by the Flowsensor"),
            Property.Select(label="Display", options=["Total volume", "Flow, unit/s"],description=""),
            Property.Number(label="Hertz", configurable=True, description="Here you can adjust the freequency for the flowmeter [Hertz, default is 7.5]. With this value you can calibrate the sensor.")])

class FlowSensor(CBPiSensor):
    
    def __init__(self, cbpi, id, props):
        super(FlowSensor, self).__init__(cbpi, id, props)
        self.value = 0
        self.fms = dict()
        self.gpio=self.props.get("GPIO",0)
        self.sensorShow=self.props.get("Display","Total Volume")
        self.Hertz=self.props.get("Hertz", 7.5)

        try:
            GPIO.setup(int(self.gpio),GPIO.IN, pull_up_down = GPIO.PUD_UP)
            GPIO.add_event_detect(int(self.gpio), GPIO.RISING, callback=self.doAClick, bouncetime=20)
            self.fms[int(self.gpio)] = FlowMeterData()
        except Exception as e:
            print(e)

    @action(key="ResetSensor", parameters=[])
    async def ResetSensor(self, **kwargs):
        self.reset()
        print("RESET FLOWSENSOR", kwargs)
  

    def get_unit(self):
        unit = self.cbpi.config.get("flowunit", "L")
        if self.sensorShow == "Flow, unit/s":
            unit = unit + "/s"
        return unit

    def doAClick(self, channel):
        currentTime = int(time.time() * FlowMeterData.MS_IN_A_SECOND)
        hertzProp = self.hertzProp
        self.fms[int(self.gpio)].update(currentTime, float(hertzProp))

    def convert(self, inputFlow):
        unit = self.cbpi.config.get("flowunit", "L")
        if unit == "gal(us)": 
            inputFlow = inputFlow * 0.264172052
        elif unit == "gal(uk)": 
            inputFlow = inputFlow * 0.219969157
        elif unit == "qt": 
            inputFlow = inputFlow * 1.056688
        else:
            pass
        if self.sensorShow == "Flow, unit/s":
            inputFlow = "{0:.2f}".format(inputFlow)
        else:
            inputFlow = "{0:.2f}".format(inputFlow)
        return inputFlow

    async def run(self):
        while self.running is True:
            if self.sensorShow == "Total volume":
                flow = self.fms[int(self.gpio)].pour
                flowConverted = self.convert(flow)
                self.value= float(flowConverted)
            elif self.sensorShow == "Flow, unit/s":
                flow = self.fms[int(self.gpio)].flow
                flowConverted = self.convert(flow)
                self.value = float(flowConverted)
            else:
                logging.info("FlowSensor error")

            self.push_update(self.value)
            await asyncio.sleep(1)

    def getValue(self):
        flow = self.fms[int(self.gpio)].pour
        flowConverted = self.convert(flow)
        return flowConverted

    def reset(self):
        self.fms[int(self.gpio)].clear()
        return "Ok"
    
    def get_state(self):
        return dict(value=self.value)

def setup(cbpi):
    cbpi.plugin.register("FlowSensor", FlowSensor)
    cbpi.plugin.register("Flowmeter_Config", Flowmeter_Config)
    pass
