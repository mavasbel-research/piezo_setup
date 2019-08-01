import random
import time
import msvcrt
import logging
import threading
import multiprocessing
from siosifm import *           #Import modules
from ctypes import *            #(Own writing module is siosifm.py)
from collections import namedtuple


logger = logging.getLogger()


InterferometerData = namedtuple('InterferometerData', ['channel_1', 'channel_2', 'channel_3', 'temperature', 'pressure'])
InterferometerQuality = namedtuple('InterferometerQuality', ['channel_1', 'channel_2', 'channel_3'])


class InterferometerSerial:
    def __init__(self, com_port):
        self._sleep = 2
        self._dev_no = 0
        self.com_port = com_port

    def init_dll(self):
        logger.info("interferometer initializing DLL...")
        error = 0
        error = ifmdll.IfmInit() # initialize the library
        if bool(error): # negative values are error numbers
            raise Exception("interferometer error during IfmInit: %s" % error)

    def open_com(self):
        logger.info("interferometer opening device...")
        self._dev_no = ifmdll.IfmOpenCOM(self.com_port)
        if self._dev_no < 0: # negative values are error numbers
            raise Exception("interferometer error during opening the device")
        logger.info("interferometer device no.: %s" % self._dev_no)

    def set_config(self, freq):
        logger.info("interferometer setting config...")
        error = 0
        error = ifmdll.IfmSetTrigger(self._dev_no, IFM_TRIGGER_OFF)
        if bool(error):
            raise Exception("interferometer error during setting trigger mode.")
        #error = ifmdll.IfmSetMeasurement(devNo, IFM_MEAS_FILTER_DEFAULT | IFM_MEAS_LENGTH , c_double(10))
        error = ifmdll.IfmSetMeasurement(self._dev_no, IFM_MEAS_FOURCHANNEL|IFM_MEAS_LENGTH|IFM_MEAS_FILTER_DEFAULT, c_double(freq))
        if bool(error):
            raise Exception("interferometer error during setting measurement mode.")
        time.sleep(self._sleep)

    def is_quality_available(self):
        return bool(ifmdll.IfmNewSignalQualityAvailable(self._dev_no))

    def read_quality(self):
        return InterferometerQuality(
            ifmdll.IfmSignalQuality(self._dev_no, 0, IFM_SIGNALQ_SUM),
            ifmdll.IfmSignalQuality(self._dev_no, 1, IFM_SIGNALQ_SUM),
            ifmdll.IfmSignalQuality(self._dev_no, 2, IFM_SIGNALQ_SUM))

    def set_to_zero(self):
        error = 0
        # set the length values to zero; assuming the measurement mirror is at the reference/zero position
        error = ifmdll.IfmSetToZero(self._dev_no, 0x0F) 
        if bool(error):
            raise Exception("interferometer error during set to zero.")
        
    def start_output(self):
        logger.info("interferometer starting output...")
        error = 0
        # start with data output
        error = ifmdll.IfmStart(self._dev_no) # begin with the output of data
        if bool(error):
            raise Exception("interferometer error during output start.")

    def is_data_avilable(self): # are new values available?
        return bool(ifmdll.IfmValueCount(self._dev_no))

    def read_output(self):
        # put the value in an internal buffer for access via IfmLengthValue
        # this is necessary to access the same syncronuously sampled values (e.g. different channels) at different times
        # IfmValueCount is decremented
        ifmdll.IfmGetValues(self._dev_no)
        return InterferometerData(
            ifmdll.IfmLengthValue(self._dev_no, 0), 
            ifmdll.IfmLengthValue(self._dev_no, 1), 
            ifmdll.IfmLengthValue(self._dev_no, 2), 
            ifmdll.IfmTemperature(self._dev_no, 0), 
            ifmdll.IfmAirPressure(self._dev_no, 0))
        
    def clear_buffer(self):
        error = 0
        error = ifmdll.IfmClearBuffers(self._dev_no) 
        if bool(error):
            raise Exception("interferometer error during clear buffer.")

    def stop_output(self):
        logger.info("interferometer stopping output...")
        ifmdll.IfmStop(self._dev_no) # stop the output of data

    def close_com(self):
        logger.info("interferometer closing device...")
        ifmdll.IfmCloseDevice(self._dev_no) # close the device; devNo will be no longer valid

    def close_dll(self):
        logger.info("interferometer closing DLL...")
        ifmdll.IfmClose() # close the DLL


