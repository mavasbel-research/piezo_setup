import csv
import time
import msvcrt
import logging
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from amplifier_utils import AmplifierController
from interferometer_utils import InterferometerController
from interferometer_utils import InterferometerData
from interferometer_utils import InterferometerQuality

#####################################################

# interferometer parameters
INTERF_SERIAL_PORT = 6
INTERF_FREQ = 100

# amplifier parameters
AMPLIF_SERIAL_PORT = 'COM5'
AMPLIF_BAUDRATE = 115200
AMPLIF_RX_TIMEOUT = 2
AMPLIF_TX_TIMEOUT = 2
AMPLIF_V_MAX = 1200
AMPLIF_V_MIN = -1200

#####################################################

# logger configuration
format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(processName)11s - %(threadName)10s : %(message)s"
logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", format=format_string, level=logging.INFO)
logger = logging.getLogger()

def generate_characterization_signal(init_amp, pulse_amp, sample_time):
    time_points = np.array([ 
             0, 0.25, 0.75, 1, 1.25, 1.75, 2,
             3, 3.25, 3.5,
             4.5])
    voltage_points = np.array([ 
              0, init_amp, -init_amp, 0, init_amp, -init_amp, 0,
              0, pulse_amp, 0,
              0])
    samples = time_points[-1]/sample_time
    instances = np.linspace(time_points[0], time_points[-1], samples)
    voltages = np.interp(instances, time_points, voltage_points)
    return instances, voltages

def worker_csv(csv_queue):
    logger.info("csv opening...")
    timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
    csv_file = open('measurement-loop-' + timestr + '.csv', mode='a+', newline='')
    csv_writer = csv.writer(csv_file, delimiter=',')

    while(True):
        data = csv_queue.get()
        if data is None: break
        csv_writer.writerow(data)

    logger.info("csv closing...")
    csv_file.flush()
    csv_file.close()

def worker_measurement(csv_queue, start_event):
    # Create amplifier controller
    amp_controller = AmplifierController(
        v_max=AMPLIF_V_MAX, v_min=AMPLIF_V_MIN, 
        com_port=AMPLIF_SERIAL_PORT, baudrate=AMPLIF_BAUDRATE, 
        rx_timeout=AMPLIF_RX_TIMEOUT, tx_timeout=AMPLIF_TX_TIMEOUT, tx_delay=0.0)
    amp_queue = amp_controller.init_comm()

    # Create interferometer controller
    interf_controller = InterferometerController(INTERF_SERIAL_PORT, INTERF_FREQ)
    interf_queue, interf_measure = interf_controller.init_comm()
    
    # Wait for space pressed
    while(not start_event.is_set()):
        obj = interf_queue.get()
        if obj is None: return
        elif isinstance(obj, InterferometerQuality):
            logger.info("Quality, Channel 1: %4.1f, Channel 2: %4.1f, Channel 3: %4.1f" 
                % (obj.channel_1, obj.channel_2, obj.channel_3))
    
    # Reading loop
    init_amps = [1200]
    pulse_amps = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]
    for init_amp in init_amps:
        for pulse_amp in pulse_amps:
            logger.info("Running measurement for initialization: %4.1f, pulse: %4.1f" % (init_amp, pulse_amp) )
            
            # Generate signal for the corresponding initialization and pulse
            _, signal = generate_characterization_signal(init_amp, pulse_amp, 1/INTERF_FREQ)
            
            # Start measurement loop
            idx = 0
            while not interf_queue.empty(): interf_queue.get() # Empty queue
            interf_measure.set() # Set measure event
            while(idx<len(signal)):
                obj = interf_queue.get()
                if obj is None: return
                elif isinstance(obj, InterferometerData):
                    deformation = obj.channel_1
                    voltage = signal[idx]
                    amp_queue.put(voltage.item())
                    csv_queue.put((init_amp, pulse_amp, idx, idx/INTERF_FREQ, voltage, deformation))
                    idx = idx + 1
            interf_measure.clear() # Clear measure event
                
    logger.info("ending control loop...")
    interf_controller.end_comm()
    amp_controller.end_comm()
    csv_queue.put(None)
    csv_queue.close()
    csv_queue.join_thread()

if __name__ ==  '__main__':
    # Create and start process for csv writing
    csv_queue = multiprocessing.Queue()
    csv_process = multiprocessing.Process(
        target=worker_csv, args=(csv_queue,) )
    csv_process.start()

    # Create and start process for measurement
    start_event = multiprocessing.Event()
    measurement_loop_process = multiprocessing.Process(
        target=worker_measurement, 
        args=(csv_queue, start_event) )
    measurement_loop_process.start()

    # Wait for key pressed to start reading of interferometer
    while(not msvcrt.kbhit()): pass
    msvcrt.getwch()
    start_event.set()

    # Wait again for key pressed to stop amplifier and interferometer
    # while(not msvcrt.kbhit()): pass
    # msvcrt.getwch()