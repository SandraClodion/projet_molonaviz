import os, glob, shutil
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from usefulfonctions import clean_filename
#from widgetpoint import WidgetPoint
import pandas as pd
from pandasmodel import PandasModel

class Point(object):
    
    '''
    classdocs
    '''

    def __init__(self, name="", pointDir="", sensor=""):
        self.name = name
        self.pointDir = pointDir
        self.sensor = sensor #nom du capteur de pression associé

    def savePointToText(self):
        pathPointText = os.path.join(self.pointDir, f"{clean_filename(self.name)}.txt")
        with open(pathPointText, "w") as pointText :
            pointText.write(f"Name: {self.name} \n")
            pointText.write(f"SensorName: {self.sensor}")

    def loadPointFromText(self):
        """
        Le fichier texte doit se présenter sous la forme suivante :
        SensorName: Nom du capteur de pression associé au point
        """
        os.chdir(self.pointDir)
        textFile = glob.glob("*.txt")[0]
        with open(textFile, 'r') as pointText:
            lines = pointText.read().splitlines() 
            nameLine = lines[0]
            sensorNameLine = lines[1]
            name = nameLine.split(' ', 1)[1]
            sensorName = sensorNameLine.split(' ', 1)[1]
        self.name = name
        self.sensor = sensorName
        
    def loadPoint(self, pointModel): 
        item = QtGui.QStandardItem(self.name)
        item.setData(self, QtCore.Qt.UserRole)
        pointModel.appendRow(item)
    
    def delete(self):
        shutil.rmtree(self.pointDir)

    #def openWidget(self):
        #self.wdgpoint = WidgetPoint(self.name, self.pointDir, self.sensor)
        #self.wdgpoint.show()

    #def closeWidget(self):
        #self.wdgpoint.close()

    def temperatureModel(self, pointDir):
        self.tempcsv = pointDir + "/processed_data/processed_temperatures.csv"
        pdtemp = pd.read_csv(self.tempcsv)
        #print(pdtemp)
        temperatureModel = PandasModel(pdtemp)
        return(temperatureModel)

    def pressureModel(self, pointDir):
        self.presscsv = pointDir + "/processed_data/processed_pressures.csv"
        pdpress = pd.read_csv(self.presscsv)
        pressureModel = PandasModel(pdpress)
        return(pressureModel)