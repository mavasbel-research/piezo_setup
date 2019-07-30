#ifndef CTRLWINDOW_H_
#define CTRLWINDOW_H_
#include <QtGui>
#ifdef _WIN32
#include <windows.h>
#endif
#include "ui_win.h"
#include <siosifmdef.h>

#define FILTER_STAGE1            0x01
#define FILTER_STAGE2            0x02
#define FILTER_STAGE3            0x04


class MWin:public QWidget,public Ui_MForm{
	Q_OBJECT
	protected:
	//void timerEvent ( QTimerEvent * event );
         int lastRequest,accumulatedCount,blockLen;
         bool isInit,waitForBlock,bEnvirRead,serialNumberSet;
        int timerId,devNo;
        FILE *file;
        void timerEvent(QTimerEvent *event);
        QTime sRateTimer;
	public:
	MWin();
	virtual ~MWin();
   public slots:
	void on_initButton_clicked();
	void on_closeButton_clicked();
    void on_closeDeviceButton_clicked();
    void on_openCOMButton_clicked();
    void on_openUSBButton_clicked();
    void on_searchUSBDevicesButton_clicked();

        //void on_setTriggerButton_clicked();
	void on_setToZeroButton_clicked();
    void on_refMirrorVibratorONButton_clicked();
    void on_refMirrorVibratorOFFButton_clicked();
	void on_valuesStartButton_clicked();
	void on_valuesSaveStartButton_clicked();
	void on_valuesStopButton_clicked();
	void on_valuesSaveStopButton_clicked();
	void on_getSensorsButton_clicked();
	void on_setMeasurementButton_clicked();
    //Blockmode
    void on_setBlockModeButton_clicked();
    void on_startBlockButton_clicked();
    void on_getFilterButton_clicked();


    private:
        int ChNumber;
        void setTrigger();
        void setEnabled (bool flag);
        void EventBoxSetEnabled();
        void TriggerBoxSetEnabled();
        void setFilter();
        void setMeasurementOptions(bool RowData);

};



#endif /*CTRLWINDOW_H_*/
