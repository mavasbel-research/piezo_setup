#!/usr/bin/python
#Filename: siosifm.py

from ctypes import *

ifmdll = cdll.siosifm   #load SIOS - dll

#other constants
IFM_MAX_CHANNELS =          4           #one device supports up to 4 channels
IFM_MAX_INTERNAL_SENSORS =  (4*6)
IFM_MAX_EXTERNAL_SENSORS =  16
IFM_MAX_ENVIR_SENSORS =     (IFM_MAX_EXTERNAL_SENSORS+IFM_MAX_INTERNAL_SENSORS)     #max. amount of environment sensors


IFM_I2C_MAXLEN = 160    #for read/write requests with the IfmI2C... functions, max count of transfered data

IFM_MIN_TEMP =          4           #°C
IFM_MAX_TEMP =          50
IFM_MIN_AIRPRESSURE =   85000       #Pa
IFM_MAX_AIRPRESSURE =   120000
IFM_MIN_HUMIDITY =      3           #%
IFM_MAX_HUMIDITY =      99

IFM_SYNTHETIC_WAVELENGTH = 632.83       #the DP-10 and IO-10 modules have the option to correct the values
                                        #for the environment influences
                                        #the corrected values seems to be derived from this synthetic wavelength

#-----------------------------------------------------Flags for settings of the parameter triggerMode in  the function :---------------------------
#----------------------------------------------int IfmSetTrigger(int devNumber, unsigned int triggerMode);-----------------------------------------
#Functions for starting and stopping measurements
IFM_TRIGGER_OFF = 0


#Trigger-Input:
IFM_TRIGGER_START =             0x0001  #start of measuring values after a valid (falling or rising) edge
IFM_TRIGGER_STARTSTOP_PROC =    0x0002  #the StartStop-input of processed values
IFM_TRIGGER_STARTSTOP =         0x0004  #the StartStop-input of raw values
IFM_TRIGGER_SET_TO_ZERO =       0x8000  #the StartStop-input for set-to-zero

#Clock-Input
IFM_TRIGGER_CLOCK = 0x0008              #clocks in unprocessed values from the counter/interpolator unit
                                        #It can be used to use an external sample rate or
                                        #to synchronize the sampling with external hardware (for example, incremental encoders)

#Event-Input
IFM_TRIGGER_EVENT = 0x0010              #takes a processed value and sends it to the PC

#Edge definitions for Trigger
IFM_TRIGGER_CLOCK_RISING_EDGE =     0x0100      #rising edge in the ext. clock input is validly
IFM_TRIGGER_STARTSTOP_RISING_EDGE = 0x0200      #rising edge in the trigger  input is validly
IFM_TRIGGER_EVENT_RISING_EDGE =     0x0400      #rising edge in the event input is validly

#Data rate of external clock or single value, for internal use only
IFM_OWR_FAST = 0x1000                   #fast data rate (OWR>200 Hz)
IFM_OWR_SLOW = 0x2000                   #slow data rate (OWR<=200Hz)
#-----------------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------Flags for settings of the parameter filterFlags in the function------------------------------
#-------------------------------------------------------int IfmSetFilter(int devNumber, unsigned int filterFlags,int avg1, int avg2)------------------
#for experts only
IFM_FILTER_STAGE1 = 0x01                #Filter stage 1 (FIR) is on
IFM_FILTER_STAGE2 = 0x02                #Filter stage 2 (avg2) is on

IFM_FILTER_AVG9 =   0x04                #AVG9 in stage 3 is on
IFM_FILTER_AVG6 =   0x08                #AVG6 in stage 3 is on
IFM_FILTER_AVG5 =   0x10                #AVG5 in stage 3 is on

IFM_FILTER_STAGE3 = (IFM_FILTER_AVG9|IFM_FILTER_AVG6|IFM_FILTER_AVG5)   #Filter stage 3 is on
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------Flags for settings of measurementFlags in  the function :-----------------------------------------
#----------------------------------------------IfmSetMeasurement(int devNumber,unsigned int measurementFlags, int outputWordRate)-----------------------
IFM_MMASK_DEFAULT = 0x0106  		#One channel, , SINX + COSX

#Field "MeasurementFlags", mask definition
IFM_MEAS_ONECHANNEL =   0x0100          #Channel number 1 is on
IFM_MEAS_TWOCHANNEL =   0x0300          #Channel number 1 and 2 are on
IFM_MEAS_THREECHANNEL = 0x0700          #Channel number 1 to 3 are on
IFM_MEAS_FOURCHANNEL =  0x0F00          #Channel number 1 to 4 are on

IFM_MEAS_TWOCHANNELS =   IFM_MEAS_TWOCHANNEL
IFM_MEAS_THREECHANNELS = IFM_MEAS_THREECHANNEL
IFM_MEAS_FOURCHANNELS =  IFM_MEAS_FOURCHANNEL

IFM_MEAS_CH1 = 0x0100
IFM_MEAS_CH2 = 0x0200
IFM_MEAS_CH3 = 0x0400
IFM_MEAS_CH4 = 0x0800


IFM_MEAS_USERMODE =      0x0001                 #Reserved
IFM_MEAS_LENGTH =        0x0002                 #Full length information
IFM_MEAS_SINCOS =        0x0004                 #SINX / COSX
IFM_MEAS_CIRCLE =        0x0008                 #Amplitude of the lissagous figure
IFM_MEAS_PATTERN =       0x0010                 #Test pattern
IFM_MEAS_CLOCKCOUNT =    0x0020                 #Internal clock counter; 50MHz timebase
IFM_MEAS_VAL_COUNTER =   IFM_MEAS_CLOCKCOUNT    #for compatibility
IFM_MEAS_SAMPLECOUNT =   0x0080                 #Sample counter
IFM_MEAS_VAL_MASK =      (0x003F|0x0080)        #Selection of measurement values is coded in these bits
IFM_MEAS_BEAMBREAK_OFF = 0x0040                 #BeamBreak should not be monitored

IFM_MEAS_FILTER_DEFAULT =   0x0000              #The default filter is to use
IFM_MEAS_FILTER_OFF =       0x1000              #No filtering
IFM_MEAS_FILTER_USER =      0x2000              #The user filter is to use
IFM_MEAS_FILTER_MASK =      0x3000              #Filter flags are coded in these bits

IFM_MEAS_RAWMODE =  0x4000                      #Mode for testing purpose, do not use
#---------------------------------------------------------------------------------------------------------------------------------------------------------

#the channel mask for
#IfmSetToZero, IfmAngleValue, IfmAngleAvailable

IFM_CHANNEL1 =  0x01
IFM_CHANNEL2 =  0x02
IFM_CHANNEL3 =  0x04
IFM_CHANNEL4 =  0x08

#special for IfmAngleValue
#return the angle in seconds instead of mrad
IFM_ANGLE_SEC = 0x80



#IfmSensorProperty

#Internal note:
#Constants for IfmSensorProperty are also used in the environmental
#firmware, changes must be commited to the firmware sources!

#Type of the Sensor
IFM_ENVIR_SENSOR_TEMP =             0x10
IFM_ENVIR_SENSOR_HUMIDITY =         0x20
IFM_ENVIR_SENSOR_AIRPRESSURE =      0x30			
IFM_ENVIR_SENSOR_TEMP_MATERIAL =    0x40
IFM_ENVIR_SENSOR_TEMP_AUX =         0x50

