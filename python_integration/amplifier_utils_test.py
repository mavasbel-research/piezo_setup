import timeit
import logging
from amplifier_utils import AmplifierController
# from loguru import logger

# logger configuration
format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(processName)11s - %(threadName)10s : %(message)s"
logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", format=format_string, level=logging.DEBUG)
logger = logging.getLogger()

if __name__ ==  '__main__':
    amp_controller = AmplifierController(v_max=1200, v_min=-1200, com_port='COM5', baudrate=115200, 
        rx_timeout=2.0, tx_timeout=2.0, tx_delay=0.0)
    amp_controller.init_comm()
    for _ in range(1,2):        
        for voltage in range(-1200,1201):
            amp_controller.send_value(voltage)
    amp_controller.stop_comm()