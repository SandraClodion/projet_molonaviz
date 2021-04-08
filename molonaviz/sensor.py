from numpy import NaN
import pandas as pd

class Sensor(object):
    '''
    classdocs
    '''

    def __init__(self, name="", intercept=NaN, dudh=NaN, dudt=NaN):
        self.name = name
        self.intercept = intercept
        self.dudh = dudh
        self.dudt = dudt

    def tensionToPressure(self, prawfile, pprocessedfile):
        df = pd.read_csv(prawfile, header = 1, index_col = 0)
        columnsNames = list(df.head(0))
        time = columnsNames[0]
        tension = columnsNames[1]
        temperature = columnsNames[2]
        df[temperature] = df[temperature] + 273.15 #conversion en Kelvin
        a, b, c = self.intercept, self.dudh, self.dudt
        df['Pression différentielle (m)'] = (1/b)*(df[tension] - c*df[temperature] - a)
        df.drop([tension, temperature], axis=1)
        df.to_csv(pprocessedfile)
