import argparse
import sys, time
import serial
import numpy as np

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from pyqtgraph import PlotWidget, mkPen, AxisItem

_NPTS = 1000
chdata = np.zeros(2 * _NPTS, dtype=np.int16)
disp = np.zeros(2 * _NPTS)
t = np.zeros(_NPTS)
debst = "R"

_dt = (10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000)

def send(cmd, rdans=True):
    if debug:
        print(cmd[:-1])
        ans = b'?\n'
    else:
        dev.write(cmd.encode())
        if rdans:
            ans = dev.readline()
        else:
            ans = b'?\n'
    return ans[:-1].decode()

def quitcb():
    if not debug:
        dev.close()
    mainwin.destroy()
    app.quit()
    return

def savecb():
    if debug:
        debst = '1'

    i = 1
    if mainwin.on1cb.isChecked():
        i += 1
        ch = 1
    if mainwin.on2cb.isChecked():
        i += 1
    if i < 2:
        QtWidgets.QMessageBox.critical(mainwin, 'Error', 'Nothing to save')
    else:
        fn = QtWidgets.QFileDialog.getSaveFileName(mainwin, 'Save As ..', '', (
            'Data files (*.dat);;All files (*)'))[0]
        if fn:
            out = np.empty([i,_NPTS])
            dt = _dt[mainwin.timecb.currentIndex()] * 1e-6
            out[0] = np.arange(0, _NPTS * dt, dt)
            fmt = "%.3e\t%.5e\n"
            if i == 3:
                out[1] = chdata[:_NPTS] * 5.0 / (1 << 14)
                out[2] = chdata[_NPTS:] * 5.0 / (1 << 14)
                fmt = "%.3e\t%.5e\t%.5e\n"
            elif mainwin.on1cb.isChecked():
                out[1] = chdata[:_NPTS] * 5.0 / (1 << 14)
            else:
                out[1] = chdata[_NPTS:] * 5.0 / (1 << 14)
            with open(fn, 'w') as file:
                for i in range(_NPTS):
                    file.write(fmt % tuple(out.T[i]))
                file.close()        
    return

def runcb():
    global chdata, debst
    
    if debug:
        debst = "R"
    if status() == 'R':
        #channels
        i = 0
        if mainwin.on1cb.isChecked():
            i = 1
        if mainwin.on2cb.isChecked():
            i += 2
        send(f"CH{i}\n")
        #sampling
        dt = _dt[mainwin.timecb.currentIndex()]
        send(f"DT{dt}\n")
        #trigger
        if mainwin.exttrgcb.isChecked():
            send(f"EX1\n")
            lev = int(mainwin.trglevsb.value() * 255 / 5.)
            send(f"TL{lev}\n")
            pol = 1 if mainwin.redgerb.isChecked() else 0
            send(f"TP{pol}\n")
        else:
            send(f"EX0\n")
        send("AR\n")
        mainwin.cancbt.setEnabled(True)

        while status() not in ['1', '2', '3']:
            time.sleep(0.1)
            app.processEvents()
            if debug:
                debst = '1'
        send(f"RD{i}\n", False)
        sz = 4 if i == 3 else 2
        sz *= _NPTS
        if debug:
            tmp = np.zeros(_NPTS, dtype=np.int16)
            for i in range(_NPTS):
                tmp[i] = int((1<<13) + (1<<12) * np.sin(10. * i / _NPTS))
        else:
            ans = b''
            while len(ans) < sz:
                waiting = dev.in_waiting
                if waiting:
                    ans += dev.read(waiting)
                else:
                    time.sleep(0.001)
            tmp = np.frombuffer(ans, dtype=np.int16)
        if i == 1:
            chdata[:_NPTS] = np.copy(tmp)
        elif i == 2:
            chdata[_NPTS:] = np.copy(tmp)
        else:
            chdata = np.copy(tmp)
        mainwin.cancbt.setEnabled(False)
        update()

    return

def cancelcb():
    send("CA\n")

def status():
    if debug:
        return debst
    else:
        return send("ST\n")

def update():
    dt = _dt[mainwin.timecb.currentIndex()] / 1.e6
    t = np.arange(0, _NPTS * dt, dt)
    clr = True
    mainwin.plotw.setXRange(0, _NPTS * dt)
    for a in mainwin.plotw.items():
        if isinstance(a, AxisItem):
            if a.orientation == 'left':
                a.setLabel(units='V')
            elif a.orientation == 'bottom':
                a.setLabel(units='s')
    if mainwin.on1cb.isChecked():
        disp[:_NPTS] = chdata[:_NPTS] * 5. / (1 << 14) + mainwin.off1sb.value()
        pen = mkPen('y', width=1)
        mainwin.plotw.plot(t, disp[:_NPTS], pen=pen, clear=clr);
        clr=False
    if mainwin.on2cb.isChecked():
        disp[_NPTS:] = chdata[_NPTS:] * 5. / (1 << 14) + mainwin.off2sb.value()
        pen = mkPen('c', width=1)
        mainwin.plotw.plot(t, disp[_NPTS:], pen=pen);
    if mainwin.exttrgcb.isChecked():
        lev = mainwin.trglevsb.value()
        ly = np.array([lev, lev])
        lt = np.array([0., (_NPTS - 1) * dt])
        pen = mkPen('w', width=1, style=QtCore.Qt.PenStyle.DotLine)
        mainwin.plotw.plot(lt, ly, pen=pen);
        
def extcb(val):    
    mainwin.redgerb.setEnabled(val)
    mainwin.fedgerb.setEnabled(val)
    mainwin.trglevsb.setEnabled(val)
    update()
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
    
    ui_file = "./scope.ui"
    mainwin = uic.loadUi(ui_file)

    mainwin.cancbt.setEnabled(False)
    mainwin.plotw.setBackground("k")
    mainwin.plotw.setYRange(0, 5.0)    
    mainwin.plotw.showGrid(x=True, y=True)    
    
    mainwin.show()
    
    mainwin.on1cb.stateChanged.connect(update)
    mainwin.on2cb.stateChanged.connect(update)
    mainwin.off1sb.editingFinished.connect(update)
    mainwin.off2sb.editingFinished.connect(update)
    mainwin.trglevsb.editingFinished.connect(update)
    mainwin.timecb.activated.connect(update)
    mainwin.exttrgcb.stateChanged.connect(extcb)
    mainwin.savebt.clicked.connect(savecb)
    mainwin.runbt.clicked.connect(runcb)
    mainwin.cancbt.clicked.connect(cancelcb)
    mainwin.quitbt.clicked.connect(quitcb)
    
    if not debug:
        try:
            dev = serial.Serial(fname, timeout=5)
        except serial.serialutil.SerialException:
            exit(f"Could not open {fname}")
    
    app.exec()
    
if __name__ == "__main__":
    main()
