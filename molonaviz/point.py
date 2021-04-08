import os, glob
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from to_filename import clean_filename

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

    def loadPointFromText(self, pointDir):
        """
        Le fichier texte doit se présenter sous la forme suivante :
        SensorName: Nom du capteur de pression associé au point
        Pour le moment la méthode renvoie le nom du capteur associé au point
        que l'on souhaite charger
        """
        os.chdir(pointDir)
        textFile = glob.glob("*.txt")[0]
        with open(textFile, 'r') as pointText:
            lines = pointText.read().splitlines() 
            nameLine = lines[0]
            sensorNameLine = lines[1]
            name = nameLine.split(' ', 1)[1]
            sensorName = sensorNameLine.split(' ', 1)[1]
        return name, sensorName
    
    def loadPoint(self, pointModel):
        
        item = QtGui.QStandardItem(self.name)
        item.setData(self, QtCore.Qt.UserRole)
        pointModel.appendRow(item)    

        

    
