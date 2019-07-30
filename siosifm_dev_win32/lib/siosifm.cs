using System;
using System.Collections.Generic;
using System.Text;

namespace IBADos.ProCaTS.Sios

{
	#region Enums for RE-06 and RE-10 

	public enum InterferometerCardType
	{
		Undefined=0,
		RE10=1,
		RE06=2,
	}

	#region RE-10

	public enum IFM_CONST
		{

			IFM_MIN_TEMP = 4,
			// °C
			IFM_MAX_TEMP = 50,

			IFM_MIN_AIRPRESSURE = 85000,
			// Pa
			IFM_MAX_AIRPRESSURE = 120000,

			IFM_MIN_HUMIDITY = 3,
			// %
			IFM_MAX_HUMIDITY = 99,
		} ;

// -----------------------------------------------------Flags for settings of the parameter triggerMode in  the function :---------------------------
// ----------------------------------------------int IfmSetTrigger(int devNumber, unsigned int triggerMode),-----------------------------------------
// Functions for starting and stopping measurements
		public enum IFM_TRIGGER
		{
			IFM_TRIGGER_OFF = 0,



// Trigger-Input:
			IFM_TRIGGER_START = 0x0001,
			//start of measuring values after a valid (falling or rising) edge
			IFM_TRIGGER_STARTSTOP_PROC = 0x0002,
			//the StartStop-input of processed values
			IFM_TRIGGER_STARTSTOP = 0x0004,
			//the StartStop-input of raw values

// Clock-Input
			IFM_TRIGGER_CLOCK = 0x0008,
			// clocks in unprocessed values from the counter/interpolator unit
			// It can be used to use an external sample rate or
			// to synchronize the sampling with external hardware (for example, incremental encoders)

//Event-Input
			IFM_TRIGGER_EVENT = 0x0010,
			// takes a processed value and sends it to the PC

// Edge definitions for Trigger
			IFM_TRIGGER_CLOCK_RISING_EDGE = 0x0100,
			//rising edge in the ext. clock input is validly
			IFM_TRIGGER_STARTSTOP_RISING_EDGE = 0x0200,
			//rising edge in the trigger  input is validly
			IFM_TRIGGER_EVENT_RISING_EDGE = 0x0400,
			//rising edge in the event input is validly
		} ;

//Data rate of external clock or single value, for internal use only
		public enum IFM_OWR
		{
			IFM_OWR_FAST = 0x1000,
			//fast data rate (OWR>200 Hz)
			IFM_OWR_SLOW = 0x2000,
			//slow data rate (OWR<=200Hz)
		} ;
//-----------------------------------------------------------------------------------------------------------------------------------------------------

//--------------------------------------------------------Flags for settings of the parameter filterFlags in the function------------------------------
//-------------------------------------------------------int IfmSetFilter(int devNumber, unsigned int filterFlags,int avg1, int avg2)------------------
// for experts only
		public enum IFM_FILTER
		{

			IFM_FILTER_STAGE1 = 0x01,
			//Filter stage 1 (FIR) is on
			IFM_FILTER_STAGE2 = 0x02,
			//Filter stage 2 (avg2) is on
			IFM_FILTER_AVG9 = 0x04,
			// AVG9 in stage 3 is on
			IFM_FILTER_AVG6 = 0x08,
			// AVG6 in stage 3 is on
			IFM_FILTER_AVG5 = 0x10,
			// AVG5 in stage 3 is on
//Enum [int] IFM_FILTER_STAGE30 (IFM_FILTER_AVG9|IFM_FILTER_AVG6|IFM_FILTER_AVG5), //Filter stage 3 is on
		} ;

//-------------------------------------------------------------------------------------------------------------------------------------------------------

// -----------------------------------------------------Flags for settings of measurementFlags in  the function :-----------------------------------------
// ----------------------------------------------IfmSetMeasurement(int devNumber,unsigned int measurementFlags, int outputWordRate)-----------------------
		public enum IFM_MEAS
		{
			IFM_MMASK_DEFAULT = 0x0106, //One channel, , SINX + COSX

// Field "MeasurementFlags", mask definition
			IFM_MEAS_ONECHANNEL = 0x0100,
			//Channel number 1 is on
			IFM_MEAS_TWOCHANNEL = 0x0300,
			//Channel number 1 and 2 are on
			IFM_MEAS_THREECHANNEL = 0x0700,
			//Channel number 1 to 3 are on
			IFM_MEAS_FOURCHANNEL = 0x0F00,
			//Channel number 1 to 4 are on

