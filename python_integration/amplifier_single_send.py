import sys
import signal
import logging
import threading
import multiprocessing
import serial
import time
import keyboard
from queue import Queue
from amplifier_utils import AmplifierSerial, tx_worker

#####################################################

# serial parameters
BAUDRATE = 115200
SERIAL_PORT = 'COM4'
RX_TIMEOUT = 2
TX_TIMEOUT = 2

# amplifier parameters
V_MAX = 1114
V_MIN = -1114

#####################################################

# logger configuration
format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(processName)11s - %(threadName)10s : %(message)s"
logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", format=format_string, level=logging.DEBUG)
logger = logging.getLogger()

if __name__ == "__main__":
    # create queue
    tx_queue = Queue()
    tx_queue.put(0.0)
    
    # create execution thread
    tx_thread = threading.Thread( target=tx_worker, 
        args=(V_MAX, V_MIN, SERIAL_PORT, BAUDRATE, 
        RX_TIMEOUT, TX_TIMEOUT, 0.0, tx_queue) )
    tx_thread.start()
    while(True):
        try:
            user_input = input()
            volts = float(user_input)
            tx_queue.put(volts)
        except ValueError as ve:
            logger.error("%s", ve)
        except KeyboardInterrupt as ke:
            logger.info('exit...')
            tx_queue.put(0.0)
            tx_queue.put(None)
            tx_thread.join()
            exit(0)
        except Exception as oe:
            logger.error("input error: %s", oe)