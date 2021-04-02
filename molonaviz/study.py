from sensor import Sensor
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import os

class Study(object):
    '''
    classdocs
    '''

    def __init__(self, name, rootDir, sensorDir):
        self.name = name
        self.rootDir = rootDir
        self.sensorDir = sensorDir
    
    def loadSensor(self, sensorName):
        sensor = Sensor(sensorName)
        pathCalib = os.path.join(self.sensorDir, sensorName, "calibfit_{}.csv".format(sensorName))
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
            item.appendRow(QtGui.QStandardItem("intercept = {:.2f}".format(float(sensor.intercept))))
            item.appendRow(QtGui.QStandardItem("dudh = {:.2f}".format(float(sensor.dudh))))
            item.appendRow(QtGui.QStandardItem("dudt = {:.2f}".format(float(sensor.dudt))))
    