#which channels is the sensor assigned?
IFM_ENVIR_CHANNEL1 =        0x01
IFM_ENVIR_CHANNEL2 =        0x02
IFM_ENVIR_CHANNEL3 =        0x04
IFM_ENVIR_CHANNEL4 =        0x08

#Flag to mark the values for Edlen-corection
IFM_ENVIR_EDLEN =   0x80

#Sensor is extern, not port if interferometer unit
IFM_ENVIR_SENSOR_EXTERN =   0x0400

#channel and sensor type are coded in one byte
#the following masks allow better to distinguish
IFM_ENVIR_SENSORMASK =  0x0070      #in these bits the sensor type is coded (IFM_ENVIR_SENSOR_TEMP ...)
IFM_ENVIR_CHANNELMASK = 0x000F      #in these bits the assitiated channels are coded (IFM_ENVIR_CHANNEL1...)
IFM_ENVIR_VALID =       0x0100      #the sensor value was at least one time measured
IFM_ENVIR_CURRENT =     0x0200      #the sensor value was measured recently, the value is current or up-to-date

#-- End IfmSensorProperty


#IfmSetOptions
IFM_OPTION_DEBUGFILES =     0x0001  #param1==1 create debug files; param1==2 recreate debug files (delete old debug infos)
IFM_OPTION_POLLSELF =       0x0002  #IfmPoll is called by the application, otherwise the DLL starts a thread which calls IfmPoll
IFM_OPTION_BLOCKONCLOSE =   0x0003  #IfmCloseDevice blocks until the device is closed
IFM_OPTION_BOOTLOADER =     0x0004  #enables special mode for transfer new firmware code
IFM_OPTION_BEAMBREAK =      0x0005  #for the global IfmWasBeamBreak function exists two different beam break indicators which can be selected here
IFM_OPTION_ZEROPHASE =      0x0006  #during set to zero the angle part of the interferometer value can be cleared or not
IFM_OPTION_ZEROONCONNECT =  0x0007  #automatic zeroing on connect
IFM_OPTION_DEBUGLEVEL =     0x0008  #debugLevel>=2 prints the IfmLenghtValue and similar calls in the ifmdll.dbg file which let the debug file grow


#IfmDeviceInfo
#the following information can be requested with IfmDeviceInfo
IFM_DEVINFO_SRATE =             1       #current sampleRate (internal, before reduction by filters)
IFM_DEVINFO_OUTRATE =           2       #output word rate, like set by IfmSetMeasurement or saved in the flash
                                        #this is the real output wird rate, which may be differ from the selected due to steps in possible sample rate
IFM_DEVINFO_FILTERFLAGS =           3       #filter flags, like set by IfmSetFilter or saved in the flash
IFM_DEVINFO_MEASUREMENTFLAGS =      4       #mesurement flags, like set by IfmSetMeasurement or saved in the flash
IFM_DEVINFO_TRIGGERMODE =           5       #trigger mode, like set by IfmSetTrigger or or saved in the flash
IFM_DEVINFO_AVG1 =                  6       #filter option for the average 1, like set by IfmSetFilter or saved in the flash
IFM_DEVINFO_AVG2 =                  7       #filter option for the average 2, like set by IfmSetFilter or saved in the flash
IFM_DEVINFO_AVAILABLE =             8       #infos available, if not wait until the DLL has get it from the device
IFM_DEVINFO_SERIALNUMBER =          9       #return the (USB-) serial number of the card
IFM_DEVINFO_RESETSTATUS =           10      #resets the given bits in the device status
IFM_DEVINFO_READY =                 11      #ready for IfmStart
IFM_DEVINFO_VERSIONSTRING =         12      #Firmware-Version and compiling data
IFM_DEVINFO_FPGAVERSION =           13      #Version of the programmable hardware (FPGA)
IFM_DEVINFO_OUTRATE_POINTER =       14      #Pointer to a double value, containing the OWR in higher resolution
IFM_DEVINFO_LINKEDCHANNELS1 =       15      #wich channels are linked to calculate an angle
IFM_DEVINFO_LINKEDCHANNELS2 =       16      #there are two pairs of linked channels possible
IFM_DEVINFO_BASEDISTANCE1_POINTER = 17      #base distance of the linkes channels
IFM_DEVINFO_BASEDISTANCE2_POINTER = 18      #same for the second pair
IFM_DEVINFO_LAST_I2C_CARDADDR =     19      #card address of the active or last I2C request
IFM_DEVINFO_LAST_I2C_MEMADDR =      20      #memory address of the active or last I2C request
IFM_DEVINFO_SRATE_POINTER =         21      #pointer to the current sample rate (double value)
IFM_DEVINFO_PSD_COUNT =             22      #count of the available PSD-Sensors (lateral shift sensors)
IFM_DEVINFO_PSD_TYPE =              23      #type of PSD implementation, see below
IFM_DEVINFO_ELLFIT_STATUS =         24      #Heydemann-corr by Ellipse fitting: Status on or off
IFM_DEVINFO_ELLFIT_COSOFFS_POINTER =25      #Heydemann-corr by Ellipse fitting: pointer to double value of cosine offset
IFM_DEVINFO_ELLFIT_SINOFFS_POINTER =26      #Heydemann-corr by Ellipse fitting: pointer to double value of sine offset
IFM_DEVINFO_ELLFIT_PHI_POINTER =    27      #Heydemann-corr by Ellipse fitting: pointer to double value of phase angle
IFM_DEVINFO_ELLFIT_AR_POINTER =     28      #Heydemann-corr by Ellipse fitting: pointer to double value of amplitude ratio
IFM_DEVINFO_ELLFIT_AMPL_POINTER =   29      #Heydemann-corr by Ellipse fitting: pointer to double value of amplitude ratio
IFM_DEVINFO_ENVIRCOUNTER =          30      #counter of the environment measurement, use with sensor Number:
                                            #IFM_DEVINFO_ENVIRCOUNTER|(sensorNumber*256)
IFM_DEVINFO_DP10LSB =           31      #the parallel output of the DP-10 can be shifted , this request returns the shift value
                                        #the LSB of the DP-10 is wavelength/pow(2,17-IfmDeviceInfo(devNo,IFM_DEVINFO_DP10LSB))
                                        #the values may be different for each channel, request (channel*256)|IFM_DEVINFO_DP10LSB

IFM_DEVINFO_DEVICESERIALNUMBER_POINTER =    32      #return a pointer to a char[12] which contains the serial number of the electronic unit

IFM_DEVINFO_CMDDELAY =      100     #delay in ms between transmitted commands
IFM_DEVINFO_I2CTIMEOUT =    101     #timeout in ms for IfmI2CRead and IfmI2CWrite


#Type of PSD implementation, returned with IFM_DEVINFO_PSD_TYPE

IFM_PSDTYPE_NONE =  0       #no PSD available
IFM_PSDTYPE_CARD =  1       #PSD based on PSD-04 card, slow rate approx 1-4 samples per second
IFM_PSDTYPE_ADU =   2       #PSD based on special ADU card; fast data rate like interferometer values


#IfmHasDeviceProperty

