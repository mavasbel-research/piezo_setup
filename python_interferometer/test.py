#Created by: SIOS Meßtechnik GmbH
#--------------------------------------------------------------------------------

from siosifm import *           #Import modules
from ctypes import *            #(Own writing module is siosifm.py)
import time
import msvcrt

sleep = 2                                   #Sleeping time after errors
devNo = 0                                   #Device Number set to 0
text_file = open('measurement.txt', 'w')    #Open the Textdocument measurement.txt

#--------------------------------------------------------------------------------

def initialize():                           #define functions "initialize"

    error = 0
    # Initialize the library
    error = ifmdll.IfmInit()
    if bool(error):
        print("Error %s during IfmInit" % error)
        time.sleep(sleep)
        exit()                              #Closing after errors
    
    #devNo = IfmOpenUSB(0)
    devNo = ifmdll.IfmOpenCOM(4)
    print("Device No.: %s" % devNo)
    if devNo < 0:          #negative values are error numbers
        print("Error during opening the device.")
        IfmClose()
        time.sleep(sleep)
        exit()

    #Alternatively, if the COM-Interface is known the device can also be opened directly
    #Windows: devNo=IfmOpenCom(1); for COM1
    #Unix:    devNo=IfmOpenCom("/dev/ttyACM0"); for the first device

    #IfmOpenUSB has returned a number (devNo) which describes the device in further calls
    #to the DLL.

    #now we configure the measurement, at least with SetMeasurement
    #we want the length values of the first channel with 0.5 Hz output rate
    #IFM_MEAS_FILTER_DEFAULT will create an internal filter which removes the
    #vibration of the reference mirror from the signal
    #in some applications IFM_MEAS_FILTER_NONE may be required for unfiltered output
    error = ifmdll.IfmSetTrigger(devNo, IFM_TRIGGER_OFF)
    if bool(error):
        print("Error during setting trigger mode.")
        IfmClose()
        time.sleep(sleep)
        exit()

    #error = ifmdll.IfmSetMeasurement(devNo, IFM_MEAS_FILTER_DEFAULT | IFM_MEAS_LENGTH , c_double(10))
    error = ifmdll.IfmSetMeasurement(devNo, IFM_MEAS_FOURCHANNEL|IFM_MEAS_LENGTH|IFM_MEAS_FILTER_DEFAULT , c_double(100))
    if bool(error):
        print("Error during setting measurement mode.")
        IfmClose()
        time.sleep(sleep)
        exit()
    time.sleep(1)
        
#--------------------------------------------------------------------------------

def main():
    #Set the length values to zero; assuming the measurement mirror is at the reference/zero position
    error = ifmdll.IfmSetToZero(devNo, 0x0F)

    #begin with the output of data
    error = ifmdll.IfmStart(devNo)
    if bool(error):
        print("Error during start out put.")
        IfmClose()
        time.sleep(sleep)
        exit()

    i = 0
    while True:
        #are new values available?
        while bool(ifmdll.IfmValueCount(devNo)):
            #put the value in an internal buffer for access via IfmLengthValue
            #this is necessary to access the same syncronuously sampled values (e.g. different channels) at different times
            #IfmValueCount is decremented
            ifmdll.IfmGetValues(devNo)
            #get the value together with environmental values
            print("Measurement %d: %s nm %s nm %s nm - %s C %s Pa" % ((i+1), IfmLengthValue(devNo,0), IfmLengthValue(devNo,1), IfmLengthValue(devNo,2), IfmTemperature(devNo,0), IfmAirPressure(devNo,0)))
            text_file.write("%d; %s; %s; %s; %s; %s;\n" % (i, IfmLengthValue(devNo,0), IfmLengthValue(devNo,1), IfmLengthValue(devNo,2), IfmTemperature(devNo,0), IfmAirPressure(devNo,0)))
            i = i + 1
        if msvcrt.kbhit() == True:
            break

    print()
    print("Measurement completed.")         #printing on console
    time.sleep(1)

#--------------------------------------------------------------------------------

def deinitialize():             #define functions "deinitialize"
    #deinitialize
    text_file.close()           #close text file
    print("Closed text file.\n [Note: in text file all measurements.]")
    #stop the output of data
    ifmdll.IfmStop(devNo)
    print("Stopped output Data.")
    #close the device; devNo will be no longer valid
    ifmdll.IfmCloseDevice(devNo)
    print("Closed Device.")
    #close the DLL
    ifmdll.IfmClose()
    print("Closed DLL.")
    time.sleep(1)

#--------------------------------------------------------------------------------

initialize()
main()
deinitialize()
