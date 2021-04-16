import sys
import os
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QPixmap
import pandas as pd
from pandasmodel import PandasModel
from dialogcleanup import DialogCleanup
from usefulfonctions import displayInfoMessage, time_plots
from point import Point
from timeaxisitem import TimeAxisItem
import pyqtgraph as pg

From_WidgetPoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"widgetpoint.ui"))[0]

class WidgetPoint(QtWidgets.QWidget,From_WidgetPoint):
    
    def __init__(self, point, pSensor):
        # Call constructor of parent classes
        super(WidgetPoint, self).__init__()
        QtWidgets.QWidget.__init__(self)
        
        self.setupUi(self)
        
        self.point = point
        self.pSensor = pSensor

        # Link every button to their function

        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonCleanUp.clicked.connect(self.cleanup)
        self.pushButtonCompute.clicked.connect(self.compute)
        self.checkBoxRaw_Data.stateChanged.connect(self.checkbox)
        self.setPressureAndTemperatureModels()
        #self.plots()

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

        self.dfpress = pd.read_csv(self.PressureDir, index_col=0)
        self.currentPressureModel = PandasModel(self.dfpress)
        self.tableViewPress.setModel(self.currentPressureModel)
        self.tableViewPress.resizeColumnsToContents()

        self.dftemp = pd.read_csv(self.TemperatureDir, index_col=0)
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
        point.processData(self.pSensor)
        #On actualise les modèles
        self.dfpress = pd.read_csv(self.PressureDir, index_col=0)
        self.dftemp = pd.read_csv(self.TemperatureDir, index_col=0)
        self.currentTemperatureModel.setData(self.dftemp)
        self.currentPressureModel.setData(self.dfpress)
        self.tableViewTemp.resizeColumnsToContents()
        self.tableViewPress.resizeColumnsToContents()


    def cleanup(self):

        pointDir = self.pointDir.getPointDir()

        if self.currentdata == "raw":
            displayInfoMessage("Please clean-up your processed data.")
        else:
            dft = self.currentTemperatureModel.getpdData()
            dfp = self.currentPressureModel.getpdData()
            dlg = DialogCleanup()
            res = dlg.exec_()
            if res == QtWidgets.QDialog.Accepted:
                new_dft, new_dfp = dlg.executeScript(dft, dfp, pointDir)
                #On enregistre les nouvelles dataframe en cvs à la place des anciens -- Est-ce qu'on enfreint la séparation entre données et visualisation ?
                #On peut en faire une méthode de la classe Point plutôt !
                os.remove(self.TemperatureDir)
                os.remove(self.PressureDir)
                new_dft.to_csv(self.TemperatureDir)
                new_dfp.to_csv(self.PressureDir)
                displayInfoMessage("Data successfully cleaned !")
                #On actualise les modèles
                self.dftemp = new_dft
                self.dfpress = new_dfp
                self.currentTemperatureModel.setData(self.dftemp)
                self.currentPressureModel.setData(self.dfpress)
                self.tableViewTemp.resizeColumnsToContents()
                self.tableViewPress.resizeColumnsToContents()

    def compute(self):
        ## À compléter
        print("compute")
    
    def checkbox(self):

        pointDir = self.point.getPointDir()

        if self.checkBoxRaw_Data.isChecked():
            self.currentdata = "raw"
        else :
            self.currentdata = "processed"

        self.TemperatureDir = pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_temperatures.csv"
        self.PressureDir = pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_pressures.csv"

        if self.currentdata == "processed":
            self.dftemp = pd.read_csv(self.TemperatureDir, index_col=0)
            self.dfpress = pd.read_csv(self.PressureDir, index_col=0)
            self.currentTemperatureModel.setData(self.dftemp)
            self.currentPressureModel.setData(self.dfpress)
            self.tableViewTemp.resizeColumnsToContents()
            self.tableViewPress.resizeColumnsToContents()
        
        elif self.currentdata == "raw":
            self.dftemp = pd.read_csv(self.TemperatureDir, index_col=0, header=1)
            self.dfpress = pd.read_csv(self.PressureDir, sep=';') #à modifier à reception des dataloggers de pression
            self.currentTemperatureModel.setData(self.dftemp)
            self.currentPressureModel.setData(self.dfpress)  
            self.tableViewTemp.resizeColumnsToContents()
            self.tableViewPress.resizeColumnsToContents()

    def plots(self):
        date_axis = [TimeAxisItem(orientation='bottom')]*4
        pg.setConfigOption('background', 'w')
        #On commence par les pressions:
        graphpressure = time_plots(self.dfpress, date_axis, Temp=False)
        vbox1 = QtWidgets.QVBoxLayout()
        self.groupBoxPress.setLayout(vbox1)
        vbox1.addWidget(graphpressure)
        #On suit avec les températures:
        graphtemp = time_plots(self.dftemp, date_axis, Temp=True)
        vbox2 = QtWidgets.QVBoxLayout()
        self.groupBoxTemp.setLayout(vbox2)
        for graph in graphtemp:
            vbox2.addWidget(graph)



""" 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WidgetPoint()
    mainWin.show()
    sys.exit(app.exec_())
"""