IFM_PROPERTY_BLOCKMODE =    1
IFM_PROPERTY_PSD =          2



#types for IfmAuxValues

IFM_VALUETYPE_COS =         1
IFM_VALUETYPE_ADC1 =        1
IFM_VALUETYPE_SIN =         2
IFM_VALUETYPE_ADC2 =        2
IFM_VALUETYPE_NORM =        3
IFM_VALUETYPE_TESTPATTERN = 4
IFM_VALUETYPE_CLOCKCOUNT =  5
IFM_VALUETYPE_COUNTER =     5
IFM_VALUETYPE_SAMPLECOUNT = 6
IFM_VALUETYPE_PSD_X =       7       #lateral displacement via PSD in 10nm steps
IFM_VALUETYPE_PSD_Y =       8
IFM_VALUETYPE_PSDRAW_X =    9       #lateral displacement via PSD in 10nm steps
IFM_VALUETYPE_PSDRAW_Y =    10
IFM_VALUETYPE_PSD_SUM =     11      #energy on the PSD

#Parameter select for IfmSignalQuality(int devNumber,int channel, int select)
IFM_SIGNALQ_A1 =        0x10        #Amplitude of the signal 1
IFM_SIGNALQ_O1 =        0x20        #Offset of the signal 2
IFM_SIGNALQ_A2 =        0x40        #Amplitude of the signal 2
IFM_SIGNALQ_O2 =        0x80        #Offset of the signal 2
IFM_SIGNALQ_SUM =       0x100       #Overall quality from 0..100%
IFM_SIGNALQ_FREQ =      0x200       #Frequency of the reference mirror vibrator
IFM_SIGNALQ_STATE =     0x400       #Status of the signal control card; for internal use


#IfmManualEnvironment
IFM_ENVIR_MANUAL_T =    0x0002      #the temperatur was set manually
IFM_ENVIR_MANUAL_H =    0x0004      #the humidity was set manually
IFM_ENVIR_MANUAL_P =    0x0008      #the air pressure was set manually
IFM_ENVIR_MANUAL_WVP =  0x0010      #the water vapour pressure was set manually
IFM_ENVIR_MANUAL_CONV = 0x0020      #the conversion coefficient was set manually
#IFM_ENVIR_MANUAL_WL =  0x0040
IFM_ENVIR_MANUAL_VWL =  0x0080      #the vacuum wavelength of the laser was set manually



#IfmTemperatureFlags, IfmAirPressureFlags, IfmHumidityFlags
IFM_ENVIRFLAG_SENSORMASK =  0x00FF  #in these bits the sensor number is coded, where the value was measured
IFM_ENVIRFLAG_MEASURED =    0x0100  #the value was measured; otherwise it's a default value
IFM_ENVIRFLAG_CURRENT =     0x0200  #the value was measured with the last data set
                                        #(in a typical configuration it's not older than 4 secs)
IFM_ENVIRFLAG_MANUAL =      0x0400  #value was given manually per IfmSet... function


#Bits in the measurement data flags field; for internal use only
IFM_MFLAGS_RESERVED1 =  0x01
IFM_MFLAGS_BEAMBREAK =  0x02
IFM_MFLAGS_OVERFLOW =   0x04
IFM_MFLAGS_MISCOUNT =   0x80


#IfmStatus returns the following flags

#the lower 16 bit are channel dependend
IFM_STATUS_BEAMBREAK_QUADRANT = 0x0001      #miscount detected: the interferometer counter has detected an invalid jump over more than one quadrants
IFM_STATUS_BEAMBREAK_LEVEL =    0x0002      #the signal amplitude is lower than a given threashold so that miscounts are likely
IFM_STATUS_LASER_STABLE =       0x0010      #the laser(s) is(are) stable (only in systems with stabilized lasers)
IFM_STATUS_LASER_WAS_UNSTABLE = 0x0020      #since last IfmSetZero the laser was at least one time unstable

#the upper 16 bit are independend from the channel
IFM_STATUS_BUFFER_OVERFLOW_DEV =    0x0100  #the FIFO in the interferometer had an overflow; data loss by to large samplerate has occured
IFM_STATUS_BUFFER_OVERFLOW_DLL =    0x0200  #the measurement value buffer in the DLL had an overlow; data loss by infrequent call of IfmGetValue
IFM_STATUS_BLOCKMODE =              0x0400  #the device is in blockmode
IFM_STATUS_TRACER_LOCK =            0x0800  #Tracer locked
IFM_STATUS_BAD_REQUEST =            0x8000  #the status request could not be answered, perhaps due to bad deviceNumber or invalid channel


#Device types for IfmDeviceType
IFM_TYPE_NONE = 0
IFM_TYPE_DEMO = 1
IFM_TYPE_RE10 = 2   #the usual type, siosifm.dll is made to support RE-10 card
IFM_TYPE_RE06 = 3
IFM_TYPE_RAW =  4   #internal type, provides raw packet communication

#Interfaces for IfmDeviceInterface
IFM_INTERFACE_NONE =    0
IFM_INTERFACE_DEMO =    1
IFM_INTERFACE_RS232 =   2
IFM_INTERFACE_USB =     3
IFM_INTERFACE_NET =     4


#Error codes
IFM_ERROR_NONE =                    0
IFM_ERROR_DEVICE_INVALID =          -1
IFM_ERROR_BAD_CHANNEL =             -2
IFM_ERROR_BAD_DEVICETYPE =          -3
IFM_ERROR_DATALEN =                 -4
IFM_ERROR_BAD_DEVICE =              IFM_ERROR_DEVICE_INVALID
IFM_ERROR_UNKNOWN =                 -6
IFM_ERROR_DEVICECOUNT_OVERFLOW =    -10
IFM_ERROR_BAD_REQUESTTYPE =         -11
IFM_ERROR_INVALID_USB_ID =          -12
IFM_ERROR_CREATE_HANDLE =           -13
IFM_ERROR_NOT_IMPLEMENTED =         -100
IFM_ERROR_I2C_INUSE =               -15
IFM_ERROR_I2C_WRITE =               -16
IFM_ERROR_I2C_TIMEOUT =             -17
IFM_ERROR_OWR_TOOHIGHT =            -18
IFM_ERROR_INFO_NOT_AVAILABLE =      -19
IFM_ERROR_BAD_SENSOR =              -20
IFM_ERROR_I2C_READ =                -21
IFM_ERROR_BAD_PARAMETER =           -22
IFM_ERROR_SPI_ANSWER =              -23


#---------------------------------------------------------------------------------------------------------------------------------------------------------
#=========================================================================================================================================================
#---------------------------------------------------------------------------------------------------------------------------------------------------------


#Function for Initialization and closing
#The function IfmDLLVersion returns the version number

IfmDLLVersion = ifmdll.IfmDLLVersion
IfmDLLVersion.restype = c_int


#The function IfmDLLVersionString returns a pointer to
#a char field with the dll name and version number

IfmDLLVersionString = ifmdll.IfmDLLVersionString
IfmDLLVersionString.restype = c_char_p


IfmSetOption = ifmdll.IfmSetOption
IfmSetOption.argtypes = [c_int, c_int]


#Initializes the library

IfmInit = ifmdll.IfmInit
IfmInit.restype = c_int


#Closes the library and gives free all resources
#Counterpart to IfmInit