			IFM_MEAS_TWOCHANNELS = IFM_MEAS_TWOCHANNEL,
			IFM_MEAS_THREECHANNELS = IFM_MEAS_THREECHANNEL,
			IFM_MEAS_FOURCHANNELS = IFM_MEAS_FOURCHANNEL,


			IFM_MEAS_CH1 = 0x0100,
			IFM_MEAS_CH2 = 0x0200,
			IFM_MEAS_CH3 = 0x0400,
			IFM_MEAS_CH4 = 0x0800,


			IFM_MEAS_USERMODE = 0x0001,
			// Reserved
			IFM_MEAS_LENGTH = 0x0002,
			// Full length information
			IFM_MEAS_SINCOS = 0x0004,
			// SINX / COSX
			IFM_MEAS_CIRCLE = 0x0008,
			// Amplitude of the lissagous figure
			IFM_MEAS_PATTERN = 0x0010,
			// Test pattern
			IFM_MEAS_CLOCKCOUNT = 0x0020,
			// Internal clock counter, 50MHz timebase
			IFM_MEAS_VAL_COUNTER = IFM_MEAS_CLOCKCOUNT,
			// for compatibility
			IFM_MEAS_SAMPLECOUNT = 0x0080,
			// Sample counter
			IFM_MEAS_VAL_MASK = (0x003F | 0x0080),
			// Selection of measurement values is coded in these bits
			IFM_MEAS_BEAMBREAK_OFF = 0x0040,
			// BeamBreak should not be monitored

			IFM_MEAS_FILTER_DEFAULT = 0x0000,
			//The default filter is to use
			IFM_MEAS_FILTER_OFF = 0x1000,
			//No filtering
			IFM_MEAS_FILTER_USER = 0x2000,
			//The user filter is to use
			IFM_MEAS_FILTER_MASK = 0x3000,
			//Filter flags are coded in these bits

			IFM_MEAS_RAWMODE = 0x4000,
			//Mode for testing purpose, do not use
		} ;
//---------------------------------------------------------------------------------------------------------------------------------------------------------

// the channel mask for
// IfmSetToZero, IfmAngleValue, IfmAngleAvailable
		public enum IFM_CHANNEL
		{
			IFM_CHANNEL1 = 0x01,
			IFM_CHANNEL2 = 0x02,
			IFM_CHANNEL3 = 0x04,
			IFM_CHANNEL4 = 0x08,
		} ;

// special for IfmAngleValue
// return the angle in seconds instead of mrad
		public enum IFM_ANGLE
		{
		IFM_ANGLE_SEC = 0x80,
		}

// IfmSensorProperty
		public enum IFM_ENVIR
		{

// Type of the Sensor
			IFM_ENVIR_SENSOR_TEMP = 0x10,
			IFM_ENVIR_SENSOR_HUMIDITY = 0x20,
			IFM_ENVIR_SENSOR_AIRPRESSURE = 0x30,

// which channels is the sensor assigned?
			IFM_ENVIR_CHANNEL1 = 0x01,
			IFM_ENVIR_CHANNEL2 = 0x02,
			IFM_ENVIR_CHANNEL3 = 0x04,
			IFM_ENVIR_CHANNEL4 = 0x08,


//Flag to mark the values for Edlen-corection
			IFM_ENVIR_EDLEN = 0x80,


// channel and sensor type are coded in one byte
// the following masks allow better to distinguish
			IFM_ENVIR_SENSORMASK = 0x0070,
			IFM_ENVIR_CHANNELMASK = 0x000F,
			IFM_ENVIR_VALID = 0x0100,
			IFM_ENVIR_CURRENT = 0x0200,
		} ;

//IfmSetOptions
		public enum IFM_OPTION
		{
			IFM_OPTION_DEBUGFILES = 0x0001,
			IFM_OPTION_POLLSELF = 0x0002,
			IFM_OPTION_BLOCKONCLOSE = 0x0003,
			IFM_OPTION_BOOTLOADER = 0x0004,
			IFM_OPTION_BEAMBREAK = 0x0005,
		} ;
		                  
//IfmDeviceInfo
// the following information can be requested with IfmDeviceInfo
		public enum IFM_DEVINFO
		{
			IFM_DEVINFO_SRATE = 1,
			//current sampleRate (internal, before reduction by filters)
			IFM_DEVINFO_OUTRATE = 2,
			//output word rate, like set by IfmSetMeasurement or saved in the flash
			// this is the real output wird rate, which may be differ from the selected due to steps in possible sample rate
			IFM_DEVINFO_FILTERFLAGS = 3,
			//filter flags, like set by IfmSetFilter or saved in the flash
			IFM_DEVINFO_MEASUREMENTFLAGS = 4,
			//mesurement flags, like set by IfmSetMeasurement or saved in the flash
			IFM_DEVINFO_TRIGGERMODE = 5,
			//trigger mode, like set by IfmSetTrigger or or saved in the flash
			IFM_DEVINFO_AVG1 = 6,
			//filter option for the average 1, like set by IfmSetFilter or saved in the flash
			IFM_DEVINFO_AVG2 = 7,
			//filter option for the average 2, like set by IfmSetFilter or saved in the flash
			IFM_DEVINFO_AVAILABLE = 8,
			// infos available, if not wait until the DLL has get it from the device
			IFM_DEVINFO_SERIALNUMBER = 9,
			// return the (USB-) serial number of the card
			IFM_DEVINFO_RESETSTATUS = 10,
			// resets the given bits in the device status
			IFM_DEVINFO_READY = 11,
			// ready for IfmStart
			IFM_DEVINFO_VERSIONSTRING = 12,
			// Firmware-Version and compiling data
			IFM_DEVINFO_FPGAVERSION = 13,
			// Version of the programmable hardware (FPGA)
			IFM_DEVINFO_OUTRATE_POINTER = 14,
			// Ponter to a double value, containing the OWR in higher resolution
			IFM_DEVINFO_LINKEDCHANNELS1 = 15,
			// wich channels are linked to calculate an angle
			IFM_DEVINFO_LINKEDCHANNELS2 = 16,
			// there are two pairs of linked channels possible
			IFM_DEVINFO_BASEDISTANCE1_POINTER = 17,
			// base distance of the linkes channels
			IFM_DEVINFO_BASEDISTANCE2_POINTER = 18,
			// same for the second pair
			IFM_DEVINFO_LAST_I2C_CARDADDR = 19,
			// card address of the active or last I2C request
			IFM_DEVINFO_LAST_I2C_MEMADDR = 20,
			// memory address of the active or last I2C request
			IFM_DEVINFO_SRATE_POINTER = 21,
			// pointer to the current sample rate
			IFM_DEVINFO_CMDDELAY = 100,
			// delay in ms between transmitted commands
			IFM_DEVINFO_I2CTIMEOUT = 101,
			// timeout in ms for IfmI2CRead and IfmI2CWrite
		} ;

// types for IfmAuxValues
		public enum IFM_VALUETYPE
		{
			IFM_VALUETYPE_COS = 1,

