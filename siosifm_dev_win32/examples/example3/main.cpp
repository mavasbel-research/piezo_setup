#include <stdio.h>
#ifdef _WIN32
#include <conio.h>
#include <windows.h>
#else
#include <termios.h>
#include <string.h>
#endif
#include "siosifmdll.h"


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

// the GetTickCount() unter Windows is very handy,
// we emulate it unter Linux as well
long GetTickCount()
{
    struct timespec tp ;
    clock_gettime(CLOCK_MONOTONIC,&tp);
    return tp.tv_sec+tp.tv_nsec/1000000;
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

    if(cnt<=0){
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
    if(devNo>0){
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

    // changed: 3 channels + samplecounter

    error=IfmSetMeasurement(devNo,IFM_MEAS_THREECHANNEL|IFM_MEAS_LENGTH|IFM_MEAS_FILTER_DEFAULT,0.5);
    if(error>0){
        printf("Error during opening the device.\n");
        IfmClose();
        return(0);
    }


    // ask for the configuration of the angle calculation
    // after opening the device the device configuration is transmitted
    // this may take some time
    // thats why before requesting things from the configuration, wait until it's available

    unsigned int ms=GetTickCount();
    while(!IfmDeviceInfo(devNo,IFM_DEVINFO_AVAILABLE))
        if((ms+2000)<GetTickCount()){
        printf("Device configuration could not be retrieved!\n");
        return 0;
    }

    int k1=-1,k2=-1,k,j;
    double distance;

    // the first pair of channels in the configuration
    k=IfmDeviceInfo(devNo,IFM_DEVINFO_LINKEDCHANNELS1);
    float *f=(float*)IfmDeviceInfo(devNo,IFM_DEVINFO_BASEDISTANCE1_POINTER);
    distance=0;
    // be carefull, older DLL versions don't know the parameter and would return 0
    if(f)distance=*f;

    // check, which channels are in thr channel mask for this pair
    for(j=0;j<4;j++){
        if(k&(1<<j))k1==-1?k1=j:k2=j;
    }

    printf("\nChannel connection 1: %d - %d\nbase distance %f\n\n",k1+1,k2+1,distance);

    // the same for channel 2
    k=IfmDeviceInfo(devNo,IFM_DEVINFO_LINKEDCHANNELS2);
    f=(float*)IfmDeviceInfo(devNo,IFM_DEVINFO_BASEDISTANCE2_POINTER);
    distance=0;
    if(f)distance=*f;
    k1=-1;k2=-1;
    for(j=0;j<4;j++){
        if(k&(1<<j))k1==-1?k1=j:k2=j;
    }
    printf("Channel connection 2: %d - %d\nbase distance %f\n\n",k1+1,k2+1,distance);

    // normally between the channels 2 and 1 the yaw angle is calculated
    if(IfmAngleAvailable(devNo,IFM_CHANNEL1|IFM_CHANNEL2))printf("Angle calculation between channels 2 and 1 is possible.\n");
    else printf("Angle calculation between channels 2 and 1 is NOT possible.\n");

    // normally between the channels 2 and 3 the pitch angle is calculated
    if(IfmAngleAvailable(devNo,IFM_CHANNEL3|IFM_CHANNEL2))printf("Angle calculation between channels 2 and 3 is possible.\n");
    else printf("Angle calculation between channels 2 and 3 is NOT possible.\n");


    // Set the length values to zero; assuming the measurement mirror is at the reference/zero position
    error=IfmSetToZero(devNo,0x0F);

    printf("Printing length data until a key is pressed\n\n");

    // begin with the output of data
    error=IfmStart(devNo);
    if(error>0){
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
            // get the values together with the angles
            printf("%8.0lf µm %8.0lf nm %8.0lf nm - yaw (2-1) %.3f pitch (2-3) %.3f      \r",
                   IfmLengthValue(devNo,0)/1000,IfmLengthValue(devNo,1)/1000,IfmLengthValue(devNo,2)/1000,
                   IfmAngleValue(devNo,IFM_CHANNEL2,IFM_CHANNEL1,1),IfmAngleValue(devNo,IFM_CHANNEL2,IFM_CHANNEL3,1));
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

