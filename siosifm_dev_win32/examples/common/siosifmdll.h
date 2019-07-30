
#ifndef SIOSIFMDLL_H
#define SIOSIFMDLL_H



#ifdef _WIN64

#ifdef BUILD_DLL
#define DLLFUNC extern "C" __declspec(dllexport)
#else
#define DLLFUNC extern "C" __declspec(dllimport)
#endif

typedef short int16;
typedef unsigned short uint16;
typedef int int32;
typedef unsigned int uint32;
typedef long long int64;
typedef unsigned long long uint64;
typedef unsigned long long int_p;

#ifdef _MSC_VER
#    pragma pack( push, packing )
#    pragma pack( 1 )
#    define PACK_STRUCT
#elif defined( __GNUC__ )
#    define PACK_STRUCT    __attribute__((packed))
#endif

#define WIN_API 1


#elif defined( _WIN32)

#ifdef BUILD_DLL
#define DLLFUNC extern "C" __declspec(dllexport)
#else
#define DLLFUNC extern "C" __declspec(dllimport)
#endif

typedef short int16;
typedef unsigned short uint16;
typedef int int32;
typedef unsigned int uint32;
typedef int int_p;

#ifdef _MSC_VER
#    pragma pack( push, packing )
#    pragma pack( 1 )
#    define PACK_STRUCT
typedef __int64 int64;
typedef unsigned __int64 uint64;
#elif defined( __GNUC__ )
#    define PACK_STRUCT    __attribute__((packed))
typedef long long int64;
typedef unsigned long long uint64;
#endif

#define WIN_API 1

#else
// Linux
#define DLLFUNC
#define CALLCONV

typedef short int16;
typedef unsigned short uint16;
typedef int int32;
typedef unsigned int uint32;
typedef long long int64;
typedef unsigned long long uint64;

#ifdef _LP64
typedef long int_p;

#else
typedef int int_p;

#define PACK_STRUCT    __attribute__((packed))

#endif


#endif

#include <siosifmdef.h>



// Function for Initialization and closing
/*
The function IfmDLLVersion returns the version number
*/
DLLFUNC int32 IfmDLLVersion();

/*
The function IfmDLLVersionString returns a pointer to
a char field with the dll name and version number
*/
DLLFUNC const char *IfmDLLVersionString();


DLLFUNC void IfmSetOption(int32 option, int32 param1);

/* Initializes the library

*/
DLLFUNC int32 IfmInit();


/* Closes the library and gives free all resources
   Counterpart to IfmInit
*/
DLLFUNC void IfmClose();

// don't use !!!
// only if IFM_OPTION_POLLSELF=0 then call IfmPoll frequently
DLLFUNC int32 IfmPoll();

/* Open a device
   returns a handle for the device, the "devNumber"
*/
DLLFUNC int32 IfmOpenUSB(int32 uniqueId);

// sets the baud rate for the following IfmSetOpenCOM functions
// the boud rate of the RE-10 RS-232 is default 115kBaud but can be
// configured induvidually, the boud rate given with this function must
// meet the configured rate in the device
// baudRate=0 resets to the default value
DLLFUNC int32 IfmSetBaudrate(int32 baudRate);

#ifdef WIN_API
DLLFUNC int32 IfmOpenCOM(int32 comNumber);
#else
DLLFUNC int32 IfmOpenCOM(const char *devName);
#endif

DLLFUNC int32 IfmOpenNetwork(const char *ipAddr, int32 port);
DLLFUNC int32 IfmOpenDemo(int32 channels);

/* Close a device which was opened with one of the IfmOpenXXX functions
*/
DLLFUNC void IfmCloseDevice(int32 devNumber);

/*
    The function IfmSearchUSBDevices finds the count of the devices on the USB-bus
    after a reset. This devices can be shown with the function IfmUSBDeviceSerial
*/
DLLFUNC int32 IfmSearchUSBDevices();

/*
 The function IfmUSBDeviceCount returns
 the count of devices on the USB-bus without a new search
*/
DLLFUNC int32 IfmUSBDeviceCount();