			IFM_VALUETYPE_ADC1 = 1,

			IFM_VALUETYPE_SIN = 2,

			IFM_VALUETYPE_ADC2 = 2,

			IFM_VALUETYPE_NORM = 3,

			IFM_VALUETYPE_TESTPATTERN = 4,

			IFM_VALUETYPE_CLOCKCOUNT = 5,

			IFM_VALUETYPE_COUNTER = 5,

			IFM_VALUETYPE_SAMPLECOUNT = 6,
		} ;

// Parameter select for IfmSignalQuality(int devNumber,int channel, int select)
		public enum IFM_SIGNALQ
		{
			IFM_SIGNALQ_A1 = 0x10,
			//Amplitude of the signal 1
			IFM_SIGNALQ_O1 = 0x20,
			//Offset of the signal 2
			IFM_SIGNALQ_A2 = 0x40,
			//Amplitude of the signal 2
			IFM_SIGNALQ_O2 = 0x80,
			//Offset of the signal 2
			IFM_SIGNALQ_SUM = 0x100,
			//Overall quality from 0..100%
			IFM_SIGNALQ_FREQ = 0x200,
			//Frequency of the reference mirror vibrator
			IFM_SIGNALQ_STATE = 0x400,
			//Status of the signal control card, for internal use
		} ;

// IfmManualEnvironment
		public enum IFM_ENVIR_MANUAL
		{
			IFM_ENVIR_MANUAL_T = 0x0002,
			// the temperatur was set manually
			IFM_ENVIR_MANUAL_H = 0x0004,
			// the humidity was set manually
			IFM_ENVIR_MANUAL_P = 0x0008,
			// the air pressure was set manually
			IFM_ENVIR_MANUAL_WVP = 0x0010,
			// the water vapour pressure was set manually
			IFM_ENVIR_MANUAL_CONV = 0x0020,
			// the conversion coefficient was set manually
//const int IFM_ENVIR_MANUAL_WL  		0x0040
			IFM_ENVIR_MANUAL_VWL = 0x0080,
			// the vacuum wavelength of the laser was set manually
		} ;

// IfmTemperatureFlags, IfmAirPressureFlags, IfmHumidityFlags
		public enum IFM_ENVIRFLAG
		{
			IFM_ENVIRFLAG_SENSORMASK = 0x00FF,
			// in these bits the sensor number is coded, where the value was measured
			IFM_ENVIRFLAG_MEASURED = 0x0100,
			// the value was measured, otherwise it's a default value
			IFM_ENVIRFLAG_CURRENT = 0x0200,
			// the value was measured with the last data set
			// (in a typical configuration it's not older than 4 secs)
			IFM_ENVIRFLAG_MANUAL = 0x0400,
			// value was given manually per IfmSet... function
		} ;


//Bits in the measurement data flags field, for internal use only
		public enum IFM_MFLAGS
		{
			IFM_MFLAGS_RESERVED1 = 0x01,
			IFM_MFLAGS_BEAMBREAK = 0x02,
			IFM_MFLAGS_OVERFLOW = 0x04,
			IFM_MFLAGS_MISCOUNT = 0x80,
		} ;

// IfmStatus returns the following flags

//the lower 16 bit are channel dependend
		public enum IFM_STATUS
		{
			IFM_STATUS_BEAMBREAK_QUADRANT = 0x0001,
			// miscount detected: the interferometer counter has detected an invalid jump over more than one quadrants
			IFM_STATUS_BEAMBREAK_LEVEL = 0x0002,
			// the signal amplitude is lower than a given threashold so that miscounts are likely
			IFM_STATUS_LASER_STABLE = 0x0010,
			// the laser(s) is(are) stable (only in systems with stabilized lasers)
			IFM_STATUS_LASER_WAS_UNSTABLE = 0x0020,
			// since last IfmSetZero the laser was at least one time unstable

// the upper 16 bit are independend from the channel
			IFM_STATUS_BUFFER_OVERFLOW_DEV = 0x0100,
			// the FIFO in the interferometer had an overflow, data loss by to large samplerate has occured
			IFM_STATUS_BUFFER_OVERFLOW_DLL = 0x0200,

