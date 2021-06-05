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
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries
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
        stats = self.db.stats_samples(10)
        myText = "<html style='color:blue'><i>Average humidity: </i></html>" + \
            str(round(stats[0])) + "\n"
        self.ui.textEdit.append(myText)
        myText = "<html style='color:blue'><i>Minimum humidity: </i></html>" + \
            str(round(stats[1])) + "\n"
        self.ui.textEdit.append(myText)
        myText = "<html style='color:blue'><i>Maximum humidity: </i></html>" + \
            str(round(stats[2])) + "\n"
        self.ui.textEdit.append(myText)
        myText = "<html style='color:green'><i>Average temperature: </i></html>" + \
            str(round(stats[3])) + "\n"
        self.ui.textEdit.append(myText)
        myText = "<html style='color:green'><i>Minimum temperature: </i></html>" + \
            str(round(stats[4])) + "\n"
        self.ui.textEdit.append(myText)
        myText = "<html style='color:green'><i>Maximum temperature: </i></html>" + \
            str(round(stats[5])) + "\n"
        self.ui.textEdit.append(myText)
        
    def slot_display(self):
        print("display")
        rows = self.db.query_samples(10)
        seriesHum = QLineSeries()
        seriesTemp = QLineSeries()
        for sample in rows:
            print(sample)
            seriesHum.append(sample[0],sample[2])
            seriesTemp.append(sample[0],sample[3])
        self.plot_series("Humidity",seriesHum)
        self.plot_series("Temperature",seriesTemp)
        print(rows)
        
    def plot_series(self,title,series):
        myChart = QChart()
        myChart.setTitle(title)
        myChart.addSeries(series)
        myChart.createDefaultAxes()       
        myChartView = QChartView(myChart)
        myDisplayDialog = QDialog(self)
        layout = QVBoxLayout()
        layout.addWidget(myChartView)
        myDisplayDialog.setWindowTitle(title)
        myDisplayDialog.setModal(0)
        myDisplayDialog.setLayout(layout)
        myDisplayDialog.setMinimumHeight(800)
        myDisplayDialog.setMinimumWidth(800)
        myDisplayDialog.adjustSize()
        myDisplayDialog.show()
        
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