IfmClose = ifmdll.IfmClose


#don't use !!!
#only if IFM_OPTION_POLLSELF=0 then call IfmPoll frequently

IfmPoll = ifmdll.IfmPoll
IfmPoll.restype = c_int


#Open a device
#returns a handle for the device, the "devNumber"

IfmOpenUSB = ifmdll.IfmOpenUSB
IfmOpenUSB.argtypes = [c_int]
IfmOpenUSB.restype = c_int


#sets the baud rate for the following IfmSetOpenCOM functions
#the boud rate of the RE-10 RS-232 is default 115kBaud but can be
#configured induvidually, the boud rate given with this function must
#meet the configured rate in the device
#baudRate=0 resets to the default value

IfmSetBaudrate = ifmdll.IfmSetBaudrate
IfmSetBaudrate.argtypes = [c_int]
IfmSetBaudrate.restype = c_int


#only for WIN32/64

IfmOpenCOM = ifmdll.IfmOpenCOM
IfmOpenCOM.argtypes = [c_int]
IfmOpenCOM.restype = c_int


IfmOpenNetwork = ifmdll.IfmOpenNetwork
IfmOpenNetwork.argtypes = [c_char_p]
IfmOpenNetwork.restype = c_int

IfmOpenDemo = ifmdll.IfmOpenDemo
IfmOpenDemo.argtypes = [c_int]
IfmOpenDemo.restype = c_int


#Close a device which was opened with one of the IfmOpenXXX functions

IfmCloseDevice = ifmdll.IfmCloseDevice
IfmCloseDevice.argtypes = [c_int]


#The function IfmSearchUSBDevices finds the count of the devices on the USB-bus
#after a reset. This devices can be shown with the function IfmUSBDeviceSerial

IfmSearchUSBDevices = ifmdll.IfmSearchUSBDevices
IfmSearchUSBDevices.restype = c_int


#The function IfmUSBDeviceCount returns
#the count of devices on the USB-bus without a new search

IfmSearchUSBDevices = ifmdll.IfmSearchUSBDevices
IfmSearchUSBDevices.restype = c_int


#The function IfmUSBDeviceSerial returns the
#USB-serial number of the requested device; 0<=uniqueId<IfmUSBDeviceCount()

IfmUSBDeviceSerial = ifmdll.IfmUSBDeviceSerial
IfmUSBDeviceSerial.argtypes = [c_int]
IfmUSBDeviceSerial.restype = c_int


#The function IfmMaxDeviceCount returns the count of maximum allowable devices

IfmMaxDeviceCount = ifmdll.IfmMaxDeviceCount
IfmMaxDeviceCount.restype = c_int


#The function IfmDeviceCount returns the count of the open devices

IfmDeviceCount = ifmdll.IfmDeviceCount
IfmDeviceCount.restype = c_int


#checks, if the devNumber is a valid device id

IfmDeviceValid = ifmdll.IfmDeviceValid
IfmDeviceValid.argtypes = [c_int]
IfmDeviceValid.restype = c_int


#returns the version number of the firmware

IfmFirmwareVersion = ifmdll.IfmFirmwareVersion
IfmFirmwareVersion.argtypes = [c_int]
IfmFirmwareVersion.restype = c_int


#returns the count of channels

IfmChannels = ifmdll.IfmChannels
IfmChannels.argtypes = [c_int]
IfmChannels.restype = c_int


#returns the type of the device, currently only RE10-cards are supported

IfmDeviceType = ifmdll.IfmDeviceType
IfmDeviceType.argtypes = [c_int]
IfmDeviceType.restype = c_int


#to which interface is the device connected ? RS232, USB od Network

IfmDeviceInterface = ifmdll.IfmDeviceInterface
IfmDeviceInterface.argtypes = [c_int]
IfmDeviceInterface.restype = c_int


#to ask for specific properties (defined in siosifmdef.h)

IfmHasDeviceProperty = ifmdll.IfmHasDeviceProperty
IfmHasDeviceProperty.argtypes = [c_int, c_int]
IfmHasDeviceProperty.restype = c_int



#IfmDeviceInfo returns required information, if it is available, otherwise it returns 0
#Befor this function will be called, the device should be opened (IfmOpenCOM, IfmOpenUSB)

IfmDeviceInfo = ifmdll.IfmDeviceInfo
IfmDeviceInfo.argtypes = [c_int, c_int]
IfmDeviceInfo.restype = c_int


#some of the device infos can also be set

IfmSetDeviceInfo = ifmdll.IfmSetDeviceInfo
IfmSetDeviceInfo.argtypes = [c_int, c_int, c_int]
IfmSetDeviceInfo.restype = c_int

#IfmResetDevice causes the software reset of the according card
#Alike after hardware reset, the device stops after this command all running processes and
#breaks all connections. The USB-interface have to be reinitialized and
#the device have to be reconfigured by user again.

IfmResetDevice = ifmdll.IfmResetDevice
IfmResetDevice.argtypes = [c_int]


#The command IfmUpdateDevice causes the update-mode of the card.
#Attention!!! After starting of the update-mode it is not possible without
#the firmware - upgrade to set back the device to the run-mode.
#A SIOS-bootloader software should be applied for the upgrading.

IfmUpdateDevice = ifmdll.IfmUpdateDevice
IfmUpdateDevice.argtypes = [c_int]


#IfmSaveConfigDevice is command for the saving of the actual measuring settings into the flash.
#After the next device reset the saved parameter will be applied
#For an explanation of the measuring settings see the function IfmSetMeasurement

#Aktuelle Eunstellungen von Page0 in den Flash speichern
IfmSaveConfigDevice = ifmdll.IfmSaveConfigDevice
IfmSaveConfigDevice.argtypes = [c_int]


#IfmSetTrigger is command for the settings of trigger conditions.
#This settings have to be made before the command IfmSetMeasurement
#For the meaning of flags see the file siosifmdef.h

IfmSetTrigger = ifmdll.IfmSetTrigger
IfmSetTrigger.argtypes = [c_int, c_uint]
IfmSetTrigger.restype = c_int


#IfmFireTrigger requests one measuring value

IfmFireTrigger = ifmdll.IfmFireTrigger
IfmFireTrigger.argtypes = [c_int]
IfmFireTrigger.restype = c_int


#IfmSetFilter is command for the setting of the averaging filter one and two.
#If the values avr1 or avr2 are equal 0, will be the corresponding filter deactivated.
#Please note the settings of the mesurementFlags in the function IfmSetMeasurement.
#For the settings of  filterFlags see siosifmdef.h

IfmSetFilter = ifmdll.IfmSetFilter
IfmSetFilter.argtypes = [c_int, c_uint, c_int, c_int]
IfmSetFilter.restype = c_int


#IfmSetFilterCoeff is the function for the setting of the FIR-filter coefficients.
#This command should be applied for every of available channels

IfmSetFilterCoeff = ifmdll.IfmSetFilterCoeff
IfmSetFilterCoeff.argtypes = [c_int, c_int, c_double]
IfmSetFilterCoeff.restype = c_int


#IfmGetFilterCoeff is the function for the requiring
#of the FIR-filter coefficient for the corresponding device and channel.
#The values will be activated by the IfmSetMeasurement function

