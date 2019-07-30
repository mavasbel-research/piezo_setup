/*
Example: Graphical User Interface to SIOS Interfermeter with siosifm.dll

This file creates the main window of the example.
All siosifm.dll specific code is in ifmtestwin.cpp and ifmblockmode.cpp

*/


#include <QApplication>
#include <QSettings>

#include "siosifmdll.h"
#include "ifmtestwin.h"

int main(int argc, char *argv[])
{
    //  Q_INIT_RESOURCE(application);

    QApplication app(argc, argv);

    // if we want to get some files with debug information
    // we uncomment the following two lines
    // IfmSetOption(IFM_OPTION_DEBUGFILES,true);

    MWin *mainWin=new MWin;
    mainWin->show();
    int ret=app.exec();
    delete mainWin;
    mainWin=NULL;
    // if we have called DebugInit, call also DebugClose
    return ret;
}
