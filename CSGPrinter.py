import math

from Options import Options
from Point import Point


class CSGPrinter():
    def __init__(self, fname):
        o = Options()
        cubeEdgeLength = o.getProperty('cubeEdgeLength')
        polygonalDiskRadius = o.getProperty('polygonalDiskRadius')
        polygonalDiskThickness = o.getProperty('polygonalDiskThickness')
        intercalatedStackNumber = o.getProperty('intercalatedStackNumber')
        intercalatedInterlayerThickness = o.getProperty('intercalatedInterlayerThickness')
        self.values = {}
        self.values['f'] = open(fname, 'w')
        self.f().write('algebraic3d\n')
        string = 'solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'
        self.values['matrixString'] = 'solid matrix = cell'
        self.f().write(string.format(cubeEdgeLength))
        
    def f(self):
        return self.values['f']
        
    def matrixString(self):
        return self.values['matrixString']
        
    def printDisk(self, disk):
        solidName = 'Disk' + disk.number()
        self.values['matrixString'] += ' and not ' + solidName
        self.f().write('solid ' + solidName + ' = ')
        dot1 = disk.bottomCenter()
        dot2 = disk.topCenter()
        diskCenter = Point(dot1.x() / 2 + dot2.x() / 2,
                           dot1.y() / 2 + dot2.y() / 2,
                           dot1.z() / 2 + dot2.z() / 2)
        for facet in disk.facets():
            self.f().write('plane(')
            facet.printToCSG(self.f())
            self.f().write('; ')
            (facet - diskCenter).printToCSG(self.f())
            self.f().write(') and ')
        self.f().write('plane(')
        dot1.printToCSG(self.f())
        self.f().write(';')
        (dot1 - diskCenter).printToCSG(self.f())
        self.f().write(') and plane(')
        dot2.printToCSG(self.f())
        self.f().write(';')
        (dot2 - diskCenter).printToCSG(self.f())
        self.f().write(');\n')
        #self.f().write('tlo ' + solidName + ' -maxh=0.1;\n')
        self.f().write('tlo ' + solidName + ';\n')
    
    def printMatrix(self):
        self.values['matrixString'] += ';\n'
        self.f().write(self.matrixString())
        self.f().write('tlo matrix -transparent;')
        
    def printDiskInTheShell(self, diskInTheShell):
        pass
