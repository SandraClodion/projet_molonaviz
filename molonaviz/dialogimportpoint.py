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

        self.pushButtonBrowsePressures.clicked.connect(self.browse)
        self.pushButtonBrowseTemperatures.clicked.connect(self.browse)
        self.pushButtonBrowseInfo.clicked.connect(self.browse)
        self.pushButtonBrowseNotice.clicked.connect(self.browse)
        self.pushButtonBrowseInstallation.clicked.connect(self.browse)

    
    def setSensorsList(self, sensorModel):
        self.comboBoxSensors.setModel(sensorModel)

    def browse(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if filePath:
            self.lineEditPressures.setText(filePath) 

    def getPointInfo(self):
        name = self.lineEditPointName.text()
        sensor = self.comboBoxSensors.currentText()
        prawfile = self.lineEditPressures.text()
        trawfile = self.lineEditTemperatures.text()
        noticefile = self.lineEditNotice.text()
        configfile = self.lineEditInstallation.text()
        return name, sensor, prawfile, trawfile