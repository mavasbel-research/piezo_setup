#include <stdio.h>
#ifdef _WIN32
#include <conio.h>
#include <windows.h>
#else
#include <termios.h>
#include <string.h>
#include <time.h>
#endif
#include "siosifmdll.h"

/*

 Basic example for using the siosifm-API

 The program opens the device, configures it and
 read out the length values of 3 channels, a sample counter,
 and the environment values

 In case of a one channel device, the unused channels should be zero

 */



#ifndef _WIN32
// in Linux there is no kbhit() function, we create one
int kbhit(void) {
    struct termios term, oterm;
    int fd = 0;
    int c = 0;

    tcgetattr(fd, &oterm);
    memcpy(&term, &oterm, sizeof(term));
    term.c_lflag = term.c_lflag & (!ICANON);
    term.c_cc[VMIN] = 0;
    term.c_cc[VTIME] = 1;
    tcsetattr(fd, TCSANOW, &term);

    c = getchar();

    tcsetattr(fd, TCSANOW, &oterm);
    if (c != -1)
        ungetc(c, stdin);
    return ((c != -1) ? 1 : 0);
}

#endif

int main(int argc, char *argv[])
{

    int error=0;

    // before IfmInit; make some settings
    // IFM_OPTION_DEBUGFILES let the DLL create files with information for debug purposes
     IfmSetOption(IFM_OPTION_DEBUGFILES, false);


    // first initialize the DLL
    error=IfmInit();
    if(error){
        printf("Error %d during IfmInit\n",error);
        return(1);
    }

    // search for connected devices; returns the number of via USB connected devices
    int cnt;
    cnt=IfmSearchUSBDevices();

    if(cnt<=0){ // 0: no device connected, < 0 is an error number
        printf("A SIOS interferometer could not be found\n");
        IfmClose();
        return(0);
    }

    // now let us show the connected devices
    // in a GUI this can be used to fill a comboBox for selecting the device
    printf("\nThe following RE-10 cards are connected to the PC:\n");
    int i;
    for(i=0;i<cnt;i++){
        printf("card no. %d with serial %6.6d\n",i,IfmUSBDeviceSerial(i));
    }
    printf("\n");

    int devNo;
    // we open the first device;
    // IfmUSBDeviceSerial and IfmOpenUSB takes a parameter for selecting the
    // device from 0 to cnt-1
    printf("Open device with serial number %d\n",IfmUSBDeviceSerial(0));
    devNo=IfmOpenUSB(0);
    if(devNo<0){ //negative values are error numbers
        printf("Error during opening the device.\n");
        IfmClose();
        return(0);
    }

    // Alternatively, if the COM-Interface is known the device can also be opened directly
    // Windows: devNo=IfmOpenCom(1); for COM1
    // Unix:    devNo=IfmOpenCom("/dev/ttyACM0"); for the first device

    // IfmOpenUSB has returned a number (devNo) which describes the device in further calls
    // to the DLL.

    // now we configure the measurement, at least with SetMeasurement
    // we want the length values of the first channel with 0.5 Hz output rate
    // IFM_MEAS_FILTER_DEFAULT will create an internal filter which removes the
    // vibration of the reference mirror from the signal
    // in some applications IFM_MEAS_FILTER_NONE may be required for unfiltered output



    error=IfmSetMeasurement(devNo,IFM_MEAS_FILTER_DEFAULT|IFM_MEAS_LENGTH|IFM_MEAS_SAMPLECOUNT,0.5);

     if(error){
        printf("Error during setting measurement mode.\n");
        IfmClose();
        return(0);
    }

    // Set the length values to zero; assuming the measurement mirror is at the reference/zero position
    error=IfmSetToZero(devNo,0x0F);

    printf("Printing length data until a key is pressed\n\n");

    // begin with the output of data
    error=IfmStart(devNo);
    if(error){
        printf("Error during start output.\n");
        IfmClose();
        return(0);
    }

    while(!kbhit()){

        // are new values available?
        if(IfmValueCount(devNo)){
            // put the value in an internal buffer for access via IfmLengthValue
            // this is necessary to access the same syncronuously sampled values (e.g. different channels) at different times
            // IfmValueCount is decremented
            IfmGetValues(devNo);
            // get the value together with environmental values
            printf("%10.0lf nm %10.0lf nm %10.0lf nm - %.2f C %.0f Pa - sample %d                  \r",
                   IfmLengthValue(devNo,0),IfmLengthValue(devNo,1),IfmLengthValue(devNo,2),
                   IfmTemperature(devNo,0),IfmAirPressure(devNo,0),IfmAuxValue(devNo,0,IFM_VALUETYPE_SAMPLECOUNT));
        }

    }

    //deinitialize

    // stop the output of data
    IfmStop(devNo);
    // close the device; devNo will be no longer valid
    IfmCloseDevice(devNo);
    // close the DLL
    IfmClose();

}

