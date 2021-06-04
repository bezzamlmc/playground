# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 13:29:30 2021

@author: laura
"""

import sys
import os
from PyQt5.QtWidgets import QDialog, QApplication
from humtemp import Ui_sensorDialog as sensorDialog

class SensorWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = sensorDialog()
        self.ui.setupUi(self)
        self.show()
        self.unit = 0
        self.unitConv = 1
        self.show()
        
if __name__ == '__main__':
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    app = QApplication(sys.argv)
    w = SensorWindow()
    w.show()
    sys.exit(app.exec_())
