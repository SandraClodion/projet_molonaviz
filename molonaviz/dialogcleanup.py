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


    def getScript(self):
        self.script = self.plainTextEdit.toPlainText()
        #On enregistre le script comme un fichier texte
        #Difficulté = le convertir ensuite en python
        #Quand est-ce qu'on met le directory en paramètres ?
        return(self.script)