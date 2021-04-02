import sys
import os
from PyQt5 import QtWidgets, uic
from study import Study

From_DialogStudy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogstudy.ui"))[0]

class DialogStudy(QtWidgets.QDialog,From_DialogStudy):
    
    def __init__(self):
        # Call constructor of parent classes
        super(DialogStudy, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.pushButtonBrowseRootDir.clicked.connect(self.browseRootDir)
        self.pushButtonBrowseSensorsDir.clicked.connect(self.browseSensorsDir)
        
    def browseRootDir(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Study Root Directory")
        if dirPath:
            self.lineEditRootDir.setText(dirPath) 
    
    def browseSensorsDir(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Study Root Directory")
        if dirPath:
            self.lineEditSensorsDir.setText(dirPath) 

    def getStudy(self):
        name = self.lineEditName.text()
        rootdir = self.lineEditRootDir.text()
        sensorsdir = self.lineEditSensorsDir.text()
        return Study(name, rootdir, sensorsdir)


