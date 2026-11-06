import argparse
import os, sys
import serial
from functools import partial

from PyQt6 import QtCore, QtGui, QtWidgets, uic

_wnames = ('a0sb', 'a1sb', 'a2sb', 'b1sb', 'b2sb', 'c1sb', 'c2sb')

def send(cmd):
    if debug:
        print(cmd[:-1])
    else:
        dev.write(cmd.encode())
        ans = dev.readline()
    return

def quitcb():
    if not debug:
        dev.close()
    mainwin.destroy()
    app.quit()
    return

def coeffcb(pref):
    w = mainwin.findChild(QtWidgets.QDoubleSpinBox, (pref + "sb").lower())    
    cmd = f"{pref}{w.value()}\n"
    running = mainwin.findChild(QtWidgets.QCheckBox, "oncb").isChecked()    
    if running:
        send("ST\n")
    send(cmd)
    if running:
        send("RU\n")
    return

def presetcb(val):
    send("ST\n")
    cmd = f"P{val + 1}\n"
    send(cmd)
    send("RU\n")
    update(val)

def editcb(val):
    for i in range(7):
        widget = mainwin.findChild(QtWidgets.QDoubleSpinBox, _wnames[i])
        widget.setEnabled(val)

def update(val):
    _eps = 0.01
    _gsat = 10
    _osceps = 0.00394784
    _notchA = 0.95
    _notchCos = 0.99802673
    _presets = [(1, 0, 0, 0, 0, 0, 0),
                (_eps/2, _eps/2, 0, 1 - _eps, 0, 0, 0),
                (_eps/2, _eps/2, 0, 1 - _eps/_gsat, 0, 0, 0),
                (_gsat, -_gsat, 0, 1 - _eps * _gsat, 0, 0, 0),
                (-1 + 2 * _eps, 1, 0, 1 - 2 * _eps, 0, 0, 0),
                (1, - 2 * _notchCos , 1, 2 * _notchCos * _notchA, - _notchA * _notchA, 0, 0),
                (4 * _eps * (1 - 5 * _eps), 8 * _eps * _eps, -4 * _eps * (1 - 7 * _eps), 2 - _eps * (12 - 68 * _eps), -1 + (12 - 72 * _eps) * _eps, 0, 0),
                (0, 0, 0, 2 - _osceps, -1, 2000, 2000 - _osceps / 2)
                ]
    
    for i in range(7):
        widget = mainwin.findChild(QtWidgets.QDoubleSpinBox, _wnames[i])
        widget.setValue(_presets[val][i])
    
def oncb(val):
    cmd = "RU\n" if val else "ST\n"
    send(cmd)
    return 

def main():
    global app, mainwin, dev, debug

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-p', '--port', help='port name (default /dev/ttyACM0)')
    args = parser.parse_args()
    debug = args.debug is True
    if args.port:
        fname = args.port
    else:
        fname = '/dev/ttyACM0'

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    ui_file = "./biquad.ui"
    mainwin = uic.loadUi(ui_file)
    mainwin.show()

    mainwin.quitbt.clicked.connect(quitcb)
    mainwin.a0sb.editingFinished.connect(partial(coeffcb, "A0"))
    mainwin.a1sb.editingFinished.connect(partial(coeffcb, "A1"))
    mainwin.a2sb.editingFinished.connect(partial(coeffcb, "A2"))
    mainwin.b1sb.editingFinished.connect(partial(coeffcb, "B1"))
    mainwin.b2sb.editingFinished.connect(partial(coeffcb, "B2"))
    mainwin.c1sb.editingFinished.connect(partial(coeffcb, "C1"))
    mainwin.c2sb.editingFinished.connect(partial(coeffcb, "C2"))
    mainwin.oncb.stateChanged.connect(oncb)
    mainwin.editcb.stateChanged.connect(editcb)
    mainwin.presetcb.activated.connect(presetcb)
    mainwin.presetcb.setFocus()
        
    update(0)
    
    if not debug:
        try:
            dev = serial.Serial(fname)
        except serial.serialutil.SerialException:
            exit(f"Could not open {fname}")
        resetcb()
    
    app.exec()
    
if __name__ == "__main__":
    main()
