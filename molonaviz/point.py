import os, glob, shutil, sys
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
        self.tprocessedfile = os.path.join(self.pointDir, "processed_data", "processed_temperatures.csv")
        self.pprocessedfile = os.path.join(self.pointDir, "processed_data", "processed_pressures.csv")
    
    def getName(self):
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
        self.dftemp = pd.read_csv(tempcsv)
        self.dfpress = pd.read_csv(presscsv) #à modifier à réception des dataloggers

    def loadPoint(self, pointModel): 
        item = QtGui.QStandardItem(self.name)
        item.setData(self, QtCore.Qt.UserRole)
        pointModel.appendRow(item)
    
    def delete(self):
        shutil.rmtree(self.pointDir)

    def processData(self, pSensorModel):
        
        trawfile = os.path.join(self.pointDir, "raw_data", "raw_temperatures.csv")
        celsiusToKelvin(trawfile, self.tprocessedfile)
        
        prawfile = os.path.join(self.pointDir, "raw_data", "raw_pressures.csv")
        
        psensor = pSensorModel.findItems(self.psensor)[0].data(QtCore.Qt.UserRole)
        psensor.tensionToPressure(prawfile, self.pprocessedfile)

        self.dftemp = pd.read_csv(self.tprocessedfile)
        self.dfpress = pd.read_csv(self.pprocessedfile)

    def cleanup(self, script, dft, dfp):

        scriptDir = self.pointDir + "/script.py"
        sys.path.append(self.pointDir)
        with open(scriptDir, "w") as f:
            f.write(script)
            f.close()

        from script import fonction
        new_dft, new_dfp = fonction(dft, dfp)
        os.remove(scriptDir)

        #On réécrit les csv:
        os.remove(self.tprocessedfile)
        os.remove(self.pprocessedfile)
        new_dft.to_csv(self.tprocessedfile, index=False)
        new_dfp.to_csv(self.pprocessedfile, index=False)

        return(new_dft, new_dfp)
