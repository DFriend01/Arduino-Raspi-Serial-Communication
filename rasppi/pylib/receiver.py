import serial

class Receiver:
    def __init__(self, transmitterName, baudrate=9600, timeout=1, callback=lambda x: print(x + "\n")):
        """
        Initializes a Receiver object and is used to communicate with a transmitting device and
        handle new data upon receiving it.

        Arguments
        ---------
        str : transmitterName
            The name of the USB communication device that acts as the transmitter.

        int : baudrate (default: 9600)
            The baudrate of the receiving device. Both the transmitter and the receiver
            must run at the same baudrate.

        float : timeout (default: 1)
            Set a read timeout value in seconds.

        callable : callback (default: print)
            Set a callback function that is invoked upon receiving data. The callback
            function must reserve the first parameter for the incoming data. By default,
            the data received is printed to the terminal.
        
        """
        self.__callback = callback
        self.__ser = serial.Serial(transmitterName, baudrate, timeout=timeout)
        self.__ser.reset_input_buffer()
        self.__latestData = ""

    def spin_for_data(self):
        """
        Busy waits for data to be received. Upon receiving data, the user-specified callback
        is invoked.

        Modifies
        --------
        __latestData
            Updates the latest data read.

        Returns
        -------
        Returns the value, if any, that is retured from the user-specified callback.

        """
        while True:
            if self.__ser.in_waiting > 0:
                data = self.__ser.readline().decode("utf-8").rstrip()
                self.__latestData = data
                return self.__invoke_callback(data)

    def get_latest_data(self):
        """
        Returns
        -------
        str
            Returns a string containing the latest data read.

        """
        return self.__latestData

    def __invoke_callback(self, data):
        """
        Invoke the callback and return its value, if any.

        """
        return self.__callback(data)
