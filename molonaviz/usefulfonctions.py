import unicodedata
import string
import pandas as pd
from PyQt5 import QtWidgets
from datetime import datetime
import pyqtgraph as pg

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    
    return cleaned_filename[:char_limit] 


def celsiusToKelvin(trawfile, tprocessedfile):
    df = pd.read_csv(trawfile, index_col=0, header=1) #modifié avec la nouvelle API
    columnsNames = list(df.head(0))
    time = columnsNames[0]
    temps = [columnsNames[i] for i in range(1,5)]
    for temp in temps:
        df[temp] = df[temp]+273.15
    df.to_csv(tprocessedfile)


def displayInfoMessage(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(message)
    msg.exec_() 

def displayInfoMessage(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(message)
    msg.exec_() 

def displayWarningMessage(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(message)
    msg.exec_() 

def listtime_convert(dates):
    #Date est une str yy/mm/dd hh:mm:ss
    #Retourne une datetime
    new_dates = []
    for date in dates :
        new_dates.append(datetime.strptime(date, "%y/%m/%d %H:%M:%S"))
    return(new_dates)

def time_plots(pd, date_axis, Temp=False):
    Timestr = pd[pd.columns[0]].values.tolist()
    Time = listtime_convert(Timestr)
    if Temp:
        #On plot les 4 courbes de température
        graph = [0]*4
        GRAPH = []
        for i in range(4):
            graph[i] = pg.PlotWidget(axisItems = {'bottom': date_axis[i]}) # crée une instance qui ne se recrée visiblement pas
            Temperatures = pd[pd.columns[i+1]].values.tolist()
            curve = graph.plot(x=[t.timestamp() for t in Time], y=Temperatures, symbol='o')
            GRAPH.append(curve)
        return(GRAPH)
    else:
        #On plot la courbe de pression
        graph = pg.PlotWidget(axisItems = {'bottom': date_axis[0]})
        Pressures = pd[pd.columns[1]].values.tolist()
        graph.plot(x=[t.timestamp() for t in Time], y=Pressures, symbol='o')
    return(graph)

def displayCriticalMessage(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(message)
    msg.exec_() 