/*
  The function IfmUSBDeviceSerial returns the
 USB-serial number of the requested device; 0<=uniqueId<IfmUSBDeviceCount()
*/
DLLFUNC int32 IfmUSBDeviceSerial(int32 uniqueId);

/*
The function IfmMaxDeviceCount returns the count of maximum allowable devices
*/
DLLFUNC int32 IfmMaxDeviceCount();

/*
The function IfmDeviceCount returns the count of the open devices
*/
DLLFUNC int32 IfmDeviceCount();

// checks, if the devNumber is a valid device id
DLLFUNC int32 IfmDeviceValid(int32 devNumber);

// returns the version number of the firmware
DLLFUNC int32 IfmFirmwareVersion(int32 devNumber);
// returns the count of channels
DLLFUNC int32 IfmChannels(int32 devNumber);
// returns the type of the device, currently only RE10-cards are supported
DLLFUNC int32 IfmDeviceType(int32 devNumber);
// to which interface is the device connected ? RS232, USB od Network
DLLFUNC int32 IfmDeviceInterface(int32 devNumber);
// to ask for specific properties (defiened in siosifmdef.h)
DLLFUNC int32 IfmHasDeviceProperty(int32 devNumber, int32 porpertyNumber);

/*
IfmDeviceInfo returns required information, if it is available, otherwise it returns 0
Befor this function will be called, the device should be opened (IfmOpenCOM, IfmOpenUSB)
*/
DLLFUNC int_p IfmDeviceInfo(int32 devNumber, int32 requestedInfo);

//some of the device infos can also be set
DLLFUNC int32 IfmSetDeviceInfo(int32 devNumber, int32 requestedInfo, int32 newValue);

/*
IfmResetDevice causes the software reset of the according card
Alike after hardware reset, the device stops after this command all running processes and
breaks all connections. The USB-interface have to be reinitialized and
the device have to be reconfigured by user again.
*/
DLLFUNC void IfmResetDevice(int32 devNumber);


/*
The command IfmUpdateDevice causes the update-mode of the card.
Attention!!! After starting of the update-mode it is not possible without
the firmware - upgrade to set back the device to the run-mode.
A SIOS-bootloader software should be applied for the upgrading.
*/
DLLFUNC void IfmUpdateDevice(int32 devNumber);


/*
IfmSaveConfigDevice is command for the saving of the actual measuring settings into the flash.
After the next device reset the saved parameter will be applied
For an explanation of the measuring settings see the function IfmSetMeasurement
*/
DLLFUNC void IfmSaveConfigDevice(int32 devNumber);//Aktuelle Eunstellungen von Page0 in den Flash speichern

/*
IfmSetTrigger is command for the settings of trigger conditions.
This settings have to be made before the command IfmSetMeasurement
For the meaning of flags see the file siosifmdef.h
*/
DLLFUNC int32 IfmSetTrigger(int32 devNumber, uint32 triggerMode);

/*
IfmFireTrigger requests one measuring value
*/
DLLFUNC int32 IfmFireTrigger(int32 devNumber);

/*
IfmSetFilter is command for the setting of the averaging filter one and two.
If the values avr1 or avr2 are equal 0, will be the corresponding filter deactivated.
Please note the settings of the mesurementFlags in the function IfmSetMeasurement.
For the settings of  filterFlags see siosifmdef.h
*/
DLLFUNC int32 IfmSetFilter(int32 devNumber, uint32 filterFlags,int32 avg1, int32 avg2);


/*
IfmSetFilterCoeff is the function for the setting of the FIR-filter coefficients.
This command should be applied for every of available channels
*/
DLLFUNC int32 IfmSetFilterCoeff(int32 devNumber, int32 channel, double coeff);

/*
IfmGetFilterCoeff is the function for the requiring
of the FIR-filter coefficient for the corresponding device and channel.
The values will be activated by the IfmSetMeasurement function
*/
DLLFUNC double IfmGetFilterCoeff(int32 devNumber, int32 channel);

