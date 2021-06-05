# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 13:29:30 2021

@author: laura
"""

import sys
import os
from PyQt5.QtWidgets import QDialog, QApplication
from humtemp import Ui_sensorDialog as sensorDialog
from pseudoSensor import PseudoSensor
from humtempdb import HumTempDB

class SensorWindow(QDialog):
    def __init__(self, db):
        super().__init__()
        self.ui = sensorDialog()
        self.ui.setupUi(self)
        
        self.db = db
# Some settings
        self.unit = 0
        self.unitConv = 1
# Connections added
        self.ui.read1PB.clicked.connect(self.slot_read1)
        self.ui.read10PB.clicked.connect(self.slot_read10)
        self.ui.statsPB.clicked.connect(self.slot_stats)
        self.ui.displayPB.clicked.connect(self.slot_display)
        self.ui.displayPB.clicked.connect(self.slot_quit)
# Show it!
        self.show()
        
    def slot_read1(self):
        h,t = ps.generate_values()
        print("H ",h)
        print("T ",t)
        
    def slot_read10(self):
        print("read1")
        
    def slot_stats(self):
        print("stats")
        
    def slot_display():
        print("display")
        
    def slot_quit(self):
        db.shutdown()
        self.ui_quitPB.close()
        
if __name__ == '__main__':
    database = r"C:\Users\laura\work\db\humtemp.db"
    db = HumTempDB(database)
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    app = QApplication(sys.argv)
    w = SensorWindow(db)
    w.show()
    sys.exit(app.exec_())
