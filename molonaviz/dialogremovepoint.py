import sys
import os
import shutil
from PyQt5 import QtWidgets, uic

From_DialogRemovePoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogremovepoint.ui"))[0]

class DialogRemovePoint(QtWidgets.QDialog, From_DialogRemovePoint):
    
    def __init__(self):
        # Call constructor of parent classes
        super(DialogRemovePoint, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)

        self.pushButtonBrowse.clicked.connect(self.browsePointDir)
    
    def browsePointDir(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Study Root Directory")
        if dirPath:
            self.lineEditPointDir.setText(dirPath) 

    def getPointToDelete(self, pointDir):
        return 
