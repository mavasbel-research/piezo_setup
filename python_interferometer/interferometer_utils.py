import logging
from siosifm import *           #Import modules
from ctypes import *            #(Own writing module is siosifm.py)
import time
import msvcrt
import threading
import multiprocessing
from collections import namedtuple

InterferometerData = namedtuple('InterferometerData', ['channel_1', 'channel_2', 'channel_3', 'temperature', 'pressure'])

class InterferometerSerial:
    def __init__(self, com_port, rx_queue, stop_process_event):
        self._sleep = 2
        self._devNo = 0
        
        # Config params
        self._com_port = com_port
        self._rx_queue = rx_queue
        self._stop_process_event = stop_process_event

    def init_comm(self):
        error = 0

        # Initialize the library
        error = ifmdll.IfmInit()
        if bool(error):     #negative values are error numbers
            logging.error("interferometer error during IfmInit: %s", error)
            self._rx_queue.put(None)
            return
        
        self._devNo = ifmdll.IfmOpenCOM(self._com_port)
        logging.info("interferometer Device No.: %s", self._devNo)
        if self._devNo < 0:       #negative values are error numbers
            logging.error("interferometer error during opening the device")
            ifmdll.IfmClose()
            self._rx_queue.put(None)
            return

        error = ifmdll.IfmSetTrigger(self._devNo, IFM_TRIGGER_OFF)
        if bool(error):
            logging.error("interferometer error during setting trigger mode.")
            ifmdll.IfmClose()
            self._rx_queue.put(None)
            return

        #error = ifmdll.IfmSetMeasurement(devNo, IFM_MEAS_FILTER_DEFAULT | IFM_MEAS_LENGTH , c_double(10))
        error = ifmdll.IfmSetMeasurement(self._devNo, IFM_MEAS_FOURCHANNEL|IFM_MEAS_LENGTH|IFM_MEAS_FILTER_DEFAULT, c_double(100))
        if bool(error):
            logging.error("interferometer error during setting measurement mode.")
            ifmdll.IfmClose()
            self._rx_queue.put(None)
            return
        
        time.sleep(self._sleep)

    def stop_comm(self):
        #stop the output of data
        ifmdll.IfmStop(self._devNo)
        logging.info("interferometer stopped output data.")

        #close the device; devNo will be no longer valid
        ifmdll.IfmCloseDevice(self._devNo)
        logging.info("interferometer closed device.")

        #close the DLL
        ifmdll.IfmClose()
        logging.info("interferometer closed DLL.")

        time.sleep(self._sleep)

    def start_reading_loop(self):
        error = 0
        
        #set the length values to zero; assuming the measurement mirror is at the reference/zero position
        error = ifmdll.IfmSetToZero(self._devNo, 0x0F)

        #begin with the output of data
        error = ifmdll.IfmStart(self._devNo)
        if bool(error):
            logging.error("Error during start out put.")
            ifmdll.IfmClose()
            self._rx_queue.put(None)
            return

        logging.debug("starting interferometer loop...")
        while not self._stop_process_event.is_set():
            # interferometer_data = InterferometerData(
            #         time.time(), 
            #         time.time(), 
            #         time.time(), 
            #         time.time(), 
            #         time.time())
            # self._rx_queue.put(interferometer_data)
            # time.sleep(0.01)
            #are new values available?
            if bool(ifmdll.IfmValueCount(self._devNo)):
                #put the value in an internal buffer for access via IfmLengthValue
                #this is necessary to access the same syncronuously sampled values (e.g. different channels) at different times
                #IfmValueCount is decremented
                ifmdll.IfmGetValues(self._devNo)

                interferometer_data = InterferometerData(
                    ifmdll.IfmLengthValue(self._devNo,0), 
                    ifmdll.IfmLengthValue(self._devNo,1), 
                    ifmdll.IfmLengthValue(self._devNo,2), 
                    ifmdll.IfmTemperature(self._devNo,0), 
                    ifmdll.IfmAirPressure(self._devNo,0)
                )
                self._rx_queue.put(interferometer_data)
        logging.debug("ending interferometer loop...")

        # Send stop notification
        self._rx_queue.put(None)


def _rx_process_worker(com_port, rx_queue, stop_event):
    interferometer_controller = InterferometerSerial(com_port, rx_queue, stop_event)
    interferometer_controller.init_comm()
    interferometer_controller.start_reading_loop()
    interferometer_controller.stop_comm()


def _rx_thread_worker(rx_queue, rx_callback):
    logging.debug("starting interferometer callback loop...")
    while(True):
        interferometer_data = rx_queue.get()
        # Validate closing
        if interferometer_data is None:
            logging.debug("ending interferometer callback loop...")
            break
        rx_callback(interferometer_data)


class InterferometerController():
    def __init__(self, com_port, rx_callback):
        self._com_port = com_port
        self._rx_callback = rx_callback
    
        # Create locks and events
        self._rx_process_lock = multiprocessing.Lock()
        self._rx_thread_lock = threading.Lock()
        self._rx_started_process_event = multiprocessing.Event()
        self._rx_started_thread_event = threading.Event()

    def init_comm(self):
        try:
            # Acquire lock
            self._rx_process_lock.acquire()
            self._rx_thread_lock.acquire()

            if( (not self._rx_started_process_event.is_set()) and 
                    (not self._rx_started_thread_event.is_set()) ):
                # Create queue and stop event
                self._rx_process_queue = multiprocessing.Queue()
                self._stop_process_event = multiprocessing.Event()

                # Create and start process
                self._rx_process = multiprocessing.Process(target=_rx_process_worker, 
                    args=(self._com_port, self._rx_process_queue, self._stop_process_event))
                self._rx_thread = threading.Thread(target=_rx_thread_worker, 
                    args=(self._rx_process_queue, self._rx_callback))
                self._rx_process.start()
                self._rx_thread.start()
                time.sleep(3)

                # Set event flags
                self._rx_started_process_event.set()
                self._rx_started_thread_event.set()
            else: 
                logging.warning('interferometer communication already started')
        finally:
            # Release lock
            self._rx_thread_lock.release()
            self._rx_process_lock.release()

    def stop_comm(self):
        try:
            # Acquire lock
            self._rx_process_lock.acquire()
            self._rx_thread_lock.acquire()

            if( (self._rx_started_process_event.is_set()) and 
                    (self._rx_started_thread_event.is_set()) ):
                # Stop queue, process and thread
                self._stop_process_event.set()
                self._rx_process.join()
                self._rx_thread.join()

                self._rx_process_queue.close()
                self._rx_process_queue.join_thread()

                # Clear event flags
                self._rx_started_process_event.clear()
                self._rx_started_thread_event.clear()
            else:
                logging.warning('interferometer communication is not running')
        finally:
            # Release lock
            self._rx_thread_lock.release()
            self._rx_process_lock.release()

        