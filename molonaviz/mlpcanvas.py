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

    def __init__(self, pdf, temp=False, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

        time = pdf[pdf.columns[0]].values.tolist()
        a = [datetime.strptime(t, '%y/%m/%d %H:%M:%S') for t in time]

        x = mdates.date2num(a)
        formatter = mdates.DateFormatter("%y/%m/%d %H:%M:%S")
        self.axes.xaxis.set_major_formatter(formatter)
        plt.setp(self.axes.get_xticklabels(), rotation = 15)

        if temp:
            #On a 4 colonnes de températures
            for i in range(4):
                data = pdf[pdf.columns[i+1]].values.tolist()
                self.axes.plot(x, data)
        else:
            data = pdf[pdf.columns[1]].values.tolist()
            self.axes.plot(x, data)

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