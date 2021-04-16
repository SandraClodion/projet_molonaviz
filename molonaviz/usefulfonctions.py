import unicodedata
import string
import pandas as pd
from PyQt5 import QtWidgets

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

def time_convert(date):
    #Date est une str yyyy/mm/dd hh:mm:ss
    #Retourne le temps en secondes
    year = int(date[0:4])
    mon = int(date[5:7])
    mday = int(date[8:10])
    hour = int(date[12:14])
    minu = int(date[15:17])
    sec = int(date[18:20])
    #On calcule le nombre de secondes écoulées depuis le 01/01/00 à 00:00
    res = (year - 2000) * 12
    res = (res + mon - 1) * 30.5
    res = (res + mday - 1) * 24
    res = (res + hour) * 60
    res = (res + minu) * 60
    res = res + sec
    return(res)
    
def displayCriticalMessage(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(message)
    msg.exec_() 