/*
Sets the notch frequency of the internal filter. A frequency of 0.0 means, that the
frequency of the reference mirror vibrator should be notched out.
This function is equivalent to IfmSetFilterCoeff but calculates the appropriate coeff based on the given frequency.
*/
DLLFUNC int32 IfmSetFilterNotchFrequency(int32 devNumber, int32 channel, double freq);

/*
Returns the notch frequency, which wre set with IfmSetFilterNotchFrequency.
The function delivers valid values AFTER IfmSetMeasurement was called
*/
DLLFUNC double IfmGetFilterNotchFrequency(int32 devNumber, int32 channel);


/*
Sets the "dead path" in mm for the environment correction.
The dead path is the distance from the sensor head to the zero position.
Because during this distance the laser beam is also influenced by changing in air refraction
it must be considered with the envirnonment correction even the distance plays no role in the
measurement itself.

ATTENTION!!! The dead path is taken over into the calculation with defining the Zero-Position (IfmSetToZero).
Therefore, IfmSetDeadPath must always be called before IfmSetToZero!

 */
DLLFUNC int32 IfmSetDeadPath(int32 devNumber,int32 channel, int32 deadPath);

/* IfmGetDeadpath returns the active dead path for the given channel in mm
   Because the dead path is set during IfmSetToZero and the dead path can be changed
   in the interferometer (for instance in LaserTracers) the returned value may be
   different from the value set with IfmSetDeadpath

   The dead path is always positive. A negative return value is an error number and indicates an error.

 */

DLLFUNC int32 IfmGetDeadPath(int32 devNumber, int32 channel);

/*
The function IfmSetMeasurementRawValues alike IfmSetMeasurement.
But the filter settings will be ignored here. It means the sampe frequency and the output word rate are equal
*/
//DLLFUNC int32 IfmSetMeasurementRawValues(int32 devNumber,unsigned int32 measurementFlags, int32 outputWordRate);

/*
The command IfmSetMeasurement is for the setting of measurement parameters like trigger conditions, filtering: on/off,
measuring value and output word rate.
For the settings of measurementFlags see siosifmdef.h
*/
DLLFUNC int32 IfmSetMeasurement(int32 devNumber,uint32 measurementFlags, double outputWordRate);


/*
The function for the erasing of the PC-input buffer
*/
DLLFUNC int32 IfmClearBuffers(int32 devNumber);
/*
The command IfmStart is for the measurement start.
The measurement starts with the actual measurement parameter.
See commands IfmSaveConfigDevice and IfmSetMeasurement for the detailed information.
*/
DLLFUNC int32 IfmStart(int32 devNumber);

/*
The command IfmStop for the measurement stop.
*/
DLLFUNC int32 IfmStop(int32 devNumber);
/*
The function IfmValueCount return the count of values, which are in the input puffer available.
*/
DLLFUNC int32 IfmValueCount(int32 devNumber);
/*
The function IfmGetValues read out the mesuring values from the input buffer according to FIFO (first in first out) principle.
*/
DLLFUNC int32 IfmGetValues(int32 devNumber);
/*
The function IfmGetRecentValues reads out the (count-index-1) mesuring values from the input buffer.
*/
DLLFUNC int32 IfmGetRecentValues(int32 devNumber, int32 index);

//IfmDataStruct *IfmValue(int32 devNumber);

/*

*/
DLLFUNC int64 IfmRawValue(int32 devNumber,int32 channel);

/*
The function IfmLengthValue read out the length mesuring values.
It is to use directly after the function IfmGetValues
*/
DLLFUNC double IfmLengthValue(int32 devNumber,int32 channel);


DLLFUNC int32 IfmAuxValue(int32 devNumber,int32 channel,int32 valueType);

