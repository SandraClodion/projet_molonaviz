from sensor import Sensor
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import os, glob, shutil
import pandas as pd
from usefulfonctions import clean_filename, celsiusToKelvin
from point import Point
from sensor import Sensor

class Study(object):
    '''
    classdocs
    '''

    def __init__(self, name="", rootDir="", sensorDir=""):
        self.name = name
        self.rootDir = rootDir
        self.sensorDir = sensorDir

    
    def loadSensor(self, sensorName):
        sensor = Sensor(sensorName)
        pathCalib = os.path.join(self.sensorDir, sensorName, f"calibfit_{sensorName}.csv")
        file = open(pathCalib,"r")
        lines = file.readlines()
        for line in lines:
            if line.split(';')[0].strip() == "Intercept":
                sensor.intercept = float(line.split(';')[1].strip())
            if line.split(';')[0].strip() == "dU/dH":
                sensor.dudh = float(line.split(';')[1].strip())
            if line.split(';')[0].strip() == "dU/dT":
                sensor.dudt = float(line.split(';')[1].strip())
        return sensor
    
    def loadSensors(self, sensorModel):
        sdir = self.sensorDir
        dirs = list(filter(('.DS_Store').__ne__, os.listdir(sdir))) 
        #permet de ne pas prendre en compte les fichier '.DS_Store' 
        for mydir in dirs:
            sensor = self.loadSensor(mydir)
            
            item = QtGui.QStandardItem(mydir)
            item.setData(sensor, QtCore.Qt.UserRole)
            
            sensorModel.appendRow(item)
            item.appendRow(QtGui.QStandardItem(f"intercept = {float(sensor.intercept):.2f}"))
            item.appendRow(QtGui.QStandardItem(f"dudh = {float(sensor.dudh):.2f}"))
            item.appendRow(QtGui.QStandardItem(f"dudt = {float(sensor.dudt):.2f}"))
        
        #newsensor = sensorModel.findItems("p508")[0].data(QtCore.Qt.UserRole)
        #print(newsensor.intercept)

    def saveStudyToText(self):
        pathStudyText = os.path.join(self.rootDir, f"{clean_filename(self.name)}.txt")
        with open(pathStudyText, "w") as studyText :
            studyText.write(f"Name: {self.name} \n")
            studyText.write(f"SensorsDirectory: {self.sensorDir}")

    def loadStudyFromText(self):
        """
        Le fichier texte doit se présenter sous la forme suivante :
        Name: Nom de l'étude
        SensorsDir: Chemin d'accès du dossier capteurs
        """
        os.chdir(self.rootDir)
        textFile = glob.glob("*.txt")[0]
        with open(textFile, 'r') as studyText:
            lines = studyText.read().splitlines() 
            nameLine = lines[0]
            sensorDirLine = lines[1]
            name = nameLine.split(' ', 1)[1]
            sensorDir = sensorDirLine.split(' ', 1)[1]
        self.name = name
        self.sensorDir = sensorDir
    

    def addPoint(self, name, sensorname, prawfile, trawfile, sensor):
    
        pointDir = os.path.join(self.rootDir, name) #le dossier porte le nom du point

        point = Point(name, pointDir, sensorname)

        os.mkdir(pointDir)
        rawDataDir = os.path.join(pointDir, "raw_data")
        processedDataDir = os.path.join(pointDir, "processed_data")

        os.mkdir(rawDataDir)
        shutil.copyfile(prawfile, os.path.join(rawDataDir, "raw_pressures.csv"))
        shutil.copyfile(trawfile, os.path.join(rawDataDir, "raw_temperatures.csv"))

        os.mkdir(processedDataDir)
        
        tprocessedfile = os.path.join(processedDataDir, "processed_temperatures.csv")
        celsiusToKelvin(trawfile, tprocessedfile)

        pprocessedfile = os.path.join(processedDataDir, "processed_pressures.csv")
        sensor.tensionToPressure(prawfile, pprocessedfile)

        return point




        


   