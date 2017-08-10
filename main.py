#!/usr/bin/env python3
# coding utf-8

import math

#import numpy as np

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

VERTICES_NUMBER = 5
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
        
    def x(self):
        return self.values['x']
        
    def y(self):
        return self.values['y']
        
    def z(self):
        return self.values['z']
        
    def setX(self, x):
        self.values['x'] = x
        
    def setY(self, y):
        self.values['y'] = y
        
    def setZ(self, z):
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

    def printToCSG(self, f):
        f.write(self.__str__())
        
    def length(self):
        return (self.x()**2 + self.y()**2 + self.z()**2)**0.5
        
    def rotateByMatrix(self, M):
        x = self.x() * M[0][0] + self.y() * M[0][1] + self.z() * M[0][2]
        y = self.x() * M[1][0] + self.y() * M[1][1] + self.z() * M[1][2]
        z = self.x() * M[2][0] + self.y() * M[2][1] + self.z() * M[2][2]
        return Point(x, y, z)


class Plane():
    def __init__(self, normal=Point(1, 1, 1), origin=Point(0, 0, 0)):
        self.values = {}
        self.values['normal'] = normal
        self.values['origin'] = origin
        
    def normal(self):
        return self.values['normal']
        
    def origin(self):
        return self.values['origin']
    
    def printToCSG(self, f):
        f.write('plane(')
        self.origin().printToCSG(f)
        f.write('; ')
        self.normal().printToCSG(f)
        f.write(')')
    
    
class Cylinder():
    def __init__(self, pointOne, pointTwo, radius):
        self.values = {}
        self.values['pointOne'] = pointOne
        self.values['pointTwo'] = pointTwo
        self.values['radius'] = radius
        
    def pointOne(self):
        return self.values['pointOne']
        
    def pointTwo(self):
        return self.values['pointTwo']
        
    def radius(self):
        return self.values['radius']
    
    def printToCSG(self, f):
        f.write('cylinder(')
        self.pointOne().printToCSG(f)
        f.write('; ')
        self.pointTwo().printToCSG(f)
        f.write('; ' + str(self.radius()))
        f.write(')')
        

class PolygonalCylinder():
    def __init__(self, pointOne, pointTwo, radius):
        self.values = {}
        self.values['pointOne'] = pointOne
        self.values['pointTwo'] = pointTwo
        self.values['radius'] = radius
        angleStep = 2 * math.pi / VERTICES_NUMBER
        axeVector = self.pointTwo() - self.pointOne()
        initialVector = Point(0, axeVector.y(), -axeVector.z())
    def pointOne(self):
        return self.values['pointOne']
        
    def pointTwo(self):
        return self.values['pointTwo']
        
    def radius(self):
        return self.values['radius']
    
    def printToCSG(self, f):
        f.write('cylinder(')
        self.pointOne().printToCSG(f)
        f.write('; ')
        self.pointTwo().printToCSG(f)
        f.write('; ' + str(self.radius()))
        f.write(')')
            
            
class PolygonalCylinderRotated():
    def __init__(self):
        self.values = {}
        self.values['pointOne'] = Point(0, 0, 0)
        self.values['pointTwo'] = Point(1, 0, 0)
        self.values['vertices'] = []
        self.values['facets'] = []
        self.values['rotationAngle'] = 2 * math.pi / VERTICES_NUMBER
        vector = Point(0, 1, 0)
        ort = vector * POLYGONAL_DISK_RADIUS / vector.length()
        print(ort)
        self.values['vertices'].append(vector)
        self.values['facets'].append(Plane(normal=vector, origin=ort))
        cosa = math.cos(self.values['rotationAngle'])
        sina = math.sin(self.values['rotationAngle'])
        print(sina, cosa)
        rotationMatrixX = [[1, 0, 0],
                           [0, cosa, -sina],
                           [0, sina, cosa]]
        for i in range(VERTICES_NUMBER - 1):
            vector = vector.rotateByMatrix(rotationMatrixX)
            self.values['vertices'].append(vector)
            ort = vector * POLYGONAL_DISK_RADIUS / vector.length()
            self.values['facets'].append(Plane(normal=vector, origin=ort))
        self.values['topPlane'] = Plane(normal=Point(1, 0, 0), origin=Point(POLYGONAL_DISK_THICKNESS / 2, 0, 0))
        self.values['bottomPlane'] = Plane(normal=Point(-1, 0, 0), origin=Point(-POLYGONAL_DISK_THICKNESS / 2, 0, 0))
            
    def printToCSG(self, f):
        for i, plane in enumerate(self.values['facets']):
            plane.printToCSG(f)
            f.write(' and ')
        top = self.values['topPlane']
        bottom = self.values['bottomPlane']
        top.printToCSG(f)
        f.write(' and ')
        bottom.printToCSG(f)


