from sensor import Sensor
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