import sys
import os
import shutil
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from study import Study
from point import Point
from dialogstudy import DialogStudy
from dialogfindstudy import DialogFindStudy
from dialogimportpoint import DialogImportPoint
from dialogopenpoint import DialogOpenPoint

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

        self.openedPointsModel = QtGui.QStandardItemModel()
        self.treeViewDataPoints.setModel(self.openedPointsModel)

        self.menubar.setNativeMenuBar(False) #Permet d'afficher la barre de menu dans la fenêtre

        self.actionOpen_Study.triggered.connect(self.openStudy)
        self.actionCreate_Study.triggered.connect(self.createStudy)
        self.actionImport_Point.triggered.connect(self.importPoint)
        self.actionOpen_Point.triggered.connect(self.openPoint)

    def createStudy(self):
        dlg = DialogStudy()
        res = dlg.exec_()
        if res == QtWidgets.QDialog.Accepted:
            self.currentStudy = dlg.setStudy()
            self.currentStudy.saveStudyToText()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("New study successfully created")
            msg.exec_() 
        
    def openStudy(self):
        self.currentStudy = Study()
        dlg = DialogFindStudy()
        res = dlg.exec_()
        if res == QtWidgets.QDialog.Accepted:
            rootDir = dlg.getRootDir()
            name, sensorDir = self.currentStudy.loadStudyFromText(rootDir)
            self.currentStudy = Study(name, rootDir, sensorDir)
            self.currentStudy.loadSensors(self.sensorModel)

    def importPoint(self):
        dlg = DialogImportPoint()
        dlg.setSensorsList(self.sensorModel)
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            name, sensorname, prawfile, trawfile = dlg.getPointInfo()
            sensor = self.sensorModel.findItems(sensorname)[0].data(QtCore.Qt.UserRole)
            point = self.currentStudy.addPoint(name, sensorname, prawfile, trawfile, sensor) 
            point.savePointToText()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Point successfully imported")
            msg.exec_() 
    
    def openPoint(self):
        point = Point()
        dlg = DialogOpenPoint()
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            pointDir = dlg.getPointDir()
            name, sensor = point.loadPointFromText(pointDir)
            point = Point(name, pointDir, sensor)
            point.loadPoint(self.openedPointsModel)

    def removePoint(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())