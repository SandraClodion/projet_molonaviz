import sys
import os
import shutil
import pandas as pd
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

        self.mdi = QtWidgets.QMdiArea()
        self.setCentralWidget(self.mdi)

        self.currentStudy = None

        self.pSensorModel = QtGui.QStandardItemModel()
        self.treeViewPressureSensors.setModel(self.pSensorModel)

        self.shaftModel = QtGui.QStandardItemModel()
        self.treeViewShafts.setModel(self.shaftModel)

        self.thermometersModel = QtGui.QStandardItemModel()
        self.treeViewThermometers.setModel(self.thermometersModel)

        self.pointModel = QtGui.QStandardItemModel()
        self.treeViewDataPoints.setModel(self.pointModel)

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
            self.openStudy() #on ouvre automatiquement une étude qui vient d'être créée
            
    def openStudy(self):
        if self.currentStudy == None :
            dlg = DialogFindStudy()
            res = dlg.exec_()
            if res == QtWidgets.QDialog.Accepted:
                self.currentStudy = Study(rootDir=dlg.getRootDir())
                self.currentStudy.loadStudyFromText() #charge le nom de l'étude et son sensorDir
                self.currentStudy.loadPressureSensors(self.pSensorModel)
                self.currentStudy.loadShafts(self.shaftModel)
                self.currentStudy.loadThermometers(self.thermometersModel)
                self.currentStudy.loadPoints(self.pointModel)
        else : #si une nouvelle étude a été créée
            self.currentStudy.loadStudyFromText() #charge le nom de l'étude et son sensorDir
            self.currentStudy.loadPressureSensors(self.pSensorModel)
            self.currentStudy.loadShafts(self.shaftModel)
            self.currentStudy.loadThermometers(self.thermometersModel)
            self.currentStudy.loadPoints(self.pointModel)

    def importPoint(self):

        dlg = DialogImportPoint()
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            
            name, infofile, prawfile, trawfile, noticefile, configfile  = dlg.getPointInfo()
            
            psensorname = pd.read_csv(infofile, sep=';', index_col=0).iloc[0][0]
            print(psensorname)
            psensor = self.pSensorModel.findItems(psensorname)[0].data(QtCore.Qt.UserRole)
            pointDir = self.currentStudy.addPoint(name, infofile, prawfile, trawfile, noticefile, configfile, psensor) #psensor nécessaire pour la conversion
            
            point = Point(name, pointDir)
            point.loadPointFromDir()
            point.loadPoint(self.pointModel)
    
    def openPoint(self):
        dlg = DialogOpenPoint()
        dlg.setPointsList(self.pointModel)
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            pointname = dlg.getPointName()
            point = self.pointModel.findItems(pointname)[0].data(QtCore.Qt.UserRole)
            
            pointDir = point.pointDir #pas ok en encapulation, juste pour tester
            
            sub = QtWidgets.QMdiSubWindow()
            sub.setWidget(WidgetPoint(pointDir))
            self.mdi.addSubWindow(sub)
            sub.show()

            #point.openWidget()
            #self.wdg = WidgetPoint(point.name, point.pointDir, point.sensor)
            #self.wdg.show()

    def removePoint(self):
        dlg = DialogRemovePoint()
        dlg.setPointsList(self.pointModel)
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            pointName = dlg.getPointToDelete()
            pointItem = self.pointModel.findItems(pointName)[0]
            
            point = pointItem.data(QtCore.Qt.UserRole)
            point.delete() #supprime le dossier du rootDir

            pointIndex = self.pointModel.indexFromItem(pointItem)
            self.pointModel.removeRow(pointIndex.row()) #supprime l'item du model

            point.closeWidget()
            
            displayInfoMessage("Point successfully removed")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())