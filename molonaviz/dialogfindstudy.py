import sys
import os
from PyQt5 import QtWidgets, uic

From_DialogFindStudy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"DialogFindStudy.ui"))[0]

class DialogFindStudy(QtWidgets.QDialog,From_DialogFindStudy):
    
    def __init__(self):
        # Call constructor of parent classes
        super(DialogFindStudy, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.pushButtonBrowse.clicked.connect(self.browseRoot)
        
    def browseRoot(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Study Root Directory")
        if dirPath:
            self.lineEditRootDir.setText(dirPath)
    
    def getRootDir(self):
        RootDir = self.lineEditRootDir.text()
        return(RootDir)