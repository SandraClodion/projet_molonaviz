from numpy import NaN

class Point(object):
    
    '''
    classdocs
    '''

    def __init__(self, name="", p=NaN, t=NaN):
        self.name = name
        self.p = p #pression
        self.t = t #température