#!/usr/bin/env python3
# coding utf-8

import math

#import numpy as np

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

VERTICES_NUMBER = 6
VOLUME_FRACTION = 0.00033
CUBE_EDGE_LENGTH = 10
POLYGONAL_DISK_THICKNESS = 0.1
POLYGONAL_DISK_RADIUS = 1
FNAME = '1.geo'


class Point():
    def __init__(self, x, y, z):
        self.values = {}
        self.values['x'] = x
        self.values['y'] = y
        self.values['z'] = z
        
    def __add__(self, otherPoint):
        return Point(self.x() + otherPoint.x(),
                     self.y() + otherPoint.y(),
                     self.z() + otherPoint.z())
    
    def __sub__(self, otherPoint):
        return Point(self.x() - otherPoint.x(),
                     self.y() - otherPoint.y(),
                     self.z() - otherPoint.z())
                     
    def __mul__(self, coefficient):
        return Point(self.x() * coefficient,
                     self.y() * coefficient,
                     self.z() * coefficient)
                     
    def __truediv__(self, coefficient):
        return Point(self.x() / coefficient,
                     self.y() / coefficient,
                     self.z() / coefficient)
                     
    def __str__(self):
        return '{}, {}, {}'.format(self.x(), self.y(), self.z())
        
    def x(self):
        return self.values['x']
        
    def y(self):
        return self.values['y']
    
    def z(self):
        return self.values['z']
    
    def setX(self, newX):
        self.values['x'] = newX
   
    def setY(self, newY):
        self.values['y'] = newY
        
    def setZ(self, newZ):
        self.values['z'] = newZ
        
    def printToCSG(self, f):
        f.write(self.__str__())
        
    #def rotateAroundAxe(self, axe):
        
        
        
class Vector():
    def __init__(self, dot1, dot2):
        self.values = {}
        self.values['beginX'] = dot1.x()
        self.values['beginY'] = dot1.y()
        self.values['beginZ'] = dot1.z()
        self.values['endX'] = dot2.x()
        self.values['endY'] = dot2.y()
        self.values['endZ'] = dot2.z()
        
    def __add__(self, otherVector):
        self.values['endX'] += (otherVector.end() - otherVector.begin()).x
        self.values['endY'] += (otherVector.end() - otherVector.begin()).y
        self.values['endZ'] += (otherVector.end() - otherVector.begin()).z
        
    def __sub__(self, otherVector):
        self.values['endX'] -= (otherVector.end() - otherVector.begin()).x
        self.values['endY'] -= (otherVector.end() - otherVector.begin()).y
        self.values['endZ'] -= (otherVector.end() - otherVector.begin()).z
        
    def __mul__(self, coefficient):
        x = self.values['endX'] - self.values['beginX']
        y = self.values['endY'] - self.values['beginY']
        z = self.values['endZ'] - self.values['beginZ']
        self.values['endX'] = self.values['beginX'] + x * coefficient
        self.values['endX'] = self.values['beginY'] + y * coefficient
        self.values['endX'] = self.values['beginZ'] + z * coefficient
        
    def __truediv__(self, coefficient):
        x = self.values['endX'] - self.values['beginX']
        y = self.values['endY'] - self.values['beginY']
        z = self.values['endZ'] - self.values['beginZ']
        self.values['endX'] = self.values['beginX'] + x / coefficient
        self.values['endX'] = self.values['beginY'] + y / coefficient
        self.values['endX'] = self.values['beginZ'] + z / coefficient
        
    def begin(self):
        return Point(self.values['beginX'],
                     self.values['beginY'],
                     self.values['beginZ'])
                     
    def end(self):
        return Point(self.values['endX'],
                     self.values['endY'],
                     self.values['endZ'])
                     
    def x(self):
        return self.values['endX'] - self.values['beginX']

    def y(self):
        return self.values['endY'] - self.values['beginY']
        
    def z(self):
        return self.values['endZ'] - self.values['beginZ']
                     
    def length(self):
        x = self.values['endX'] - self.values['beginX']
        y = self.values['endY'] - self.values['beginY']
        z = self.values['endZ'] - self.values['beginZ']
        return (x**2 + y**2 + z**2)**0.5
        

