import sys
import os
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QPixmap
import pandas as pd
from pandasmodel import PandasModel
from dialogcleanup import DialogCleanup
from dialogcompute import DialogCompute
from usefulfonctions import displayInfoMessage
from point import Point
from mplcanvas import MplCanvas
from compute import Compute
import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

From_WidgetPoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"widgetpoint.ui"))[0]

class WidgetPoint(QtWidgets.QWidget,From_WidgetPoint):
    
    def __init__(self, point, study):
        # Call constructor of parent classes
        super(WidgetPoint, self).__init__()
        QtWidgets.QWidget.__init__(self)
        
        self.setupUi(self)
        
        self.point = point
        self.study = study
        self.pointDir = self.point.getPointDir()
        self.directmodelDir = self.pointDir + "/results/direct_model_results"
        self.MCMCDir = self.pointDir + "/results/MCMC_results"
        self.directdepthsdir = self.directmodelDir + "/depths.csv"
        self.MCMCdepthsdir = self.MCMCDir + "/depths.csv"

        # Link every button to their function

        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonCleanUp.clicked.connect(self.cleanup)
        self.pushButtonCompute.clicked.connect(self.compute)
        self.checkBoxRaw_Data.stateChanged.connect(self.checkbox)
        self.setPressureAndTemperatureModels()
        self.setPlots()


    def setInfoTab(self):
        # Set the "Infos" tab
            #Installation
        self.labelSchema.setPixmap(QPixmap(self.pointDir + "/info_data" + "/config.png"))
            #Notice
        file = open(self.pointDir + "/info_data" + "/notice.txt")
        notice = file.read()
        self.plainTextEditNotice.setPlainText(notice)
        file.close()
            #Infos
        infoFile = self.pointDir + "/info_data" + "/info.csv"
        dfinfo = pd.read_csv(infoFile, sep=';', header=None)
        self.infosModel = PandasModel(dfinfo)
        self.tableViewInfos.setModel(self.infosModel)

    def setPressureAndTemperatureModels(self):
        # Set the Temperature and Pressure models
        self.currentdata = "processed"

        self.TemperatureDir = self.pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_temperatures.csv"
        self.PressureDir = self.pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_pressures.csv"

        self.dfpress = pd.read_csv(self.PressureDir)
        self.currentPressureModel = PandasModel(self.dfpress)
        self.tableViewPress.setModel(self.currentPressureModel)
        self.tableViewPress.resizeColumnsToContents()

        self.dftemp = pd.read_csv(self.TemperatureDir)
        self.currentTemperatureModel = PandasModel(self.dftemp)
        self.tableViewTemp.setModel(self.currentTemperatureModel)
        self.tableViewTemp.resizeColumnsToContents()

    def setWidgetInfos(self):
        pointName = self.point.getName()
        pointPressureSensor = self.point.getPressureSensor()
        pointShaft = self.point.getShaft()

        self.setWindowTitle(pointName)
        self.lineEditSensor.setText(pointPressureSensor)
        self.lineEditShaft.setText(pointShaft)

    def reset(self):
        self.point.processData(self.study.getSensorDir())
        #On actualise les modèles
        self.dfpress = pd.read_csv(self.PressureDir)
        self.dftemp = pd.read_csv(self.TemperatureDir)
        self.currentTemperatureModel.setData(self.dftemp)
        self.currentPressureModel.setData(self.dfpress)
        self.tableViewTemp.resizeColumnsToContents()
        self.tableViewPress.resizeColumnsToContents()
        self.graphpress.update_(self.dfpress)
        self.graphtemp.update_(self.dftemp)
        displayInfoMessage("Data successfully reset !")


    def cleanup(self):
        if self.currentdata == "raw":
            displayInfoMessage("Please clean-up your processed data.")
        else:
            dlg = DialogCleanup()
            res = dlg.exec_()
            if res == QtWidgets.QDialog.Accepted:
                script = dlg.getScript()
                self.dftemp, self.dfpress = self.point.cleanup(script, self.dftemp, self.dfpress)
                displayInfoMessage("Data successfully cleaned !")
                #On actualise les modèles
                self.currentTemperatureModel.setData(self.dftemp)
                self.currentPressureModel.setData(self.dfpress)
                self.tableViewTemp.resizeColumnsToContents()
                self.tableViewPress.resizeColumnsToContents()
                self.graphpress.update_(self.dfpress)
                self.graphtemp.update_(self.dftemp)

    def compute(self):
        
        sensorDir = self.study.getSensorDir()

        dlg = DialogCompute()
        res = dlg.exec()

        if res == 0 : 
            params, nb_cells = dlg.getInputDirectModel()
            compute = Compute(self.point)
            compute.computeDirectModel(params, nb_cells, sensorDir)
            new_dfwater = pd.read_csv(self.waterdir)
            new_dfsolvedtemp = pd.read_csv(self.solvedtempdir)
            new_dfadvective = pd.read_csv(self.advectivedir)
            new_dfconductive = pd.read_csv(self.conductivedir)
            new_dfdepths = pd.read_csv(self.directdepthsdir)

            if self.modeldirectiscomputed :
                self.graphwater.update_(new_dfwater)
                self.graphsolvedtemp.update_(new_dfsolvedtemp, new_dfdepths)
                self.graphAdvective.update_(new_dfadvective, new_dfdepths)
                self.graphConductive.update_(new_dfconductive, new_dfdepths)
            else :
                #Flux d'eau
                self.graphwater = MplCanvas(new_dfwater, "water flow")
                self.toolbarwater = NavigationToolbar(self.graphwater, self)
                self.vboxwatersimple.removeWidget(self.nomodellabel[0])
                self.vboxwatersimple.addWidget(self.graphwater)
                self.vboxwatersimple.addWidget(self.toolbarwater)
                #Frise de température
                self.graphsolvedtemp = MplCanvas(new_dfsolvedtemp, "frise", new_dfdepths)
                self.toolbarsolvedtemp = NavigationToolbar(self.graphsolvedtemp, self)
                self.vboxfrisetemp.removeWidget(self.nomodellabel[1])
                self.vboxfrisetemp.addWidget(self.graphsolvedtemp)
                self.vboxfrisetemp.addWidget(self.toolbarsolvedtemp)
                #Les flux d'énergie
                self.graphAdvective = MplCanvas(new_dfadvective, "frise", new_dfdepths)
                self.toolbarAdvective = NavigationToolbar(self.graphAdvective, self)
                self.vboxAdvective.removeWidget(self.nomodellabel[2])
                self.vboxAdvective.addWidget(self.graphAdvective)
                self.vboxConductive.addWidget(self.toolbarAdvective)

                self.graphConductive = MplCanvas(new_dfconductive, "frise", new_dfdepths)
                self.toolbarConductive = NavigationToolbar(self.graphConductive, self)
                self.vboxConductive.removeWidget(self.nomodellabel[3])
                self.vboxConductive.addWidget(self.graphConductive)
                self.vboxConductive.addWidget(self.toolbarConductive)

    
        if res == 1 :
            nb_iter, priors, nb_cells = dlg.getInputMCMC()
            compute = Compute(self.point)
            compute.computeMCMC(nb_iter, priors, nb_cells, sensorDir)
            # ajouter fonction plot
    
    def checkbox(self):

        if self.checkBoxRaw_Data.isChecked():
            self.currentdata = "raw"
        else :
            self.currentdata = "processed"

        self.TemperatureDir = self.pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_temperatures.csv"
        self.PressureDir = self.pointDir + "/" + self.currentdata + "_data" + "/" + self.currentdata + "_pressures.csv"

        if self.currentdata == "processed":
            self.dftemp = pd.read_csv(self.TemperatureDir)
            self.dfpress = pd.read_csv(self.PressureDir)
            self.currentTemperatureModel.setData(self.dftemp)
            self.currentPressureModel.setData(self.dfpress)
            self.tableViewTemp.resizeColumnsToContents()
            self.tableViewPress.resizeColumnsToContents()
        
        elif self.currentdata == "raw":
            self.dftemp = pd.read_csv(self.TemperatureDir)
            self.dfpress = pd.read_csv(self.PressureDir) #à modifier à reception des dataloggers de pression
            self.currentTemperatureModel.setData(self.dftemp)
            self.currentPressureModel.setData(self.dfpress)  
            self.tableViewTemp.resizeColumnsToContents()
            self.tableViewPress.resizeColumnsToContents()

    def setPlots(self):
        #La pression :
        self.graphpress = MplCanvas(self.dfpress, "pressure")
        self.toolbarPress = NavigationToolbar(self.graphpress, self)
        vbox = QtWidgets.QVBoxLayout()
        self.groupBoxPress.setLayout(vbox)
        vbox.addWidget(self.graphpress)
        vbox.addWidget(self.toolbarPress)
        #Les températures :
        self.graphtemp = MplCanvas(self.dftemp, "temperature")
        self.toolbarTemp = NavigationToolbar(self.graphtemp, self)
        vbox2 = QtWidgets.QVBoxLayout()
        self.groupBoxTemp.setLayout(vbox2)
        vbox2.addWidget(self.graphtemp)
        vbox2.addWidget(self.toolbarTemp)
        
        #Les résultats
        self.modeldirectiscomputed = len(os.listdir(self.directmodelDir) ) > 1
        self.MCMCiscomputed = len(os.listdir(self.MCMCDir)) > 1

        #Le flux d'eau:
        self.vboxwatersimple = QtWidgets.QVBoxLayout()
        self.groupBoxWaterSimple.setLayout(self.vboxwatersimple)
        self.vboxwaterMCMC = QtWidgets.QVBoxLayout()
        self.groupBoxWaterMCMC.setLayout(self.vboxwaterMCMC)
        self.waterdir = self.directmodelDir + "/solved_flows.csv"
        #La frise de température
        self.vboxfrisetemp = QtWidgets.QVBoxLayout()
        self.groupBoxFriseTemp.setLayout(self.vboxfrisetemp)
        self.solvedtempdir = self.directmodelDir + "/solved_temperatures.csv"
        #Les quantiles de température
        self.vboxTempMCMC = QtWidgets.QVBoxLayout()
        self.groupBoxTempMCMC.setLayout(self.vboxTempMCMC)
        self.tempmcmcdir = self.MCMCDir + "/MCMC_temps_quantile.csv"
        #Les flux d'énergie
        self.vboxAdvective = QtWidgets.QVBoxLayout()
        self.groupBoxAdvective.setLayout(self.vboxAdvective)
        self.advectivedir = self.directmodelDir + "/advective_flux.csv"
        self.vboxConductive = QtWidgets.QVBoxLayout()
        self.groupBoxConductive.setLayout(self.vboxConductive)
        self.conductivedir = self.directmodelDir + "/conductive_flux.csv"
        self.vboxTotEnergy = QtWidgets.QVBoxLayout()
        self.groupBoxTotEnergy.setLayout(self.vboxTotEnergy)
        #RAJOUTER SON DIRECTORY


        if self.modeldirectiscomputed:
            #Le flux d'eau:
            dfwater = pd.read_csv(self.waterdir)
            self.graphwater = MplCanvas(dfwater, "water flow")
            self.toolbarwater = NavigationToolbar(self.graphwater, self)
            self.vboxwatersimple.addWidget(self.graphwater)
            self.vboxwatersimple.addWidget(self.toolbarwater)

            #La frise de température
            dfsolvedtemp = pd.read_csv(self.solvedtempdir)
            depths = pd.read_csv(self.directdepthsdir)
            self.graphsolvedtemp = MplCanvas(dfsolvedtemp, "frise", depths)
            self.toolbarsolvedtemp = NavigationToolbar(self.graphsolvedtemp, self)
            self.vboxfrisetemp.addWidget(self.graphsolvedtemp)
            self.vboxfrisetemp.addWidget(self.toolbarsolvedtemp)

            #Les flux d'énergie
            dfadvective = pd.read_csv(self.advectivedir)
            self.graphAdvective = MplCanvas(dfadvective, "frise", depths)
            self.toolbarAdvective = NavigationToolbar(self.graphAdvective, self)
            self.vboxAdvective.addWidget(self.graphAdvective)
            self.vboxConductive.addWidget(self.toolbarAdvective)

            dfconductive = pd.read_csv(self.conductivedir)
            self.graphConductive = MplCanvas(dfconductive, "frise", depths)
            self.toolbarConductive = NavigationToolbar(self.graphConductive, self)
            self.vboxConductive.addWidget(self.graphConductive)
            self.vboxConductive.addWidget(self.toolbarConductive)

            #Énergie totale à rajouter

        else:
            self.nomodellabel = [QtWidgets.QLabel("Direct Model has not been computed yet")]*5
            self.vboxwatersimple.addWidget(self.nomodellabel[0])
            self.vboxfrisetemp.addWidget(self.nomodellabel[1])
            self.vboxAdvective.addWidget(self.nomodellabel[2])
            self.vboxConductive.addWidget(self.nomodellabel[3])

        if self.MCMCiscomputed:
            pass
        else:
            self.noMCMClabel = QtWidgets.QLabel("MCMC has not been computed yet")
            self.vboxwaterMCMC.addWidget(self.noMCMClabel)
            


""" 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WidgetPoint()
    mainWin.show()
    sys.exit(app.exec_())
"""