import sys
import os
from PyQt5 import QtWidgets, QtCore, uic
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
        
        #self.pointName = pointName
        self.pointDir = pointDir
        #self.pointSensor = pointSensor
        #self.setWindowTitle(self.pointName)
        #self.lineEditSensor.setText(self.pointSensor)

        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonCleanUp.clicked.connect(self.cleanup)
        self.pushButtonCompute.clicked.connect(self.compute)
        self.checkBoxRaw_Data.stateChanged.connect(self.checkbox)

        #point = Point()
        #self.temperatureModel = point.temperatureModel(self.pointDir)
        #self.tableViewTemp.setModel(self.temperatureModel)
        self.currentPressureModel = PandasModel(pd.DataFrame())
        self.tableViewPress.setModel(self.currentPressureModel)

        #self.pressureModel = point.pressureModel(self.pointDir)
        #self.tableViewPress.setModel(self.pressureModel)
        self.currentTemperatureModel = PandasModel(pd.DataFrame())
        self.tableViewTemp.setModel(self.currentTemperatureModel)

    def setWidgetInfos(self, pointName, pointSensor):
        self.setWindowTitle(pointName)
        self.lineEditSensor.setText(pointSensor)

    def setCurrentTemperatureModel(self, dftemp):
        self.currentTemperatureModel._data = dftemp # --> plutot changeData(dftemp)
        #self.tableViewTemp.resizeColumnsToContents() --> rame un peu

    def setCurrentPressureModel(self, dfpress):
        self.currentPressureModel._data = dfpress # --> plutot changeData(dftemp)
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
        ## À compléter
        print("checkbox")

""" 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WidgetPoint()
    mainWin.show()
    sys.exit(app.exec_())
"""