import os, glob, shutil
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from usefulfonctions import clean_filename
from widgetpoint import WidgetPoint
import pandas as pd
from numpy import NaN
#from pandasmodel import PandasModel

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

    def openWidget(self):
        self.wdgpoint = WidgetPoint(self.pointDir)
        self.wdgpoint.setWidgetInfos(self.name, self.psensor)
        # à terme, à remplacer par self.wdgpoint.setWidgetInfos(self.dataframeinfos) ?
        #self.wdgpoint.setCurrentTemperatureModel(self.dftemp)
        #self.wdgpoint.setCurrentPressureModel(self.dfpress)
        self.wdgpoint.show()

    def closeWidget(self):
        self.wdgpoint.close()