			// the measurement value buffer in the DLL had an overlow, data loss by infrequent call of IfmGetValue
			IFM_STATUS_BLOCKMODE = 0x0400,
			// the device is in blockmode
			IFM_STATUS_TRACER_LOCK = 0x0800,
			// Tracer locked
			IFM_STATUS_BAD_REQUEST = 0x8000,
			// the status request could not be answered, perhaps due to bad deviceNumber or invalid channel
		} ;

//Device types for IfmDeviceType
		public enum FM_TYPE
		{
			IFM_TYPE_NONE = 0,
			IFM_TYPE_DEMO = 1,
			IFM_TYPE_RE10 = 2,
			IFM_TYPE_RE06 = 3,

		} ;

//Interfaces for IfmDeviceInterface
		public enum IFM_INTERFACE
		{
			IFM_INTERFACE_NONE = 0,
			IFM_INTERFACE_DEMO = 1,
			IFM_INTERFACE_RS232 = 2,
			IFM_INTERFACE_USB = 3,
			IFM_INTERFACE_NET = 4,
		} ;


// Error codes
		public enum IFM_ERROR
		{
			IFM_ERROR_NONE = 0,//The function was executed successfully. No error has occurred.
			IFM_ERROR_DEVICE_INVALID = -1,//The function has tried to access a device which is not valid. The devNumber parameter was wrong (out of range, device was not opened, device was closed...)
			IFM_ERROR_BAD_CHANNEL = -2,//The channel number was wrong. Up to four channels are supported for each device, so channel numbers can be 0,1, 2 or 3.
			IFM_ERROR_BAD_DEVICETYPE = -3,//The DLL supports more device types than the RE-10 for which it was created. But this operation is not possible with the given device because of the type doesn't support it. Some operations can for instance only be made with RE-10 devices.
			IFM_ERROR_DATALEN = -4,//The requested block of data is too large. It may be device dependent what amount is supported.
			IFM_ERROR_BAD_DEVICE = -5,//IFM_ERROR_DEVICE_INVALID,
			IFM_ERROR_UNKNOWN = -6,//An error with a non specified case has occurred.
			IFM_ERROR_DEVICECOUNT_OVERFOW = -10,//The maximum amount of opened devices has exceeded. It's not likely that this occurs under normal conditions.
			IFM_ERROR_BAD_REQUESTTYPE = -11,//You have requested an information which is not available.
			IFM_INVALID_USB_ID = -12,//The id to identify the USB device (found with IfmSearchUSBDevices) is not valid
			IFM_ERROR_CREATE_HANDLE = -13,//The device could not be opened. Perhaps the resource (com-number, device file ..) is not present or is already in use.
			IFM_ERROR_NOT_IMPLEMENTED = -100,//This function exists as prototype but is not yet implemented.
			IFM_ERROR_I2C_IN_USE = -15,//The I2C subsystem is already in use.
			IFM_ERROR_I2C_WRITE = -16,//The write operation was not successful.
			IFM_ERROR_I2C_TIMEOUT = -17,//The I2C operation could not be carried out in the given time.
			IFM_ERROR_OWR_TO_HIGH = -18,//The requested output word rate (OWR) was too high or the resulting sample rate (with user filter settings) was too high
			IFM_ERROR_INFO_NOT_AVAILABLE = -19,//The requested information is not yet available. Try it again later.
			IFM_BAD_SENSOR = -20,//The sensorNumber in this function is invalid.
			IFM_ERROR_I2C_READ = -21,
			
		} ;
	#endregion RE-10


