from sensor import Sensor
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import os, glob
from to_filename import clean_filename

class Study(object):
    '''
    classdocs
    '''

    def __init__(self, name="", rootDir="", sensorDir=""):
        self.name = name
        self.rootDir = rootDir
        self.sensorDir = sensorDir
    
    def getStudyAttributes(self):
        dico = {"name": self.name, "rootDir": self.rootDir, "sensorDir": self.sensorDir}
        return dico
    
    def loadSensor(self, sensorName):
        sensor = Sensor(sensorName)
        pathCalib = os.path.join(self.sensorDir, sensorName, f"calibfit_{sensorName}.csv")
        file = open(pathCalib,"r")
        lines = file.readlines()
        for line in lines:
            if line.split(';')[0].strip() == "Intercept":
                sensor.intercept = line.split(';')[1].strip()
            if line.split(';')[0].strip() == "dU/dH":
                sensor.dudh = line.split(';')[1].strip()
            if line.split(';')[0].strip() == "dU/dT":
                sensor.dudt = line.split(';')[1].strip()
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

    def loadStudyFromText(self, rootDir):
        """
        Le fichier texte doit se présenter sous la forme suivante :
        Name: Nom de l'étude
        SensorsDir: Chemin d'accès du dossier capteurs
        Pour le moment la méthode renvoie le nom de l'étude qu'on souhaite charger 
        et le chemin d'accès vers le dossier des capteurs utilisés pour l'étude
        """
        os.chdir(rootDir)
        textFile = glob.glob("*.txt")[0]
        with open(textFile, 'r') as studyText:
            lines = studyText.read().splitlines() 
            nameLine = lines[0]
            sensorDirLine = lines[1]
            name = nameLine.split(' ', 1)[1]
            sensorDir = sensorDirLine.split(' ', 1)[1]
        return name, sensorDir




        


   