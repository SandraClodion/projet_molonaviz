import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from study import Study
from dialogstudy import DialogStudy

From_MainWindow,dummy = uic.loadUiType(os.path.join(os.path.dirname(__file__),"mainwindow.ui"))

class MainWindow(QtWidgets.QMainWindow,From_MainWindow):
    
    def __init__(self):
        # Call constructor of parent classes
        super(MainWindow, self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        
        self.setupUi(self)

        self.currentStudy = None

        self.sensorModel = QtGui.QStandardItemModel()
        self.treeViewSensors.setModel(self.sensorModel)

        self.menubar.setNativeMenuBar(False) #Permet d'afficher la barre de menu dans la fenêtre

        self.actionOpen_Study.triggered.connect(self.openStudy)
        self.actionCreate_Study.triggered.connect(self.createStudy)

    def createStudy(self):
        dlg = DialogStudy()
        res = dlg.exec_()
        if res == QtWidgets.QDialog.Accepted:
            self.currentStudy = dlg.getStudy()
        # à modifier par Charlotte pour appeler la fonction save to
        
    def openStudy(self):
        # à modifier par Charlotte pour appeler nouvelle fenêtre de dialogue
        # qui permet de charger une étude qu'on stocke dans currentStudy
        self.currentStudy.loadSensors(self.sensorModel)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())