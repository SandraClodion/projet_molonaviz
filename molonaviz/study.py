from sensors import PressureSensor, Shaft, Thermometer
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import os, glob, shutil
import pandas as pd
from usefulfonctions import clean_filename, celsiusToKelvin
from point import Point

class Study(object):
    '''
    classdocs
    '''

    def __init__(self, name="", rootDir="", sensorDir=""):
        self.name = name
        self.rootDir = rootDir
        self.sensorDir = sensorDir
    
    def getRootDir(self):
        return self.rootDir
    
    def loadPressureSensors(self, sensorModel):
        sdir = os.path.join(self.sensorDir, "Pressure")
        files = list(filter(('.DS_Store').__ne__, os.listdir(sdir))) 
        files.sort()
        #permet de ne pas prendre en compte les fichier '.DS_Store' 
        for file in files:
            csv = os.path.join(sdir, file)  
            psensor = PressureSensor(name=file)
            psensor.loadPressureSensor(csv, sensorModel)
        
    def loadShafts(self, sensorModel):
        sdir = os.path.join(self.sensorDir, "Shafts")
        files = list(filter(('.DS_Store').__ne__, os.listdir(sdir))) 
        files.sort()
        #permet de ne pas prendre en compte les fichier '.DS_Store' 
        for file in files:
            csv = os.path.join(sdir, file)  
            shaft = Shaft(name=file)
            shaft.loadShaft(csv, sensorModel)  

    def loadThermometers(self, sensorModel):
        sdir = os.path.join(self.sensorDir, "Thermometers")
        files = list(filter(('.DS_Store').__ne__, os.listdir(sdir))) 
        files.sort()
        #permet de ne pas prendre en compte les fichier '.DS_Store' 
        for file in files:
            csv = os.path.join(sdir, file)  
            thermometer = Thermometer(name=file)
            thermometer.loadThermometer(csv, sensorModel)  

    def loadPoints(self, pointModel):
        rdir = self.rootDir
        dirs = [ name for name in os.listdir(rdir) if os.path.isdir(os.path.join(rdir, name)) ] #no file
        dirs = list(filter(('.DS_Store').__ne__, dirs)) 
        print(dirs)
        #permet de ne pas prendre en compte les fichier '.DS_Store' 
        for mydir in dirs:
            pointDir = os.path.join(self.rootDir, mydir)
            name = os.path.basename(pointDir)
            point = Point(name, pointDir)
            point.loadPointFromDir()
            point.loadPoint(pointModel)

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
    

    def addPoint(self, name, infofile, prawfile, trawfile, noticefile, configfile, pSensorModel):

        """
        Crée, remplit le répertoire du point et retourne l'objet point
        """
    
        pointDir = os.path.join(self.rootDir, name) #le dossier porte le nom du point
        
        df_info = pd.read_csv(infofile, sep=";", header=None, index_col=0)
        psensor = df_info.iloc[1].at[1]
        shaft = df_info.iloc[2].at[1]
        rivBed = float(df_info.iloc[5].at[1])
        deltaH = float(df_info.iloc[6].at[1])
        
        point = Point(name, pointDir, psensor, shaft, rivBed, deltaH)

        os.mkdir(pointDir)
        rawDataDir = os.path.join(pointDir, "raw_data")
        processedDataDir = os.path.join(pointDir, "processed_data")
        infoDataDir = os.path.join(pointDir, "info_data")

        os.mkdir(rawDataDir)
        shutil.copyfile(prawfile, os.path.join(rawDataDir, "raw_pressures.csv"))
        shutil.copyfile(trawfile, os.path.join(rawDataDir, "raw_temperatures.csv"))

        os.mkdir(infoDataDir)
        shutil.copyfile(infofile, os.path.join(infoDataDir, "info.csv"))
        shutil.copyfile(noticefile, os.path.join(infoDataDir, "notice.txt"))
        shutil.copyfile(configfile, os.path.join(infoDataDir, "config.png"))
        
        os.mkdir(processedDataDir)  
        point.processData(pSensorModel)

        return point



        


   