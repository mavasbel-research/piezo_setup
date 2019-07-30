#include "ifmtestwin.h"
#include "siosifmdll.h"

QString style_red,style_green;

MWin::MWin()
:QWidget(NULL)
{
    style_red=QString("QProgressBar:horizontal { border: 1px solid gray; border-radius:4px; background: white; padding: 1px; text-align: right; margin-right: 4ex;text-align: center; }");
    style_red.append("QProgressBar::chunk:horizontal {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 red, stop: 1 white);margin-right: 2px;width: 10px; margin: 1px;border-radius:2px;}");
    style_green=QString("QProgressBar:horizontal { border: 1px solid gray; border-radius:4px; background: white; padding: 1px; text-align: right; margin-right: 4ex;text-align: center; }");
    style_green.append("QProgressBar::chunk:horizontal {background: qlineargradient(x1: 0, y1: 0.5, x2: 1, y2: 0.5, stop: 0 green, stop: 1 white);margin-right: 2px;width: 10px; margin: 1px;border-radius:2px;}");

    setupUi(this);

    // we start a timer (--> timerEvent())
    timerId=startTimer(10);
    isInit=false;
    closeButton->setEnabled(false);
    valuesSaveStopButton->setEnabled(true);
    waitForBlock=false;
    devNo=-1;
    file=NULL;
    sRateTimer.start();
    accumulatedCount=0;
    bEnvirRead=false;
    serialNumberSet=false;

#ifdef _WIN32
    lineEditCom->setVisible(false);
#else
    spinBoxCom->setVisible(false);
#endif


}

MWin::~MWin()
{
        killTimer(timerId);
	on_closeButton_clicked();
}


/*
The timerEvent function is called every 10ms (es defiened in the startTimer function in MWin::MWin

It polls for new data and displays the most recent values in the length labels

If data saving was enabled, the all data are read out and saved in an ASCII file

If block mode was enabled, it polls for the availability of a data block, read it out and store it in a file
*/


