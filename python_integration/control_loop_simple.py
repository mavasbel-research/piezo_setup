import csv
import time
import msvcrt
import logging
import multiprocessing
from amplifier_utils import AmplifierController
from interferometer_utils import InterferometerController
from interferometer_utils import InterferometerData
from interferometer_utils import InterferometerQuality

# logger configuration
format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(processName)11s - %(threadName)10s : %(message)s"
logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", format=format_string, level=logging.INFO)
logger = logging.getLogger()

def worker_csv(csv_queue):
    logger.info("csv opening...")
    timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
    csv_file = open('simple-control-' + timestr + '.csv', mode='a+', newline='')
    csv_writer = csv.writer(csv_file, delimiter=',')

    while(True):
        data = csv_queue.get()
        if data is None: break
        csv_writer.writerow(data)

    logger.info("csv closing...")
    csv_file.flush()
    csv_file.close()

def worker_control(interf_queue, amp_queue, csv_queue):
    logger.info("starting control loop...")
    while(True):
        obj = interf_queue.get()
        if obj is None: break
        if isinstance(obj, InterferometerQuality):
            logger.info("Quality, Channel 1: %4.1f, Channel 2: %4.1f, Channel 3: %4.1f" 
                % (obj.channel_1, obj.channel_2, obj.channel_3))
        if isinstance(obj, InterferometerData):
            logger.info("Data, Channel 1: %4.1f, Channel 2: %4.1f, Channel 3: %4.1f" 
                % (obj.channel_1, obj.channel_2, obj.channel_3))
            amp_queue.put(obj.channel_1)
            csv_queue.put(obj)
    logger.info("ending control loop...")
    csv_queue.put(None)
    csv_queue.close()
    csv_queue.join_thread()
    
if __name__ ==  '__main__':
    # Create amplifier controller
    amp_controller = AmplifierController(
        v_max=1200, v_min=-1200, 
        com_port='COM6', baudrate=115200, 
        rx_timeout=0.5, tx_timeout=0.5, tx_delay=0.0)
    amp_controller.init_comm()

    # Create interferometer controller
    interf_controller = InterferometerController(5, 10)
    interf_controller.init_comm()

    # Create queue of csv
    csv_queue = multiprocessing.Queue()
    
    # Create and start process for control computations
    control_process = multiprocessing.Process(
        target=worker_control, 
        args=(interf_controller.get_queue(), 
        amp_controller.get_queue(),
        csv_queue))
    control_process.start()

    # Create and start process for csv writing
    csv_process = multiprocessing.Process(
        target=worker_csv, args=(csv_queue,) )
    csv_process.start()

    # Wait for key pressed to start reading of interferometer
    while(not msvcrt.kbhit()): pass
    msvcrt.getwch()
    interf_controller.get_start_event().set()

    # Wait again for key pressed to stop amplifier and interferometer
    while(not msvcrt.kbhit()): pass
    msvcrt.getwch()
    interf_controller.stop_comm()
    amp_controller.stop_comm()