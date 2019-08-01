import timeit
import logging
from amplifier_utils import AmplifierController
# from loguru import logger

#####################################################

# serial parameters
BAUDRATE = 115200
SERIAL_PORT = 'COM5'
RX_TIMEOUT = 2
TX_TIMEOUT = 2

# amplifier parameters
V_MAX = 1200
V_MIN = -1200

#####################################################

# logger configuration
format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(processName)11s - %(threadName)10s : %(message)s"
logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", format=format_string, level=logging.DEBUG)
logger = logging.getLogger()

if __name__ ==  '__main__':
    amp_controller = AmplifierController(v_max=V_MAX, v_min=V_MIN, 
        com_port=SERIAL_PORT, baudrate=BAUDRATE, 
        rx_timeout=RX_TIMEOUT, tx_timeout=TX_TIMEOUT, tx_delay=0.0)
    amp_controller.init_comm()
    for _ in range(1,2):        
        for voltage in range(-1200,1201):
            amp_controller.send_value(voltage)
    amp_controller.end_comm()