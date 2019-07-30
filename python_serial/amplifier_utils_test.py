import timeit
import logging
from amplifier_utils import AmplifierController

format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(threadName)10s : %(message)s"
logging.basicConfig(format=format_string, level=logging.DEBUG, datefmt="%H:%M:%S")

if __name__ ==  '__main__':
    amp_controller = AmplifierController(v_max=1200, v_min=-1200, 
        tx_delay=0.0, com_port='COM4', baudrate=115200, rx_timeout=0.01, tx_timeout=0.01)
    for j in range(1,2):        
        amp_controller.init_comm()
        for i in range(1,1201):
            amp_controller.send_value(i)
    amp_controller.stop_comm()