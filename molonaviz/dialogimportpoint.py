import sys
import os
import shutil
from PyQt5 import QtWidgets, uic
from usefulfonctions import clean_filename
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

    def getPointInfo(self):
        name = self.lineEditPointName.text()
        prawfile = self.lineEditPressures.text()
        trawfile = self.lineEditTemperatures.text()
        sensor = self.comboBoxSensors.currentText()
        return name, sensor, prawfile, trawfile