import math

from DiskMadeOfDots import DiskMadeOfDots
from Options import Options


class DiskMadeOfDotsInTheShell(DiskMadeOfDots):
    def __init__(self, dot1, dot2, radius,
                 verticesNumber=16, shellThickness=1):
        super().__init__(dot1, dot2, radius, verticesNumber)
        o = Options()
        self.values['shellThickness'] = o.getProperty('shellThickness')
        self.interactingDisks = set()
        self.values['number'] = None
