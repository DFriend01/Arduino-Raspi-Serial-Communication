from .receiver import Receiver
from gpiozero import LED

MAX_LEDS = 8
BASE16 = 16

def getDataAsInt(data):
    dec_val = int(data)
    return dec_val

class GpioToLedMapper:
    def __init__(self, *leds, transmitterName, baudrate=9600, timeout=1):
        led_pins = leds if len(leds) <= MAX_LEDS else leds[:MAX_LEDS]
        self.__leds = []
        for i in range(len(led_pins)):
            self.__leds.append(LED(led_pins[i]))

        self.__numLeds = len(self.__leds)
        self.__led_config = [0] * self.__numLeds
        self.__receiver = Receiver(transmitterName, baudrate, timeout, getDataAsInt)
        

    def updateLeds(self):
        new_data = self.__receiver.spin_for_data()
        self.__getNewLedConfig(new_data)
        self.__lightLeds()

    def __getNewLedConfig(self, configAsInteger):
        for i in range(self.__numLeds):
            self.__led_config[i] = (configAsInteger >> i) & 1

    def __lightLeds(self):
        for i in range(self.__numLeds):
            if self.__led_config[i]:
                self.__leds[i].on()
            else:
                self.__leds[i].off()
    