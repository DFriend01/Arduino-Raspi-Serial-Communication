from .receiver import Receiver
from gpiozero import LED

MAX_LEDS = 8

def getDataAsInt(data):
    dec_val = int(data)
    return dec_val

class GpioToLedMapper:
    def __init__(self, *leds, transmitterName, baudrate=9600, timeout=1):
        """
        Initializes a GpioToLedMapper object used to map GPIO pins on the raspberry pi
        to LEDs. This class also handles updating the LED configuration when it is changed.

        Arguments
        ---------
        *leds
            This variadic argument accepts integers that represent the GPIO pins that are
            being mapped to LEDs. Visit https://pinout.xyz/# to learn about the GPIO pinouts.
            The LSB of the data received by this object represents the status (0 - off, 1- on) 
            of the first GPIO pin passed in this argument, and the MSB for the last argument.

            Note: A maximum of 8 GPIO pins can be mapped using this class. Any pins exceeding
                  the maximum allowable threshold are discarded.

        str : transmitterName
            The name of the USB communication device that acts as the transmitter.

        int : baudrate (default: 9600)
            The baudrate of the receiving device. Both the transmitter and the receiver
            must run at the same baudrate.

        float : timeout (default: 1)
            Set a read timeout value in seconds.
        """
        led_pins = leds if len(leds) <= MAX_LEDS else leds[:MAX_LEDS]
        self.__leds = []
        for i in range(len(led_pins)):
            self.__leds.append(LED(led_pins[i]))

        self.__numLeds = len(self.__leds)
        self.__led_config = [0] * self.__numLeds
        self.__receiver = Receiver(transmitterName, baudrate, timeout, getDataAsInt)

    def updateLeds(self):
        """
        Waits for new data and updates the LED configuration upon receiving data.

        """
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
    