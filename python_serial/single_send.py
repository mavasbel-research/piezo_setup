import serial
import time

V_MAX = 1200
V_MIN = -1200

volt = 0
volt = max(V_MIN, min(volt, V_MAX)) #Clamp value
volt_dac = round((volt/(V_MAX-V_MIN) + 0.5)*0xFFFF)
volt_bytes = (volt_dac&0xFFFF).to_bytes(2, byteorder='big')

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM4'
ser.timeout = 2
ser.writeTimeout = 2

ser.open()
time.sleep(2)
if(not ser.is_open):
    raise Exception('Serial is not open')
    print(ser)

ser.write(volt_bytes)
print('Sent: ' + volt_bytes.hex())
recv = ser.readline()
print('Recv: ' + recv.hex())

ser.close()