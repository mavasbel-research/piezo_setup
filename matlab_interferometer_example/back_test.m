% Test Script
clc

% Please write the path where the dll is here
dllPath = pwd;
cd(dllPath);
% Load library to Matlab
if(~libisloaded('siosifm64'))
%    [nf, m]=loadlibrary('siosifm','siosifmdll.h')
   [notfound, message]=loadlibrary('../commons/64bit/siosifm64.dll',...
    '../commons/include/siosifmdll.h',...
    'includepath',strcat([pwd(),'/../commons/include']))
end 

% Give an overview to all functions
libfunctions('siosifm64')

% Init the dll
err = calllib('siosifm64','IfmInit');
if(err<0)
   error('Error during IfmInit!');
   return;
end

% search for connected devices and stop the script if a device couldn't found
cnt = calllib('siosifm64','IfmSearchUSBDevices');
if(cnt<1)
   error('No devices found');
   return;
end

% open the first device
disp(sprintf('Open device with serial number %d\n',calllib('siosifm64','IfmUSBDeviceSerial',int32(0))));
devNo = calllib('siosifm64','IfmOpenUSB',int32(0));
if(devNo<0)
   calllib('siosifm64','IfmClose');
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

err = calllib('siosifm64','IfmSetMeasurement',int32(devNo),measurementFlag,2.5);
if(err<0)
   calllib('siosifm64','IfmClose');
   error('Error during set measurement.');
end

% begin with the output of data
err = calllib('siosifm64','IfmStart',int32(devNo));
if(err<0)
   calllib('siosifm64','IfmClose');
   error('Error while starting measurement.');
end

cont = 1;
IFM_VALUETYPE_SAMPLECOUNT = int32(6);
pause(6);
while(cont)
   % are new values available?
   cnt = calllib('siosifm64','IfmValueCount',int32(devNo));
   if(cnt>0)
      % put the value in an internal buffer for access via IfmLengthValue
      % this is necessary to access the same syncronuously sampled values (e.g. different channels) at different times
      % IfmValueCount is decremented
      strout='';
      for(k=1:cnt)
         calllib('siosifm64','IfmGetValues',int32(devNo));
         % get the values together with environmental values and the samplecounter
         strout = sprintf('%s%10.1f nm\t%10.1f nm\t%10.1f nm\t - %.2f ?C\t%.0f Pa\t- sample: %d\n',strout,...
            calllib('siosifm64','IfmLengthValue',int32(devNo),int32(0)),...
            calllib('siosifm64','IfmLengthValue',int32(devNo),int32(1)),...
            calllib('siosifm64','IfmLengthValue',int32(devNo),int32(2)),...
            calllib('siosifm64','IfmTemperature',int32(devNo),int32(0)),...
            calllib('siosifm64','IfmAirPressure',int32(devNo),int32(0)),...
            calllib('siosifm64','IfmAuxValue',int32(devNo),int32(0),IFM_VALUETYPE_SAMPLECOUNT));
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
calllib('siosifm64','IfmStop',int32(devNo));
% close the device; devNo will be no longer valid
calllib('siosifm64','IfmCloseDevice',int32(devNo));
% close the DLL
calllib('siosifm64','IfmClose');

% unload the siosifm.dll
unloadlibrary('siosifm64')
% eof