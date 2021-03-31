import sys
import os
from PyQt5 import QtWidgets, uic

From_DialogStudy,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogstudy.ui"))
class DialogStudy(QtWidgets.QDialog,From_DialogStudy):
    def __init__(self):
        # Call constructor of parent classes
        super(DialogStudy, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)
        
        self.pushButtonBrowseRootDir.clicked.connect(self.browseRootDir)
        
    def browseRootDir(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Study Root Directory")
        if dirPath:
            self.lineEditRootDir.setText(dirPath) 

