from pylib.gpio_to_led_mapper import GpioToLedMapper

ARDUINO_NAME = "/dev/ttyACM0"
LEDS = [21, 20, 16, 12]

led_mapper = GpioToLedMapper(*LEDS, transmitterName=ARDUINO_NAME)

while True:
    led_mapper.updateLeds()
