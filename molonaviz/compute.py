import os, shutil
import numpy as np
import pandas as pd
from datetime import datetime
from PyQt5 import QtCore

from pyheatmy import *
from point import Point


class ColumnMCMCRunner(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    
    def __init__(self, col, nb_iter: int, priors: dict, nb_cells: str, quantiles: list):
        # Call constructor of parent classes
        super(ColumnMCMCRunner, self).__init__()
        
        self.col = col
        self.nb_iter = nb_iter
        self.priors = priors
        self.nb_cells = nb_cells
        self.quantiles = quantiles
        
    def run(self):
        print("Launching MCMC...")
        
        self.col.compute_mcmc(self.nb_iter, self.priors, self.nb_cells, self.quantiles)

        self.finished.emit()


class Compute(QtCore.QObject):

    """
    How to use this class : 
    - Create a Compute object : compute = Compute(point: Point)
    - Create an associated Column object : compute.setColumn(sensorDir: str)
    - Launch the computation :
        - with given parameters : compute.computeDirectModel(params: tuple, nb_cells: int, sensorDir: str)
        - with parameters inferred from MCMC : compute.computeMCMC(nb_iter: int, priors: dict, nb_cells: str, sensorDir: str)
    """
    MCMCFinished = QtCore.pyqtSignal()

    def __init__(self, point: Point=None):
        # Call constructor of parent classes
        super(Compute, self).__init__()
        self.thread = QtCore.QThread()

        self.point = point
        self.col = None
    
    def setColumn(self, sensorDir: str):
        self.col = self.point.setColumn(sensorDir)

        
    def computeMCMC(self, nb_iter: int, priors: dict, nb_cells: str, sensorDir: str):
        
        self.nb_cells = nb_cells
        if self.thread.isRunning():
            print("Please wait while previous MCMC is finished")
            return
    
        # Initialisation de la colonne
        self.setColumn(sensorDir)

        # Lancement de la MCMC
        #self.col.compute_mcmc(nb_iter, priors, nb_cells, quantile = (.05, .5, .95))

        self.mcmc_runner = ColumnMCMCRunner(self.col, nb_iter, priors, nb_cells, quantiles = (.05, .5, .95))
        self.mcmc_runner.finished.connect(self.endMCMC)
        self.mcmc_runner.moveToThread(self.thread)
        self.thread.started.connect(self.mcmc_runner.run)
        self.thread.start()


    def endMCMC(self):

        self.thread.quit()
        print("MCMC finished")

        best_params = self.col.get_best_param()

        # Sauvegarde des résultats de la MCMC
        resultsDir = os.path.join(self.point.getPointDir(), 'results', 'MCMC_results')
        self.saveBestParams(resultsDir)
        self.saveAllParams(resultsDir)
        
        # Lancement du modèle direct avec les paramètres inférés
        self.col.compute_solve_transi(best_params, self.nb_cells)
        
        # Sauvegarde des différents résultats du modèle direct
        self.saveResults(resultsDir)

        # Sauvegarde des quantiles
        self.saveFlowWithQuantiles(resultsDir)
        self.saveTempWithQuantiles(resultsDir)

        self.MCMCFinished.emit()
        

    def computeDirectModel(self, params: tuple, nb_cells: int, sensorDir: str):

        # Initialisation de la colonne
        self.setColumn(sensorDir)

        # Lancement du modèle direct
        self.col.compute_solve_transi(params, nb_cells)

        # Sauvegarde des différents résultats du modèle direct
        resultsDir = os.path.join(self.point.getPointDir(), 'results', 'direct_model_results')
        self.saveResults(resultsDir)
    
  
    def saveBestParams(self, resultsDir: str):
        """
        Sauvegarde les meilleurs paramètres inférés par la MMC dans un fichier csv en local
        Pour accéder au fichier : pointDir --> results --> MCMC_best_params.csv
        """

        best_params = self.col.get_best_param()

        best_params_dict = {
            'moinslog10K':[best_params[0]], 
            'n':[best_params[1]], 
            'lambda_s':[best_params[2]], 
            'rhos_cs':[best_params[3]]
        }

        df_best_params = pd.DataFrame.from_dict(best_params_dict)

        best_params_file = os.path.join(resultsDir, 'MCMC_best_params.csv')
        df_best_params.to_csv(best_params_file, index=True)

    def saveAllParams(self, resultsDir: str):

        all_moins10logK = self.col.get_all_moinslog10K()
        all_n = self.col.get_all_n()
        all_lambda_s = self.col.get_all_lambda_s()
        all_rhos_cs = self.col.get_all_rhos_cs()

        all_params_dict = {
            'moinslog10K': all_moins10logK, 
            'n': all_n, 
            'lambda_s': all_lambda_s, 
            'rhos_cs': all_rhos_cs
        }

        df_all_params = pd.DataFrame.from_dict(all_params_dict)

        all_params_file = os.path.join(resultsDir, 'MCMC_all_params.csv')
        df_all_params.to_csv(all_params_file, index=True)
    


    def saveFlowWithQuantiles(self, resultsDir: str):

        times = self.col.times_solve

        flows = self.col.flows_solve
        quantile05 = self.col.get_flows_quantile(0.05)
        quantile50 = self.col.get_flows_quantile(0.5)
        quantile95 = self.col.get_flows_quantile(0.95)

        # Formatage des dates
        n_dates = len(times)
        times_string = np.zeros((n_dates,1))
        times_string = times_string.astype('str')
        for i in range(n_dates):
            times_string[i,0] = times[i].strftime('%y/%m/%d %H:%M:%S')

        # Création du dataframe
        np_flows_quantiles = np.zeros((n_dates,4))
        for i in range(n_dates):
            np_flows_quantiles[i,0] = flows[i]
            np_flows_quantiles[i,1] = quantile05[i]
            np_flows_quantiles[i,2] = quantile50[i]
            np_flows_quantiles[i,3] = quantile95[i]
        np_flows_times_and_quantiles = np.concatenate((times_string, np_flows_quantiles), axis=1)
        df_flows_quantiles = pd.DataFrame(np_flows_times_and_quantiles, 
        columns=["Date Heure, GMT+01:00", 
        "Débit d'eau échangé (m/s) - pour les meilleurs paramètres",
        "Débit d'eau échangé (m/s) - quantile 5%",
        "Débit d'eau échangé (m/s) - quantile 50%",
        "Débit d'eau échangé (m/s) - quantile 95%"])
    
        # Sauvegarde sous forme d'un fichier csv
        flows_quantiles_file = os.path.join(resultsDir, 'MCMC_flows_quantiles.csv')
        df_flows_quantiles.to_csv(flows_quantiles_file, index=False)
    

    def saveTempWithQuantiles(self, resultsDir: str):
        
        times = self.col.times_solve

        temp = self.col.temps_solve[:,0] #température à l'interface
        quantile05 = self.col.get_temps_quantile(0.05)[:,0]
        quantile50 = self.col.get_temps_quantile(0.5)[:,0]
        quantile95 = self.col.get_temps_quantile(0.95)[:,0]

        # Formatage des dates
        n_dates = len(times)
        times_string = np.zeros((n_dates,1))
        times_string = times_string.astype('str')
        for i in range(n_dates):
            times_string[i,0] = times[i].strftime('%y/%m/%d %H:%M:%S')

        # Création du dataframe
        np_temps_quantiles = np.zeros((n_dates,4))
        for i in range(n_dates):
            np_temps_quantiles[i,0] = temp[i]
            np_temps_quantiles[i,1] = quantile05[i]
            np_temps_quantiles[i,2] = quantile50[i]
            np_temps_quantiles[i,3] = quantile95[i]
        np_temps_times_and_quantiles = np.concatenate((times_string, np_temps_quantiles), axis=1)
        df_temps_quantiles = pd.DataFrame(np_temps_times_and_quantiles, 
        columns=["Date Heure, GMT+01:00", 
        "Température à l'interface (K) - pour les meilleurs paramètres",
        "Température à l'interface (K) - quantile 5%",
        "Température à l'interface (K) - quantile 50%",
        "Température à l'interface (K) - quantile 95%"])

        # Sauvegarde sous forme d'un fichier csv
        temps_quantiles_file = os.path.join(resultsDir, 'MCMC_temps_quantiles.csv')
        df_temps_quantiles.to_csv(temps_quantiles_file, index=False)


    def saveResults(self, resultsDir: str):

        """
        Sauvegarde les différents résultats calculés sous forme de fichiers csv en local :
        - profils de températures calculés aux différentes profondeurs
        - chronique des flux d'eau échangés entre la nappe et la rivière

        Les résultats sont disponibles respectivement dans les fichiers suivants :
        - pointDir --> results --> solved_temperatures.csv
        - pointDir --> results --> solved_flows.csv

        Prend en argument :
        - la colonne sur laquelle les calculs ont été faits (type: Column)
        - le chemin d'accès vers le dossier 'results' du point (type: str)
        Ne retourne rien
        """
        
        temps = self.col.temps_solve
        times = self.col.times_solve
        flows = self.col.flows_solve
        advective_flux = self.col.get_advec_flows_solve()
        conductive_flux = self.col.get_conduc_flows_solve()
        depths = self.col.get_depths_solve()
        
        ## Formatage des dates
        n_dates = len(times)
        times_string = np.zeros((n_dates,1))
        times_string = times_string.astype('str')
        for i in range(n_dates):
            times_string[i,0] = times[i].strftime('%y/%m/%d %H:%M:%S')
        
        ## Profondeurs
        df_depths = pd.DataFrame(depths, columns=['Depth (m)'])
        depths_file = os.path.join(resultsDir, 'depths.csv')
        df_depths.to_csv(depths_file, index=False)

        ## Profils de températures

        # Création du dataframe
        np_temps_solve = np.concatenate((times_string, temps), axis=1)
        df_temps_solve = pd.DataFrame(np_temps_solve, columns=['Date Heure, GMT+01:00']+[f'Température (K) pour la profondeur {depth:.4f} m' for depth in depths])
        # Sauvegarde sous forme d'un fichier csv
        temps_solve_file = os.path.join(resultsDir, 'solved_temperatures.csv')
        df_temps_solve.to_csv(temps_solve_file, index=False)


        ## Flux d'énergie advectifs

        # Création du dataframe
        np_advective_flux = np.concatenate((times_string, advective_flux), axis=1)
        df_advective_flux = pd.DataFrame(np_advective_flux, columns=['Date Heure, GMT+01:00']+[f'Flux advectif (W/m2) pour la profondeur {depth:.4f} m' for depth in depths])
        # Sauvegarde sous forme d'un fichier csv
        advective_flux_file = os.path.join(resultsDir, 'advective_flux.csv')
        df_advective_flux.to_csv(advective_flux_file, index=False)


        ## Flux d'énergie conductifs

        # Création du dataframe
        np_conductive_flux = np.concatenate((times_string, conductive_flux), axis=1)
        df_conductive_flux = pd.DataFrame(np_conductive_flux, columns=['Date Heure, GMT+01:00']+[f'Flux conductif (W/m2) pour la profondeur {depth:.4f} m' for depth in depths])
        # Sauvegarde sous forme d'un fichier csv
        conductive_flux_file = os.path.join(resultsDir, 'conductive_flux.csv')
        df_conductive_flux.to_csv(conductive_flux_file, index=False)

        ## Flux d'énergie totaux

        # Création du dataframe
        np_total_flux = np.concatenate((times_string, advective_flux+conductive_flux), axis=1)
        df_total_flux = pd.DataFrame(np_total_flux, columns=['Date Heure, GMT+01:00']+[f"Flux d'énergie total (W/m2) pour la profondeur {depth:.4f} m" for depth in depths])
        # Sauvegarde sous forme d'un fichier csv
        total_flux_file = os.path.join(resultsDir, 'total_flux.csv')
        df_total_flux.to_csv(total_flux_file, index=False)


        ## Flux d'eau échangés entre la nappe et la rivière

        # Création du dataframe
        np_flows = np.zeros((n_dates,1))
        for i in range(n_dates):
            np_flows[i,0] = flows[i]
        np_flows_solve = np.concatenate((times_string, np_flows), axis=1)
        df_flows_solve = pd.DataFrame(np_flows_solve, columns=["Date Heure, GMT+01:00", "Débit d'eau échangé (m/s)"])
        # Sauvegarde sous forme d'un fichier csv
        flows_solve_file = os.path.join(resultsDir, 'solved_flows.csv')
        df_flows_solve.to_csv(flows_solve_file, index=False)


