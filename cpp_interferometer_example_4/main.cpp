#include <stdio.h>
#ifdef _WIN32
#include <conio.h>
#include <windows.h>
#else
#include <time.h>
#include <termios.h>
#include <string.h>
#endif
#include <siosifmdll.h>

/*
 This is a sample application which shows the usage of the siosifm.dll
 for reading out data of (optional) lateral position sensors, also called PSD sensors


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
    // we want the length values of the first channel with 1 Hz output rate
    // IFM_MEAS_FILTER_DEFAULT will create an internal filter which removes the
    // vibration of the reference mirror from the signal
    // in some applications IFM_MEAS_FILTER_NONE may be required for unfiltered output


    // The data of the position sensors must not be requested. The presence of the PSD sensors
    // and the data rate is set in the internal device configuration of the RE-10 card

    error=IfmSetMeasurement(devNo,IFM_MEAS_LENGTH|IFM_MEAS_FILTER_DEFAULT,1);
    if(error>0){
        printf("Error during opening the device.\n");
        IfmClose();
        return(0);
    }


    // ask for the configuration of the for the PSDs
    // after opening the device the device configuration is transmitted
    // this may take some time
    // thats why before requesting things from the configuration, wait until it's available

    unsigned int ms=GetTickCount();
    while(!IfmDeviceInfo(devNo,IFM_DEVINFO_AVAILABLE))
        if((ms+3000)<GetTickCount()){
        printf("Device configuration could not be retrieved!\n");
        return 0;
    }

    int psdType,psdCount;

    // first we look for the count of PSD sensors
    psdCount=IfmDeviceInfo(devNo,IFM_DEVINFO_PSD_COUNT);
    printf("There are %d PSD sensors available\n",psdCount);

    // optionally we look for the type of the PSD-sensors, so we know the properties
    psdType=IfmDeviceInfo(devNo,IFM_DEVINFO_PSD_TYPE);
    const char *psdTypeString="unknown PSD type";
    if(psdType==IFM_PSDTYPE_NONE)psdTypeString="no PSD sensor";
    else if(psdType==IFM_PSDTYPE_CARD)psdTypeString="PSD-04 card";
    else if(psdType==IFM_PSDTYPE_ADU)psdTypeString="ADU card";

    printf("The PSD sensors have type %d (%s)\n",psdType,psdTypeString);

    if(!psdCount || !psdType){
        printf("There is no PSD (lateral sensor) available.\nExiting\n");
        return 0;
    }


    // Set the length values to zero; assuming the measurement mirror is at the reference/zero position
    error=IfmSetToZero(devNo,0x0F);

    printf("Printing length and PSD data until a key is pressed\n\n");

    // begin with the output of data
    error=IfmStart(devNo);
    if(error>0){
        printf("Error during start output.\n");
        IfmClose();
        return(0);
    }
    printf("channel length/mm   x/microns  y/microns\n");

    while(!kbhit()){

        // are new values available?
        if(IfmValueCount(devNo)){
            // put the value in an internal buffer for access via IfmLengthValue
            // this is necessary to access the same syncronuously sampled values (e.g. different channels) at different times
            // IfmValueCount is decremented
            IfmGetValues(devNo);
            // The PSD values come inline with the length values even if they are not sampled toghether
            // in case of PSD-04 cards the PSD values are sent to the PC one or max. 4 times in a second and
            // the values are related to the length values and stored in the internal buffer

            int i;
/*
#ifdef _WIN32
            clrscr();
#else
            system("clear");
#endif
*/          printf("channel length/mm   x/microns  y/microns\n");
            for(i=0;i<psdCount;i++){
                printf("%d       %10.6f %10.2f %10.2f\n",i,IfmLengthValue(devNo,i)/1000000,
                       double(IfmAuxValue(devNo,i,IFM_VALUETYPE_PSD_X))/100.0,
                       double(IfmAuxValue(devNo,i,IFM_VALUETYPE_PSD_Y))/100.0);
            }
            printf("\n");
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

