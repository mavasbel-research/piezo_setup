
Private Declare Function ifminit& Lib "siosIfmvb6.dll" Alias "IfmInit@0" () 
Private Declare Sub IfmClose Lib "siosIfmvb6.dll" Alias "IfmClose@0" ()     
Private Declare Sub IfmCloseDevice Lib "siosIfmvb6.dll" Alias "IfmCloseDevice@4" (ByVal devNr&) 
Private Declare Function IfmSearchUSBDevices& Lib "siosIfmvb6.dll" Alias "IfmSearchUSBDevices@0" ()  

'Private Declare Function IfmUSBDeviceSerial Lib "siosIfmvb6.dll" Alias "IfmUSBDeviceSerial@4" (ByVal uniqueId&) As Long  

Private Declare Function IfmOpenUSB& Lib "siosIfmvb6.dll" Alias "IfmOpenUSB@4" (ByVal uniqueId&) 
Private Declare Function IfmDeviceValid& Lib "siosIfmvb6.dll" Alias "IfmDeviceValid@4" (ByVal devNr&)

Private Declare Function IfmStart& Lib "siosIfmvb6.dll" Alias "IfmStart@4" (ByVal devNr&) 
Private Declare Function IfmStop& Lib "siosIfmvb6.dll" Alias "IfmStop@4" (ByVal devNr&)  
Private Declare Sub IfmEnableEdlenCorrection Lib "siosIfmvb6.dll" Alias "IfmEnableEdlenCorrection@12" (ByVal devNr&, ByVal Channel&, ByVal EdlenOn&) 

Private Declare Function IfmIsEdlenEnabled& Lib "siosIfmvb6.dll" Alias "IfmIsEdlenEnabled@8" (ByVal devNr&, ByVal Channel&)
Private Declare Function IfmGetDeadPath& Lib "siosIfmvb6.dll" Alias "IfmGetDeadPath@8" (ByVal devNr&, ByVal Channel&)
Private Declare Function IfmSetDeadPath& Lib "siosIfmvb6.dll" Alias "IfmSetDeadPath@12" (ByVal devNr&, ByVal Channel&, ByVal deadPath&)

Private Declare Function IfmSetMeasurement& Lib "siosIfmvb6.dll" Alias "IfmSetMeasurement@16" (ByVal devNr&, ByVal measurementFlags&, ByVal outputWordRate#)
Private Declare Function IfmWasBeamBreak& Lib "siosIfmvb6.dll" Alias "IfmWasBeamBreak@8" (ByVal devNr&, ByVal Channel&)
Private Declare Function IfmWasLaserUnstable& Lib "siosIfmvb6.dll" Alias "IfmWasLaserUnstable@8" (ByVal devNr&, ByVal Channel&)
Private Declare Function IfmStatus& Lib "siosIfmvb6.dll" Alias "IfmStatus@8" (ByVal devNr&, ByVal Channel&)

Private Declare Function IfmSetToZero& Lib "siosIfmvb6.dll" Alias "IfmSetToZero@8" (ByVal devNr&, ByVal channelMask&) 'internen Counter Null setzen
Private Declare Function IfmClearBuffers& Lib "siosIfmvb6.dll" Alias "IfmClearBuffers@4" (ByVal devNr&)     'Puffer löschen

Private Declare Function IfmValueCount Lib "siosIfmvb6.dll" Alias "IfmValueCount@4" (ByVal devNr&) As Long 'Zahl der Einträge im Buffer
Private Declare Function IfmGetRecentValues Lib "siosIfmvb6.dll" Alias "IfmGetRecentValues@8" (ByVal devNr&, ByVal index&) As Long 'Messwert aus Puffer lesen
Private Declare Function IfmLengthValue Lib "siosIfmvb6.dll" Alias "IfmLengthValue@8" (ByVal devNr&, ByVal Channel&) As Double 'aktueller Messwert, Kanal 0

Private Declare Function IfmSensorValue Lib "siosIfmvb6.dll" Alias "IfmSensorValue@8" (ByVal devNr&, ByVal senNr&) As Double
