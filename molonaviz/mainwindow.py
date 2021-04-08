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
from dialogremovepoint import DialogRemovePoint
from usefulfonctions import displayInfoMessage
from widgetpoint import WidgetPoint

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
        self.actionRemove_Point.triggered.connect(self.removePoint)

    def createStudy(self):
        dlg = DialogStudy()
        res = dlg.exec_()
        if res == QtWidgets.QDialog.Accepted:
            self.currentStudy = dlg.setStudy()
            self.currentStudy.saveStudyToText()
            displayInfoMessage("New study successfully created")
        
    def openStudy(self):
        dlg = DialogFindStudy()
        res = dlg.exec_()
        if res == QtWidgets.QDialog.Accepted:
            self.currentStudy = Study(rootDir=dlg.getRootDir())
            self.currentStudy.loadStudyFromText() #charge le nom de l'étude et son sensorDir
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
            displayInfoMessage("Point successfully imported")
    
    def openPoint(self):
        dlg = DialogOpenPoint()
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            pointDir = dlg.getPointDir()
            point = Point(pointDir=pointDir)
            point.loadPointFromText() #charge le nom du point et son capteur associé
            point.loadPoint(self.openedPointsModel)
            #point.openWidget()
            self.wdg = WidgetPoint(point.name, point.pointDir, point.sensor)
            self.wdg.show()


    def removePoint(self):
        dlg = DialogRemovePoint()
        dlg.setPointsList(self.openedPointsModel)
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            pointName = dlg.getPointToDelete()
            pointItem = self.openedPointsModel.findItems(pointName)[0]
            
            point = pointItem.data(QtCore.Qt.UserRole)
            point.delete() #supprime le dossier du rootDir

            pointIndex = self.openedPointsModel.indexFromItem(pointItem)
            self.openedPointsModel.removeRow(pointIndex.row()) #supprime l'item du model

            point.closeWidget()
            
            displayInfoMessage("Point successfully removed")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())