void MWin::timerEvent(QTimerEvent *event)
{
    if(isInit && devNo>=0){
        //we ask for the latest length values and display them
        //Index 0 refers to the most recent value
        if(IfmGetRecentValues(devNo,0)){
            lengthValueLabel1->setText(QString("%1").arg(IfmLengthValue(devNo,0)));
            lengthValueLabel2->setText(QString("%1").arg(IfmLengthValue(devNo,1)));
            lengthValueLabel3->setText(QString("%1").arg(IfmLengthValue(devNo,2)));
            lengthValueLabel4->setText(QString("%1").arg(IfmLengthValue(devNo,3)));
        }

        // example to get all values
        if(!waitForBlock){ // don't do it in block mode
            int i,count;
            // how much values are available
            count=IfmValueCount(devNo);
            if(count){
                for(i=0;i<count;i++){ // get the values
                    IfmGetValues(devNo);
                    // if saving has been startet (file!=NULL) save the values in to file
                    if(file)fprintf(file,"%f %f %f %f\n",
                                    IfmLengthValue(devNo,0),
                                    IfmLengthValue(devNo,1),
                                    IfmLengthValue(devNo,2),
                                    IfmLengthValue(devNo,3));
                }
            }

            // we calculate the output word rate; just für the GUI
            accumulatedCount+=count;
            if(sRateTimer.elapsed()>1000)
            {
                double msecs=sRateTimer.restart();
                wordRateLabel->setText(QString("%1").arg(1000*accumulatedCount/msecs,0,'f',1));
                accumulatedCount=0;
            }
        }

        // new environment values avalable?
        if(IfmNewEnvValuesAvailable(devNo)|| !bEnvirRead){
            tempLabel0->setText(QString("%1").arg(IfmTemperature(devNo,0),0,'f',3));
            tempLabel1->setText(QString("%1").arg(IfmTemperature(devNo,1),0,'f',3));
            tempLabel2->setText(QString("%1").arg(IfmTemperature(devNo,2),0,'f',3));
            tempLabel3->setText(QString("%1").arg(IfmTemperature(devNo,3),0,'f',3));
            // Pressure comes as Pa, but we show it as mBar (==hPa) because it's more common in daily use
            airPLabel0->setText(QString("%1").arg(IfmAirPressure(devNo,0)/100,0,'f',0));
            airPLabel1->setText(QString("%1").arg(IfmAirPressure(devNo,1)/100,0,'f',0));
            airPLabel2->setText(QString("%1").arg(IfmAirPressure(devNo,2)/100,0,'f',0));
            airPLabel3->setText(QString("%1").arg(IfmAirPressure(devNo,3)/100,0,'f',0));
            humidyLabel0->setText(QString("%1").arg(IfmHumidity(devNo,0),0,'f',0));
            humidyLabel1->setText(QString("%1").arg(IfmHumidity(devNo,1),0,'f',0));
            humidyLabel2->setText(QString("%1").arg(IfmHumidity(devNo,2),0,'f',0));
            humidyLabel3->setText(QString("%1").arg(IfmHumidity(devNo,3),0,'f',0));
            bEnvirRead=true;
        }

        // signal monitor
        if(IfmNewSignalQualityAvailable(devNo)){
            int A1=IfmSignalQuality(devNo,0,IFM_SIGNALQ_SUM);
            pbSum_1->setValue(A1);
            if ((pbSum_1->value()>242)||(pbSum_1->value()<13))
                pbSum_1->setStyleSheet(style_red);
            else pbSum_1->setStyleSheet( style_green);

            A1=IfmSignalQuality(devNo,1,IFM_SIGNALQ_SUM);
            pbSum_2->setValue(A1);//
            if ((pbSum_2->value()>242)||(pbSum_2->value()<13))
                pbSum_2->setStyleSheet(style_red);
            else pbSum_2->setStyleSheet( style_green);

            A1=IfmSignalQuality(devNo,2,IFM_SIGNALQ_SUM);
            pbSum_3->setValue(A1);//
            if ((pbSum_3->value()>242)||(pbSum_3->value()<13))
                pbSum_3->setStyleSheet(style_red);
            else pbSum_3->setStyleSheet( style_green);

            A1=IfmSignalQuality(devNo,3,IFM_SIGNALQ_SUM);
            pbSum_4->setValue(A1);//
            if ((pbSum_4->value()>242)||(pbSum_4->value()<13))
                pbSum_4->setStyleSheet(style_red);
            else pbSum_4->setStyleSheet( style_green);
        }


        // now comes the block mode
        if(waitForBlock&&IfmIsBlockAvailable(devNo)){
            waitForBlock=false;
            QString fileName=QFileDialog::getSaveFileName(this,"Save File with block data",""," Text files (*.txt);;all files (*.*)");
            if(!fileName.isEmpty()){
                file=fopen(fileName.toLocal8Bit(),"wt");
                if(!file)return;
                int i;
                for(i=0;i<blockLen;i++){
                    bool ret=IfmGetRecentValues(devNo,blockLen-i-1);
                    fprintf(file,"%f %f %f %f %d\n",
                            IfmLengthValue(devNo,0),
                            IfmLengthValue(devNo,1),
                            IfmLengthValue(devNo,2),
                            IfmLengthValue(devNo,3),
                            ret);
                }
                fclose(file);
            }
            progressBarBlock->setValue(0);
        }
        if(waitForBlock){
            progressBarBlock->setValue(IfmValueCount(devNo));
        }

        // this is a sample how more information about the connected device can be gathered
        // after opening the device, the DLL requests the configuration from it
        // it takes some milliseconds after opening until the configuration is available
        // IfmDeviceInfo(devNo,IFM_DEVINFO_AVAILABLE) returns 1 if the configuration can be read out
        if(!serialNumberSet && IfmDeviceInfo(devNo,IFM_DEVINFO_AVAILABLE)){
            QString str="Device info :";
            str.append(QString("%1 (%2)").arg(IfmDeviceInfo(devNo,IFM_DEVINFO_SERIALNUMBER),8,10,QChar('0')).arg(IfmFirmwareVersion(devNo)));

            lDeviceInfo->setText(  str);
            serialNumberSet=true;
            ChNumber= IfmChannels(devNo);
            switch(ChNumber){
            case 1: cbChannel1->setChecked(true);
                cbChannel2->setChecked(false);
                cbChannel3->setChecked(false);
                cbChannel4->setChecked(false);
                break;
            case 2: cbChannel1->setChecked(true);
                cbChannel2->setChecked(true);
                cbChannel3->setChecked(false);
                cbChannel4->setChecked(false);
                break;
            case 3: cbChannel1->setChecked(true);
                cbChannel2->setChecked(true);
                cbChannel3->setChecked(true);
                cbChannel4->setChecked(false);
                break;
            case 4: cbChannel1->setChecked(true);
                cbChannel2->setChecked(true);
                cbChannel3->setChecked(true);
                cbChannel4->setChecked(true);
                break;
            }

        }



    }
}


