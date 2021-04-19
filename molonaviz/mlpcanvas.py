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


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, pdf, temp=False, parent=None, width=5, height=5, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, position=[0.15, 0.225, 0.75, 0.75])
        super(MplCanvas, self).__init__(self.fig)

        self.temp = temp
        self.pdf = pdf
        self.setTime()
        self.setCurves()

    def setTime(self):
        time = self.pdf[self.pdf.columns[0]].values.tolist()
        a = [datetime.strptime(t, '%y/%m/%d %H:%M:%S') for t in time]
        self.x = mdates.date2num(a)
        formatter = mdates.DateFormatter("%y/%m/%d %H:%M:%S")
        self.axes.xaxis.set_major_formatter(formatter)
        plt.setp(self.axes.get_xticklabels(), rotation = 15)
        #self.axes.set_xlabel("Dates") Inutile

    def setCurves(self):
        if self.temp:
            #On a 4 colonnes de températures
            for i in range(1,5):
                data = self.pdf[self.pdf.columns[i]].values.tolist()
                self.axes.plot(self.x, data, label=f"Capteur n°{i}")
            self.axes.legend(loc='best')
            self.axes.set_ylabel("Températures (K)")

        else:
            data = self.pdf[self.pdf.columns[1]].values.tolist()
            self.axes.plot(self.x, data)
            self.axes.set_ylabel("Pression différentielle (m)")

    def update_(self, new_pdf):
        self.axes.cla()
        self.pdf = new_pdf
        self.setTime()
        self.setCurves()
        self.draw()

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