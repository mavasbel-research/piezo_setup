import time
import msvcrt
import logging
import multiprocessing
from interferometer_utils import InterferometerController
from interferometer_utils import InterferometerData
from interferometer_utils import InterferometerQuality

# logger configuration
format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(processName)11s - %(threadName)10s : %(message)s"
logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", format=format_string, level=logging.INFO)
logger = logging.getLogger()

def worker_test(start_event, queue):
    logger.debug("starting test loop...")
    while(True):
        obj = queue.get()
        if obj is None: break
        if isinstance(obj, InterferometerQuality):
            logger.info("Quality, Channel 1: %4.1f, Channel 2: %4.1f, Channel 3: %4.1f" 
                % (obj.channel_1, obj.channel_2, obj.channel_3))
        if isinstance(obj, InterferometerData):
            logger.info("Data, Channel 1: %4.1f, Channel 2: %4.1f, Channel 3: %4.1f" 
                % (obj.channel_1, obj.channel_2, obj.channel_3))
    time.sleep(0.01)
    logger.debug("ending test loop...")

if __name__ ==  '__main__':
    interferometer_controller = InterferometerController(5)
    queue, start_event = interferometer_controller.init_comm()
    process_test = multiprocessing.Process(target=worker_test, args=(start_event, queue))
    process_test.start()
    
    while(not msvcrt.kbhit()): pass
    msvcrt.getwch()
    start_event.set()

    while(not msvcrt.kbhit()): pass
    msvcrt.getwch()
    interferometer_controller.stop_comm()