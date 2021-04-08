import sys
import os
import shutil
from PyQt5 import QtWidgets, uic
from to_filename import clean_filename
from point import Point

From_DialogImportPoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogimportpoint.ui"))[0]

class DialogImportPoint(QtWidgets.QDialog, From_DialogImportPoint):
    
    def __init__(self):
        # Call constructor of parent classes
        super(DialogImportPoint, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)

        self.pushButtonBrowsePressures.clicked.connect(self.browsePressuresFile)
        self.pushButtonBrowseTemperatures.clicked.connect(self.browseTemperaturesFile)
    
    def setSensorsList(self, sensorModel):
        self.comboBoxSensors.setModel(sensorModel)

    def browsePressuresFile(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self, "Select Pressures File")[0]
        if filePath:
            self.lineEditPressures.setText(filePath) 

    def browseTemperaturesFile(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self, "Select Temperatures File")[0]
        if filePath:
            self.lineEditTemperatures.setText(filePath) 

    def addPoint(self, rootDir):

        name = self.lineEditPointName.text()
        prawfile = self.lineEditPressures.text()
        trawfile = self.lineEditTemperatures.text()
        sensor = self.comboBoxSensors.currentText()

        pointDir = os.path.join(rootDir, name) #le dossier porte le nom du point
        os.mkdir(pointDir)
        rawDataDir = os.path.join(pointDir, "raw_data")
        processedDataDir = os.path.join(pointDir, "processed_data")

        os.mkdir(rawDataDir)
        shutil.copyfile(prawfile, os.path.join(rawDataDir, "raw_pressures.csv"))
        shutil.copyfile(trawfile, os.path.join(rawDataDir, "raw_temperatures.csv"))

        os.mkdir(processedDataDir)
        # à compléter, faire les conversions nécessaires

        return Point(name, pointDir, sensor)