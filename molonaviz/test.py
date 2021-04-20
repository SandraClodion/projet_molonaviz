from pyheatmy import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from point import Point
from datetime import datetime
from dialogcompute import DialogCompute
from PyQt5 import QtWidgets, QtCore, uic
import sys, os
import matplotlib.pyplot as plt
from itertools import islice

point = Point('point n°1', pointDir = '/Users/sandraclodion/MINES/2A/MOLONARI/PROJET/Étude Sandra/point n°1')
point.loadPointFromDir()

sensorDir = '/Users/sandraclodion/MINES/2A/MOLONARI/PROJET/projet_molonaviz/EXEMPLES FICHIERS/Sensors'

"""
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dlg = DialogCompute()
    res = dlg.exec()
    if res == 0 : 
        params, nb_cells = dlg.getInputDirectModel()  
"""

times = [datetime.fromtimestamp(1000*k) for k in range(13)]
var = np.stack(
    4*[np.cos(np.linspace(0,2*np.pi,13))],
    axis = -1
)
temps = np.array(13*[[310.15, 308, 306, 285.15]])+2*var  

col_dict = {
	"river_bed": 1., 
    "depth_sensors": [.15, .25, .4], #En vrai y aura une 4e valeur ici mais ca prendra en charge pareil
	"offset": .05,
    "dH_measures": list(zip(times,list(zip(.01*np.random.rand(13), temps[:,0])))),
	"T_measures": list(zip(times, temps[:,1:])),
    "sigma_meas_P": None, #float
    "sigma_meas_T": None, #float
}

col = Column.from_dict(col_dict)

priors = {
    "moinslog10K": ((1.5, 6), .005), # (intervalle, sigma)
    "n": ((.01, .25), .005),
    "lambda_s": ((1, 5), .05),
    "rhos_cs": ((1e6,1e7), 1e4),
}


col.compute_mcmc(
    nb_iter = 400,
    priors = priors,
    nb_cells = 100,
    quantile = (.05, .5, .95)
)

params = col.get_best_param()
print(params)
best_params_dict = {'moinslog10K':[params[0]], 'n':[params[1]], 'lambda_s':[params[2]], 'rhos_cs':[params[3]]}
df_best_params = pd.DataFrame.from_dict(best_params_dict)
df_best_params

col.compute_solve_transi(params, 100)
col.temps_solve
col.get_all_moinslog10K()
col.get_all_n()
col.get_all_lambda_s()
col.get_all_rhos_cs()
print(col.get_flows_quantile(0.05))
print(len(col.get_temps_quantile(0.05)))

"""
col.compute_solve_transi(params, nb_cells)

n_dates=13

temps = col.temps_solve
times = col.times_solve
flows = col.flows_solve
depths = col.get_depths_solve()

## Formatage des dates
n_dates = len(times)
times_string = np.zeros((n_dates,1))
times_string = times_string.astype('str')
for i in range(n_dates):
    times_string[i,0] = times[i].strftime('%y/%m/%d %H:%M:%S')

np_flows = np.zeros((n_dates,1))
for i in range(n_dates):
    np_flows[i,0] = flows[i]

np_flows_solve = np.concatenate((times_string, np_flows), axis=1)
df_flows_solve = pd.DataFrame(np_flows_solve, columns=["Date Heure, GMT+01:00", "Débit d'eau échangé (m/s)"])
#flows_solve_file = os.path.join(resultsDir, 'solved_flows.csv')
print(df_flows_solve)
"""




