# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 13:29:30 2021

@author: laura

"""
# Create ui file with designer and python code with : pyuic5 humtemp.ui > humtemp.py
import sys
import os
import datetime
import time
from PyQt5.QtWidgets import QDialog, QApplication
from humtemp import Ui_sensorDialog as sensorDialog
from pseudoSensor import PseudoSensor
from humtempdb import HumTempDB

class SensorWindow(QDialog):
    def __init__(self, ps, db):
        super().__init__()
        self.ui = sensorDialog()
        self.ui.setupUi(self)
        
        self.db = db
        
        self.ps = ps

# Connections added
        self.ui.read1PB.clicked.connect(self.slot_read1)
        self.ui.read10PB.clicked.connect(self.slot_read10)
        self.ui.statsPB.clicked.connect(self.slot_stats)
        self.ui.displayPB.clicked.connect(self.slot_display)
        self.ui.quitPB.clicked.connect(self.slot_quit)
# Show it!
        self.show()
        
    def get_1sample(self):
        h,t = self.ps.generate_values()
        tmax = self.ui.alarmTSB.value()
        if self.ui.unitCB.currentIndex() == 1:
            t = ( 32. - t ) * 5. / 9.
            tmax = ( tmax * 9./5. ) + 32.
        hr = round(h)
        tr = round(t)
        ts = get_timestamp()
        myText = "At timestamp " + str(ts) + ":\n Humidity: " + \
        str(hr) + \
        " %; Temperature: " + \
        str(tr) + " " + \
        self.ui.unitCB.currentText() + \
        "\n"
        self.ui.textEdit.append(myText)
        self.db.insert_record(ts,hr,tr)
 
        if  h > self.ui.alarmHSB.value():
            myText = "<html><b>ALARM: Humidity exceeded\n<html><b>"
            self.ui.textEdit.append(myText)
        if  t > tmax:
            myText = "<html><b>ALARM: Temperature exceeded<\b><html>\n"
            self.ui.textEdit.append(myText)
        
    def slot_read1(self):
        self.get_1sample()
        
    def slot_read10(self):
        for i in range(10):
            self.get_1sample()
            time.sleep(1)
        
    def slot_stats(self):
        print("stats")
        self.db.stats_samples(10)
        
    def slot_display():
        print("display")
        
    def slot_quit(self):
        db.shutdown()
        self.done(0)
        
def get_timestamp():
    # ct stores current time
    ct = datetime.datetime.now() 
    # ts store timestamp of current time
    ts = ct.timestamp()
    return ts
        
if __name__ == '__main__':
    database = r"C:\Users\laura\work\db\humtemp.db"
    db = HumTempDB(database)
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    
    ps = PseudoSensor()
    
    app = QApplication(sys.argv)
    w = SensorWindow(ps,db)
    w.show()
    sys.exit(app.exec_())
