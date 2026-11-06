import argparse
import os, sys
import serial
from functools import partial

from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic

def send(cmd):
    if debug:
        print(cmd[:-1])
    else:
        dev.write(cmd.encode())
        ans = dev.readline()
    return

def resetcb():
    cmd = 'RS\n'
    send(cmd)
    
    mainwin.per1sb.blockSignals(True)
    mainwin.dt1sb.blockSignals(True)
    mainwin.per2sb.blockSignals(True)
    mainwin.dt2sb.blockSignals(True)

    mainwin.per1sb.setValue(10.)
    mainwin.dt1sb.setValue(50.)
    mainwin.per2sb.setValue(10.)
    mainwin.dt2sb.setValue(50.)

    mainwin.per1sb.blockSignals(False)
    mainwin.dt1sb.blockSignals(False)
    mainwin.per2sb.blockSignals(False)
    mainwin.dt2sb.blockSignals(False)


def synccb():
    cmd = 'SY\n'
    send(cmd)

def quitcb():
    if not debug:
        dev.close()
    mainwin.destroy()
    app.quit()
    return

def percb(ch, val):
    cmd = f"P{ch}{val:.1f}\n"
    send(cmd)
    dtcy = mainwin.dt1sb.value() if ch == "1" else mainwin.dt2sb.value()
    up = dtcy * val / 100.
    cmd = f"U{ch}{up:.1f}\n" 
    send(cmd)
    return

def dtcycb(ch, val):
    cmd = f"U{ch}"
    per = mainwin.per1sb.value() if ch == "1" else mainwin.per2sb.value()
    up = per * (1 - 0.01 * val)
    cmd += f"{up:.3f}"
    send(cmd)
    return

def invcb(ch, val):
    s = "1" if val else "0"
    cmd = f"I{ch}{s}\n" 
    send(cmd)
    return 

def oncb(ch, val):
    cmd = f"R{ch}\n" if val else f"S{ch}\n"
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

    ui_file = "./pulsegen.ui"
    mainwin = uic.loadUi(ui_file)
    mainwin.show()

    mainwin.resetbt.clicked.connect(resetcb)
    mainwin.syncbt.clicked.connect(synccb)
    mainwin.quitbt.clicked.connect(quitcb)
    mainwin.per1sb.valueChanged.connect(partial(percb, "1"))
    mainwin.per2sb.valueChanged.connect(partial(percb, "2"))
    mainwin.dt1sb.valueChanged.connect(partial(dtcycb, "1"))
    mainwin.dt2sb.valueChanged.connect(partial(dtcycb, "2"))
    mainwin.inv1cb.stateChanged.connect(partial(invcb, "1"))
    mainwin.inv2cb.stateChanged.connect(partial(invcb, "2"))
    mainwin.on1cb.stateChanged.connect(partial(oncb, "1"))
    mainwin.on2cb.stateChanged.connect(partial(oncb, "2"))
    
    if not debug:
        try:
            dev = serial.Serial(fname)
        except serial.serialutil.SerialException:
            exit(f"Could not open {fname}")
        resetcb()
    
    app.exec()
    
if __name__ == "__main__":
    main()
