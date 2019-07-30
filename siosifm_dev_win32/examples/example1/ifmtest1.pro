#-------------------------------------------------
#
# Project created by QtCreator 2009-10-19T09:42:42
#
#-------------------------------------------------

QT       -= core gui

TARGET = ifmtest1
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app

INCLUDEPATH += ..;../common
SOURCES += main.cpp
win32::LIBS += -L "." -lsiosifm
unix::LIBS += -L "." -lsiosifm -lrt