def interf_worker(com_port, freq, measure_event, exit_event, queue):
    intfm_ctrl = InterferometerSerial(com_port)
    try:
        intfm_ctrl.init_dll()
        try:
            intfm_ctrl.open_com()
            intfm_ctrl.set_config(freq)
            try:
                intfm_ctrl.set_to_zero()
                logger.info("interferometer starting loop...")
                while(not exit_event.is_set()):
                    if(measure_event.is_set()):
                        intfm_ctrl.start_output()
                        while( measure_event.is_set() and not exit_event.is_set() ):
                            ########### Test code
                            data = random.randint(-1200, 1200)
                            data = InterferometerData(data, data, data, data, data)
                            logger.debug("interferometer simulated value: %i" % data.channel_1)
                            queue.put(data)
                            time.sleep(0.001)
                            ###########
                            if(intfm_ctrl.is_data_avilable()):
                                data = intfm_ctrl.read_output()
                                queue.put(data)
                        intfm_ctrl.stop_output()
                        intfm_ctrl.clear_buffer()
                    else:
                        ########### Test code
                        quality = random.randint(0, 100)
                        quality = InterferometerQuality(quality, quality, quality)
                        logger.debug("interferometer simulated quality: %i" % quality.channel_1)
                        queue.put(quality)
                        time.sleep(0.5)
                        ###########
                        if(intfm_ctrl.is_quality_available()):
                            quality = intfm_ctrl.read_quality()
                            queue.put(quality())
                logger.info("interferometer ending loop...")
            finally:
                intfm_ctrl.stop_output()
        finally:
            intfm_ctrl.close_com()
    finally:
        queue.put(None)
        intfm_ctrl.close_dll()


class InterferometerController():
    def __init__(self, com_port=None, freq=100):
        self.com_port = com_port
        self.freq = freq
    
        # create locks and events
        self._process_lock = multiprocessing.Lock()
        self._thread_lock = threading.Lock()
        self._process_event = multiprocessing.Event()
        self._thread_event = threading.Event()

    def _lock_acquire(self): # private method to acquire locks
        self._process_lock.acquire()
        self._thread_lock.acquire()
    
    def _lock_release(self): # private method to release locks
        self._thread_lock.release()
        self._process_lock.release()

    def _init_set(self):
        self._process_event.set()
        self._thread_event.set()

    def _init_clear(self):
        self._process_event.clear()
        self._thread_event.clear()

    def is_init(self):
        return self._process_event.is_set() or self._thread_event.is_set()

    def get_queue(self):
        try:
            self._lock_acquire()
            if( not self.is_init() ):
                raise Exception('interferometer communication is not running')
            else:
                return self._queue
        finally:
            self._lock_release()

    def measure_event(self):
        try:
            self._lock_acquire()
            if( not self.is_init() ):
                raise Exception('interferometer communication is not running')
            else:
                return self._measure_event
        finally:
            self._lock_release()

    def init_comm(self):
        try:
            self._lock_acquire()
            if( self.is_init() ):
                raise Exception('interferometer communication already started')
            else:
                self._queue = multiprocessing.Queue()
                self._exit_event = multiprocessing.Event()
                self._measure_event = multiprocessing.Event()

                self._process = multiprocessing.Process(
                    target=interf_worker, 
                    args=(self.com_port, self.freq, 
                        self._measure_event, self._exit_event, self._queue))
                self._process.start()
                self._init_set()
                time.sleep(1)
                return self._queue, self._measure_event
        finally:
            self._lock_release()

    def end_comm(self):
        self._lock_acquire()
        try:
            if( not self.is_init() ):
                raise Exception('interferometer communication is not running')
            else:
                self._exit_event.set()
                self._process.join()
                self._queue.close()
                self._queue.join_thread()
                self._init_clear()
        finally:
            self._lock_release()
