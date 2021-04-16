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
from usefulfonctions import displayInfoMessage, displayCriticalMessage
#from widgetpoint import WidgetPoint
from subwindow import SubWindow

From_MainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__),"mainwindow.ui"))[0]

class MainWindow(QtWidgets.QMainWindow,From_MainWindow):
    
    def __init__(self):
        # Call constructor of parent classes
        super(MainWindow, self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        
        self.setupUi(self)

        self.mdi = QtWidgets.QMdiArea()
        self.setCentralWidget(self.mdi)
        self.mdi.setTabsMovable(True)
        self.mdi.setTabsClosable(True)

        self.currentStudy = None

        self.pSensorModel = QtGui.QStandardItemModel()
        self.treeViewPressureSensors.setModel(self.pSensorModel)
        self.treeViewPressureSensors.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.shaftModel = QtGui.QStandardItemModel()
        self.treeViewShafts.setModel(self.shaftModel)
        self.treeViewShafts.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.thermometersModel = QtGui.QStandardItemModel()
        self.treeViewThermometers.setModel(self.thermometersModel)
        self.treeViewThermometers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        self.pointModel = QtGui.QStandardItemModel()
        self.treeViewDataPoints.setModel(self.pointModel)
        self.treeViewDataPoints.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.menubar.setNativeMenuBar(False) #Permet d'afficher la barre de menu dans la fenêtre

        self.actionOpen_Study.triggered.connect(self.openStudy)
        self.actionCreate_Study.triggered.connect(self.createStudy)
        self.actionImport_Point.triggered.connect(self.importPoint)
        self.actionOpen_Point.triggered.connect(self.openPoint)
        self.actionRemove_Point.triggered.connect(self.removePoint)
        self.actionSwitch_To_Tabbed_View.triggered.connect(self.switchToTabbedView)
        self.actionSwitch_To_SubWindow_View.triggered.connect(self.switchToSubWindowView)
        self.treeViewDataPoints.doubleClicked.connect(self.openPointfromTree)

        #On adapte la taille de la fenêtre principale à l'écran
        screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.setGeometry(screenSize)
        self.setMaximumWidth(self.geometry().width())
        self.setMaximumHeight(self.geometry().height())

    def createStudy(self):
        dlg = DialogStudy()
        res = dlg.exec_()
        if res == QtWidgets.QDialog.Accepted:
            self.currentStudy = dlg.setStudy()
            self.currentStudy.saveStudyToText()
            displayInfoMessage("New study successfully created")
            self.openStudy() #on ouvre automatiquement une étude qui vient d'être créée
            
    def openStudy(self):
        if self.currentStudy == None : #si on ne vient pas de créer une étude
            dlg = DialogFindStudy()
            res = dlg.exec_()
            if res == QtWidgets.QDialog.Accepted:
                try :
                    self.currentStudy = Study(rootDir=dlg.getRootDir())
                except FileNotFoundError :
                    displayCriticalMessage("No such directory \n Please try again")
        self.currentStudy.loadStudyFromText() #charge le nom de l'étude et son sensorDir
        self.currentStudy.loadPressureSensors(self.pSensorModel)
        self.currentStudy.loadShafts(self.shaftModel)
        self.currentStudy.loadThermometers(self.thermometersModel)
        self.currentStudy.loadPoints(self.pointModel)
        self.menuPoint.setEnabled(True)
        #on n'autorise pas l'ouverture ou la création d'une étude s'il y a déjà une étude ouverte
        self.actionOpen_Study.setEnabled(False) 
        self.actionCreate_Study.setEnabled(False)

    def importPoint(self):

        dlg = DialogImportPoint()
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            
            name, infofile, prawfile, trawfile, noticefile, configfile  = dlg.getPointInfo()
            
            point = self.currentStudy.addPoint(name, infofile, prawfile, trawfile, noticefile, configfile, self.pSensorModel) 
            point.loadPoint(self.pointModel)
           
    def openPoint(self):
        dlg = DialogOpenPoint()
        dlg.setPointsList(self.pointModel)
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            pointname = dlg.getPointName()
            point = self.pointModel.findItems(pointname)[0].data(QtCore.Qt.UserRole)
            self.openPointView(point)

    def openPointfromTree(self):
        point = self.treeViewDataPoints.selectedIndexes()[0].data(QtCore.Qt.UserRole)
        self.openPointView(point)

    def openPointView(self, point):
        
        pSensor = self.pSensorModel
        subWin = SubWindow(point, pSensor)
        subWin.setPointWidget()

        if self.mdi.viewMode() == QtWidgets.QMdiArea.SubWindowView:
            self.mdi.addSubWindow(subWin)
            subWin.show()
            self.mdi.tileSubWindows()

        elif self.mdi.viewMode() == QtWidgets.QMdiArea.TabbedView:
            self.switchToSubWindowView()
            self.mdi.addSubWindow(subWin)
            subWin.show()
            self.mdi.tileSubWindows()
            self.switchToTabbedView()
        
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

            #On ferme la fenêtre associée au point qu'on enlève
            openedSubWindows = self.mdi.subWindowList()
            for subWin in openedSubWindows:
                if subWin.getName() == pointName:
                    subWin.close()
            
            displayInfoMessage("Point successfully removed")

    def switchToTabbedView(self):
        self.mdi.setViewMode(QtWidgets.QMdiArea.TabbedView)
        self.actionSwitch_To_Tabbed_View.setEnabled(False)
        self.actionSwitch_To_SubWindow_View.setEnabled(True)

    def switchToSubWindowView(self):
        self.mdi.setViewMode(QtWidgets.QMdiArea.SubWindowView)
        self.mdi.tileSubWindows()
        self.actionSwitch_To_Tabbed_View.setEnabled(True)
        self.actionSwitch_To_SubWindow_View.setEnabled(False)
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())