// gives back the angle between two channels if they are linked
// the angle is calculated via the difference channel1 - channel2
// with interchange the channels the sign of the angle is inverted
// Attention: channel numbers must be given by with the IFM_CHANNEL1 - IFM_CHANNEL4 constants
// NOT with integer numbers
// if unit = 0 the unit is mrad, otherwise seconds
DLLFUNC double IfmAngleValue(int32 devNumber, int32 channel1, int32 channel2, int32 unit);

// return 1 if the channels, defined in channelmask are linked and
// an angle between these channels can be calculated
DLLFUNC int32 IfmAngleAvailable(int32 devNumber,int32 channelMask);

DLLFUNC uint32 IfmStatus(int32 devNumber,int32 channel);

// Block mode
DLLFUNC int32 IfmSetBlockModeFilter(int32 devNumber, uint32 filterFlags,int32 avg1, int32 avg2);
DLLFUNC int32 IfmSetBlockModeFilterCoeff(int32 devNumer, int32 channel, double coeff);
// not yet implemented, coming later
//DLLFUNC int32 IfmSetBlockModeFilterNotchFrequency(int32 devNumer, int32 channel, double frequency);
DLLFUNC int32 IfmSetBlockMode(int32 devNumber,int32 measurementFlags,int32 triggerMode, int32 outputWordRate);
DLLFUNC int32 IfmStartBlock(int32 devNumber, int32 blockLen);
DLLFUNC int32 IfmIsBlockAvailable(int32 devNumber);
DLLFUNC int32 IfmCancelBlock(int32 devNumber);

// Functions for controling the interferometer
/*
Command IfmSetRefMirrorVibration for setting on the mirror vibration
*/
DLLFUNC int32 IfmSetRefMirrorVibration(int32 devNumber,int32 channel, int32 on);
DLLFUNC int32 IfmGetRefMirrorVibration(int32 devNumber,int32 channel);

DLLFUNC int32 IfmSetAGC(int32 devNumber,int32 channel, int32 on);
DLLFUNC int32 IfmGetAGC(int32 devNumber,int32 channel);


// enhanced functions for service tasks, do not use
DLLFUNC int32 IfmExtAGCStatus(int32 devNumber, int32 channel);
DLLFUNC int32 IfmSaveAGCStatus(int32 devNumber, int32 channel);

// normally IfmSetToZero sets the length values to zero
// IfmSetPreset lets add a fixed offset
// must be called before IfmSetToZero, preset is in nm
DLLFUNC int32 IfmSetPreset(int32 devNumber, int32 channel, double preset);

// returns the active preset, which was set by IfmSetPreset
// attention, the preset value becumes active during IfmSetToZero
DLLFUNC double IfmGetPreset(int32 devNumber, int32 channel);

// sets the dead path, the preset values, clears the overlow and beambreak flags
// and clears the interferometer counter
DLLFUNC int32 IfmSetToZero(int32 devNumber,int32 channelMask);

// detailierte Monitoring data in service Teil als struktur
DLLFUNC int32 IfmSignalQuality(int32 devNumber,int32 channel, int32 select);
DLLFUNC int32 IfmNewSignalQualityAvailable(int32 devNumber);

DLLFUNC int32 IfmWasBeamBreak(int32 devNumber,int32 channel);
DLLFUNC int32 IfmWasLostValues(int32 devNumber);
DLLFUNC int32 IfmWasLaserUnstable(int32 devNumber,int32 channel);

// Functions for environmental data and data depending from environmental values

// returns 1 if new (since the last call of this function) environment values are available
DLLFUNC int32 IfmNewEnvValuesAvailable(int32 devNumber);


// returns the connected/configured amount of sensors
DLLFUNC int32 IfmEnvSensorCount(int32 devNumber);

// returns a flag for the sensor on place "sensor" where sensor is 0.. IfmEnvSensorCount()-1
DLLFUNC uint32 IfmSensorProperty(int32 devNumber, int32 sensor);

// returns the value of the sensor
DLLFUNC double IfmSensorValue(int32 devNumber, int32 sensor);

// returns the value of several auxilarry values, like battery level and wireless receiver smeter
DLLFUNC int32 IfmSensorAuxValue(int32 devNumber, int32 sensorNumber, int32 valueType);

