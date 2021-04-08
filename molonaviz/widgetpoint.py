import sys
import os
from PyQt5 import QtWidgets, uic
from point import Point, loadPointFromText

From_WidgetPoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"widgetpoint.ui"))[0]

class WidgetPoint(QtWidgets.QWidget,From_WidgetPoint):
    
    def __init__(self, pointDir):
        # Call constructor of parent classes
        super(WidgetPoint, self).__init__()
        QtWidgets.QWidget.__init__(self)
        
        self.setupUi(self)
        name, sensorName = loadPointFromText(pointDir)
        self.point= Point(name, pointDir, sensorName)

        self.setWindowTitle(name)

        self.lineEditSensor.setText(sensorName)

        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonCleanUp.clicked.connect(self.cleanup)
        self.pushButtonCompute.clicked.connect(self.compute)
        self.checkBoxRaw_Data.stateChanged.connect(self.checkbox)


    def reset(self):
        ## À compléter
        print("reset")

    def cleanup(self):
        ## À compléter
        print("cleanup")

    def compute(self):
        ## À compléter
        print("compute")
    
    def checkbox(self):
        ## À compléter
        print("checkbox")

 
    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WidgetPoint()
    mainWin.show()
    sys.exit(app.exec_())