import signal
import logging
import threading
import serial
import time
import keyboard

from queue import Queue
from collections import deque
from stoppable_loop_thread import StoppableLoopThread

import rx
import sys

#Serial paremters
BAUDRATE = 115200
SERIAL_PORT = 'COM4'
RX_TIMEOUT = 2
TX_TIMEOUT = 2

#Amplifier paramters
V_MAX = 10
V_MIN = -10

# CRC computation
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

#Serial tx worker
def tx_worker(ser, values_deque):
    if(len(values_deque)>0):
        #Convert value for DAC
        value = values_deque.popleft()
        value = max(V_MIN, min(value, V_MAX)) #Clamp value
        value_dac = round((value/(V_MAX-V_MIN) + 0.5)*0xFFFF)
        value_bytes = (value_dac&0xFFFF).to_bytes(2, byteorder='big')
        value_crc = crc8(value_bytes).to_bytes(1, byteorder='big')

        logging.debug("sending volts:%4.2f, DAC:%5s, HEX:%4s, CRC:%2s", 
            value, value_dac, value_bytes.hex(), value_crc.hex())
        ser.write(value_bytes + value_crc)
        recv = ser.read(3)
        logging.debug("received HEX:%4s, CRC:%2s", recv.hex()[0:4], recv.hex()[4:6])
    return 0

def main():
    #Logger configuration
    format_string = "%(asctime)s.%(msecs)03d - %(levelname)5s - %(threadName)10s : %(message)s"
    logging.basicConfig(format=format_string, level=logging.DEBUG, datefmt="%H:%M:%S")

    #Serial port configuration
    ser = serial.Serial()
    ser.baudrate = BAUDRATE
    ser.port = SERIAL_PORT
    ser.timeout = RX_TIMEOUT
    ser.writeTimeout = TX_TIMEOUT

    #Open serial port
    ser.open()
    time.sleep(2)
    if(not ser.is_open):
        raise Exception('Serial is not open')
        print(ser)
        exit()
    
    #Queue for voltage values
    tx_deque = deque(maxlen=100)
    tx_deque.append(0.0)
    
    #Tx task thread
    tx_thread = StoppableLoopThread( target=tx_worker, args=(ser, tx_deque) )
    tx_thread.start()
    while(True):
        try:
            user_input = input()
            volts = float(user_input)
            tx_deque.append(volts)
        except ValueError as ve:
            logging.error("%s", ve)
        except KeyboardInterrupt as ke:
            logging.info('exit...')
            tx_deque.append(0.0)
            while(len(tx_deque)>0): pass
            tx_thread.stop()
            tx_thread.join()
            ser.close()
            exit(0)
        except Exception as oe:
            logging.error("input error: %s", oe)

if __name__ == "__main__":
    main()