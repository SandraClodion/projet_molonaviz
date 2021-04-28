import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic

From_DialogCompute = uic.loadUiType(os.path.join(os.path.dirname(__file__),"dialogcompute.ui"))[0]

class DialogCompute(QtWidgets.QDialog, From_DialogCompute):
    
    def __init__(self):
        # Call constructor of parent classes
        super(DialogCompute, self).__init__()
        QtWidgets.QDialog.__init__(self)
        
        self.setupUi(self)

        self.setMouseTracking(True)

        self.label10Power.setText(f"10 <sup>-</sup>")
        self.label10Power_2.setText(f"10 <sup>-</sup>")
        self.label10Power_3.setText(f"10 <sup>-</sup>")

        #self.permeabilityValidator = QtGui.QDoubleValidator(0.0, 5.0, 2)
        #self.lineEditMoinsLog10KDirect.setValidator(self.permeabilityValidator)
        #self.lineEditMoinsLog10KMax.setValidator(self.permeabilityValidator)
        #self.lineEditMoinsLog10KMin.setValidator(self.permeabilityValidator)

        for i in range(50, 151, 5):
            self.comboBoxNCellsDirect.addItem(f'{i}')
            self.comboBoxNCellsMCMC.addItem(f'{i}')
        
        self.setDefaultValues()

        self.directModelLineEdits = [self.lineEditMoinsLog10KDirect, self.lineEditPorosityDirect, self.lineEditThermalConductivityDirect,
            self.lineEditThermalCapacityDirect]

        self.MCMCLineEdits = [self.lineEditMaxIterMCMC, 
            self.lineEditMoinsLog10KMin, self.lineEditMoinsLog10KMax, self.lineEditMoinsLog10KSigma,
            self.lineEditPorosityMin, self.lineEditPorosityMax, self.lineEditPorositySigma,
            self.lineEditThermalConductivityMin, self.lineEditThermalConductivityMax, self.lineEditThermalConductivitySigma,
            self.lineEditThermalCapacityMin, self.lineEditThermalCapacityMax, self.lineEditThermalCapacitySigma]

        self.radioButtonDirect.toggled.connect(self.inputDirect)
        self.radioButtonMCMC.toggled.connect(self.inputMCMC)

        #On pré-coche le modèle direct
        self.radioButtonDirect.setChecked(True)

        self.pushButtonDirect.clicked.connect(self.getInputDirectModel)
        self.pushButtonMCMC.clicked.connect(self.getInputMCMC)

        self.pushButtonRestoreDefault.clicked.connect(self.setDefaultValues)
        self.pushButtonRestoreDefault.setToolTip("All parameters will be set to default value")

        self.labelMoinsLog10KDirect.setToolTip("Please enter -log10K, K being permeability")

    def setDefaultValues(self):
        pass #À COMPLÉTER

    def inputDirect(self):

        self.pushButtonDirect.setEnabled(True)
        self.pushButtonMCMC.setEnabled(False)

        self.comboBoxNCellsDirect.setEnabled(True)
        self.comboBoxNCellsMCMC.setEnabled(False)

        for lineEdit in self.directModelLineEdits :
            lineEdit.setReadOnly(False)
    
        for lineEdit in self.MCMCLineEdits :
            lineEdit.setReadOnly(True)


    def inputMCMC(self):

        self.pushButtonDirect.setEnabled(False)
        self.pushButtonMCMC.setEnabled(True)

        self.comboBoxNCellsDirect.setEnabled(False)
        self.comboBoxNCellsMCMC.setEnabled(True)

        for lineEdit in self.directModelLineEdits :
            lineEdit.setReadOnly(True)
            
        for lineEdit in self.MCMCLineEdits :
            lineEdit.setReadOnly(False)



    def getInputDirectModel(self):
        moinslog10K = float(self.lineEditMoinsLog10KDirect.text())
        n = float(self.lineEditPorosityDirect.text())
        lambda_s = float(self.lineEditThermalConductivityDirect.text())
        rhos_cs = float(self.lineEditThermalCapacityDirect.text())
        nb_cells = int(self.comboBoxNCellsDirect.currentText())
        self.done(10)
        return (moinslog10K, n, lambda_s, rhos_cs), nb_cells

    def getInputMCMC(self):

        nb_iter = int(self.lineEditMaxIterMCMC.text())
        nb_cells = int(self.comboBoxNCellsMCMC.currentText())

        moins10logKmin = float(self.lineEditMoinsLog10KMin.text())
        moins10logKmax = float(self.lineEditMoinsLog10KMax.text())
        moins10logKsigma = float(self.lineEditMoinsLog10KSigma.text())

        nmin = float(self.lineEditPorosityMin.text())
        nmax = float(self.lineEditPorosityMax.text())
        nsigma = float(self.lineEditPorositySigma.text())

        lambda_s_min = float(self.lineEditThermalConductivityMin.text())
        lambda_s_max = float(self.lineEditThermalConductivityMax.text())
        lambda_s_sigma = float(self.lineEditThermalConductivitySigma.text())

        rhos_cs_min = float(self.lineEditThermalCapacityMin.text())
        rhos_cs_max = float(self.lineEditThermalCapacityMax.text())
        rhos_cs_sigma = float(self.lineEditThermalCapacitySigma.text())

        priors = {
        "moinslog10K": ((moins10logKmin, moins10logKmax), moins10logKsigma),
        "n": ((nmin, nmax), nsigma),
        "lambda_s": ((lambda_s_min, lambda_s_max), lambda_s_sigma),
        "rhos_cs": ((rhos_cs_min, rhos_cs_max), rhos_cs_sigma) }

        quantiles = self.lineEditQuantiles.text()
        quantiles = quantiles.split(",")
        quantiles = tuple(quantiles)
        quantiles = [float(quantile) for quantile in quantiles]
        
        self.done(1)
        return nb_iter, priors, nb_cells, quantiles


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = DialogCompute()
    mainWin.show()
    sys.exit(app.exec_())