import os, glob, shutil
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import pandas as pd
from numpy import NaN
from usefulfonctions import clean_filename, celsiusToKelvin
from sensors import PressureSensor

class Point(object):
    
    '''
    classdocs
    '''

    def __init__(self, name="", pointDir="", psensor="", shaft="", deltaH=NaN):
        self.name = name
        self.pointDir = pointDir
        self.psensor = psensor #nom du capteur de pression associé
        self.shaft = shaft #nom de la tige de température associée
        self.deltaH = deltaH
        self.dftemp = pd.DataFrame()
        self.dfpress = pd.DataFrame()
    
    def getName():
        return self.name

    def getPointDir(self):
        return self.pointDir

    def getPressureSensor(self):
        return self.psensor

    def getShaft(self):
        return self.shaft    

    def loadPointFromDir(self):
        
        tempcsv = os.path.join(self.pointDir, "processed_data", "processed_temperatures.csv")
        presscsv = os.path.join(self.pointDir, "processed_data", "processed_pressures.csv")
        infocsv = os.path.join(self.pointDir, "info_data", "info.csv")
        
        df = pd.read_csv(infocsv, sep=";", header=None, index_col=0)
        #self.oldName = df.iloc[0].at[1] 
        self.psensor = df.iloc[1].at[1]
        self.shaft = df.iloc[2].at[1]
        self.deltaH = float(df.iloc[6].at[1])
        self.dftemp = pd.read_csv(tempcsv, sep=';')
        self.dfpress = pd.read_csv(presscsv, sep=';')

    def loadPoint(self, pointModel): 
        item = QtGui.QStandardItem(self.name)
        item.setData(self, QtCore.Qt.UserRole)
        pointModel.appendRow(item)
    
    def delete(self):
        shutil.rmtree(self.pointDir)

    def processData(self, pSensorModel):
        
        trawfile = os.path.join(self.pointDir, "raw_data", "raw_temperatures.csv")
        tprocessedfile = os.path.join(self.pointDir, "processed_data", "processed_temperatures.csv")
        celsiusToKelvin(trawfile, tprocessedfile)
        
        prawfile = os.path.join(self.pointDir, "raw_data", "raw_pressures.csv")
        pprocessedfile = os.path.join(self.pointDir, "processed_data", "processed_pressures.csv")
        
        psensor = pSensorModel.findItems(self.psensor)[0].data(QtCore.Qt.UserRole)
        psensor.tensionToPressure(prawfile, pprocessedfile)

        self.dftemp = pd.read_csv(tprocessedfile, sep=';')
        self.dfpress = pd.read_csv(pprocessedfile, sep=';')
