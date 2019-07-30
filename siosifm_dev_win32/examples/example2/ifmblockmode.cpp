#include "ifmtestwin.h"
#include "siosifmdll.h"


// sets the DLL into block mode; continuous data transfer stops
// similar to on_SetMeasurementButton_clicked()
void MWin::on_setBlockModeButton_clicked()
{
    if(devNo<0)return;

    // we want to get all four channels with interferometer values
    //int measurementFlags=IFM_MEAS_ONECHANNEL|IFM_MEAS_LENGTH|IFM_MEAS_SINCOS;

    int measurementFlags=0;

    if (cbChannel1->isChecked()==true)measurementFlags|=0x0100;
    if (cbChannel2->isChecked()==true)measurementFlags|=0x0200;
    if (cbChannel3->isChecked()==true)measurementFlags|=0x0400;
    if (cbChannel4->isChecked()==true)measurementFlags|=0x0800;

    // request the length values
    measurementFlags|=IFM_MEAS_LENGTH;

    // settings for the filtering
    if(radioButtonFilterOffBM->isChecked())measurementFlags|=IFM_MEAS_FILTER_OFF;
    if(radioButtonFilterDefaultBM->isChecked())measurementFlags|=IFM_MEAS_FILTER_DEFAULT;
    if(radioButtonFilterUserBM->isChecked())measurementFlags|=IFM_MEAS_FILTER_USER;
    // with user settings the filter mst be set manually, see on_setFilterButton_clicked()


    int triggerMode=IFM_TRIGGER_OFF;
      if (gbTriggerBM->isChecked())
        {

          if(rbClockExternalBM->isChecked())
            {
                triggerMode|=IFM_TRIGGER_CLOCK;
                //if(rbFalling->isChecked())triggerMode|=IFM_TRIGGER_CLOCK_RISING_EDGE;
                // ???
            }

            if(rbSingle2BM->isChecked())
            {
                triggerMode|=IFM_TRIGGER_EVENT;
                if(rbRisingBM->isChecked())triggerMode|=IFM_TRIGGER_EVENT_RISING_EDGE	;
            }

            if(rbStartTrigger2BM->isChecked())
            {
                triggerMode|=IFM_TRIGGER_START;
                if(rbRisingBM->isChecked())triggerMode|=IFM_TRIGGER_STARTSTOP_RISING_EDGE;
            }
        }



    int error=IfmSetBlockMode(devNo,measurementFlags,triggerMode,spinBoxWordRateBM->value());
    if(error){
        QMessageBox::warning(this, tr("SIOS Demo Application"),
               tr("SetMeasurement returns an error (Error %1)").arg(error),
               QMessageBox::Ok, QMessageBox::Ok);
    }

}


// request a block; the settings for the measurement have been done in on_startBlockModeButton_clicked()
// with IfmSetBlockMode, what has to be called before IfmStartBlock
// the data block is received in timerEvent
void MWin::on_startBlockButton_clicked()
{
    if(devNo<0)return;

    blockLen=spinBoxBlockLength->value();
    int error=IfmStartBlock(devNo,blockLen);
    if(error){
        QMessageBox::warning(this, tr("SIOS Demo Application"),
               tr("SetMeasurement returns an error (Error %1)").arg(error),
               QMessageBox::Ok, QMessageBox::Ok);
    }else{
        progressBarBlock->setMaximum(spinBoxBlockLength->value());
        waitForBlock=true;
    }


}