IfmGetFilterCoeff = ifmdll.IfmGetFilterCoeff
IfmGetFilterCoeff.argtypes = [c_int, c_int]
IfmGetFilterCoeff.restype = c_double


#Sets the notch frequency of the internal filter. A frequency of 0.0 means, that the
#frequency of the reference mirror vibrator should be notched out.
#This function is equivalent to IfmSetFilterCoeff but calculates the appropriate coeff based on the given frequency.

IfmSetFilterNotchFrequency = ifmdll.IfmSetFilterNotchFrequency
IfmSetFilterNotchFrequency.argtypes = [c_int, c_int, c_double]
IfmSetFilterNotchFrequency.restype = c_int


#Returns the notch frequency, which wre set with IfmSetFilterNotchFrequency.
#The function delivers valid values AFTER IfmSetMeasurement was called

IfmGetFilterNotchFrequency = ifmdll.IfmGetFilterNotchFrequency
IfmGetFilterNotchFrequency.argtypes = [c_int, c_int]
IfmGetFilterNotchFrequency.restype = c_double


#Sets the "dead path" in mm for the environment correction.
#The dead path is the distance from the sensor head to the zero position.
#Because during this distance the laser beam is also influenced by changing in air refraction
#it must be considered with the envirnonment correction even the distance plays no role in the
#measurement itself.

#ATTENTION!!! The dead path is taken over into the calculation with defining the Zero-Position (IfmSetToZero).
#Therefore, IfmSetDeadPath must always be called before IfmSetToZero!

IfmSetDeadPath = ifmdll.IfmSetDeadPath
IfmSetDeadPath.argtypes = [c_int, c_int, c_int]
IfmSetDeadPath.restype = c_int


#IfmGetDeadpath returns the active dead path for the given channel in mm
#Because the dead path is set during IfmSetToZero and the dead path can be changed
#in the interferometer (for instance in LaserTracers) the returned value may be
#different from the value set with IfmSetDeadpath

#The dead path is always positive. A negative return value is an error number and indicates an error.

IfmGetDeadPath = ifmdll.IfmGetDeadPath
IfmGetDeadPath.argtypes = [c_int, c_int]
IfmGetDeadPath.restype = c_int


#The function IfmSetMeasurementRawValues alike IfmSetMeasurement.
#But the filter settings will be ignored here. It means the sampe frequency and the output word rate are equal

# DLLFUNC int IfmSetMeasurementRawValues(int devNumber,unsigned int measurementFlags, int outputWordRate);
##IfmSetMeasurementRawValues = ifmdll.IfmSetMeasurementRawValues
##IfmSetMeasurementRawValues.argtypes = [c_int, c_uint, c_int]
##IfmSetMeasurementRawValues.restype = c_int


#The command IfmSetMeasurement is for the setting of measurement parameters like trigger conditions, filtering: on/off,
#measuring value and output word rate.
#For the settings of measurementFlags see siosifmdef.h

IfmSetMeasurement = ifmdll.IfmSetMeasurement
IfmSetMeasurement.argtypes = [c_int, c_uint, c_double]
IfmSetMeasurement.restype = c_int


#The function for the erasing of the PC-input buffer

IfmClearBuffers = ifmdll.IfmClearBuffers
IfmClearBuffers.argtypes = [c_int]
IfmClearBuffers.restpye = c_int


#The command IfmStart is for the measurement start.
#The measurement starts with the actual measurement parameter.
#See commands IfmSaveConfigDevice and IfmSetMeasurement for the detailed information.

IfmStart = ifmdll.IfmStart
IfmStart.argtypes = [c_int]
IfmStart.restype = c_int


#The command IfmStop for the measurement stop.

IfmStop = ifmdll.IfmStop
IfmStop.argtypes = [c_int]
IfmStop.restype = c_int


#The function IfmValueCount return the count of values, which are in the input puffer available.

IfmValueCount = ifmdll.IfmValueCount
IfmValueCount.argtypes = [c_int]
IfmValueCount.restype = c_int


#The function IfmGetValues read out the mesuring values from the input buffer according to FIFO (first in first out) principle.

IfmGetValues = ifmdll.IfmGetValues
IfmGetValues.argtypes = [c_int]
IfmGetValues.restype = c_int


#The function IfmGetRecentValues reads out the (count-index-1) mesuring values from the input buffer.

IfmGetRecentValues = ifmdll.IfmGetRecentValues
IfmGetRecentValues.argtypes = [c_int, c_int]
IfmGetRecentValues.restype = c_int


##IfmDataStruct *IfmValue(int devNumber);


IfmRawValue = ifmdll.IfmRawValue
IfmRawValue.argtypes = [c_int, c_int]
IfmRawValue.restype = c_longlong


#The function IfmLengthValue read out the length mesuring values.
#It is to use directly after the function IfmGetValues

IfmLengthValue = ifmdll.IfmLengthValue
IfmLengthValue.argtypes = [c_int, c_int]
IfmLengthValue.restype = c_double


IfmAuxValue = ifmdll.IfmAuxValue
IfmAuxValue.argtypes = [c_int, c_int, c_int]
IfmAuxValue.restype = c_int


#gives back the angle between two channels if they are linked
#the angle is calculated via the difference channel1 - channel2
#with interchange the channels the sign of the angle is inverted
#Attention: channel numbers must be given by with the IFM_CHANNEL1 - IFM_CHANNEL4 constants
#NOT with integer numbers
#if unit = 0 the unit is mrad, otherwise seconds

IfmAngleValue = ifmdll.IfmAngleValue
IfmAngleValue.argtypes = [c_int, c_int, c_int, c_int]
IfmAngleValue.restype = c_double


#return 1 if the channels, defined in channelmask are linked and
#an angle between these channels can be calculated

IfmAngleAvailable = ifmdll.IfmAngleAvailable
IfmAngleAvailable.argtypes = [c_int, c_int]
IfmAngleAvailable.restype = c_int


IfmStatus = ifmdll.IfmStatus
IfmStatus.argtypes = [c_int, c_int]
IfmStatus.restype = c_uint


#Block mode

IfmSetBlockModeFilter = ifmdll.IfmSetBlockModeFilter
IfmSetBlockModeFilter.argtypes = [c_int, c_uint, c_int, c_int]
IfmSetBlockModeFilter.restype = c_int

IfmSetBlockModeFilterCoeff = ifmdll.IfmSetBlockModeFilterCoeff
IfmSetBlockModeFilterCoeff.argtypes = [c_int, c_int, c_double]
IfmSetBlockModeFilterCoeff.restype = c_int


#not yet implemented, coming later

#DLLFUNC int IfmSetBlockModeFilterNotchFrequency(int devNumer, int channel, double frequency);
#IfmSetBlockModeFilterNotchFrequency = ifmdll.IfmSetBlockModeFilterNotchFrequency
#IfmSetBlockModeFilterNotchFrequency.argtypes = [c_int, c_int, c_double]
#IfmSetBlockModeFilterNotchFrequency.restype = c_int

IfmSetBlockMode = ifmdll.IfmSetBlockMode
IfmSetBlockMode.argtypes = [c_int, c_int, c_int, c_int]
IfmSetBlockMode.restype = c_int

IfmStartBlock = ifmdll.IfmStartBlock
IfmStartBlock.argtypes = [c_int, c_int]
IfmStartBlock.restype = c_int

