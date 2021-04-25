import unicodedata
import string
import pandas as pd
from PyQt5 import QtWidgets
from datetime import datetime
import pyqtgraph as pg


def clean_filename(filename: str, char_limit: int= 255, replace=' '):

    valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in valid_filename_chars)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    
    return cleaned_filename[:char_limit] 


def celsiusToKelvin(df: pd.DataFrame):

    """
    Inplace
    """
    
    columnsNames = list(df.head(0))

    temps = [columnsNames[i] for i in range(1,5)]
    for temp in temps:
        df[temp] = df[temp]+273.15
    

def convertDates(df: pd.DataFrame):

    """
    Inplace
    """

    columnsNames = list(df.head(0))
    times = columnsNames[0]
    try : #On vérifie que le format des dates est le bon
        datetime.strptime(times[0], '%y/%m/%d %H:%M:%S')
    except ValueError : #Si ce n'est pas le cas on convertit les dates
        df[times] = pd.to_datetime(df[times]).apply(lambda x:x.strftime('%y/%m/%d %H:%M:%S'))

        
def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())


def displayInfoMessage(mainMessage: str, infoMessage: str=''):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(mainMessage)
    msg.setInformativeText(infoMessage)
    msg.exec_() 

def displayInfoMessage(mainMessage: str, infoMessage: str=''):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(mainMessage)
    msg.setInformativeText(infoMessage)
    msg.exec_() 

def displayWarningMessage(mainMessage: str, infoMessage: str=''):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(mainMessage)
    msg.setInformativeText(infoMessage)
    msg.exec_() 

def displayConfirmationMessage(mainMessage: str, infoMessage: str=''):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText(mainMessage)
    msg.setInformativeText(infoMessage)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    msg.setDefaultButton(QtWidgets.QMessageBox.Cancel)
    return msg.exec_()

def displayCriticalMessage(mainMessage: str, infoMessage: str=''):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(mainMessage)
    msg.setInformativeText(infoMessage)
    msg.exec_() 