class PolygonalDisk():
    def __init__(self, name='0', radius=POLYGONAL_DISK_RADIUS,
                 thickness=POLYGONAL_DISK_THICKNESS,
                 normal=Point(1, 1, 1), origin=Point(1, 1, 1)):
        self.values = {}
        self.values['radius'] = radius
        self.values['thickness'] = thickness
        self.values['name'] = 'PolygonalDisk' + name
        self.values['vertices'] = []
        #self.values['cylinder'] = PolygonalCylinder(origin, origin + normal, radius)
        self.values['cylinder'] = PolygonalCylinderRotated()
        end = normal + origin * POLYGONAL_DISK_THICKNESS / origin.length()
        self.values['topPlane'] = Plane(normal=normal, origin=end)
        self.values['bottomPlane'] = Plane(normal= normal * (-1), origin=origin)

    def aspectRatio(self):
        return self.values['thickness'] / self.values['radius'] / 2

    def volume(self):
        return self.values['thickness'] * math.pi * self.values['radius'] ** 2
        
    def printToCSG(self, f=None):
        if f is None:
            print('Error, output file is not specified')
        f.write('solid ' + self.name() + ' = ')
        self.values['cylinder'].printToCSG(f)
        f.write(';\n')
        f.write('tlo {} -maxh=0.1;\n'.format(self.name()))
            
    def name(self):
        return self.values['name']


class SimulationCell():
    def __init__(self, edgeLength=CUBE_EDGE_LENGTH,
                 volumeFraction=VOLUME_FRACTION):
        self.fillersList = []
        self.edgeLength = edgeLength
        fillersNumber = VOLUME_FRACTION * CUBE_EDGE_LENGTH**3
        fillersNumber /= POLYGONAL_DISK_THICKNESS * POLYGONAL_DISK_RADIUS**2
        fillersNumber /= math.pi
        fillersNumber = int(fillersNumber)
        fillersVolume = fillersNumber * POLYGONAL_DISK_RADIUS**2
        fillersVolume *= POLYGONAL_DISK_THICKNESS * math.pi
        print('Filler number:', fillersNumber)
        print('Filler volume part:', fillersVolume / CUBE_EDGE_LENGTH**3)
        while self.fillersNumber() < fillersNumber:
            self.addFiller()
            
    def fillers(self):
        return self.fillersList
        
    def addFiller(self):
        filler = PolygonalDisk(name=str(self.fillersNumber()))
        self.fillersList.append(filler)
    
    def fillersNumber(self):
        return len(self.fillersList)

    def checkIntersections(self):
        pass

    def checkBoxCrossing(self):
        pass

    def checkDisksCrossing(self):
        pass

    def printCSG(self):
        f = open(FNAME, 'w')
        excludedMatrix = ''
        f.write('algebraic3d\n')
        f.write('solid cell = orthobrick(0.0, 0.0, 0.0; 10, 10, 10);\n')
        for filler in self.fillers():
            filler.printToCSG(f)
            excludedMatrix += ' and not ' + filler.name()
        f.write('solid matrix = cell' + excludedMatrix + ';\n')
        f.write('tlo matrix -transparent -maxh=0.3;')
        f.close()
        pass
    

def main(cubeSize=10, diskRadius=1, diskThickness=0.1):
    cell = SimulationCell()
    cell.printCSG()
    
    
main()
