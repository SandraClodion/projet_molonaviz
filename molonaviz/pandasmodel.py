import sys
from PyQt5 import QtWidgets, uic, QtCore
import pandas as pd
Qt = QtCore.Qt


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, datadir, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        pdtemp = pd.read_csv(datadir)
        self._data = pdtemp

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size
    

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.iloc[index.row()][index.column()]))
        return QtCore.QVariant()
    
    def getpdData(self):
        return(self._data)



if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    view = QtWidgets.QTableView()
    model = point.temperatureModel("/Users/charlottedemaillynesle/Desktop/Étude 1/Point 01")
    view.setModel(model)

    view.show()
    sys.exit(application.exec_())