from sensor import Sensor
from point import Point
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
    
   # def loadPoint(self, pointName):
        #point = Point(pointName)
        #pathPressure = os.path.join(self.rootDir, pointname, f"")
        # à compléter
        #return point