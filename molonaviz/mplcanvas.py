import sys
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
import pandas as pd
from datetime import datetime

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np
from matplotlib.ticker import MaxNLocator


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, pdf, datatype, depths=None, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.fig.tight_layout(h_pad=5, pad=5)
        self.pdf = pdf
        self.datatype = datatype
        self.depths = depths
        self.setTime()
        if self.datatype == "pressure" or self.datatype == "temperature" or self.datatype == "water flow":
            self.setCurves()
        elif self.datatype == "frise":
            self.setFrises()

    def setTime(self):
        time = self.pdf[self.pdf.columns[0]].values.tolist()
        #print(time)
        a = [datetime.strptime(t, '%y/%m/%d %H:%M:%S') for t in time]
        self.x = mdates.date2num(a)
        formatter = mdates.DateFormatter("%y/%m/%d %H:%M:%S")
        self.axes.xaxis.set_major_formatter(formatter)
        self.axes.xaxis.set_major_locator(MaxNLocator(4))
        plt.setp(self.axes.get_xticklabels(), rotation = 15)
        #self.axes.set_xlabel("Dates") Inutile

    def setCurves(self):
        if self.datatype == "temperature":
            #On a 4 colonnes de températures
            for i in range(1,5):
                data = self.pdf[self.pdf.columns[i]].values.tolist()
                self.axes.plot(self.x, data, label=f"Capteur n°{i}")
            self.axes.legend(loc='best')
            self.axes.set_ylabel("Températures (K)")

        else :
            data = self.pdf[self.pdf.columns[1]].values.tolist()
            self.axes.plot(self.x, data)
            if self.datatype == "pressure":
                self.axes.set_ylabel("Pression différentielle (m)")
            elif self.datatype == "water flow":
                self.axes.set_ylabel("Débit d'eau (m/s)")
    
    def setFrises(self):
        profils = self.pdf.to_numpy()
        profils = profils[:,1:].astype(np.float)
        depths = self.depths[self.depths.columns[0]].values.tolist()
        image = self.axes.imshow(profils, cmap=cm.Spectral_r, aspect="auto", extent=[self.x[0], self.x[-1], float(depths[-1]), float(depths[0])], data="float")
        self.axes.xaxis_date()
        plt.colorbar(image, ax=self.axes)

    def update_(self, new_pdf, depths=None):
        self.axes.cla()
        self.pdf = new_pdf
        self.depths = depths
        self.setTime()
        if self.datatype == "pressure" or self.datatype == "temperature" or self.datatype == "water flow":
            self.setCurves()
        elif self.datatype == "frise":
            self.setFrises()

"""
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object, 
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(pd.read_csv("/Users/charlottedemaillynesle/Desktop/Cours Mines/2A/MOLONARI/Interface/projet_molonaviz/EXEMPLES FICHIERS/Measures/Point001/Point001_T_Measures.csv"), temp=True, width=5, height=4, dpi=100)
        self.setCentralWidget(sc)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
""" 