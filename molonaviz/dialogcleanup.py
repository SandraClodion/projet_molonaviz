import sys
import os
from PyQt5 import QtWidgets, uic

From_DialogCleanup = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogcleanup.ui"))[0]

class DialogCleanup(QtWidgets.QDialog, From_DialogCleanup):
    
    def __init__(self):
        # Call constructor of parent classes
        super(DialogCleanup, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)


    def executeScript(self, dft, dfp, dir):
        self.scriptpartiel = self.plainTextEdit.toPlainText()
        self.scriptindente = self.scriptpartiel.replace("\n", "\n   ")
        self.script = "def fonction(dft, dfp): \n   " + self.scriptindente + "\n" + "   return(dft, dfp)"

        scriptDir = dir + "/script.py"
        sys.path.append(dir)
        with open(scriptDir, "w") as f:
            f.write(self.script)
            f.close()

        from script import fonction
        new_dft, new_dfp = fonction(dft, dfp)
        return(new_dft, new_dfp)
        os.remove(scriptDir)