// Initialize the DLL with IfmInit
void MWin::on_initButton_clicked()
{
   if(!isInit)   //first call to init
    {

        if(IfmInit())
        {
            QMessageBox::warning(this, tr("SIOS Demo Application"),
                                 tr("Error during initialisation of SIOSIFM.DLL"),
                                 QMessageBox::Ok, QMessageBox::Ok);
            return;
        }
        isInit=true;

    }

   if(isInit){
        closeButton->setEnabled(true);
        initButton->setEnabled(false);
        openCOMButton->setEnabled(true);
        searchUSBDevicesButton->setEnabled(true);
        openUSBButton->setEnabled(true);
    }
}


// open a device with a known COM-number
void MWin::on_openCOMButton_clicked()
{

    if(isInit){ //Open the device
#ifdef _WIN32
        int error=IfmOpenCOM(spinBoxCom->value());
        if(error<0){
            QMessageBox::warning(this, tr("SIOS Demo Application"),
                                 tr("The COM %1 could not be opened. (Error %2)").arg(spinBoxCom->value()).arg(error),
                                 QMessageBox::Ok);
            return;
        }
#else
        int error=IfmOpenCOM(lineEditCom->text().toLocal8Bit().constData());
        if(error<0){
            QMessageBox::warning(this, tr("SIOS Demo Application"),
                                 tr("The device %1 could not be opened. (Error %2)").arg(lineEditCom->text()).arg(error),
                                 QMessageBox::Ok);
            return;
        }
#endif
        // if IfmOpenCom has returned positive number (or zero) this number that identifies the device in further calls to the API
        devNo=error;
        serialNumberSet=false;  //read out serial number in the timerEvent function
    }

    // if success we enable some buttons
    if(isInit){
        setMeasurementButton->setEnabled(true);
        openCOMButton->setEnabled(false);
        openUSBButton->setEnabled(false);
        closeDeviceButton->setEnabled(true);
   }

}


// open a device, that has been searched with IfmSearchUSBDevices
void MWin::on_openUSBButton_clicked()
{

    if(isInit){ //Open the device
        int error=IfmOpenUSB(comboBoxUSBDev->currentIndex());
        if(error<0){ // if error was less than zero, it was indeed an error number
            QMessageBox::warning(this, tr("SIOS Demo Application"),
                                 tr("The device %1 (index %2) could not be opened. (Error %3)").arg(comboBoxUSBDev->currentText()).arg(comboBoxUSBDev->currentIndex()).arg(error),
                                 QMessageBox::Ok);
            return;
        }
        // if IfmOpenUSB has returned positive number (or zero) this number that identifies the device in further calls to the API
        devNo=error;
        serialNumberSet=false;  //read out serial number in the timerEvent function

    }

    // if success we enable some buttons
    if(isInit){
        setMeasurementButton->setEnabled(true);
        openCOMButton->setEnabled(false);
        openUSBButton->setEnabled(false);
        closeDeviceButton->setEnabled(true);
   }

}


// close a device what is no longer need
void MWin::on_closeDeviceButton_clicked()
{
   if(devNo>=0)IfmStop(devNo);      //Stop measurement
   if(devNo>=0)IfmCloseDevice(devNo);
   devNo=-1;
   setMeasurementButton->setEnabled(false);
   openCOMButton->setEnabled(true);
   openUSBButton->setEnabled(true);
   closeDeviceButton->setEnabled(false);
}


// close the DLL; counterpart to IfmInit
void MWin::on_closeButton_clicked()
{
   if(!isInit)return;
   IfmClose();
   isInit=false;
   initButton->setEnabled(true);
   closeButton->setEnabled(false);
   openCOMButton->setEnabled(false);
   openUSBButton->setEnabled(false);
   closeDeviceButton->setEnabled(false);
   searchUSBDevicesButton->setEnabled(false);

}


// do a search on the USB-Bus for RE-10 devices
// the serial numbers of all devices, we found, are added to a combo box
void MWin::on_searchUSBDevicesButton_clicked()
{
    comboBoxUSBDev->clear();
    if(!isInit)return;
    int count=IfmSearchUSBDevices();
    if(count>0){
        int i;
        for(i=0;i<count;i++){
            comboBoxUSBDev->addItem(QString("%1").arg(IfmUSBDeviceSerial(i)),i);
        }
    }

}