class LineMadeOfDots():
    def __init__(self, dot1, dot2):
        self.values = {}
        self.values['vector'] = Vector(dot1, dot2)


class PlaneMadeOfDots():
    def __init__(self, dot1, dot2, dot3):
        vector1 = dot2 - dot1
        vector2 = dot3 - dot1
        normal = (vector1.y() * vector2.x() - vector2.y() * vector1.z(),
                  vector2.x() * vector1.z() - vector1.x() * vector2.z(),
                  vector1.x() * vector2.y() - vector2.x() * vector1.y())
        self.values = {}
        self.values['normal'] = normal
        self.values['origin'] = dot1
        
    def printToCSG(self, f):
        f.write('plane(')
        self.origin().printToCSG(f)
        f.write('; ')
        self.normal().printToCSG(f)
        f.write(')')
        

class DiskMadeOfDots():
    def __init__(self, dot1, dot2, radius):
        self.values = {}
        self.values['bottomCenter'] = dot1
        self.values['topCenter'] = dot2
        self.values['radius'] = radius
        self.values['facetsCenters'] = []
        for i in range(VERTICES_NUMBER):
            diskCenter = Point(dot1.x() / 2 + dot2.x() / 2,
                               dot1.y() / 2 + dot2.y() / 2,
                               dot1.z() / 2 + dot2.z() / 2)
            dot = diskCenter + Point(math.cos(2 * math.pi * i / VERTICES_NUMBER),
                                     math.sin(2 * math.pi * i / VERTICES_NUMBER),
                                     0)
            self.values['facetsCenters'].append(dot)
            
    def rotate(self, rotationMatrix)            :
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
        
    
    def printToCSG(self, f, solidName):
        f.write('solid ' + solidName + ' = ')
        dot1 = self.values['bottomCenter']
        dot2 = self.values['topCenter']
        diskCenter = Point(dot1.x() / 2 + dot2.x() / 2,
                           dot1.y() / 2 + dot2.y() / 2,
                           dot1.z() / 2 + dot2.z() / 2)
        for facet in self.values['facetsCenters']:
            f.write('plane(')
            facet.printToCSG(f)
            f.write('; ')
            (facet - diskCenter).printToCSG(f)
            f.write(') and ')
        f.write('plane(')
        dot1.printToCSG(f)
        f.write(';')
        (dot1 - diskCenter).printToCSG(f)
        f.write(') and plane(')
        dot2.printToCSG(f)
        f.write(';')
        (dot2 - diskCenter).printToCSG(f)
        f.write(');\n')
        f.write('tlo ' + solidName + ';')
        
        
def det(M, recDepth=0):
    l = len(M)
    if l == 1:
        return M[0][0]
    result = 0
    for i in range(l):
        newM = []
        for j in range(1, l):
            newM.append(copy.deepcopy(M[j]))
            newM[j-1].pop(i)
        result += ((-1) ** i) * det(newM, recDepth + 1) * M[0][i]
    return result


def boxCross(boxSize, disk):
    return False
    
    
def disksCross(disk1, disk2):
    return False

def main(cubeSize=10, diskRadius=1, diskThickness=0.1):
    f = open(FNAME, 'w')
    f.write('algebraic3d;\n')
    f.write('solid cell = orthobrick(0, 0, 0; 10, 10, 10);\n')
    f.write('tlo cell -transparent;\n')
    disk = DiskMadeOfDots(Point(0, 0, -0.1), Point(0, 0, 0.1), 1)
    s = 1/2**0.5
    M = [[1, 0, 0],
         [0, s, -s],
         [0, s, s]]
    disk.rotate(M)
    disk.translate(Vector(Point(0, 0, 0), Point(5, 5, 5)))
    disk.printToCSG(f, 'Disk1')
    

main()