// extended functions, dealing with internal positions for "sensor", for internal use only!!
DLLFUNC uint32 IfmSensorPropertyEx(int32 devNumber, int32 sensor);
DLLFUNC double IfmSensorValueEx(int32 devNumber, int32 sensor);
DLLFUNC int32 IfmEnvSensorCountEx(int32 devNumber);

// returns the temperature which is assotiated with "channel"
DLLFUNC double IfmTemperature(int32 devNumber, int32 channel);
// returns a description, from where the value is
DLLFUNC int32    IfmTemperatureFlags(int32 devNumber, int32 channel);

// returns the humidy which is assotiated with "channel"
DLLFUNC double IfmHumidity(int32 devNumber, int32 channel);
DLLFUNC int32    IfmHumidityFlags(int32 devNumber, int32 channel);

// returns the air pressure which is assotiated with "channel"
DLLFUNC double IfmAirPressure(int32 devNumber, int32 channel);
DLLFUNC int32    IfmAirPressureFlags(int32 devNumber, int32 channel);

// returns the water vapour pressure (calculated from humidy, temperature and air pressure) which is assotiated with "channel"
DLLFUNC double IfmWaterVapourPressure(int32 devNumber, int32 channel);

// returns the conversion coefficient (Edlen correction, calculated humidity, temperature and air pressure) which is assotiated with "channel"
DLLFUNC double IfmConversionCoeff(int32 devNumber, int32 channel);

// returns the conversion coefficient for the dead path correction
DLLFUNC double IfmDeadpathCoeff(int32 devNumber, int32 channel);

// returns the vacuum wavelength of the laser
DLLFUNC double IfmVacuumWavelength(int32 devNumber, int32 channel);

// returns the corrected wavelength
DLLFUNC double IfmWavelength(int32 devNumber, int32 channel);

// returns the air refraction index used for the environment correction of the channel
DLLFUNC double IfmAirRefraction(int32 devNumber, int32 channel);

// switch Edlen correction off, for example for measurements in vacuum or if you want to make your own correction
DLLFUNC void IfmEnableEdlenCorrection(int32 devNumber, int32 channel, int32 on);

// ask, if Edlen correction is enabled
DLLFUNC int32 IfmIsEdlenEnabled(int32 devNumber,int32 channel);

DLLFUNC void IfmSetTemperature(int32 devNumber, int32 channel, double value);
DLLFUNC void IfmSetHumidity(int32 devNumber, int32 channel, double value);
DLLFUNC void IfmSetAirPressure(int32 devNumber, int32 channel, double value);
DLLFUNC void IfmSetWaterVapourPressure(int32 devNumber, int32 channel, double value);
DLLFUNC void IfmSetConversionCoeff(int32 devNumber, int32 channel, double value);
DLLFUNC void IfmSetVacuumWavelength(int32 devNumber, int32 channel, double value);

DLLFUNC int32 IfmEnvironmentFlags(int32 devNumber, int32 channel);
DLLFUNC int32 IfmManualEnvironment(int32 devNumber, int32 channel);  //depricated; use IfmEnvironmentFlags
DLLFUNC void IfmResetManualEnvironment(int32 devNumber,int32 channel, int32 mask);

// calculates the real wavelength in air (also called Edlen-correction),
// based on the vacuum-wavelength, the air temperature in °C
// the pressure in Pa and the rel. humidity in %
DLLFUNC double IfmCalculateWavelength(double vacuumWL, double T, double P, double H);

// Special control commands


/*
section i2c-communication Special commands for accessing other cards

*/

/*
 Low level function for writing a block of data to a card in the interferometer
*/

DLLFUNC int32 IfmI2CRequestWrite(int32 devNumber, int32 i2cAddr, int32 ramAddr, int32 count, unsigned char* buffer);

