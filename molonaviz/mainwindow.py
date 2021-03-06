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
from dialogaboutus import DialogAboutUs
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
        # sys.stderr = WriteStream(self.queue)
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

        self.menubar.setNativeMenuBar(False) #Permet d'afficher la barre de menu dans la fen??tre
        self.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.setWindowTitle("MolonaViz")

        self.actionQuit_MolonaViz.triggered.connect(self.exitApp)
        self.actionAbout_MolonaViz.triggered.connect(self.aboutUs)
        self.actionOpen_Study.triggered.connect(self.openStudy)
        self.actionCreate_Study.triggered.connect(self.createStudy)
        self.actionClose_Study.triggered.connect(self.closeStudy)
        self.actionImport_Point.triggered.connect(self.importPoint)
        self.actionOpen_Point.triggered.connect(self.openPoint)
        self.actionRemove_Point.triggered.connect(self.removePoint)
        self.actionSwitch_To_Tabbed_View.triggered.connect(self.switchToTabbedView)
        self.actionSwitch_To_SubWindow_View.triggered.connect(self.switchToSubWindowView)
        
        self.actionData_Points.triggered.connect(self.changeDockPointsStatus)

        self.treeViewDataPoints.doubleClicked.connect(self.openPointfromTree)

        self.pushButtonClear.clicked.connect(self.clearText)

        #On adapte la taille de la fen??tre principale ?? l'??cran
        # screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)
        # self.setGeometry(screenSize)
        # self.setMaximumWidth(self.geometry().width())
        # self.setMaximumHeight(self.geometry().height())
    
    def appendText(self,text):
        self.textEditApplicationMessages.moveCursor(QtGui.QTextCursor.End)
        self.textEditApplicationMessages.insertPlainText(text)
    
    def clearText(self):
        self.textEditApplicationMessages.clear()
        print("MolonaViz - 0.0.1beta - 2021-04-26")
    
    def exitApp(self):
        QtWidgets.QApplication.quit()
    
    def aboutUs(self):
        dlg = DialogAboutUs()
        dlg.exec_()
    
    def changeDockPointsStatus(self):
        if self.actionData_Points.isChecked() == True :
            self.dockDataPoints.hide()
            self.actionData_Points.setChecked(False)
        else :
            pass

    def createStudy(self):
        dlg = DialogStudy()
        res = dlg.exec_()
        errors = False
        if res == QtWidgets.QDialog.Accepted:
            try :
                self.currentStudy = dlg.setStudy()
                self.currentStudy.saveStudyToText()
                try :
                    self.openStudy() #on ouvre automatiquement une ??tude qui vient d'??tre cr????e
                except LoadingError as e :
                    print(e)
                    print('Study creation aborted')
                    displayCriticalMessage('Study creation aborted', f'An error occured \n Please check "Application messages" for further information')
                    shutil.rmtree(self.currentStudy.getRootDir())
                    self.currentStudy = None
                    return None
                except Exception as e :
                    try :
                        print(e)
                    except :
                        print('Unknown error')
                    print('Study creation aborted')
                    displayCriticalMessage('Study creation aborted', f'An error occured. Please check "Application messages" for further information')
                    shutil.rmtree(self.currentStudy.getRootDir())
                    self.currentStudy = None
                    return None
            except EmptyFieldError as e:
                displayCriticalMessage(f"{str(e)} \nPlease try again")
                self.createStudy()
            except FileNotFoundError as e:
                displayCriticalMessage(f"{str(e)} \nPlease try again")
                self.createStudy()
            except Exception as error:
                print(f'error : {str(error)}')
                self.currentStudy = None
            print("New study successfully created")

    def openStudy(self):
        if self.currentStudy == None : #si on ne vient pas de cr??er une ??tude
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
            self.currentStudy.loadStudyFromText() #charge le nom de l'??tude et son sensorDir
            self.setWindowTitle(f'MolonaViz ??? {self.currentStudy.getName()}')
        except TextFileError as e:
            infoMessage = f"You might have selected the wrong root directory \n\nIf not, please see the Help section "
            displayCriticalMessage(str(e), infoMessage)
            self.currentStudy = None
            return None
        try :
            self.currentStudy.loadPressureSensors(self.pSensorModel)
        except Exception :
            raise LoadingError("pressure sensors")
        try : 
            self.currentStudy.loadShafts(self.shaftModel)
        except Exception :
            raise LoadingError("shafts")
        try :
            self.currentStudy.loadThermometers(self.thermometersModel)
        except Exception :
            raise LoadingError("thermometers")
        try :
            self.currentStudy.loadPoints(self.pointModel)
        except Exception :
            print('Error in loading points')


        #le menu point n'est pas actif tant qu'aucune ??tude n'est ouverte et charg??e
        self.menuPoint.setEnabled(True)
        self.actionClose_Study.setEnabled(True)

        #on n'autorise pas l'ouverture ou la cr??ation d'une ??tude s'il y a d??j?? une ??tude ouverte
        self.actionOpen_Study.setEnabled(False) 
        self.actionCreate_Study.setEnabled(False)
    
    def closeStudy(self):

        #On ferme tous les points ouverts
        openedSubWindows = self.mdi.subWindowList()
        for subWin in openedSubWindows:
            subWin.close()

        #On remet les mod??les ?? z??ro
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
        point = Point()
        dlg = DialogImportPoint()
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            try :
                name, infofile, prawfile, trawfile, noticefile, configfile  = dlg.getPointInfo()
                point = self.currentStudy.addPoint(name, infofile, prawfile, trawfile, noticefile, configfile) 
                point.loadPoint(self.pointModel)
            except Exception as e :
                print(f"Point import aborted : {str(e)}")
                displayCriticalMessage('Point import aborted', f"Couldn't import point due to the following error : \n{str(e)}")
           
    def openPoint(self):
        dlg = DialogOpenPoint()
        dlg.setPointsList(self.pointModel)
        res = dlg.exec()
        if res == QtWidgets.QDialog.Accepted:
            pointname = dlg.getPointName()
            print(f"Opening {pointname} ...") #Pb : ne s'affiche pas tant que tout n'est pas charg?? chez Sandra
            point = self.pointModel.findItems(pointname)[0].data(QtCore.Qt.UserRole)
            self.openPointView(point)
            print(" ==> done")

    def openPointfromTree(self):
        point = self.treeViewDataPoints.selectedIndexes()[0].data(QtCore.Qt.UserRole)
        print(f"Opening {point.getName()} ...")
        self.openPointView(point)
        print(" ==> done")

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

                #On ferme la fen??tre associ??e au point qu'on enl??ve
                openedSubWindows = self.mdi.subWindowList()
                for subWin in openedSubWindows:
                    if subWin.getName() == pointName:
                        subWin.close()
                
                print(f"{pointName} successfully removed")
            else : 
                #displayInfoMessage("Point removal aborted")
                print("Point removal aborted")

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
    app.setWindowIcon(QtGui.QIcon("MolonavizIcon.png")) #?? modifier quand l'icone est pr??te
    mainWin = MainWindow()
    mainWin.showMaximized()

    # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
    thread = QtCore.QThread()
    my_receiver = MyReceiver(mainWin.queue)
    my_receiver.mysignal.connect(mainWin.appendText)
    my_receiver.moveToThread(thread)
    thread.started.connect(my_receiver.run)
    thread.start()

    sys.exit(app.exec_())