import sys
import os
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QPixmap
import pandas as pd
from pandasmodel import PandasModel
from dialogcleanup import DialogCleanup
from dialogcompute import DialogCompute
from usefulfonctions import displayInfoMessage
from point import Point
from mlpcanvas import MplCanvas
from compute import Compute
import numpy as np 

From_WidgetPoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"widgetpoint.ui"))[0]

class WidgetPoint(QtWidgets.QWidget,From_WidgetPoint):
    
    def __init__(self, point, study):
        # Call constructor of parent classes
        super(WidgetPoint, self).__init__()
        QtWidgets.QWidget.__init__(self)
        
        self.setupUi(self)
        
        self.point = point
        self.study = study

        # Link every button to their function

        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonCleanUp.clicked.connect(self.cleanup)
        self.pushButtonCompute.clicked.connect(self.compute)
        self.checkBoxRaw_Data.stateChanged.connect(self.checkbox)
        self.setPressureAndTemperatureModels()
        self.setPlots()

    def setInfoTab(self):
        # Set the "Infos" tab
        pointDir = self.point.getPointDir()
            #Installation
        self.labelSchema.setPixmap(QPixmap(pointDir + "/info_data" + "/config.png"))
            #Notice
        file = open(pointDir + "/info_data" + "/notice.txt")
        notice = file.read()
        self.plainTextEditNotice.setPlainText(notice)
        file.close()
            #Infos
        infoFile = pointDir + "/info_data" + "/info.csv"
        dfinfo = pd.read_csv(infoFile, sep=';', header=None)
        self.infosModel = PandasModel(dfinfo)
        self.tableViewInfos.setModel(self.infosModel)

    def setPressureAndTemperatureModels(self):
        # Set the Temperature and Pressure models
        self.currentdata = "processed"
        pointDir = self.point.getPointDir()

        self.TemperatureDir = pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_temperatures.csv"
        self.PressureDir = pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_pressures.csv"

        self.dfpress = pd.read_csv(self.PressureDir)
        self.currentPressureModel = PandasModel(self.dfpress)
        self.tableViewPress.setModel(self.currentPressureModel)
        self.tableViewPress.resizeColumnsToContents()

        self.dftemp = pd.read_csv(self.TemperatureDir)
        self.currentTemperatureModel = PandasModel(self.dftemp)
        self.tableViewTemp.setModel(self.currentTemperatureModel)
        self.tableViewTemp.resizeColumnsToContents()

    def setWidgetInfos(self):
        pointName = self.point.getName()
        pointPressureSensor = self.point.getPressureSensor()
        pointShaft = self.point.getShaft()

        self.setWindowTitle(pointName)
        self.lineEditSensor.setText(pointPressureSensor)
        self.lineEditShaft.setText(pointShaft)

    def reset(self):
        self.point.processData(self.study.getSensorDir())
        #On actualise les modèles
        self.dfpress = pd.read_csv(self.PressureDir)
        self.dftemp = pd.read_csv(self.TemperatureDir)
        self.currentTemperatureModel.setData(self.dftemp)
        self.currentPressureModel.setData(self.dfpress)
        self.tableViewTemp.resizeColumnsToContents()
        self.tableViewPress.resizeColumnsToContents()
        self.graphpress.update_(self.dfpress)
        self.graphtemp.update_(self.dftemp)
        displayInfoMessage("Data successfully reset !")


    def cleanup(self):
        if self.currentdata == "raw":
            displayInfoMessage("Please clean-up your processed data.")
        else:
            dlg = DialogCleanup()
            res = dlg.exec_()
            if res == QtWidgets.QDialog.Accepted:
                script = dlg.getScript()
                self.dftemp, self.dfpress = self.point.cleanup(script, self.dftemp, self.dfpress)
                displayInfoMessage("Data successfully cleaned !")
                #On actualise les modèles
                self.currentTemperatureModel.setData(self.dftemp)
                self.currentPressureModel.setData(self.dfpress)
                self.tableViewTemp.resizeColumnsToContents()
                self.tableViewPress.resizeColumnsToContents()
                self.graphpress.update_(self.dfpress)
                self.graphtemp.update_(self.dftemp)

    def compute(self):
        
        sensorDir = self.study.getSensorDir()

        dlg = DialogCompute()
        res = dlg.exec()

        if res == 0 : 
            params, nb_cells = dlg.getInputDirectModel()
            compute = Compute(self.point)
            compute.computeDirectModel(params, nb_cells, sensorDir)
            # ajouter fonction plot
 
        if res == 1 :
            nb_iter, priors, nb_cells = dlg.getInputMCMC()
            compute = Compute(self.point)
            compute.computeMCMC(nb_iter, priors, nb_cells, sensorDir)
            # ajouter fonction plot
    
    def checkbox(self):

        pointDir = self.point.getPointDir()

        if self.checkBoxRaw_Data.isChecked():
            self.currentdata = "raw"
        else :
            self.currentdata = "processed"

        self.TemperatureDir = pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_temperatures.csv"
        self.PressureDir = pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_pressures.csv"

        if self.currentdata == "processed":
            self.dftemp = pd.read_csv(self.TemperatureDir)
            self.dfpress = pd.read_csv(self.PressureDir)
            self.currentTemperatureModel.setData(self.dftemp)
            self.currentPressureModel.setData(self.dfpress)
            self.tableViewTemp.resizeColumnsToContents()
            self.tableViewPress.resizeColumnsToContents()
        
        elif self.currentdata == "raw":
            self.dftemp = pd.read_csv(self.TemperatureDir)
            self.dfpress = pd.read_csv(self.PressureDir) #à modifier à reception des dataloggers de pression
            self.currentTemperatureModel.setData(self.dftemp)
            self.currentPressureModel.setData(self.dfpress)  
            self.tableViewTemp.resizeColumnsToContents()
            self.tableViewPress.resizeColumnsToContents()

    def setPlots(self):
        #Commençons par la pression :
        self.graphpress = MplCanvas(self.dfpress)
        vbox = QtWidgets.QVBoxLayout()
        #vbox.setContentsMargins(0, 0, 0, 0)
        self.groupBoxPress.setLayout(vbox)
        vbox.addWidget(self.graphpress)
        #Maintenant les températures :
        self.graphtemp = MplCanvas(self.dftemp, temp=True)
        vbox2 = QtWidgets.QVBoxLayout()
        #vbox2.setContentsMargins(0, 0, 0, 0)
        self.groupBoxTemp.setLayout(vbox2)
        vbox2.addWidget(self.graphtemp)


""" 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WidgetPoint()
    mainWin.show()
    sys.exit(app.exec_())
"""