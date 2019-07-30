import time
import logging
import serial
import threading
import multiprocessing


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
    def __init__(self, v_max, v_min, tx_delay, tx_process_queue, 
        com_port, baudrate, rx_timeout, tx_timeout):
        # Amplifier paramters
        self._v_max = v_max
        self._v_min = v_min
        self._tx_delay = tx_delay

        # Serial port configuration
        self._com_port = com_port
        self._baudrate = baudrate
        self._rx_timeout = rx_timeout
        self._tx_timeout = tx_timeout

        # Queue and serial port
        self._tx_process_queue = tx_process_queue
        self._ser = serial.Serial()
    
    def open_serial_port(self):
        self._ser.baudrate = self._baudrate
        self._ser.port = self._com_port
        self._ser.timeout = self._rx_timeout
        self._ser.writeTimeout = self._tx_timeout

        self._ser.open()
        time.sleep(2)
        if(not self._ser.is_open):
            print(self._ser)
            raise Exception('amplificer serial is not open')

    def close_serial_port(self):
        self._ser.close()

    def start_tx_loop(self):
        # Sending loop
        logging.debug("starting amplifier tx loop...")
        loop_start_time = time.time()
        while True:
            value = self._tx_process_queue.get()

            # Validate closing
            if value is None:
                logging.debug("ending amplifier tx loop...")
                break

            # Convert value for DAC
            value = max(self._v_min, min(value, self._v_max)) # Clamp value
            value_dac = round((value/(self._v_max-self._v_min) + 0.5)*0xFFFF)
            value_bytes = (value_dac&0xFFFF).to_bytes(2, byteorder='big')
            value_crc = crc8(value_bytes).to_bytes(1, byteorder='big')

            logging.debug("amplifier sending  volts:%4.2f, DAC:%5s, HEX:%4s, CRC:%2s", 
                value, value_dac, value_bytes.hex(), value_crc.hex())
            
            tx_start_time = time.time()
            self._ser.write(value_bytes + value_crc)
            recv = self._ser.read(3)
            tx_end_time = time.time()

            recv_int = int.from_bytes(recv[0:2], byteorder='big', signed=False)
            recv_volts = ((recv_int/0xFFFF) - 0.5)*(self._v_max-self._v_min)
            logging.debug("amplifier received volts:%4.2f, DAC:%5s, HEX:%4s, CRC:%2s, elapsed time: %4.6f", 
                recv_volts, recv_int, recv.hex()[0:4], recv.hex()[4:6], tx_end_time-tx_start_time)

            time.sleep(self._tx_delay)
        
        loop_end_time = time.time()
        logging.debug("amplifier loop elapsed time: %4.6f", loop_end_time-loop_start_time)


def _tx_worker(v_max, v_min, tx_delay,  tx_process_queue,
        com_port, baudrate, rx_timeout, tx_timeout):
    amplifier_serial_controller = AmplifierSerial(
        v_max, v_min, tx_delay, tx_process_queue,
        com_port, baudrate, rx_timeout, tx_timeout)
    amplifier_serial_controller.open_serial_port()
    amplifier_serial_controller.start_tx_loop()
    amplifier_serial_controller.close_serial_port()


class AmplifierController:
    def __init__(self, v_max=10, v_min=-10, tx_delay=0.01, 
        com_port=None, baudrate=115200, rx_timeout=2, tx_timeout=2):
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
        # Amplifier paramters
        self._v_max = v_max
        self._v_min = v_min
        self._tx_delay = tx_delay

        # Serial port configuration
        self._com_port = com_port
        self._baudrate = baudrate
        self._rx_timeout = rx_timeout
        self._tx_timeout = tx_timeout

        # Create locks and events
        self._tx_process_lock = multiprocessing.Lock()
        self._tx_thread_lock = threading.Lock()
        self._tx_started_process_event = multiprocessing.Event()
        self._tx_started_thread_event = threading.Event()

    def init_comm(self):
        try:
            # Acquire lock
            self._tx_process_lock.acquire()
            self._tx_thread_lock.acquire()

            # Validate process is not running with event flag
            if( (not self._tx_started_process_event.is_set()) and 
                    (not self._tx_started_thread_event.is_set()) ):
                # Create queue
                self._tx_process_queue = multiprocessing.Queue()

                # Create and start process
                self._tx_process = multiprocessing.Process(target=_tx_worker, 
                    args=(self._v_max, self._v_min, self._tx_delay,  self._tx_process_queue,
                    self._com_port, self._baudrate, self._rx_timeout, self._tx_timeout))
                self._tx_process.start()
                time.sleep(2)

                # Set event flags
                self._tx_started_process_event.set()
                self._tx_started_thread_event.set()
            else: 
                logging.warning('amplifier communication already started')
        finally:
            # Release lock
            self._tx_thread_lock.release()
            self._tx_process_lock.release()

    def send_value(self, value):
        try:
            # Acquire lock
            self._tx_process_lock.acquire()
            self._tx_thread_lock.acquire()

            # Validate process is running with event flag
            if( (self._tx_started_process_event.is_set()) and 
                    (self._tx_started_thread_event.is_set()) ):
                # Put value in queue
                self._tx_process_queue.put(value)
            else: 
                raise Exception('amplifier communication is not running')
        finally:
            # Release lock
            self._tx_thread_lock.release()
            self._tx_process_lock.release()

    def stop_comm(self):
        try:
            # Acquire lock
            self._tx_process_lock.acquire()
            self._tx_thread_lock.acquire()

            # Validate process is running with event flag
            if( (self._tx_started_process_event.is_set()) and 
                    (self._tx_started_thread_event.is_set()) ):
                # Stop queue and process
                self._tx_process_queue.put(0.0) # Set final value to 0
                self._tx_process_queue.put(None) # Send closing signal
                self._tx_process_queue.close()
                self._tx_process_queue.join_thread()
                self._tx_process.join()

                # Clear event flags
                self._tx_started_process_event.clear()
                self._tx_started_thread_event.clear()
            else: 
                logging.warning('amplifier communication is not running')
        finally:
            # Release lock
            self._tx_thread_lock.release()
            self._tx_process_lock.release()