	#region RE-06
		/// <summary>
		/// Errors
		///dec 2    = 0x0002 (Hex) Signal amplitude bellow threshold -zu hohe verstärkung des Signales
		///dec 4096 = 0x1000 (Hex) Laser beam break reported by signal amplifier -  kurzfristige strahlunterbrechung
		/// </summary>
		public enum InterferometerErrorListRe06
		{
			BeamShortBreak = 4096,
			BeamAmplitudeLow = 2,
		}
		#endregion RE-06

	#endregion Enums

		public class Re06
	{
	#region SIOS method initialisation for siosusb.dll (only RE-06 Card und old FW)

		[System.Runtime.InteropServices.StructLayout(System.Runtime.InteropServices.LayoutKind.Sequential, Pack = 1)]
		public struct IMPTONM_REC
		{
			public ushort Status;
			public double ConversionK;
			public double DeadPathK;
		}
		#region Method for connection to USB of Interferomether
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern int SearchForSIOSDevices(string listName);
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern bool ConfigUSBDevice(int deviceNumber);
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern string GetDeviceSerialNumber(int deviceNumber);
		#endregion

		#region Read current value
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern bool SetToZero(int deviceNumber, long deadPath);
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		//public static extern bool ReadLengthValues(long DevNum, IntPtr NValues, IMPTONM_REC Rec);
		public static extern bool ReadLengthValues(ushort DevNum, IntPtr NValues, IntPtr Rec);
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern double ReadNextBufValueLV(int deviceNumber);
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern bool ReadLastLengthValueML(ushort DevNum, IntPtr NValues);
		#endregion

		#region Close connection to USB of interferomether
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern bool UnConfigUSBDevice(int deviceNumber);
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern void CloseSIOSDeviceList();
		[System.Runtime.InteropServices.DllImport("siosusb.dll")]
		public static extern int GetFoundedDevices();
		#endregion

		#endregion SIOS RE-06 Card
	}

	public class Re10
	{
		#region SOIS method initialisation for siosifm.dll (only with new FW and RE-06 or RE-10 Card)

		#region Methods for connection to USB of Interferomether


		/// <summary>
		/// The function modifies some behaviour of the library. It should be called before IfmInit to take effect.
		/// </summary>
		/// <param name="option">IFM_ OPTION_DEBUGFILES If param1 is set to 1 the library creates some text files with debug informations
		///IFM_OPTION_POLLSELF Normally the library starts a thread and calls IfmPollfrequently in this thread. If param1 is set to 1, no thread is started and IfmPoll must be called by the application. Use with care!
		///IFM_OPTION_BLOCKONCLOSE Normally a device will be destroyed some times after closing it. If param1 is set to 1 IfmCloseDevice will wait until the device is closed and destroyed before returning.</param>
		/// <param name="isDebugMode">0 = false,  1 = true</param>
		/// <returns>Zero on success or an error number is returned.</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmSetOption(int option, int isDebugMode);

		

		/// <summary>
		/// This function deinitializes the library, stops the internal thread and gives free all allocated resources.
		/// </summary>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern void IfmClose();


		/// <summary>
		/// This function get the device serial
		/// </summary>
		/// <param name="devNumberOnUsbBus">Number of device on the USB-bus </param>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern void IfmUSBDeviceSerial(int devNumberOnUsbBus);

		/// <summary>
		/// This function deinitializes a device which has been opened by IfmOpenCOM or IfmOpenUSB. The devNumber becomes invalid after calling this function. The device cannot be used later.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device, returned by IfmOpenCOM or IfmOpenUSB</param>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern void IfmCloseDevice(int devNumber);