IfmIsBlockAvailable = ifmdll.IfmIsBlockAvailable
IfmIsBlockAvailable.argtypes = [c_int]
IfmIsBlockAvailable.restype = c_int

IfmCancelBlock =ifmdll.IfmCancelBlock
IfmCancelBlock.argtypes = [c_int]
IfmCancelBlock.restype = c_int


#Functions for controling the interferometer

#Command IfmSetRefMirrorVibration for setting on the mirror vibration

IfmSetRefMirrorVibration = ifmdll.IfmSetRefMirrorVibration
IfmSetRefMirrorVibration.argtypes = [c_int, c_int, c_int]
IfmSetRefMirrorVibration.restype = c_int

IfmSetRefMirrorVibration = ifmdll.IfmSetRefMirrorVibration
IfmSetRefMirrorVibration.argtypes = [c_int, c_int]
IfmSetRefMirrorVibration.restype = c_int

IfmSetAGC = ifmdll.IfmSetAGC
IfmSetAGC.argtypes = [c_int, c_int, c_int]
IfmSetAGC.restype = c_int

IfmGetAGC = ifmdll.IfmGetAGC
IfmGetAGC.argtypes = [c_int, c_int]
IfmGetAGC.restype = c_int


#enhanced functions for service tasks, do not use

IfmExtAGCStatus = ifmdll.IfmExtAGCStatus
IfmExtAGCStatus.argtypes = [c_int, c_int]
IfmExtAGCStatus.restype = c_int

IfmSaveAGCStatus = ifmdll.IfmSaveAGCStatus
IfmSaveAGCStatus.argtypes = [c_int, c_int]
IfmSaveAGCStatus.restype = c_int


#normally IfmSetToZero sets the length values to zero
#IfmSetPreset lets add a fixed offset
#must be called before IfmSetToZero, preset is in nm

IfmSetPreset = ifmdll.IfmSetPreset
IfmSetPreset.argtypes = [c_int, c_int, c_double]
IfmSetPreset.restype = c_int


#returns the active preset, which was set by IfmSetPreset
#attention, the preset value becumes active during IfmSetToZero

IfmGetPreset = ifmdll.IfmGetPreset
IfmGetPreset.argtypes = [c_int, c_int]
IfmGetPreset.restype = c_double


#sets the dead path, the preset values, clears the overlow and beambreak flags
#and clears the interferometer counter

IfmSetToZero = ifmdll.IfmSetToZero
IfmSetToZero.argtypes = [c_int, c_int]
IfmSetToZero.restype = c_int


#detailed Monitoring data in service Part as strukture

IfmSignalQuality = ifmdll.IfmSignalQuality
IfmSignalQuality.argtypes = [c_int, c_int, c_int]
IfmSignalQuality.restype = c_int

IfmNewSignalQualityAvailable = ifmdll.IfmNewSignalQualityAvailable
IfmNewSignalQualityAvailable.argtypes = [c_int]
IfmNewSignalQualityAvailable.restype = c_int

IfmWasBeamBreak = ifmdll.IfmWasBeamBreak
IfmWasBeamBreak.argtypes = [c_int, c_int]
IfmWasBeamBreak.restype = c_int

IfmWasBeamBreak = ifmdll.IfmWasBeamBreak
IfmWasBeamBreak.argtypes = [c_int]
IfmWasBeamBreak.restype = c_int

IfmWasLaserUnstable = ifmdll.IfmWasLaserUnstable
IfmWasLaserUnstable.argtypes = [c_int, c_int]
IfmWasLaserUnstable.restype = c_int


#Functions for environmental data and data depending from environmental values

#returns 1 if new (since the last call of this function) environment values are available

IfmNewEnvValuesAvailable = ifmdll.IfmNewEnvValuesAvailable
IfmNewEnvValuesAvailable.argtypes = [c_int]
IfmNewEnvValuesAvailable.restype = c_int


#returns the connected/configured amount of sensors

IfmEnvSensorCount = ifmdll.IfmEnvSensorCount
IfmEnvSensorCount.argtypes = [c_int]
IfmEnvSensorCount.restype = c_int


#returns a flag for the sensor on place "sensor" where sensor is 0.. IfmEnvSensorCount()-1

IfmSensorProperty = ifmdll.IfmSensorProperty
IfmSensorProperty.argtypes = [c_int, c_int]
IfmSensorProperty.restype = c_uint


#return s the value of the sensor

IfmSensorValue = ifmdll.IfmSensorValue
IfmSensorValue.argtypes = [c_int, c_int]
IfmSensorValue.restype = c_double


#extended functions, dealing with internal positions for "sensor", for internal use only!!

IfmSensorPropertyEx = ifmdll.IfmSensorPropertyEx
IfmSensorPropertyEx.argtypes = [c_int, c_int]
IfmSensorPropertyEx.restype = c_uint

IfmSensorValueEx = ifmdll.IfmSensorValueEx
IfmSensorValueEx.argtypes = [c_int, c_int]
IfmSensorValueEx.restype = c_double

IfmEnvSensorCountEx = ifmdll.IfmEnvSensorCountEx
IfmEnvSensorCountEx.argtypes = [c_int]
IfmEnvSensorCountEx.restype = c_int


#returns the temperature which is assotiated with "channel"

IfmTemperature = ifmdll.IfmTemperature
IfmTemperature.argtypes = [c_int, c_int]
IfmTemperature.restype = c_double


#returns a description, from where the value is

IfmTemperatureFlags = ifmdll.IfmTemperatureFlags
IfmTemperatureFlags.argtypes = [c_int, c_int]
IfmTemperatureFlags.restype = c_int


#returns the humidy which is assotiated with "channel"

IfmHumidity = ifmdll.IfmHumidity
IfmHumidity.argtypes = [c_int, c_int]
IfmHumidity.restype = c_double

IfmHumidityFlags = ifmdll.IfmHumidityFlags
IfmHumidityFlags.argtypes = [c_int, c_int]
IfmHumidityFlags.restype = c_int


#returns the air pressure which is assotiated with "channel"

IfmAirPressure = ifmdll.IfmAirPressure
IfmAirPressure.argtypes = [c_int, c_int]
IfmAirPressure.restype = c_double

IfmAirPressureFlags = ifmdll.IfmAirPressureFlags
IfmAirPressureFlags.argtypes = [c_int, c_int]
IfmAirPressureFlags.restype = c_int


#returns the water vapour pressure (calculated from humidy, temperature and air pressure) which is assotiated with "channel"

IfmWaterVapourPressure = ifmdll.IfmWaterVapourPressure
IfmWaterVapourPressure.argtypes = [c_int, c_int]
IfmWaterVapourPressure.restype = c_double

#returns the conversion coefficient (Edlen correction, calculated humidity, temperature and air pressure) which is assotiated with "channel"

IfmConversionCoeff = ifmdll.IfmConversionCoeff
IfmConversionCoeff.argtypes = [c_int, c_int]
IfmConversionCoeff.restype = c_double


#returns the conversion coefficient for the dead path correction

IfmDeadpathCoeff = ifmdll.IfmDeadpathCoeff
IfmDeadpathCoeff.argtypes = [c_int, c_int]
IfmDeadpathCoeff.restype = c_double


