;QT += network
DEFINES -= UNICODE
HEADERS = ifmtestwin.h \
    ../common/siosifmdll.h \
    ../common/siosifmdef.h
SOURCES = main.cpp \
    ifmtestwin.cpp \
    ifmblockmode.cpp
FORMS = win.ui
;RESOURCES = application.qrc
INCLUDEPATH += ..;../common
win32::LIBS += -L "." -lsiosifm
unix::LIBS += -L "." -lsiosifm -lrt
TARGET = ifmtest2