/*
Check the last IfmI2CWrite operation

0 if successfull
IFM_ERROR_I2C_WRITE if an error has occured,
IFM_ERROR_I2C_INUSE if the system is yet waiting for the acknowledge
*/
DLLFUNC int32 IfmI2CStatus(int32 devNumber);

/*
  wie IfmI2CRequestWrite, blockiert aber so lange, bis Rï¿½ckmeldung von Firmware da oder Timeout
 */
DLLFUNC int32 IfmI2CWrite(int32 devNumber, int32 i2cAddr, int32 ramAddr, int32 count, unsigned char* buffer);



/*
 Low level function for requesting a read of a block of data from a card in the interferometer
*/
DLLFUNC int32 IfmI2CRequestRead(int32 devNumber, int32 i2cAddr, int32 ramAddr, int32 count);

/*
 Test whether a request to read was successfully.

\param devNumber the unique identifier for the device
\ret true if read has been successfully done, otherwise false

see IfmI2CRequestRead(int32 devNumber, int32 i2cAddr, int32 ramAddr, int32 count)
*/

DLLFUNC int32 IfmI2CReadReady(int32 devNumber);

/*! \brief Access to the internal read buffer

\param index the index in the buffer, valid from 0 to count-1
(see IfmI2CRequestRead(int32 devNumber, int32 i2cAddr, int32 ramAddr, int32 count))
*/
DLLFUNC unsigned char IfmI2CReadValue(int32 devNumber, int32 index);


/*
  like IfmI2CRequestRead but is blocking until read was successfully or an error has reported
*/
DLLFUNC int32 IfmI2CRead(int32 devNumber, int32 i2cAddr, int32 ramAddr, int32 count);

DLLFUNC unsigned char *IfmI2CReadBuffer(int32 devNumber);

// do not use; for internal operations only
DLLFUNC double IfmI2CReadOscFrequency(int32 devNumber, int32 card);
DLLFUNC int32 IfmI2CWriteOscFrequency(int32 devNumber, int32 card, double freq);

// Error Handling
DLLFUNC const char*IfmGetErrorString(int32 errorCode);
DLLFUNC int32 IfmGetError(); //den ersten Fehler seit letztem Aufruf dieser Funktion

// only for internal use
DLLFUNC int32 IfmOpenRawUSB(int32 uniqueId);

#ifdef _WIN32
DLLFUNC int32 IfmOpenRawCOM(int32 comNumber);
#else
DLLFUNC int32 IfmOpenRawCOM(const char *devName);
#endif


// the following functions are intended for internal use only
DLLFUNC int32 IfmSendRawPacket(int32 devNo,char *buffer, int32 len);
DLLFUNC int32 IfmRawPacketCount(int32 devNo);
DLLFUNC int32 IfmGetRawPacket(int32 devNo, int32 maxlen, char *buffer, int32 *len);


// Motor control, not implemented yet, will internally use I2C functions

/*!
\brief Stops the motor and disables the power amplifiers

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)

\ret error value
*/
DLLFUNC int32 IfmMotorStop(int32 devNumber, int32 motorNumber);

/*!
\brief Moves the motor with a constant speed

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
\param speed (in steps/s)

\ret error value
*/
DLLFUNC int32 IfmMotorMove(int32 devNumber,int32 motorNumber,int32 speed);


/*!
\brief Moves the motor to a new position relative to the current position

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
\param position the amount of steps the motor should move
\param speed (in steps/s)

\ret error value
*/
DLLFUNC int32 IfmMotorMoveRel(int32 devNumber, int32 motorNumber,int32 position,int32 speed);

/*!
\brief Moves the motor to a new position

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
\param position the new position
\param speed (in steps/s)

\ret error value
*/
DLLFUNC int32 IfmMotorMoveAbs(int32 devNumber, int32 motorNumber,int32 position, int32 speed);

/*!
\brief Sets the a position

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
\param newPosition the new position

This function only updates the internal position counter. The motor will not move.

\ret error value
*/
DLLFUNC int32 IfmMotorSetPos(int32 devNumber, int32 motorNumber,int32 newPosition);