		/// <summary>
		/// The function IfmDeviceCount returns the number of opened devices.
		/// </summary>
		/// <returns>Required count of open devices.</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmDeviceCount();

		/// <summary>
		///This function initializes the DLL and starts an internal thread for the communication with the connected devices, this method must be called before any other function
		/// </summary>
		/// <returns>0 if the function has success, an error number otherwise.</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmInit();

		/// <summary>
		/// The function IfmMaxDeviceCount returns the number of the maximum allowed devices.
		/// </summary>
		/// <returns></returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmMaxDeviceCount();

		/// <summary>
		/// This function opens a device which is connected via the USB-interface for communication.
		/// </summary>
		/// <param name="uniqueId">The ID which describes the device. See IfmSearchUSBDevices for more information.</param>
		/// <returns>The function returns an unique ID, the devNumber, which must be used to access the device by the future calls to the library. 
		/// The devNumber is always a non negative number.In case of an error an error number is returned. Error numbers are always negative.</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmOpenUSB(int uniqueId);

		/// <summary>
		/// The function IfmSearchUSBDevices looks for devices (this time only RE-10 cards)
		///  which are connected to the PC via the USB-Bus and returns the number of connected devices. These devices can be opened by IfmOpenUSB.
		/// </summary>
		/// <returns>returns the number of connected devices</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmSearchUSBDevices();


		/// <summary>
		/// The function IfmUSBDeviceCount returns the number of devices on the USB-bus found at the last search by IfmSearchUSBDevices.
		/// </summary>
		/// <returns>Number of devices on the USB-bus.</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmUSBDeviceCount();

		#endregion

		#region Methods for configuration and measurement

		/// <summary>
		/// The function IfmSetMeasurement is used to set the measurement parameters.
		///  This function should be called directly before the measurement starts (see IfmStart).
		///  If this function is not called the settings which are saved in the flash of the interferometer are used.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="measurementFlags">Following parameter can be used: 
		///IFM_MEAS_ONECHANNEL Channel number 1 is on
		///IFM_MEAS_TWOCHANNEL Channels number 1-2 are on
		///IFM_MEAS_THREECHANNEL Channels number 1-3 are on
		///IFM_MEAS_FOURCHANNEL Channels number 1-4 are on
		///IFM_MEAS_CH1 Channel number 1 is on
		///IFM_MEAS_CH2 Channel number 2 is on
		///IFM_MEAS_CH3 Channel number 3 is on
		///IFM_MEAS_CH4 Channel number 4 is on
		///IFM_MEAS_LENGTH Full length information
		///IFM_MEAS_SINCOSSIN / COS values from the input are transmitted
		///IFM_MEAS_CIRCLE Amplitude of the Lissajous figure
		///IFM_MEAS_PATTERN Test pattern (value 0x5555)*
		///IFM_MEAS_VAL_COUNTER Internal value counter*
		///IFM_MEAS_FILTER_DEFAULT Default filter will be applied
		///IFM_MEAS_FILTER_OFF No filter will be used
		///IFM_MEAS_FILTER_USER User filter settings will be used 
		/// </param>
		/// <param name="outputWordRate"></param>
		/// <returns>0 on success, an negative error number if an error has occurred</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmSetMeasurement(int devNumber, int measurementFlags, double outputWordRate);


		/// <summary>
		/// The function sets the internal counter of the interferometer to zero 
		/// and defines the reference point for the displacement measurement.
		///  The parameter channelMask defines which channel should be cleared.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channelMask">Mask which defines, which channels should be affected (use the constants IFM_ENVIR_CHANNEL1 to IFM_ENVIR_CHANNEL4)</param>
		/// <returns>0 on success, an negative error number if an error has occurred</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmSetToZero(int devNumber, int channelMask);

		/// <summary>
		/// The function gives the measurement free.
		/// It should be used after the function IfmSetMeasurement. 
		/// Otherwise the device takes the settings, that has been saved in the flash as default settings. 
		/// See functions IfmSaveConfigDevice and IfmSetMeasurement for the detailed information.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns>0 on success, an negative error number if an error has occurred</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmStart(int devNumber);

		/// <summary>
		/// The function stops the measurement. It's the counterpart to IfmStart.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns>0 on success, an negative error number if an error has occurred</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmStop(int devNumber);

		/// <summary>
		/// The function IfmLengthValue is to read out the length measuring values,
		///  that was extracted from a data field of the input buffer. 
		/// It is intended to use directly after the function IfmGetValues or IfmGetRecentValues
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">Channel number</param>
		/// <returns>measuring value in nanometres</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern double IfmLengthValue(int devNumber, int channel);