// begin with data transmission from the device
// the default settings from the RE-10 or the settings made with SetMeasurement are used
void MWin::on_valuesStartButton_clicked()
{
	if(!isInit || devNo<0) return;
	IfmStart(devNo);
}

// stop the transmission of lenght values
// has no influence to the transmission of envorinmental data
void MWin::on_valuesStopButton_clicked()
{
	if(!isInit || devNo<0) return;
	IfmStop(devNo);
}

// for testing purposes all incoming length values can be saved in a file
// the saving is done in the timerEvent function
void MWin::on_valuesSaveStartButton_clicked()
{
	if(!isInit || devNo<0) return;
	if(file)fclose(file);
	file=NULL;
	QString fileName=QFileDialog::getSaveFileName(this,"Save File",""," Text files (*.txt);;all files (*.*)");
	if(!fileName.isEmpty()){
		IfmClearBuffers(devNo);
		file=fopen(fileName.toLocal8Bit(),"wt");
		valuesSaveStartButton->setEnabled(false);
		valuesSaveStopButton->setEnabled(true);
	}

}

// stop the saving and close the file
void MWin::on_valuesSaveStopButton_clicked()
{
	if(file)fclose(file);
	file=NULL;
	valuesSaveStartButton->setEnabled(true);
	valuesSaveStopButton->setEnabled(false);

}

// set all channels to zero and set the death path
void MWin::on_setToZeroButton_clicked()
{
    if(devNo<0)return;
    int error1,error2,error3, error4, error5;

    error1 = IfmSetDeadPath(devNo, 0, spinBoxDeadPath0->value());
    error2 = IfmSetDeadPath(devNo, 1, spinBoxDeadPath1->value());
    error3 = IfmSetDeadPath(devNo, 2, spinBoxDeadPath2->value());
    error4 = IfmSetDeadPath(devNo, 3, spinBoxDeadPath3->value());
    error5 = IfmSetToZero(devNo,  0x0F); // all 4 channels
    if(error1||error2||error3||error4||error5){
        QMessageBox::warning(this, tr("SIOS Demo Application"),
                             tr("SetToZero returns an error %5 (Error %1 %2 %3 %4)").arg(error1).arg(error2).arg(error3).arg(error4).arg(error5),
                             QMessageBox::Ok, QMessageBox::Ok);
    }
}

// set the measurement settings/conditions like sample rate respective output word rate
// triggers and filters

void MWin::on_setMeasurementButton_clicked()
{
	if(devNo<0)return;

        if (gbTrigger->isChecked()) setTrigger(); // Set hardware trigger, if wished
        else
        {           
            int error=IfmSetTrigger(devNo, IFM_TRIGGER_OFF); //Stop trigger mode
             if(error)
                QMessageBox::warning(this, tr("SIOS Demo Application"),
                tr("SetTriggerMode returns an error (Error %1)").arg(error),
                QMessageBox::Ok);

        }
        setEnabled(true);
        // first, set the channels that should be transmitted
        int measurementFlags=0;

        if (cbChannel1->isChecked()==true)
        {
            measurementFlags|=0x0100;
        }
        if (cbChannel2->isChecked()==true)
        {
            measurementFlags|=0x0200;
        }
        if (cbChannel3->isChecked()==true)
        {
            measurementFlags|=0x0400;
        }
        if (cbChannel4->isChecked()==true)
        {
            measurementFlags|=0x0800;
        }

        // we want the length values
        measurementFlags|=IFM_MEAS_LENGTH;

        // settings for the filtering
        setFilter();
        if(radioButtonFilterOff->isChecked())measurementFlags|=IFM_MEAS_FILTER_OFF;
        if(radioButtonFilterDefault->isChecked())measurementFlags|=IFM_MEAS_FILTER_DEFAULT;
        if(radioButtonFilterUser->isChecked())measurementFlags|=IFM_MEAS_FILTER_USER;

        int error=0;

         error=IfmSetMeasurement(devNo,measurementFlags,spinBoxWordRate->value());
	if(error){
		QMessageBox::warning(this, tr("SIOS Demo Application"),
               tr("SetMeasurement returns an error (Error %1)").arg(error),
               QMessageBox::Ok, QMessageBox::Ok);
	}
}



