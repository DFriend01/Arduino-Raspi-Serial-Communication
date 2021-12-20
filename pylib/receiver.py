import serial

class Receiver:
    def __init__(self, transmitterName, baudrate=9600, timeout=1, callback=lambda x: print(x + "\n")):
        self.__transmitterName = transmitterName
        self.__baudrate = baudrate
        self.__timeout = timeout
        self.__callback = callback

        self.__ser = serial.Serial(transmitterName, baudrate, timeout=timeout)
        self.__ser.reset_input_buffer()

    def spin_for_data(self):
        while True:
            if self.__ser.in_waiting > 0:
                data = self.__ser.readline().decode("utf-8").rstrip()
                return self.__invoke_callback(data)

    def __invoke_callback(self, data):
        return self.__callback(data)
