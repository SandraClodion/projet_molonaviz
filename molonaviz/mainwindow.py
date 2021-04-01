import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from study import Study
from dialogstudy import DialogStudy

From_MainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__),"mainwindow.ui"))[0]

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

        self.actionCreate_Study.triggered.connect(self.clickedCreateStudy)
        self.actionOpen_Study.triggered.connect(self.clickedOpenStudy)

        self.dialogstudy = DialogStudy()

        self.dialogstudy.buttonBox.accepted.connect(self.createStudy)
    
    def createStudy(self):
        name = self.dialogstudy.lineEditName.text()
        rootdir = self.dialogstudy.lineEditRootDir.text()
        sensorsdir = self.dialogstudy.lineEditSensorsDir.text()
        self.currentStudy = Study(name, rootdir, sensorsdir)   
    
    def loadSensors(self):
        sdir = self.currentStudy.sensorDir
        dirs = os.listdir(sdir)
        for mydir in dirs:
            sensor = self.currentStudy.loadSensor(mydir)
            item = QtGui.QStandardItem(mydir)
            item.setData(sensor, QtCore.Qt.UserRole)
            self.sensorModel.appendRow(item)
            item.appendRow(QtGui.QStandardItem(f"intercept = {float(sensor.intercept):.2f}"))
            item.appendRow(QtGui.QStandardItem(f"dudh = {float(sensor.dudh):.2f}"))
            item.appendRow(QtGui.QStandardItem(f"dudt = {float(sensor.dudt):.2f}"))

    def openStudy(self, study):
        self.currentStudy = study
        self.loadSensors()

    def clickedCreateStudy(self):
        print("clicked create study !")
        self.dialogstudy.show()
    
    def clickedOpenStudy(self):
        print("clicked open study !")
        print(self.currentStudy.name)
        self.openStudy(self.currentStudy)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())