void MWin::setEnabled (bool flag)
{
        valuesStartButton->setEnabled(flag);
        valuesStopButton->setEnabled(flag);
}



// sets the trigger settings;
//usually called before IfmSetMeasurement (we call it in on_setMeasurementButton_clicked())

void MWin::setTrigger()
{
  if(devNo<0)return;

   if (gbTrigger->isChecked())
        {

          unsigned int triggerMode=IFM_TRIGGER_OFF;
          if(rbClockExternal->isChecked())
            {
                triggerMode|=IFM_TRIGGER_CLOCK;
               if(rbClockRising->isChecked())triggerMode|=IFM_TRIGGER_CLOCK_RISING_EDGE;
            }

            if(rbStartStopProcessed->isChecked())
            {
                triggerMode|=IFM_TRIGGER_STARTSTOP_PROC;
                if(rbTriggerRising->isChecked())triggerMode|=IFM_TRIGGER_STARTSTOP_RISING_EDGE	;
            }

            if(rbStartStopTrigger->isChecked())
            {
                triggerMode|=IFM_TRIGGER_STARTSTOP ;
                if(rbTriggerRising->isChecked())triggerMode|=IFM_TRIGGER_STARTSTOP_RISING_EDGE	;
            }


            if(rbStartTrigger->isChecked())
            {
                triggerMode|=IFM_TRIGGER_START;
                if(rbTriggerRising->isChecked())triggerMode|=IFM_TRIGGER_STARTSTOP_RISING_EDGE	;
            }



            if(rbEventSingle->isChecked())
            {
                triggerMode|=IFM_TRIGGER_EVENT;
                if(rbEventRising->isChecked())triggerMode|=IFM_TRIGGER_EVENT_RISING_EDGE;
            }


            int error=IfmSetTrigger(devNo,triggerMode);
            if(error){
                QMessageBox::warning(this, tr("SIOS Demo Application"),
               tr("SetTriggerMode returns an error (Error %1)").arg(error),
               QMessageBox::Ok);
            }
        }
}


// get the current settings for the filter from the DLL
// the DLL automatically requensts the settings from a device after opening
// so in the DLL the settings are always in line with the settings in the device
void MWin::on_getFilterButton_clicked()
{
    int flags=IfmDeviceInfo(devNo,IFM_DEVINFO_FILTERFLAGS);
    if (flags & IFM_FILTER_STAGE1) gbFiltreStage1->setChecked(true);
    else gbFiltreStage1->setChecked(false);
    if (flags & IFM_FILTER_STAGE2) gbFiltreStage2->setChecked(true);
    else gbFiltreStage2->setChecked(false);
    if (flags & IFM_FILTER_AVG5) checkBoxFilterAVG5->setChecked(true);
    else checkBoxFilterAVG5->setChecked(false);
    if (flags & IFM_FILTER_AVG6) checkBoxFilterAVG6->setChecked(true);
    else checkBoxFilterAVG6->setChecked(false);
    if (flags & IFM_FILTER_AVG9) checkBoxFilterAVG9->setChecked(true);
    else checkBoxFilterAVG9->setChecked(false);
    spinBoxAVG1->setValue(IfmDeviceInfo(devNo, IFM_DEVINFO_AVG1));
    spinBoxAVG2->setValue(IfmDeviceInfo(devNo, IFM_DEVINFO_AVG2));
    doubleSpinBoxFilter0->setValue(IfmGetFilterCoeff(devNo, 0));
    doubleSpinBoxFilter1->setValue(IfmGetFilterCoeff(devNo, 1));
    doubleSpinBoxFilter2->setValue(IfmGetFilterCoeff(devNo, 2));
    doubleSpinBoxFilter3->setValue(IfmGetFilterCoeff(devNo, 3));
    doubleSpinBoxNotch->setValue(IfmGetFilterNotchFrequency(devNo,0));
}


