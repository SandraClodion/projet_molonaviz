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


def celsiusToKelvin(df):
    
    columnsNames = list(df.head(0))

    temps = [columnsNames[i] for i in range(1,5)]
    for temp in temps:
        df[temp] = df[temp]+273.15
    
    
def convertDates(df):
    columnsNames = list(df.head(0))
    times = columnsNames[0]
    try : #On vérifie que le format des dates est le bon
        datetime.strptime(times[0], '%y/%m/%d %H:%M:%S')
    except ValueError : #Si ce n'est pas le cas on convertit les dates
        df[times] = pd.to_datetime(df[times]).apply(lambda x:x.strftime('%y/%m/%d %H:%M:%S'))


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

def displayConfirmationMessage(title, message):
    msg = QtWidgets.QMessageBox()
    msg.setText(title)
    msg.setIcon(QtWidgets.QMessageBox.Warning)  
    msg.setInformativeText(message)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    msg.setDefaultButton(QtWidgets.QMessageBox.Cancel)
    return msg.exec_()

def displayCriticalMessage(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(message)
    msg.exec_() 