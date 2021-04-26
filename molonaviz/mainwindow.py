import sys, os, shutil
import pandas as pd
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from queue import Queue

from study import Study
from point import Point
from subwindow import SubWindow
from dialogstudy import DialogStudy
from dialogfindstudy import DialogFindStudy
from dialogimportpoint import DialogImportPoint
from dialogopenpoint import DialogOpenPoint
from dialogremovepoint import DialogRemovePoint
from queuethread import *
from usefulfonctions import *
from errors import *


From_MainWindow = uic.loadUiType(os.path.join(os.path.dirname(__file__),"mainwindow.ui"))[0]

class MainWindow(QtWidgets.QMainWindow,From_MainWindow):
    
    def __init__(self):
        # Call constructor of parent classes
        super(MainWindow, self).__init__()
        QtWidgets.QMainWindow.__init__(self)
        
        self.setupUi(self)
        
        # Create Queue and redirect sys.stdout to this queue
        self.queue = Queue()
        sys.stdout = WriteStream(self.queue)
        print("MolonaViz - 0.0.1beta - 2021-04-26")

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
        self.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("MolonaViz")

        self.actionQuit_MolonaViz.triggered.connect(self.exitApp)
        self.actionOpen_Study.triggered.connect(self.openStudy)
        self.actionCreate_Study.triggered.connect(self.createStudy)
        self.actionClose_Study.triggered.connect(self.closeStudy)
        self.actionImport_Point.triggered.connect(self.importPoint)
        self.actionOpen_Point.triggered.connect(self.openPoint)
        self.actionRemove_Point.triggered.connect(self.removePoint)
        self.actionSwitch_To_Tabbed_View.triggered.connect(self.switchToTabbedView)
        self.actionSwitch_To_SubWindow_View.triggered.connect(self.switchToSubWindowView)
        self.treeViewDataPoints.doubleClicked.connect(self.openPointfromTree)

        self.pushButtonClear.clicked.connect(self.clearText)

        #On adapte la taille de la fenêtre principale à l'écran
        screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.setGeometry(screenSize)
        self.setMaximumWidth(self.geometry().width())
        self.setMaximumHeight(self.geometry().height())
    
    def appendText(self,text):
        self.textEditApplicationMessages.moveCursor(QtGui.QTextCursor.End)
        self.textEditApplicationMessages.insertPlainText(text)
    
    def clearText(self):
        self.textEditApplicationMessages.clear()
        print("MolonaViz - 0.0.1beta - 2021-04-26")
    
    def exitApp(self):
        QtWidgets.QApplication.quit()

    def createStudy(self):
        dlg = DialogStudy()
        res = dlg.exec_()
        if res == QtWidgets.QDialog.Accepted:
            try :
                self.currentStudy = dlg.setStudy()
                self.currentStudy.saveStudyToText()
                print("New study successfully created")
                self.openStudy() #on ouvre automatiquement une étude qui vient d'être créée
            except EmptyFieldError as e:
                displayCriticalMessage(f"{str(e)} \nPlease try again")
                self.createStudy()
            except FileNotFoundError as e:
                displayCriticalMessage(f"{str(e)} \nPlease try again")
                self.createStudy()

    def openStudy(self):
        if self.currentStudy == None : #si on ne vient pas de créer une étude
            dlg = DialogFindStudy()
            res = dlg.exec_()
            if res == QtWidgets.QDialog.Accepted:
                try :
                    self.currentStudy = Study(rootDir=dlg.getRootDir())
                except FileNotFoundError as e:
                    displayCriticalMessage(f"{str(e)} \nPlease try again")
                    self.openStudy()
            else :
                return None
        try :
            self.currentStudy.loadStudyFromText() #charge le nom de l'étude et son sensorDir
            self.setWindowTitle(f'MolonaViz – {self.currentStudy.getName()}')
        except TextFileError as e:
            infoMessage = f"You might have selected the wrong root directory \n\nIf not, please see the Help section "
            displayCriticalMessage(str(e), infoMessage)
            self.currentStudy = None
            return None
                
        self.currentStudy.loadPressureSensors(self.pSensorModel)
        self.currentStudy.loadShafts(self.shaftModel)
        self.currentStudy.loadThermometers(self.thermometersModel)
        self.currentStudy.loadPoints(self.pointModel)

        #le menu point n'est pas actif tant qu'aucune étude n'est ouverte et chargée
        self.menuPoint.setEnabled(True)
        self.actionClose_Study.setEnabled(True)

        #on n'autorise pas l'ouverture ou la création d'une étude s'il y a déjà une étude ouverte
        self.actionOpen_Study.setEnabled(False) 
        self.actionCreate_Study.setEnabled(False)
    
    def closeStudy(self):

        #On ferme tous les points ouverts
        openedSubWindows = self.mdi.subWindowList()
        for subWin in openedSubWindows:
            subWin.close()

        #On remet les modèles à zéro
        self.pSensorModel.clear()
        self.shaftModel.clear()
        self.thermometersModel.clear()
        self.pointModel.clear()

        self.setWindowTitle("MolonaViz")

        self.menuPoint.setEnabled(False)
        self.actionClose_Study.setEnabled(False)
        self.actionOpen_Study.setEnabled(True) 
        self.actionCreate_Study.setEnabled(True)

        self.currentStudy = None


    def importPoint(self):

        dlg = DialogImportPoint()
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            
            name, infofile, prawfile, trawfile, noticefile, configfile  = dlg.getPointInfo()
            
            point = self.currentStudy.addPoint(name, infofile, prawfile, trawfile, noticefile, configfile) 
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

    def openPointView(self, point: Point):
        
        subWin = SubWindow(point, self.currentStudy)
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
            
            title = "Warning ! You are about to delete a point"
            message = "All point data will be deleted. Are you sure you want to proceed ?"
            msgBox = displayConfirmationMessage(title, message)
            
            if msgBox == QtWidgets.QMessageBox.Ok:
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
                
                print("Point successfully removed")
            else : 
                displayInfoMessage("Point removal aborted")

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
    #app.setStyle('windows')
    app.setWindowIcon(QtGui.QIcon("fakeMolonavizIcon.png")) #à modifier quand l'icone est prête
    mainWin = MainWindow()
    mainWin.show()

    # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
    thread = QtCore.QThread()
    my_receiver = MyReceiver(mainWin.queue)
    my_receiver.mysignal.connect(mainWin.appendText)
    my_receiver.moveToThread(thread)
    thread.started.connect(my_receiver.run)
    thread.start()

    sys.exit(app.exec_())