// sets the settings for user specific filter
//usually called before IfmSetMeasurement (we call it in on_setMeasurementButton_clicked())
void MWin::setFilter()
{
    if(devNo<0)return;
    unsigned int filterFlags=0;

    //if(spinBoxAVG1->value()>0)              filterFlags |= FILTER_STAGE1;
    if(radioButtonFilterUser->isChecked())
    {
        if(gbFiltreStage1->isChecked())
        {
            filterFlags |= IFM_FILTER_STAGE1;

            if(rbFilterManuel->isChecked()){
                IfmSetFilterCoeff(devNo,0,doubleSpinBoxFilter0->value());
                IfmSetFilterCoeff(devNo,1,doubleSpinBoxFilter1->value());
                IfmSetFilterCoeff(devNo,2,doubleSpinBoxFilter2->value());
                IfmSetFilterCoeff(devNo,3,doubleSpinBoxFilter3->value());
            }else if(rbFilterAutomatic->isChecked()){
                IfmSetFilterCoeff(devNo,0,0.0);
                IfmSetFilterCoeff(devNo,1,0.0);
                IfmSetFilterCoeff(devNo,2,0.0);
                IfmSetFilterCoeff(devNo,3,0.0);
            }else{
                IfmSetFilterNotchFrequency(devNo,0,doubleSpinBoxNotch->value());
                IfmSetFilterNotchFrequency(devNo,1,doubleSpinBoxNotch->value());
                IfmSetFilterNotchFrequency(devNo,2,doubleSpinBoxNotch->value());
                IfmSetFilterNotchFrequency(devNo,3,doubleSpinBoxNotch->value());
            }

        }

        if(gbFiltreStage2->isChecked())     filterFlags |= IFM_FILTER_STAGE2;
        if(checkBoxFilterAVG5->isChecked())	filterFlags |= IFM_FILTER_AVG5;
        if(checkBoxFilterAVG6->isChecked())	filterFlags |= IFM_FILTER_AVG6;
        if(checkBoxFilterAVG9->isChecked())	filterFlags |= IFM_FILTER_AVG9;

        int error=IfmSetFilter(devNo,filterFlags,spinBoxAVG1->value(),spinBoxAVG2->value());


        if(error){
            QMessageBox::warning(this, tr("SIOS Demo Application"),
                                 tr("SetMeasurement returns an error (Error %1)").arg(error),
                                 QMessageBox::Ok);
        }
    }
}


// switch on all piezo vibrators of the reference mirror(s)
void MWin::on_refMirrorVibratorONButton_clicked()
{
    if(devNo<0)return;
    int error1,error2,error3,error4;
    error1=IfmSetRefMirrorVibration(devNo,0,true);
    error2=IfmSetRefMirrorVibration(devNo,1,true);
    error3=IfmSetRefMirrorVibration(devNo,2,true);
    error4=IfmSetRefMirrorVibration(devNo,3,true);
    if(error1||error2||error3||error4){
        QMessageBox::warning(this, tr("SIOS Demo Application"),
                             tr("SetRefMirrorVibration returns an error (Error %1 %2 %3 %4)").arg(error1).arg(error2).arg(error3).arg(error4),
                             QMessageBox::Ok, QMessageBox::Ok);
    }

}

// switch them off
void MWin::on_refMirrorVibratorOFFButton_clicked()
{
    if(devNo<0)return;
    int error1,error2,error3,error4;
    error1=IfmSetRefMirrorVibration(devNo,0,false);
    error2=IfmSetRefMirrorVibration(devNo,1,false);
    error3=IfmSetRefMirrorVibration(devNo,2,false);
    error4=IfmSetRefMirrorVibration(devNo,3,false);
    if(error1||error2||error3||error4){
        QMessageBox::warning(this, tr("SIOS Demo Application"),
                             tr("SetRefMirrorVibration returns an error (Error %1 %2 %3 %4)").arg(error1).arg(error2).arg(error3).arg(error4),
                             QMessageBox::Ok, QMessageBox::Ok);
    }

}


// ******************* Handling the environment values ********************

void MWin::on_getSensorsButton_clicked()
{
	if(devNo<0)return;
    int i;
    environmentTextEdit->setText("");
    for(i=0;i<IfmEnvSensorCount(devNo);i++){
        int sensorType=IfmSensorProperty(devNo,i);
        double sensorValue=IfmSensorValue(devNo,i);
        QString typeString;
        if(sensorType&IFM_ENVIR_SENSOR_TEMP)typeString="Temperature";
        else if(sensorType&IFM_ENVIR_SENSOR_AIRPRESSURE)typeString="Air pressure";
        else if(sensorType&IFM_ENVIR_SENSOR_HUMIDITY)typeString="Humidity";
        if(sensorType&IFM_ENVIR_EDLEN)typeString+=" (WL)";
        environmentTextEdit->append(QString("%1 %2 (%3) = %4").arg(i).arg(typeString).arg(sensorType,2,16,QChar('0')).arg(sensorValue));
    }
}

