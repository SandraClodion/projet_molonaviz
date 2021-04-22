class EmptyFieldError(Exception):

    """
    classdoc
    """

    def __init__(self, message='Please do not leave any field blank'):
        self.message = message

    def __str__(self):
        return self.message

class TimeStepError(Exception):

    """
    classdoc
    """

    def __init__(self, timeStepTemp, timeStepPress):
        self.timeStepTemp = timeStepTemp
        self.timeStepPress = timeStepPress
    
    def __str__(self):
        return f"Time steps aren't matching : {self.timeStepTemp} in the pressures file, {self.timeStepPress} in the temperatures file"