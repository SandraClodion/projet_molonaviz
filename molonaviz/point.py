import os, glob, shutil, sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import pandas as pd
from numpy import NaN
from usefulfonctions import clean_filename, celsiusToKelvin
from sensors import PressureSensor, Shaft, Thermometer
from datetime import datetime
from pyheatmy import *

class Point(object):
    
    '''
    classdocs
    '''

    def __init__(self, name="", pointDir="", psensor="", shaft="", rivBed=NaN, deltaH=NaN):
        self.name = name
        self.pointDir = pointDir
        self.psensor = psensor #nom du capteur de pression associé
        self.shaft = shaft #nom de la tige de température associée
        self.rivBed = rivBed
        self.deltaH = deltaH
        self.dftemp = pd.DataFrame()
        self.dfpress = pd.DataFrame()
    
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
        self.rivBed = float(df.iloc[5].at[1])
        self.deltaH = float(df.iloc[6].at[1])
        self.dftemp = pd.read_csv(tempcsv)
        self.dfpress = pd.read_csv(presscsv)
        

    def loadPoint(self, pointModel): 
        item = QtGui.QStandardItem(self.name)
        item.setData(self, QtCore.Qt.UserRole)
        pointModel.appendRow(item)
    
    def delete(self):
        shutil.rmtree(self.pointDir)

    def processData(self, sensorDir):

        # ajout vérification des dates à faire
        
        trawfile = os.path.join(self.pointDir, "raw_data", "raw_temperatures.csv")
        tprocessedfile = os.path.join(self.pointDir, "processed_data", "processed_temperatures.csv")
        pprocessedfile = os.path.join(self.pointDir, "processed_data", "processed_pressures.csv")
        celsiusToKelvin(trawfile, tprocessedfile)
        
        prawfile = os.path.join(self.pointDir, "raw_data", "raw_pressures.csv")
        
        #psensor = pSensorModel.findItems(self.psensor)[0].data(QtCore.Qt.UserRole)
        psensor = PressureSensor(self.psensor)
        info_csv = os.path.join(sensorDir, 'Pressure', f'{self.psensor}.csv')
        psensor.setPressureSensorFromFile(info_csv)
        psensor.tensionToPressure(prawfile, pprocessedfile)

        self.dftemp = pd.read_csv(tprocessedfile)
        self.dfpress = pd.read_csv(pprocessedfile)

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

    
    def setColumn(self, sensorDir):

        df = self.dftemp
        temperatures = df.drop(columns=df.columns[0], axis=1).to_numpy()
        df = self.dfpress
        pressures_and_temperatures = list(df.drop(columns=df.columns[0], axis=1).itertuples(index=False, name=None))

        # Assuming times are matching
        times = df[df.columns[0]].values.tolist() 
        times = [datetime.strptime(t, '%y/%m/%d %H:%M:%S') for t in times]

        # Getting sensors info

        psensor = PressureSensor(self.psensor)
        infofile = os.path.join(sensorDir, 'Pressure', f'{self.psensor}.csv')
        psensor.setPressureSensorFromFile(infofile)
        
        shaft = Shaft(self.shaft)
        infofile = os.path.join(sensorDir, 'Shafts', f'{self.shaft}.csv')
        shaft.setShaftFromFile(infofile)

        thermometerName = shaft.getThermometer()
        thermometer = Thermometer(thermometerName)
        infofile = os.path.join(sensorDir, 'Thermometers', f'{thermometerName}.csv')
        thermometer.setThermometerFromFile(infofile)

        # Setting dictionnary

        col_dict = {
	        "river_bed": self.rivBed, 
            "depth_sensors": shaft.getDepths(),
	        "offset": self.deltaH,
            "dH_measures": list(zip(times, pressures_and_temperatures)),
	        "T_measures": list(zip(times, temperatures)),
            "sigma_meas_P": psensor.getSigma(),
            "sigma_meas_T": thermometer.getSigma()
            }
        
        col = Column.from_dict(col_dict)
        
        return col