#returns the vacuum wavelength of the laser

IfmVacuumWavelength = ifmdll.IfmVacuumWavelength
IfmVacuumWavelength.argtypes = [c_int, c_int]
IfmVacuumWavelength.restype = c_double


#returns the corrected wavelength

IfmWavelength = ifmdll.IfmWavelength
IfmWavelength.argtypes = [c_int, c_int]
IfmWavelength.restype = c_double


#returns the air refraction index used for the environment correction of the channel

IfmAirRefraction = ifmdll.IfmAirRefraction
IfmAirRefraction.argtypes = [c_int, c_int]
IfmAirRefraction.restype = c_double


#switch Edlen correction off, for example for measurements in vacuum or if you want to make your own correction

IfmEnableEdlenCorrection = ifmdll.IfmEnableEdlenCorrection
IfmEnableEdlenCorrection.argtypes = [c_int, c_int, c_int]


#ask, if Edlen correction is enabled

IfmIsEdlenEnabled = ifmdll.IfmIsEdlenEnabled
IfmIsEdlenEnabled.argtypes = [c_int, c_int]
IfmIsEdlenEnabled.restype = c_int


IfmSetTemperature = ifmdll.IfmSetTemperature
IfmSetTemperature.argtypes = [c_int, c_int, c_double]

IfmSetHumidity =ifmdll.IfmSetHumidity
IfmSetHumidity.argtypes = [c_int, c_int, c_double]

IfmSetAirPressure = ifmdll.IfmSetAirPressure
IfmSetAirPressure.argtypes = [c_int, c_int, c_double]

IfmSetWaterVapourPressure = ifmdll.IfmSetWaterVapourPressure
IfmSetWaterVapourPressure.argtypes = [c_int, c_int, c_double]

#       IfmSetConversionCoeff = ifmdll.IfmSetConversionCoeff
#       IfmSetConversionCoeff.argtypes = [c_int, c_int, c_double]

IfmSetVacuumWavelength = ifmdll.IfmSetVacuumWavelength
IfmSetVacuumWavelength.argtypes = [c_int, c_int, c_double]


IfmEnvironmentFlags = ifmdll.IfmEnvironmentFlags
IfmEnvironmentFlags.argtypes = [c_int, c_int]
IfmEnvironmentFlags.restype = c_int

IfmManualEnvironment = ifmdll.IfmManualEnvironment
IfmManualEnvironment.argtypes = [c_int, c_int]
IfmManualEnvironment.restype = c_int


IfmResetManualEnvironment = ifmdll.IfmResetManualEnvironment
IfmResetManualEnvironment.argtypes = [c_int, c_int, c_int]


#calculates the real wavelength in air (also called Edlen-correction),
#based on the vacuum-wavelength, the air temperature in °C
#the pressure in Pa and the rel. humidity in %

IfmCalculateWavelength = ifmdll.IfmCalculateWavelength
IfmCalculateWavelength.argtypes = [c_double, c_double, c_double, c_double]
IfmCalculateWavelength.restype = c_double



#Special control commands

#section i2c-communication Special commands for accessing other cards

#Low level function for writing a block of data to a card in the interferometer

IfmI2CRequestWrite = ifmdll.IfmI2CRequestWrite
IfmI2CRequestWrite.argtypes = [c_int, c_int, c_int, c_int, c_ubyte]
IfmI2CRequestWrite.restype = c_int


#Check the last IfmI2CWrite operation

#0 if successfull
#IFM_ERROR_I2C_WRITE if an error has occured,
#IFM_ERROR_I2C_INUSE if the system is yet waiting for the acknowledge

IfmI2CStatus = ifmdll.IfmI2CStatus
IfmI2CStatus.artypes = [c_int]
IfmI2CStatus.restype = c_int


#wie IfmI2CRequestWrite, blockiert aber so lange, bis Rueckmeldung von Firmware da oder Timeout

IfmI2CWrite = ifmdll.IfmI2CWrite
IfmI2CWrite.argtypes = [c_int, c_int, c_int, c_int, c_ubyte]
IfmI2CWrite.restype = c_int


#Low level function for requesting a read of a block of data from a card in the interferometer

IfmI2CRequestRead = ifmdll.IfmI2CRequestRead
IfmI2CRequestRead.argtypes = [c_int, c_int, c_int, c_int]
IfmI2CRequestRead.restype = c_int


#Test whether a request to read was successfully.

#param devNumber the unique identifier for the device
#ret true if read has been successfully done, otherwise false

#see IfmI2CRequestRead(int devNumber, int i2cAddr, int ramAddr, int count)

IfmI2CReadReady = ifmdll.IfmI2CReadReady
IfmI2CReadReady.argtypes = [c_int]
IfmI2CReadReady.restype = c_int


#! \brief Access to the internal read buffer

#param index the index in the buffer, valid from 0 to count-1
#(see IfmI2CRequestRead(int devNumber, int i2cAddr, int ramAddr, int count))

IfmI2CReadValue = ifmdll.IfmI2CReadValue
IfmI2CReadValue.argtypes = [c_int, c_int]
IfmI2CReadValue.restype = c_ubyte


#like IfmI2CRequestRead but is blocking until read was successfully or an error has reported

IfmI2CRead = ifmdll.IfmI2CRead
IfmI2CRead.argtypes = [c_int, c_int, c_int, c_int]
IfmI2CRead.restype = c_int

#Hier waren Sternchen vor den Variablen
IfmI2CReadBuffer = ifmdll.IfmI2CReadBuffer
IfmI2CReadBuffer.argtypes = [c_int]
IfmI2CReadBuffer.restype = c_ubyte


#do not use; for internal operations only

IfmI2CReadOscFrequency = ifmdll.IfmI2CReadOscFrequency
IfmI2CReadOscFrequency.argtypes = [c_int, c_int]
IfmI2CReadOscFrequency.restype = c_double

IfmI2CWriteOscFrequency = ifmdll.IfmI2CWriteOscFrequency
IfmI2CWriteOscFrequency.argtypes = [c_int, c_int, c_double]
IfmI2CWriteOscFrequency.restype = c_int


#Error Handling

IfmGetErrorString = ifmdll.IfmGetErrorString
IfmGetErrorString.argtypes = [c_int]
IfmGetErrorString.restype = c_char_p

IfmGetError = ifmdll.IfmGetError
IfmGetError.restype = c_int

#den ersten Fehler seit letztem Aufruf dieser Funktion


#only for internal use

IfmOpenRawUSB = ifmdll.IfmOpenRawUSB
IfmOpenRawUSB.argtypes = [c_int]
IfmOpenRawUSB.restype = c_int


#only for WIN32/64

IfmOpenRawCOM = ifmdll.IfmOpenRawCOM
IfmOpenRawCOM.argtypes = [c_int]
IfmOpenRawCOM.restype = c_int


#the following functions are intended for internal use only

IfmSendRawPacket = ifmdll.IfmSendRawPacket
IfmSendRawPacket.argtypes = [c_int, c_char, c_int]
IfmSendRawPacket.restype = c_int

IfmRawPacketCount = ifmdll.IfmRawPacketCount
IfmRawPacketCount.argtypes = [c_int]
IfmRawPacketCount.restype = c_int

