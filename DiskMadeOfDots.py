import math

from Options import Options
from Point import Point
from Vector import Vector


class DiskMadeOfDots():
    def __init__(self, dot1, dot2, radius, verticesNumber=16):
        o = Options()
        self.values = {}
        self.values['bottomCenter'] = dot1
        self.values['topCenter'] = dot2
        self.values['radius'] = radius
        self.values['facetsCenters'] = []
        self.values['verticesNumber'] = o.getProperty('verticesNumber')
        for i in range(int(self.values['verticesNumber'])):
            diskCenter = Point(dot1.x() / 2 + dot2.x() / 2,
                               dot1.y() / 2 + dot2.y() / 2,
                               dot1.z() / 2 + dot2.z() / 2)
            centralAngle = 2 * math.pi * i / self.values['verticesNumber']
            dot = diskCenter + Point(radius * math.cos(centralAngle),
                                     radius * math.sin(centralAngle),
                                     0)
            self.values['facetsCenters'].append(dot)

    def verticesNumber(self):
        return self.values['verticesNumber']
            
    def facets(self):
        return self.values['facetsCenters']
        
    def center(self):
        return Point(self.values['bottomCenter'].x() / 2 +
                     self.values['topCenter'].x() / 2,
                     self.values['bottomCenter'].y() / 2 +
                     self.values['topCenter'].y() / 2,
                     self.values['bottomCenter'].z() / 2 +
                     self.values['topCenter'].z() / 2)
        
    def mainAxe(self):
        dot1 = self.values['bottomCenter']
        dot2 = self.values['topCenter']
        return Vector(Point(0, 0, 0), Point(dot2.x() - dot1.x(),
                                            dot2.y() - dot1.y(),
                                            dot2.z() - dot1.z()))
                                            
    def bottomCenter(self):
        return self.values['bottomCenter']
        
    def topCenter(self):
        return self.values['topCenter']
    
    def edgeLength(self):
        alpha = math.pi / self.verticesNumber()
        return self.values['radius'] / math.cos(alpha) * math.sin(alpha)
    
    def rotate(self, rotationMatrix):
        M = rotationMatrix
        dot1 = self.values['bottomCenter']
        dot2 = self.values['topCenter']
        for dot in [dot1, dot2, *self.values['facetsCenters']]:
            x = dot.x() * M[0][0] + dot.y() * M[0][1] + dot.z() * M[0][2]
            y = dot.x() * M[1][0] + dot.y() * M[1][1] + dot.z() * M[1][2]
            z = dot.x() * M[2][0] + dot.y() * M[2][1] + dot.z() * M[2][2]
            dot.setX(x)
            dot.setY(y)
            dot.setZ(z)
            
    def translate(self, translationsVector):
        dx = translationsVector.x()
        dy = translationsVector.y()
        dz = translationsVector.z()
        dot1 = self.values['bottomCenter']
        dot2 = self.values['topCenter'] 
        for dot in [dot1, dot2, *self.values['facetsCenters']]:
            x = dot.x() + dx
            y = dot.y() + dy
            z = dot.z() + dz
            dot.setX(x)
            dot.setY(y)
            dot.setZ(z)
            
    def setSelfNumber(self, number):
        self.values['number'] = number
        
    def number(self):
        return str(self.values['number'])