/*!
\brief Enables the motor

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)

\ret error value
*/
DLLFUNC int32 IfmMotorEnable(int32 devNumber, int32 motorNumber);

/*!
\brief Disables the motor

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)

\ret error value
*/
DLLFUNC int32 IfmMotorDisable(int32 devNumber, int32 motorNumber);

/*!
\brief Requests the status of the motor

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)

The transmission of the status takes up to appox. 100 milliseconds. This function requests the transmission and returns immediately.
The status itself can be read using IfmMotorStatus.

IfmMotorReadStatus requests the status and blocks until the data are transferred.

\ret error value
*/
DLLFUNC int32 IfmMotorRequestStatus(int32 devNumber, int32 motorNumber);

/*!
\brief Read the status of the motor

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
\param status pointer to an integer an which the status word will be written
\param position pointer to an integer on which the current position will be written
\param application pointer to an integer on which an identifier of the motor will be written. This identifier stands for the specific application
 (gauging probe, tonometer test, NMM ...) the motor card is configured for

Before using this function the status must be requested using IfmMotorRequestStatus. If the requested status is not yet available,
the function returns with an error.

\ret error value
*/

DLLFUNC int32 IfmMotorStatus(int32 devNumber, int32 motorNumber,int32 *status, int32 *position, uint32 *application);

/*!
\brief Read the status of the motor

\param devNumber the unique identifier for the device
\param motorNumber the number of the motor
(each controller card controls two motors, 0 and 1 refers the motors of the first card, 2 and 3 the motors of a second controller card and so on)
\param status pointer to an integer an which the status word will be written
\param position pointer to an integer on which the current position will be written
\param application pointer to an integer on which an identifier of the motor will be written. This identifier stands for the specific application
 (gauging probe, tonometer test, NMM ...) the motor card is configured for
\param timeout_ms the time in ms this function will wait for the status information. Should be typically above 200ms.

\ret error value
*/
DLLFUNC int32 IfmMotorReadStatus(int32 devNumber, int32 motorNumber,int32 *status, int32 *position, uint32 *application,int32 timeout_ms);


// service functions; do not use

DLLFUNC int32 IfmMotorRequestControlStruct(int32 devNumber, int32 motorNumber);
DLLFUNC int32 IfmMotorGetControlStruct(int32 devNumber, int32 motorNumber,unsigned char *buffer);
DLLFUNC int32 IfmMotorSetControlStruct(int32 devNumber, int32 motorNumber,unsigned char *buffer);

DLLFUNC int32 IfmRequestFactoryCfg(int32 devNumber);
DLLFUNC int32 IfmRequestSystemCfg(int32 devNumber);
DLLFUNC int32 IfmGetSystemCfg(int32 devNumber,void *cfg);
DLLFUNC int32 IfmSetSystemCfg(int32 devNumber,void *cfg);
DLLFUNC int32 IfmMirrorSystemCfg(int32 devNumber);

DLLFUNC int32 IfmSendByteArray(int32 devNumber, void *Data);       // Bootloader
DLLFUNC int32 IfmSendBootAddr(int32 devNumber, void *Data);        // Bootloader
DLLFUNC int32 IfmGetAnswer(int32 devNumber);                       // Bootloader

DLLFUNC int32 IfmSpiCommand(int32 devNumber, int32 command, int32 val1, int32 val2);
DLLFUNC int32 IfmSpiAnswer(int32 devNumber, int32 *val1, int32 *val2, int32 *val3);

DLLFUNC void IfmSetSensorValue(int32 devNumber, int32 sensorNumber, double value);
DLLFUNC void IfmSetSlaveSensorValue(int32 devNumber, int32 sensorNumber, double value);
DLLFUNC void IfmSetSensorProperty(int32 devNumber, int32 sensorNumber, int32 value);

// Human readable error message
DLLFUNC const char* IfmGetErrorString(int32 errorCode);



#ifdef _MSC_VER
#    pragma pack( pop, packing )
#endif

#endif