		/// <summary>
		/// The function delivers the count of the samples which are available in the input buffer. 
		/// The count is incremented by incoming data from the device and decremented by IfmGetValues.
		/// See also IfmGetValues for more information.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns>Count of values which can be read out from the input buffer by IfmGetValues.</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmValueCount(int devNumber);


		/// <summary>
		/// This function is used to request of the measuring values from the input buffer. 
		/// The available values will be read out according to FIFO (first in first out) principle. 
		/// Usually this function will be used together with the functions IfmLengthValue, IfmRawValue or IfmAuxValue.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns>0 on success (otherwise a negative error number)</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmGetValues(int devNumber);


		/// <summary>
		/// The function IfmGetRecentValues is used to read out the measurement values at the indexreadout from the input puffer.
		/// indexreadout=count−index−1 
		/// The count of the measuring values can be requested by the function IfmValueCount
		/// In contrast to IfmGetValues this function does not influence the amount of available values which is returned by IfmValueCount.
		/// </summary>
		/// <param name="devNumber">Unique ID for the devic</param>
		/// <param name="index">Index, 0 means the most recent value</param>
		/// <returns></returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmGetRecentValues(int devNumber, int index);

		/// <summary>
		/// Normally IfmSetToZero defines the reference point for the measurement and sets the length value to 0. 
		/// There are possible applications where it seems more practical to set the position at the reference point to another value, the so called preset value. 
		/// IfmSetPreset sets this preset value.
		/// IfmSetPreset must be called before IfmSetToZero, and that the preset value becomes active not before IfmSetToZero is called
		/// 
		/// This cann used for set the laser offset. In this case the offset is automaticaly allowed.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">Channel number</param>
		/// <param name="presetValue">The value, IfmLengthValue should return at the reference position in nm</param>
		/// <returns>0 in success, otherwise an error number</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmSetPreset(int devNumber, int channel, double presetValue);


		/// <summary>
		/// With IfmSetPreset a so called preset value can be set, what sets the reference point, defined with IfmSetToZero to a length value other than zero.
		/// The preset value becomes active when IfmSetToZero is called and the zeroing procedure (which may take some ms) is complete!!!!
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">Channel number</param>
		/// <returns>The current preset value in nm. In case of an error, it returns always 0.</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern double IfmGetPreset(int devNumber, int channel);


		/// <summary>
		/// function the erasing of the PC-input buffer
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns>0 in success, otherwise an error number</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmClearBuffers(int devNumber);




		#endregion Method for configuration and measurement

		#region Functions for the controlling of the interferometers

		/// <summary>
		/// The function delivers the required value dependent on the input parameters.
		/// The sampling period can be different. The typical value is 500 ms.
		/// Please note, for the adjusting of the laser signal the mirror vibration modulator 
		/// and amplifier gain controller should be set on (See IfmSetRefMirrorVibration and IfmSetAGC)
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">channel number (from 0 up to 3)</param>
		/// <param name="select">selectpossible selection (defined in siosifmdef.h):</param>
		/// <returns></returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmSignalQuality(int devNumber, int channel, int select);
		#region Signal quality notation
		// IFM_SIGNALQ_A1
		//    Amplitude of the sine-signal
		//Amplifier gain:
		//0: the best signal quality
		//255: the worst signal quality
		//IFM_SIGNALQ_O1
		//Offset of the sine-signal*
		//Offset position:
		//127 (=50%): the best position
		//0, 255: the worst positions
		//IFM_SIGNALQ_A2
		//Amplitude of the cosine-signal
		//Amplifier gain:
		//0: the best signal quality
		//255: the worst signal quality
		//IFM_SIGNALQ_O2
		//Offset of the cosine-signal*
		//Offset position:
		//127 (=50%): the best position
		//0, 255: the worst positions
		//IFM_SIGNALQ_SUM
		//Overall signal
		//Amplitude signal quality in (0..100)% in both channels together. The best value: 100%
		#endregion  Signal quality notation


		/// <summary>
		/// This function delivers the state of the controller for the according device and channel.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">channel number (from 0 up to 3)</param>
		/// <returns>0 for the state “controller is off”, 1 for the state “controller is on”</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmGetAGC(int devNumber, int channel);


		/// <summary>
		/// This function sets the state of the controller for the according device and channel. 
		/// The switching on of the controller has got a sense only if the the mirror vibration (modulator) is on too. 
		/// See also IfmSetRefMirrorVibration, IfmGetRefMirrorVibration, IfmGetAGC.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">channel number (from 0 up to 3)</param>
		/// <param name="on">0 for the state “controller is off”, 1 for the state “controller is on”<</param>
		/// <returns>0 on success, an negative error number in case of an error</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmSetAGC(int devNumber, int channel, int on);


