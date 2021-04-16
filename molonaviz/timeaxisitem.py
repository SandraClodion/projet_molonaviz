from PyQt5 import QtWidgets, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from datetime import datetime

"""
dftemp = pd.read_csv("/Users/charlottedemaillynesle/Desktop/ÉTUDE QUI VA MARCHER/Point 1/raw_data/raw_temperatures.csv", index_col=0)
#print(dftemp)
Timestr = list(dftemp.index)
Timeint = []
for date in Timestr:
    Timeint.append(time_convert(date))
Tempcapteur1 = dftemp[dftemp.columns[0]].values.tolist()

#VOIR https://stackoverflow.com/questions/49046931/how-can-i-use-dateaxisitem-of-pyqtgraph
"""

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]
"""
list_x = Timeint

list_y = Tempcapteur1

app = QtGui.QApplication([])


date_axis = TimeAxisItem(orientation='bottom') #dans la fenêtre wdgt
graph = pg.PlotWidget(axisItems = {'bottom': date_axis}) # OK

graph.plot(x=[x.timestamp() for x in list_x], y=list_y, pen=None, symbol='o')
graph.show()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
"""