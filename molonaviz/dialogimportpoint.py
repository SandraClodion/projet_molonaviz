import sys, os, shutil, re
from PyQt5 import QtWidgets, uic
from usefulfonctions import clean_filename
from point import Point
import pandas as pd

From_DialogImportPoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogimportpoint.ui"))[0]

class DialogImportPoint(QtWidgets.QDialog, From_DialogImportPoint):
    
    def __init__(self):
        # Call constructor of parent classes
        super(DialogImportPoint, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)

        self.radioButtonAuto.toggled.connect(self.autoEntry)
        self.radioButtonManual.toggled.connect(self.manualEntry)

        self.pushButtonBrowseDataDir.clicked.connect(self.browseDataDir)
        self.pushButtonBrowseInfo.clicked.connect(self.browseInfo)
        self.pushButtonBrowsePressures.clicked.connect(self.browsePressures)
        self.pushButtonBrowseTemperatures.clicked.connect(self.browseTemperatures)
        self.pushButtonBrowseNotice.clicked.connect(self.browseNotice)
        self.pushButtonBrowseConfig.clicked.connect(self.browseConfig)

    def autoEntry(self):

        self.pushButtonBrowseDataDir.setEnabled(True)
        self.pushButtonBrowseInfo.setEnabled(False)
        self.pushButtonBrowsePressures.setEnabled(False)
        self.pushButtonBrowseTemperatures.setEnabled(False)
        self.pushButtonBrowseNotice.setEnabled(False)
        self.pushButtonBrowseConfig.setEnabled(False)

        self.lineEditDataDir.setReadOnly(False)
        self.lineEditInfo.setReadOnly(True)
        self.lineEditPressures.setReadOnly(True)
        self.lineEditTemperatures.setReadOnly(True)
        self.lineEditConfig.setReadOnly(True)
        self.lineEditNotice.setReadOnly(True)

    def manualEntry(self):

        self.pushButtonBrowseDataDir.setEnabled(False)
        self.pushButtonBrowseInfo.setEnabled(True)
        self.pushButtonBrowsePressures.setEnabled(True)
        self.pushButtonBrowseTemperatures.setEnabled(True)
        self.pushButtonBrowseNotice.setEnabled(True)
        self.pushButtonBrowseConfig.setEnabled(True)

        self.lineEditDataDir.setReadOnly(True)
        self.lineEditInfo.setReadOnly(False)
        self.lineEditPressures.setReadOnly(False)
        self.lineEditTemperatures.setReadOnly(False)
        self.lineEditConfig.setReadOnly(False)
        self.lineEditNotice.setReadOnly(False)


    def browseDataDir(self):

        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Point Data Directory")
        
        if dirPath:

            self.lineEditDataDir.setText(dirPath)
            files = list(filter(('.DS_Store').__ne__, os.listdir(dirPath))) 
            print(files)

            for file in files : 

                if re.search('info', file):
                    filePath = os.path.join(dirPath, file)
                    self.lineEditInfo.setText(filePath) 

                    df = pd.read_csv(filePath, sep=';', header=None, index_col=0)
                    self.lineEditPressureSensor.setText(df.iloc[1].at[1])
                    self.lineEditShaft.setText(df.iloc[2].at[1])
                    self.lineEditDeltaH.setText(df.iloc[6].at[1])

                if re.search('config', file):
                    filePath = os.path.join(dirPath, file)
                    self.lineEditConfig.setText(filePath) 

                if re.search('notice', file):
                    filePath = os.path.join(dirPath, file)
                    self.lineEditNotice.setText(filePath) 

                if re.search('P_', file):
                    filePath = os.path.join(dirPath, file)
                    self.lineEditPressures.setText(filePath) 

                if re.search('T_', file):
                    filePath = os.path.join(dirPath, file)
                    self.lineEditTemperatures.setText(filePath) 

    def browseInfo(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if filePath:
            self.lineEditInfo.setText(filePath) 
            print(filePath)
            df = pd.read_csv(filePath)
            self.lineEditPressureSensor = df.iloc[0][0]
            self.lineEditTemperatureShaft = df.iloc[1][0]
            self.lineEditDeltaH = df.iloc[5][0]
    
    def browsePressures(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if filePath:
            self.lineEditPressures.setText(filePath) 
    
    def browseTemperatures(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if filePath:
            self.lineEditTemperatures.setText(filePath) 
    
    def browseNotice(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if filePath:
            self.lineEditNotice.setText(filePath) 
    
    def browseConfig(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if filePath:
            self.lineEditConfig.setText(filePath) 
    
    def getPointInfo(self):
        name = self.lineEditName.text()
        infofile = self.lineEditInfo.text()
        prawfile = self.lineEditPressures.text()
        trawfile = self.lineEditTemperatures.text()
        noticefile = self.lineEditNotice.text()
        configfile = self.lineEditConfig.text()
        return name, infofile, prawfile, trawfile, noticefile, configfile