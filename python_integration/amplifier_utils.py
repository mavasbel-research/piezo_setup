import time
import serial
import threading
import multiprocessing
import inspect
import logging


logger = logging.getLogger()


def crc8(data):
    crc = 0
    for i in range(len(data)):
        byte = data[i]
        for b in range(8):
            fb_bit = (crc ^ byte) & 0x01
            if fb_bit == 0x01:
                crc = crc ^ 0x18
            crc = (crc >> 1) & 0x7f
            if fb_bit == 0x01:
                crc = crc | 0x80
            byte = byte >> 1
    return crc


class AmplifierSerial():
    def __init__(self, v_max=10, v_min=-10,
        com_port=None, baudrate=115200, rx_timeout=1, tx_timeout=1):
        # save all arguments passed to __init__
        attrs = vars()
        for attr in inspect.getargspec(attrs['self'].__init__).args[1:]:
            setattr(self, attr, attrs[attr])

        # serial port
        self._ser = serial.Serial()
    
    def open_serial_port(self):
        logger.info("amplifier opening port: %s" % self.com_port)
        self._ser.baudrate = self.baudrate
        self._ser.port = self.com_port
        self._ser.timeout = self.rx_timeout
        self._ser.writeTimeout = self.tx_timeout
        self._ser.open()
        time.sleep(3)
        if(not self._ser.is_open):
            logger.error(self._ser)
            raise Exception('amplifier serial is not open')

    def close_serial_port(self):
        logger.info("amplifier closing port: %s" % self.com_port)
        self._ser.close()

    def send_voltage(self, value, tx_delay=0.0):
        value = max(self.v_min, min(value, self.v_max)) # clamp value
        value_dac = round((-value/(self.v_max-self.v_min) + 0.5)*0xFFFF)
        value_bytes = (value_dac&0xFFFF).to_bytes(2, byteorder='big', signed=False)
        value_crc = crc8(value_bytes).to_bytes(1, byteorder='big', signed=False)

        logger.debug("amplifier sending  volts:%5.2f, DAC:%5s, HEX:%4s, CRC:%2s" % 
            (value, value_dac, value_bytes.hex(), value_crc.hex()) )
        self._ser.write(value_bytes + value_crc)
        # recv = self._ser.read(3)
        # recv = value_bytes + recv
        # recv = (0).to_bytes(3, byteorder='big', signed=False)
        # recv_int = int.from_bytes(recv[0:2], byteorder='big', signed=False)
        # recv_volts = (-((recv_int/0xFFFF) - 0.5)*(self.v_max-self.v_min))
        # logger.debug("amplifier received volts:%5.2f, DAC:%5s, HEX:%4s, CRC:%2s" % 
        #     (recv_volts, recv_int, recv.hex()[0:4], recv.hex()[4:6]) )
        

def tx_worker(v_max, v_min, com_port, baudrate, 
        rx_timeout, tx_timeout, tx_delay, queue):
    amplifier_serial = AmplifierSerial(v_max, v_min, 
        com_port, baudrate, rx_timeout, tx_timeout)

    try:
        amplifier_serial.open_serial_port() # open serial port
        logger.info("amplifier starting queue listening...")
        loop_start_time = time.time()
        while True:
            tx_start_time = time.time()
            value = queue.get() # get next value in queue
            if value is None: # validate process stop
                logger.debug("amplifier ending queue listening...")
                break
            amplifier_serial.send_voltage(value) # send value
            tx_elapsed_time = time.time() - tx_start_time
            time.sleep( max( 0.0, tx_delay-tx_elapsed_time ) )
            # logger.debug("amplifier sending elapsed time: %2.4f" % (time.time()-tx_start_time))
        loop_end_time = time.time()
        logger.info("amplifier queue listening elapsed time: %4.6f" % (loop_end_time-loop_start_time) )
    finally:
        amplifier_serial.close_serial_port() # close serial port


class AmplifierController:
    def __init__(self, v_max=10, v_min=-10, com_port=None, baudrate=115200, 
        rx_timeout=1, tx_timeout=1, tx_delay=0.01):
        """
            This constructor should always be called with keyword arguments. Arguments are:

            *v_max* is the maximum voltage of the amplifier output.

            *v_min* is the minimum voltage of the amplifier output.

            *tx_delay* is the time delay after each value dequeued and sent.

            *com_port* is the serial port number (ex: 'COM1').

            *baudrate* is the serial port baudrate.

            *rx_timeout* is the serial port read timeout.

            *tx_timeout* is the serial port write timeout.
        """
        # save all arguments passed to __init__
        attrs = vars()
        for attr in inspect.getargspec(attrs['self'].__init__).args[1:]:
            setattr(self, attr, attrs[attr])

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

    def _started_set(self):
        self._process_event.set()
        self._thread_event.set()

    def _started_clear(self):
        self._process_event.clear()
        self._thread_event.clear()

    def is_started(self):
        return self._process_event.is_set() or self._thread_event.is_set()
        
    def get_queue(self):
        try:
            self._lock_acquire()
            if( not self.is_started() ):
                raise Exception('amplifier communication is not running')
            else:
                return self._queue
        finally:
            self._lock_release()
    
    def init_comm(self):
        try:
            self._lock_acquire()
            if( self.is_started() ): # validate process is not running
                raise Exception('amplifier communication already started')
            else: 
                self._queue = multiprocessing.Queue() # create queue
                self._process = multiprocessing.Process( # create process
                    target=tx_worker,
                    args=(self.v_max, self.v_min, self.com_port, self.baudrate, 
                        self.rx_timeout, self.tx_timeout, self.tx_delay, self._queue)) 
                self._process.start() # start process
                self._started_set()
                time.sleep(1)
                return self._queue
        finally:
            self._lock_release()

    def send_value(self, value):
        try:
            self._lock_acquire()
            if( value==None ): 
                raise Exception('amplifier value must be different from None')
            if( not self.is_started() ): # validate process is running
                raise Exception('amplifier communication is not running')
            else:
                self._queue.put(value) 
        finally:
            self._lock_release()

    def end_comm(self):
        try:
            self._lock_acquire()
            if( not self.is_started() ): # validate process is running
                raise Exception('amplifier communication is not running')
            else: 
                self._queue.put(0.0) # set final value to 0
                self._queue.put(None) # send closing signal
                self._queue.close()
                self._queue.join_thread()
                self._process.join()
                self._started_clear() # clear started event
        finally:
            self._lock_release()