		/// <summary>
		/// This function delivers the state of the mirror vibration for the according device and channel.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">channel number (from 0 up to 3)</param>
		/// <returns>0 for the state “vibration is off”, 1 for the state “vibration is on”</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmGetRefMirrorVibration(int devNumber, int channel);

		/// <summary>
		/// This function delivers the state of the mirror vibration for the according device and channel.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">channel number (from 0 up to 3)</param>
		/// <returns>0 for the state “vibration is off”, 1 for the state “vibration is on”</returns>
		/// <param name="on">0 means “the set the modulator off”, 1 means “the set the modulator on”</param>
		/// <returns></returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmSetRefMirrorVibration(int devNumber, int channel, int on);



		/// <summary>
		/// This function delivers the information about the device status as well as about the possible measuring error sources.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">channel number (from 0 up to 3)</param>
		/// <returns>The flags, which can be set ( defined in “siosifmdef.h” ): </returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmStatus(int devNumber, int channel);
		#region Status notation
		///The lower 16 bit are channel depended:
		///IFM_STATUS_LASER_STABLE the laser(s) is(are) stable (only in systems with stabilized lasers)
		/// IFM_STATUS_LASER_WAS_UNSTABLE since last IfmSetToZero the laser was at least one time unstable
		/// IFM_STATUS_BEAMBREAK_QUADRANT miscount detected: the interferometer counter has detected an invalid jump over more than one quadrants
		/// IFM_STATUS_BEAMBREAK_LEVEL the signal amplitude is lower than a given threshold so that miscounts are likely
		/// The upper 16 bit are independent from the channel:
		/// IFM_STATUS_BUFFER_OVERFLOW_DEV the FIFO in the interferometer had an overflow; dataloss by to large sample rate has occurred
		/// IFM_STATUS_BUFFER_OVERFLOW_DLL the measurement value buffer in the DLL had an overflow; data loss by infrequent call of IfmGetValues
		/// IFM_STATUS_BLOCKMODE the device is in block mode
		/// IFM_STATUS_BAD_REQUEST the status request could not be answered, perhaps due to bad deviceNumber or invalid channel
		#endregion Status notation


		/// <summary>
		/// This function checks whether the laser beam was broken in the according device and sensor channel. It can cause a failed measurement.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">channel number (from 0 up to 3)</param>
		/// <returns>zero for the state “the beam was NOT broken” or 1 for the state “the beam was broken”</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmWasBeamBreak(int devNumber, int channel);

		/// <summary>
		/// This function checks whether the laser was unstable in the according device and sensor channel. 
		/// An unstable laser is an error source for a measurement. This option is relevant only for the stabilized laser.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <param name="channel">channel number (from 0 up to 3)</param>
		/// <returns>zero for the state “the laser was stable” or 1 for the state “the laser was unstable”</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmWasLeaserUnstable(int devNumber, int channel);


		/// <summary>
		/// This function checks whether the measuring values ware lost due to buffer overflow in the PC or device. For the getting of exact information see IfmStatus.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns>zero for the state “no measuring values were lost” or 1 for the state “the measuring values were lost”</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmWasLostValues(int devNumber);

		#endregion Functions for the controlling of the interferometers

		#region Extended functions

		/// <summary>
		/// 
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns></returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int intIfmDeviceType(int devNumber);

		/// <summary>
		/// The function returns the count in the device available channels
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns>Required information if the answer >=0 or error code otherwise</returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmCannels(int devNumber);


		/// <summary>
		/// The function returns the device type.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns>
		/// IFM_TYPE_NONE No information about the device type
		/// IFM_TYPE_DEMO The demo-application runs
		/// IFM_TYPE_RE10 The device type is the RE-10-card
		/// IFM_TYPE_RE06 The device type is the RE-06-card
		/// </returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmDeviceType(int devNumber);

		/// <summary>
		/// The function returns the version number of the firmware for required device.
		/// </summary>
		/// <param name="devNumber">Unique ID for the device</param>
		/// <returns></returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmFirmwareVersion(int devNumber);

		/// <summary>
		/// The function returns the first error number after last calling of this function.
		/// </summary>
		/// <returns></returns>
		[System.Runtime.InteropServices.DllImport("siosifm.dll")]
		public static extern int IfmGetError();
		#endregion Extended functions
		#endregion SOIS method initialisation for siosifm.dll
	}
	
}
