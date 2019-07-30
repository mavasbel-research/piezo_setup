import time
import logging
import msvcrt
from interferometer_utils import InterferometerController

format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(threadName)10s : %(message)s"
logging.basicConfig(format=format_string, level=logging.DEBUG, datefmt="%H:%M:%S")

def callback(data):
    logging.info(data.channel_1)

if __name__ ==  '__main__':
    interferometer_controller = InterferometerController(4, callback)
    interferometer_controller.init_comm()
    while(not msvcrt.kbhit()): 
        pass
    interferometer_controller.stop_comm()