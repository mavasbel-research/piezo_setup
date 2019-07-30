% Test Script

% Please write the path where the dll is here
dllPath = pwd;
cd(dllPath);
% Load library to Matlab
if(~libisloaded('siosifm'))
   [nf, m]=loadlibrary('siosifm','siosifmdll.h')
end 

% Give an overview to all functions
libfunctions('siosifm')

% Init the dll
err = calllib('siosifm','IfmInit');
if(err<0)
   error('Error during IfmInit!');
   break;
end

% search for connected devices and stop the script if a device couldn't found
cnt = calllib('siosifm','IfmSearchUSBDevices');
if(cnt<1)
   error('No devices found');
   break;
end

% open the first device
disp(sprintf('Open device with serial number %d\n',calllib('siosifm','IfmUSBDeviceSerial',int32(0))));
devNo = calllib('siosifm','IfmOpenUSB',int32(0));
if(devNo<0)
   calllib('siosifm','IfmClose');
   error('Error during opening the device.');
end

% now we configure the measurement, at least with SetMeasurement
% we want the length values of the first 3 channels with 2.5 Hz output rate and the sample counter value
% IFM_MEAS_FILTER_DEFAULT will create an internal filter which removes the
% vibration of the reference mirror from the signal
% in some applications IFM_MEAS_FILTER_NONE may be required for unfiltered output

IFM_MEAS_THREECHANNEL = uint32(hex2dec('0700'));
IFM_MEAS_LENGTH = uint32(hex2dec('0002'));
IFM_MEAS_FILTER_DEFAULT = uint32(hex2dec('0000'));
IFM_MEAS_SAMPLECOUNT = uint32(hex2dec('0080'));
measurementFlag=bitor(IFM_MEAS_THREECHANNEL,IFM_MEAS_LENGTH);
measurementFlag=bitor(measurementFlag,IFM_MEAS_FILTER_DEFAULT);
measurementFlag=bitor(measurementFlag,IFM_MEAS_SAMPLECOUNT);

err = calllib('siosifm','IfmSetMeasurement',int32(devNo),measurementFlag,2.5);
if(err<0)
   calllib('siosifm','IfmClose');
   error('Error during set measurement.');
end

% begin with the output of data
err = calllib('siosifm','IfmStart',int32(devNo));
if(err<0)
   calllib('siosifm','IfmClose');
   error('Error while starting measurement.');
end

cont = 1;
IFM_VALUETYPE_SAMPLECOUNT = int32(6);
pause(6);
while(cont)
   % are new values available?
   cnt = calllib('siosifm','IfmValueCount',int32(devNo));
   if(cnt>0)
      % put the value in an internal buffer for access via IfmLengthValue
      % this is necessary to access the same syncronuously sampled values (e.g. different channels) at different times
      % IfmValueCount is decremented
      strout='';
      for(k=1:cnt)
         calllib('siosifm','IfmGetValues',int32(devNo));
         % get the values together with environmental values and the samplecounter
         strout = sprintf('%s%10.1f nm\t%10.1f nm\t%10.1f nm\t - %.2f °C\t%.0f Pa\t- sample: %d\n',strout,...
            calllib('siosifm','IfmLengthValue',int32(devNo),int32(0)),...
            calllib('siosifm','IfmLengthValue',int32(devNo),int32(1)),...
            calllib('siosifm','IfmLengthValue',int32(devNo),int32(2)),...
            calllib('siosifm','IfmTemperature',int32(devNo),int32(0)),...
            calllib('siosifm','IfmAirPressure',int32(devNo),int32(0)),...
            calllib('siosifm','IfmAuxValue',int32(devNo),int32(0),IFM_VALUETYPE_SAMPLECOUNT));
      end
      disp(strout);
   end
   str = input('continue (y/n)?','s');
   if(strcmp(lower(str),'n'))
      cont = 0;
   end
end   

% deinitialize

% stop the output of data
calllib('siosifm','IfmStop',int32(devNo));
% close the device; devNo will be no longer valid
calllib('siosifm','IfmCloseDevice',int32(devNo));
% close the DLL
calllib('siosifm','IfmClose');

% unload the siosifm.dll
unloadlibrary('siosifm')
% eof