IfmGetRawPacket = ifmdll.IfmGetRawPacket
IfmGetRawPacket.argtypes = [c_int, c_int, c_char, c_int]
IfmGetRawPacket.restype = c_int


#Motor control, not implemented yet, will internally use I2C functions

#brief Stops the motor and disables the power amplifiers

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)

#ret error value

IfmMotorStop = ifmdll.IfmMotorStop
IfmMotorStop.argtypes = [c_int, c_int]
IfmMotorStop.restype = c_int


#brief Moves the motor with a constant speed

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
#param speed (in steps/s)

#ret error value

IfmMotorMove = ifmdll.IfmMotorMove
IfmMotorMove.argtypes = [c_int, c_int, c_int]
IfmMotorMove.restype = c_int


#brief Moves the motor to a new position relative to the current position

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
#param position the amount of steps the motor should move
#param speed (in steps/s)

#ret error value

IfmMotorMoveRel = ifmdll.IfmMotorMoveRel
IfmMotorMoveRel.argtypes = [c_int, c_int, c_int, c_int]
IfmMotorMoveRel.restype = c_int


#brief Moves the motor to a new position

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
#param position the new position
#param speed (in steps/s)

#ret error value

IfmMotorMoveAbs = ifmdll.IfmMotorMoveAbs
IfmMotorMoveAbs.argtypes = [c_int, c_int, c_int, c_int]
IfmMotorMoveAbs.resytpe = c_int


#brief Sets the a position

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
#param newPosition the new position

#This function only updates the internal position counter. The motor will not move.

#ret error value

IfmMotorSetPos = ifmdll.IfmMotorSetPos
IfmMotorSetPos.argtypes = [c_int, c_int, c_int]
IfmMotorSetPos.restype = c_int


#brief Enables the motor

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)

#ret error value

IfmMotorEnable = ifmdll.IfmMotorEnable
IfmMotorEnable.argtypes = [c_int, c_int]
IfmMotorEnable.restype = c_int


#brief Disables the motor

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)

#ret error value

IfmMotorDisable = ifmdll.IfmMotorDisable
IfmMotorDisable.argtypes = [c_int, c_int]
IfmMotorDisable.restype = c_int


#brief Requests the status of the motor

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)

#The transmission of the status takes up to appox. 100 milliseconds. This function requests the transmission and returns immediately.
#The status itself can be read using IfmMotorStatus.

#IfmMotorReadStatus requests the status and blocks until the data are transferred.

#ret error value

IfmMotorRequestStatus =ifmdll.IfmMotorRequestStatus
IfmMotorRequestStatus.argtypes = [c_int, c_int]
IfmMotorRequestStatus.restype = c_int


#brief Read the status of the motor

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
#param status pointer to an integer an which the status word will be written
#param position pointer to an integer on which the current position will be written
#param application pointer to an integer on which an identifier of the motor will be written. This identifier stands for the specific application
#(gauging probe, tonometer test, NMM ...) the motor card is configured for

#Before using this function the status must be requested using IfmMotorRequestStatus. If the requested status is not yet available,
#the function returns with an error.

#ret error value

IfmMotorStatus = ifmdll.IfmMotorStatus
IfmMotorStatus.argtypes = [c_int, c_int, c_int, c_int, c_uint]
IfmMotorStatus.restype = c_int


#brief Read the status of the motor

#param devNumber the unique identifier for the device
#param motorNumber the number of the motor
#(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
#param status pointer to an integer an which the status word will be written
#param position pointer to an integer on which the current position will be written
#param application pointer to an integer on which an identifier of the motor will be written. This identifier stands for the specific application
#(gauging probe, tonometer test, NMM ...) the motor card is configured for
#param timeout_ms the time in ms this function will wait for the status information. Should be typically above 200ms.

#ret error value

IfmMotorReadStatus = ifmdll.IfmMotorReadStatus
IfmMotorReadStatus.argtypes = [c_int, c_int, c_void_p, c_void_p, c_void_p, c_int]
IfmMotorReadStatus.restype = c_int


#service functions; do not use

IfmMotorRequestControlStruct = ifmdll.IfmMotorRequestControlStruct
IfmMotorRequestControlStruct.argtypes = [c_int, c_int]
IfmMotorRequestControlStruct.restype = c_int

IfmMotorGetControlStruct = ifmdll.IfmMotorGetControlStruct
IfmMotorGetControlStruct.argtypes = [c_int, c_int, c_ubyte]
IfmMotorGetControlStruct.restype = c_int

IfmMotorSetControlStruct = ifmdll.IfmMotorSetControlStruct
IfmMotorSetControlStruct.argtypes = [c_int, c_int, c_ubyte]
IfmMotorSetControlStruct.restype = c_int


IfmRequestFactoryCfg = ifmdll.IfmRequestFactoryCfg
IfmRequestFactoryCfg.argtypes = [c_int]
IfmRequestFactoryCfg.restype = c_int

IfmRequestSystemCfg = ifmdll.IfmRequestSystemCfg
IfmRequestSystemCfg.argtypes = [c_int]
IfmRequestSystemCfg.restype = c_int

IfmGetSystemCfg = ifmdll.IfmGetSystemCfg
IfmGetSystemCfg.argtypes = [c_int, c_void_p]
IfmGetSystemCfg.restype = c_int

IfmGetSystemCfg = ifmdll.IfmGetSystemCfg
IfmGetSystemCfg.argtypes = [c_int, c_void_p]
IfmGetSystemCfg.restype = c_int

IfmMirrorSystemCfg =ifmdll.IfmMirrorSystemCfg
IfmMirrorSystemCfg.argtypes = [c_int]
IfmMirrorSystemCfg.restype = c_int

IfmSendByteArray = ifmdll.IfmSendByteArray          #Bootloader
IfmSendByteArray.argtypes = [c_int, c_void_p]
IfmSendByteArray.restype = c_int

IfmSendBootAddr = ifmdll.IfmSendBootAddr            #Bootloader
IfmSendBootAddr.argtypes = [c_int, c_void_p]
IfmSendBootAddr.restype = c_int

IfmGetAnswer = ifmdll.IfmGetAnswer                  #Bootloader
IfmGetAnswer.argtypes = [c_int]
IfmGetAnswer.restype = c_int


IfmSpiCommand = ifmdll.IfmSpiCommand
IfmSpiCommand.argtypes = [c_int, c_int, c_int, c_int]
IfmSpiCommand.restype = c_int

IfmSpiAnswer = ifmdll.IfmSpiAnswer
IfmSpiAnswer.argtypes = [c_int, c_int, c_int, c_int]
IfmSpiAnswer.restype = c_int

IfmSetSensorValue = ifmdll.IfmSetSensorValue
IfmSetSensorValue.argtypes = [c_int, c_int, c_double]

IfmSetSlaveSensorValue =ifmdll.IfmSetSlaveSensorValue
IfmSetSlaveSensorValue.argtypes = [c_int, c_int, c_double]

IfmSetSensorProperty = ifmdll.IfmSetSensorProperty
IfmSetSensorProperty.argtypes = [c_int, c_int, c_int]


#Human readable error message

IfmGetErrorString = ifmdll.IfmGetErrorString
IfmGetErrorString.argtypes = [c_int]
IfmGetErrorString.restype = c_char_p


#End of siosifm.py
