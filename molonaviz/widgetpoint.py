import sys
import os
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QPixmap
import pandas as pd
from pandasmodel import PandasModel
#from point import Point

From_WidgetPoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"widgetpoint.ui"))[0]

class WidgetPoint(QtWidgets.QWidget,From_WidgetPoint):
    
    def __init__(self, pointDir):
        # Call constructor of parent classes
        super(WidgetPoint, self).__init__()
        QtWidgets.QWidget.__init__(self)
        
        self.setupUi(self)
        
        self.pointDir = pointDir

        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonCleanUp.clicked.connect(self.cleanup)
        self.pushButtonCompute.clicked.connect(self.compute)
        self.checkBoxRaw_Data.stateChanged.connect(self.checkbox)

        self.labelSchema.setPixmap(QPixmap(self.pointDir + "/info_data" + "/config.png"))

        file = open(self.pointDir + "/info_data" + "/notice.txt")
        self.notice = file.read()
        self.plainTextEditNotice.setPlainText(self.notice)
        file.close()

        self.currentdata = "processed"

        self.TemperatureDir = self.pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_temperatures.csv"
        self.PressureDir = self.pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_pressures.csv"

        self.currentPressureModel = PandasModel(self.PressureDir)
        self.tableViewPress.setModel(self.currentPressureModel)


        self.currentTemperatureModel = PandasModel(self.TemperatureDir)
        self.tableViewTemp.setModel(self.currentTemperatureModel)

    def setWidgetInfos(self, pointName, pointSensor):
        self.setWindowTitle(pointName)
        self.lineEditSensor.setText(pointSensor)

    #def setCurrentTemperatureModel(self, dftemp):
        #self.currentTemperatureModel._data = dftemp # --> plutot changeData(dftemp)
        #self.tableViewTemp.resizeColumnsToContents() --> rame un peu

    #def setCurrentPressureModel(self, dfpress):
        #self.currentPressureModel._data = dfpress # --> plutot changeData(dftemp)
        #self.tableViewPress.resizeColumnsToContents() --> rame un peu

    def reset(self):
        ## À compléter
        print("reset")

    def cleanup(self):
        ## À compléter
        print("cleanup")

    def compute(self):
        ## À compléter
        print("compute")
    
    def checkbox(self):
        if self.checkBoxRaw_Data.isChecked():
            self.currentdata = "raw"
        else :
            self.currentdata = "processed"

        self.TemperatureDir = self.pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_temperatures.csv"
        self.PressureDir = self.pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_pressures.csv"

        self.currentPressureModel = PandasModel(self.PressureDir)
        self.tableViewPress.setModel(self.currentPressureModel)


        self.currentTemperatureModel = PandasModel(self.TemperatureDir)
        self.tableViewTemp.setModel(self.currentTemperatureModel)


""" 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WidgetPoint()
    mainWin.show()
    sys.exit(app.exec_())
"""