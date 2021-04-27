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
from study import Study
from mplcanvas import MplCanvas, MplCanvasHisto, MplCanvaHeatFluxes
from compute import Compute
import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from usefulfonctions import clearLayout

From_WidgetPoint = uic.loadUiType(os.path.join(os.path.dirname(__file__),"widgetpoint.ui"))[0]

class WidgetPoint(QtWidgets.QWidget,From_WidgetPoint):
    
    def __init__(self, point: Point, study: Study):
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

        self.directmodeliscomputed = len(os.listdir(self.directmodelDir) ) > 1
        self.MCMCiscomputed = len(os.listdir(self.MCMCDir)) > 1

        # Link every button to their function

        self.pushButtonReset.clicked.connect(self.reset)
        self.pushButtonCleanUp.clicked.connect(self.cleanup)
        self.pushButtonCompute.clicked.connect(self.compute)
        self.checkBoxRaw_Data.stateChanged.connect(self.checkbox)
        
        self.setPressureAndTemperatureModels()
        self.setDataPlots()
        self.setResultsPlots()


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
        self.tableViewInfos.horizontalHeader().hide()
        self.tableViewInfos.verticalHeader().hide()
        self.tableViewInfos.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableViewInfos.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

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


    def reset(self):
        print("Resetting data...")
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
        print("Data successfully reset !")


    def cleanup(self):
        if self.currentdata == "raw":
            print("Please clean-up your processed data.")
        else:
            dlg = DialogCleanup()
            res = dlg.exec_()
            if res == QtWidgets.QDialog.Accepted:
                script = dlg.getScript()
                print("Cleaning data...")
                self.dftemp, self.dfpress = self.point.cleanup(script, self.dftemp, self.dfpress)
                print("Data successfully cleaned !...")
                
                #On actualise les modèles
                self.currentTemperatureModel.setData(self.dftemp)
                self.currentPressureModel.setData(self.dfpress)
                self.tableViewTemp.resizeColumnsToContents()
                self.tableViewPress.resizeColumnsToContents()
                self.graphpress.update_(self.dfpress)
                self.graphtemp.update_(self.dftemp)
                print("Plots successfully updated")
    

    def compute(self):
        
        sensorDir = self.study.getSensorDir()

        dlg = DialogCompute()
        res = dlg.exec()

        if res == 0 : #Direct Model
            params, nb_cells = dlg.getInputDirectModel()
            compute = Compute(self.point)
            compute.computeDirectModel(params, nb_cells, sensorDir)

            self.setDataFrames('DirectModel')

            if self.directmodeliscomputed :
                print('Direct Model is computed')
                self.graphwaterdirect.update_(self.dfwater)
                self.graphsolvedtempdirect.update_(self.dfsolvedtemp, self.dfdepths)
                self.graphintertempdirect.update_(self.dfintertemp)
                self.graphfluxesdirect.update_(self.dfadvec, self.dfconduc, self.dftot, self.dfdepths)
                self.parapluies.update_(self.dfsolvedtemp, self.dfdepths)
                print("Model successfully updated !")

            else :

                #Flux d'eau
                clearLayout(self.vboxwaterdirect)
                self.plotWaterFlowsDirect(self.dfwater)

                #Flux d'énergie
                clearLayout(self.vboxfluxesdirect)
                self.plotFriseHeatFluxesDirect(self.dfadvec, self.dfconduc, self.dftot, self.dfdepths)

                #Frise de température
                clearLayout(self.vboxfrisetempdirect)
                self.plotFriseTempDirect(self.dfsolvedtemp, self.dfdepths)
                #Parapluies
                clearLayout(self.vboxsolvedtempdirect)
                self.plotParapluies(self.dfsolvedtemp, self.dfdepths)

                #Température à l'interface
                clearLayout(self.vboxintertempdirect)
                self.plotInterfaceTempDirect(self.dfintertemp)

                self.directmodeliscomputed = True
                print("Model successfully created !")

    
        if res == 1 : #MCMC
            nb_iter, priors, nb_cells = dlg.getInputMCMC()
            compute = Compute(self.point)
            compute.computeMCMC(nb_iter, priors, nb_cells, sensorDir)

            self.setDataFrames('MCMC')

            if self.MCMCiscomputed :
                print('MCMC is computed')
                self.graphwaterMCMC.update_(self.dfwater)
                self.graphsolvedtempMCMC.update_(self.dfsolvedtemp, self.dfdepths)
                self.graphintertempMCMC.update_(self.dfintertemp)
                self.graphfluxesMCMC.update_(self.dfadvec, self.dfconduc, self.dftot, self.dfdepths)
                self.histos.update_(self.dfallparams)
                self.parapluiesMCMC.update_(self.dfsolvedtemp, self.dfdepths)
                self.BestParamsModel.setData(self.dfbestparams)
                print("Model successfully updated !")

            else :

                #Flux d'eau
                clearLayout(self.vboxwaterMCMC)
                self.plotWaterFlowsMCMC(self.dfwater)

                #Flux d'énergie
                clearLayout(self.vboxfluxesMCMC)
                self.plotFriseHeatFluxesMCMC(self.dfadvec, self.dfconduc, self.dftot, self.dfdepths)

                #Frise de température
                clearLayout(self.vboxfrisetempMCMC)
                self.plotFriseTempMCMC(self.dfsolvedtemp, self.dfdepths)
                #Parapluies
                clearLayout(self.vboxsolvedtempMCMC)
                self.plotParapluiesMCMC(self.dfsolvedtemp, self.dfdepths)
                #Température à l'interface
                clearLayout(self.vboxintertempMCMC)
                self.plotInterfaceTempMCMC(self.dfintertemp)

                #Histogrammes
                clearLayout(self.vboxhistos)
                self.histos(self.dfallparams)
                #Les meilleurs paramètres
                self.setBestParamsModel(self.dfbestparams)

                self.MCMCiscomputed = True
                print("Model successfully created !")


    def setDataPlots(self):

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
    

    def setResultsPlots(self):

        ## Création des layouts

        #Le flux d'eau:
        self.vboxwaterdirect = QtWidgets.QVBoxLayout()
        self.groupBoxWaterDirect.setLayout(self.vboxwaterdirect)
        self.vboxwaterMCMC = QtWidgets.QVBoxLayout()
        self.groupBoxWaterMCMC.setLayout(self.vboxwaterMCMC)
        
        # Le reste directement dans le fichier .ui (permet de voir les 2 méthodes)

        if self.directmodeliscomputed:

            self.setDataFrames('DirectModel')
            
            #Le flux d'eau
            self.plotWaterFlowsDirect(self.dfwater)

            #Les flux d'énergie
            self.plotFriseHeatFluxesDirect(self.dfadvec, self.dfconduc, self.dftot, self.dfdepths)

            #La frise de température
            self.plotFriseTempDirect(self.dfsolvedtemp, self.dfdepths)
            #Les parapluies
            self.plotParapluies(self.dfsolvedtemp, self.dfdepths)

            #La température à l'interface
            self.plotInterfaceTempDirect(self.dfintertemp)

            #Le reste à rajouter plus tard

        else:
            self.vboxwaterdirect.addWidget(QtWidgets.QLabel("Direct Model has not been computed yet"))
            self.vboxfluxesdirect.addWidget(QtWidgets.QLabel("Direct Model has not been computed yet"))
            self.vboxfrisetempdirect.addWidget(QtWidgets.QLabel("Direct Model has not been computed yet"))
            self.vboxintertempdirect.addWidget(QtWidgets.QLabel("Direct Model has not been computed yet"))
            self.vboxsolvedtempdirect.addWidget(QtWidgets.QLabel("Direct Model has not been computed yet"))

        if self.MCMCiscomputed:

            self.setDataFrames('MCMC')

            #Le flux d'eau
            self.plotWaterFlowsMCMC(self.dfwater)

            #Les flux d'énergie
            self.plotFriseHeatFluxesMCMC(self.dfadvec, self.dfconduc, self.dftot, self.dfdepths)

            #La frise de température
            self.plotFriseTempMCMC(self.dfsolvedtemp, self.dfdepths)
            #Les parapluies
            self.plotParapluiesMCMC(self.dfsolvedtemp, self.dfdepths)

            #La température à l'interface
            self.plotInterfaceTempMCMC(self.dfintertemp)

            #Les histogrammes
            self.histos(self.dfallparams)
            #Les meilleurs paramètres
            self.setBestParamsModel(self.dfbestparams)

        else:
            self.vboxwaterMCMC.addWidget(QtWidgets.QLabel("MCMC has not been computed yet"))
            self.vboxfluxesMCMC.addWidget(QtWidgets.QLabel("MCMC has not been computed yet"))
            self.vboxfrisetempMCMC.addWidget(QtWidgets.QLabel("MCMC has not been computed yet"))
            self.vboxintertempMCMC.addWidget(QtWidgets.QLabel("MCMC has not been computed yet"))
            self.vboxhistos.addWidget(QtWidgets.QLabel("MCMC has not been computed yet"))
            self.vboxsolvedtempMCMC.addWidget(QtWidgets.QLabel("MCMC has not been computed yet"))
    
        

    def setDataFrames(self, mode:str):

        if mode == 'DirectModel':
            self.dfwater = pd.read_csv(self.directmodelDir + "/solved_flows.csv")
            self.dfdepths = pd.read_csv(self.directdepthsdir)
            self.dfsolvedtemp = pd.read_csv(self.directmodelDir + "/solved_temperatures.csv")
            self.dfintertemp = self.dfsolvedtemp[self.dfsolvedtemp.columns[0:2]]
            #print(self.dfintertemp)
            self.dfadvec = pd.read_csv(self.directmodelDir + "/advective_flux.csv")
            self.dfconduc = pd.read_csv(self.directmodelDir + "/conductive_flux.csv")
            self.dftot = pd.read_csv(self.directmodelDir + "/total_flux.csv")

        elif mode == 'MCMC':
            self.dfwater = pd.read_csv(self.MCMCDir + "/MCMC_flows_quantiles.csv")
            self.dfsolvedtemp = pd.read_csv(self.MCMCDir + "/solved_temperatures.csv")
            self.dfdepths = pd.read_csv(self.MCMCdepthsdir)
            self.dfintertemp = pd.read_csv(self.MCMCDir + "/MCMC_temps_quantiles.csv")
            self.dfallparams = pd.read_csv(self.MCMCDir + "/MCMC_all_params.csv")
            self.dfadvec = pd.read_csv(self.MCMCDir + "/advective_flux.csv")
            self.dfconduc = pd.read_csv(self.MCMCDir + "/conductive_flux.csv")
            self.dftot = pd.read_csv(self.MCMCDir + "/total_flux.csv")
            self.dfbestparams = pd.read_csv(self.MCMCDir + "/MCMC_best_params.csv")
            self.dfbestparams = self.dfbestparams[self.dfbestparams.columns[1:]]



    def plotWaterFlowsDirect(self, dfwater):
        self.graphwaterdirect = MplCanvas(dfwater, "water flow")
        self.toolbarwaterdirect = NavigationToolbar(self.graphwaterdirect, self)
        self.vboxwaterdirect.addWidget(self.graphwaterdirect)
        self.vboxwaterdirect.addWidget(self.toolbarwaterdirect)
    
    def plotWaterFlowsMCMC(self, dfwater):
        self.graphwaterMCMC = MplCanvas(dfwater, "water flow with quantiles")
        self.toolbarwaterMCMC = NavigationToolbar(self.graphwaterMCMC, self)
        self.vboxwaterMCMC.addWidget(self.graphwaterMCMC)
        self.vboxwaterMCMC.addWidget(self.toolbarwaterMCMC)
    
    def plotFriseHeatFluxesDirect(self, dfadvec, dfconduc, dftot, dfdepths):
        self.graphfluxesdirect = MplCanvaHeatFluxes(dfadvec, dfconduc, dftot, dfdepths)
        self.toolbarfluxesdirect = NavigationToolbar(self.graphfluxesdirect, self)
        self.vboxfluxesdirect.addWidget(self.graphfluxesdirect)
        self.vboxfluxesdirect.addWidget(self.toolbarfluxesdirect)       

    def plotFriseHeatFluxesMCMC(self, dfadvec, dfconduc, dftot, dfdepths):
        self.graphfluxesMCMC = MplCanvaHeatFluxes(dfadvec, dfconduc, dftot, dfdepths)
        self.toolbarfluxesMCMC = NavigationToolbar(self.graphfluxesMCMC, self)
        self.vboxfluxesMCMC.addWidget(self.graphfluxesMCMC)
        self.vboxfluxesMCMC.addWidget(self.toolbarfluxesMCMC)      
    
    def plotFriseTempDirect(self, dfsolvedtemp, dfdepths):
        self.graphsolvedtempdirect = MplCanvas(dfsolvedtemp, "frise", dfdepths)
        self.toolbarsolvedtempdirect = NavigationToolbar(self.graphsolvedtempdirect, self)
        self.vboxfrisetempdirect.addWidget(self.graphsolvedtempdirect)
        self.vboxfrisetempdirect.addWidget(self.toolbarsolvedtempdirect)

    def plotFriseTempMCMC(self, dfsolvedtemp, dfdepths):
        self.graphsolvedtempMCMC = MplCanvas(dfsolvedtemp, "frise", dfdepths)
        self.toolbarsolvedtempMCMC = NavigationToolbar(self.graphsolvedtempMCMC, self)
        self.vboxfrisetempMCMC.addWidget(self.graphsolvedtempMCMC)
        self.vboxfrisetempMCMC.addWidget(self.toolbarsolvedtempMCMC)
    
    def plotInterfaceTempDirect(self, dfintertemp):
        self.graphintertempdirect = MplCanvas(dfintertemp, "temperature interface")
        self.toolbarintertempdirect = NavigationToolbar(self.graphintertempdirect, self)
        self.vboxintertempdirect.addWidget(self.graphintertempdirect)
        self.vboxintertempdirect.addWidget(self.toolbarintertempdirect)
    
    def plotInterfaceTempMCMC(self, dfintertemp):
        self.graphintertempMCMC = MplCanvas(dfintertemp, "temperature with quantiles")
        self.toolbarintertempMCMC = NavigationToolbar(self.graphintertempMCMC, self)
        self.vboxintertempMCMC.addWidget(self.graphintertempMCMC)
        self.vboxintertempMCMC.addWidget(self.toolbarintertempMCMC)
    
    def histos(self, dfallparams):
        self.histos = MplCanvasHisto(dfallparams)
        self.toolbarhistos = NavigationToolbar(self.histos, self)
        self.vboxhistos.addWidget(self.histos)
        self.vboxhistos.addWidget(self.toolbarhistos)

    def plotParapluies(self, dfsolvedtemp, dfdepths):
        self.parapluies = MplCanvas(dfsolvedtemp, "parapluies", dfdepths)
        self.toolbarparapluies = NavigationToolbar(self.parapluies, self)
        self.vboxsolvedtempdirect.addWidget(self.parapluies)
        self.vboxsolvedtempdirect.addWidget(self.toolbarparapluies)
    
    def plotParapluiesMCMC(self, dfsolvedtemp, dfdepths):
        self.parapluiesMCMC = MplCanvas(dfsolvedtemp, "parapluies", dfdepths)
        self.toolbarparapluiesMCMC = NavigationToolbar(self.parapluiesMCMC, self)
        self.vboxsolvedtempMCMC.addWidget(self.parapluiesMCMC)
        self.vboxsolvedtempMCMC.addWidget(self.toolbarparapluiesMCMC)

    def setBestParamsModel(self, dfbestparams):
        self.BestParamsModel = PandasModel(self.dfbestparams)
        self.tableViewBestParams.setModel(self.BestParamsModel)
        self.tableViewBestParams.resizeColumnsToContents()




""" 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WidgetPoint()
    mainWin.show()
    sys.exit(app.exec_())
"""