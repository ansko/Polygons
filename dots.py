#!/usr/bin/env python3
# coding utf-8

import math
import random
import copy
import sys

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

NUMBER_OF_DISKS = 5
MAX_ATTEMPTS = 10000
EPSILON = 10 ** (-10)
TOUCHING_DISKS_FRACTION = 0.02
RECURSION_MAX_ATTEMPTS = 10
DEPTHS = [0 for i in range(NUMBER_OF_DISKS)]

VERTICES_NUMBER = 16 # must be power of 2
VOLUME_FRACTION = 0.00033
CUBE_EDGE_LENGTH = 300
POLYGONAL_DISK_THICKNESS = 0.7
POLYGONAL_DISK_RADIUS = 50
INTERLAYER_THICKNESS = 0.3
INTERCALATED_INTERLAYER_THICKNESS = 3.3
INTERCALATED_STACK_NUMBER = 7 # -- should be odd
EXFOLIATED_STACK_NUMBER = 15  # /
FNAME = '1.geo'

Ef = 232
Em = 2
nu = 0.3


def delta(i, j):
    if i == j:
        return 1
    return 0


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
            dot = diskCenter + Point(radius * math.cos(2 * math.pi * i / VERTICES_NUMBER),
                                     radius * math.sin(2 * math.pi * i / VERTICES_NUMBER),
                                     0)
            self.values['facetsCenters'].append(dot)
            
    def facets(self):
        return self.values['facetsCenters']
        
    def center(self):
        return Point(self.values['bottomCenter'].x() / 2 + self.values['topCenter'].x() / 2,
                     self.values['bottomCenter'].y() / 2 + self.values['topCenter'].y() / 2,
                     self.values['bottomCenter'].z() / 2 + self.values['topCenter'].z() / 2)
        
    def mainAxe(self):
        dot1 = self.values['bottomCenter']
        dot2 = self.values['topCenter']
        return Vector(Point(0, 0, 0), Point(dot2.x() - dot1.x(),
                                            dot2.y() - dot2.y(),
                                            dot2.z() - dot2.z()))
                                            
    def bottomCenter(self):
        return self.values['bottomCenter']
        
    def topCenter(self):
        return self.values['topCenter']
    
    def edgeLength(self):
        alpha = math.pi / VERTICES_NUMBER
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
        #f.write('tlo ' + solidName + ' -maxh=0.1;\n')
        f.write('tlo ' + solidName + ';\n')
        
        
def det(M):
    l = len(M)
    if l == 0 or M is None:
        print('Error in determinant calculation!')
        return None
    if l == 1:
        return M[0][0]
    if l > 100:
        print('Too big matrix for the recursive algorithm.')
        return None
    result = 0
    for i in range(l):
        newM = []
        for j in range(1, l):
            newM.append(copy.deepcopy(M[j]))
            newM[j-1].pop(i)
        result += ((-1) ** i) * det(newM) * M[0][i]
    #if result == 0:
    #    pprint(M)
    return result


def boxCross(disk):
    vectorUp = disk.topCenter() - disk.bottomCenter()
    vectorUp /= 2
    for i, dot in enumerate(disk.facets()):
        vectorSide = disk.facets()[i - int(VERTICES_NUMBER * 3 / 4)] - disk.facets()[i - int(VERTICES_NUMBER / 4) ]
        vectorSide /= 2
        if ((dot + vectorUp + vectorSide).x() < 0 or 
            (dot + vectorUp + vectorSide).y() < 0 or
            (dot + vectorUp + vectorSide).z() < 0 or
            (dot + vectorUp + vectorSide).x() > CUBE_EDGE_LENGTH or
            (dot + vectorUp + vectorSide).y() > CUBE_EDGE_LENGTH or
            (dot + vectorUp + vectorSide).z() > CUBE_EDGE_LENGTH):
            return True
        if ((dot - vectorUp + vectorSide).x() < 0 or 
            (dot - vectorUp + vectorSide).y() < 0 or
            (dot - vectorUp + vectorSide).z() < 0 or
            (dot - vectorUp + vectorSide).x() > CUBE_EDGE_LENGTH or
            (dot - vectorUp + vectorSide).y() > CUBE_EDGE_LENGTH or
            (dot - vectorUp + vectorSide).z() > CUBE_EDGE_LENGTH):
            return True
        if ((dot + vectorUp - vectorSide).x() < 0 or 
            (dot + vectorUp - vectorSide).y() < 0 or
            (dot + vectorUp - vectorSide).z() < 0 or
            (dot + vectorUp - vectorSide).x() > CUBE_EDGE_LENGTH or
            (dot + vectorUp - vectorSide).y() > CUBE_EDGE_LENGTH or
            (dot + vectorUp - vectorSide).z() > CUBE_EDGE_LENGTH):
            return True
        if ((dot - vectorUp - vectorSide).x() < 0 or 
            (dot - vectorUp - vectorSide).y() < 0 or
            (dot - vectorUp - vectorSide).z() < 0 or
            (dot - vectorUp - vectorSide).x() > CUBE_EDGE_LENGTH or
            (dot - vectorUp - vectorSide).y() > CUBE_EDGE_LENGTH or
            (dot - vectorUp - vectorSide).z() > CUBE_EDGE_LENGTH):
            return True
    return False
    
    
def disksCross(disk1, disk2):
    bigDistance = 2 * (POLYGONAL_DISK_RADIUS**2 + POLYGONAL_DISK_THICKNESS**2)**0.5
    smallDistance = POLYGONAL_DISK_THICKNESS * 2
    # check if centers are very far from each other
    c1 = disk1.center()
    c2 = disk2.center()
    tc1 = disk1.topCenter()
    tc2 = disk2.topCenter()
    bc1 = disk1.bottomCenter()
    bc2 = disk2.bottomCenter()
    vector = Vector(c1, c2)
    if vector.length() > bigDistance:
        return False
    if vector.length() < smallDistance:
        return True
    # more accurate checking
    for i in range(len(disk1.facets())):
        vectorUp1 = disk1.topCenter() - disk1.bottomCenter()
        vectorUp1 /= 2
        vectorSide1 = disk1.facets()[i - int(VERTICES_NUMBER * 3 / 4)] - disk1.facets()[i - int(VERTICES_NUMBER / 4) ]
        vectorSide1 /= 2
        for j in range(len(disk2.facets())):
            vectorUp2 = disk2.topCenter() - disk2.bottomCenter()
            vectorUp2 /= 2
            vectorSide2 = disk2.facets()[i - int(VERTICES_NUMBER * 3 / 4)] - disk2.facets()[i - int(VERTICES_NUMBER / 4) ]
            vectorSide2 /= 2
            [flag, intersectionPoint] = planeLineIntersection(disk2.facets()[j], c2, disk1.facets()[i] - vectorUp1 - vectorSide1, disk1.facets()[i] + vectorUp1 + vectorSide1)
            if flag:
                if intersectionPoint is None:
                    return True
                vector = Vector(intersectionPoint, disk2.facets()[j])
                if vector.length() > POLYGONAL_DISK_THICKNESS**2 / 4 + POLYGONAL_DISK_RADIUS**2 / 4:
                    pass
                    #return False
    axeVector = tc1 - bc1          
    for i, facet1 in enumerate(disk1.facets()):
        if i == 0:
            continue
        basisVector1 = (disk1.facets()[i - 1] + disk1.facets()[i - 2] - c1 * 2) / 2
        basisVector2 = (disk1.facets()[i] + disk1.facets()[i - 1] - c1 * 2) / 2
        for j, facet2 in enumerate(disk2.facets()):
            if j == 0:
                continue
            angles = decompose1(axeVector, basisVector1, basisVector2, facet2)
            if not angles is None:
                [alpha, beta, gamma] = angles
            else:
                return True
            #print(alpha, beta, gamma)
            if abs(beta) + abs(gamma) < 1:
                #print(alpha, beta, gamma)
                return True
    return False


def disksCross1(disk1, disk2):
    bigDistance = 2 * (POLYGONAL_DISK_RADIUS**2 + POLYGONAL_DISK_THICKNESS**2)**0.5
    smallDistance = POLYGONAL_DISK_THICKNESS * 2
    # check if centers are very far from each other
    c1 = disk1.center()
    c2 = disk2.center()
    tc1 = disk1.topCenter()
    tc2 = disk2.topCenter()
    bc1 = disk1.bottomCenter()
    bc2 = disk2.bottomCenter()
    vector = Vector(c1, c2)
    if vector.length() > bigDistance:
        return False
    if vector.length() < smallDistance:
        return True
    # more accurate checking
    # facet-facet intersection
    axeVector = tc1 - bc1
    for i in range(1, len(disk1.facets()) - 1):
        basisVector1 = disk1.facets()[i - 1] / 2 + disk1.facets()[i] / 2
        basisVector2 = disk1.facets()[i + 1] / 2 + disk1.facets()[i] / 2
        for facet2 in disk2.facets():
            angles = decompose1(axeVector, basisVector1, basisVector2, facet2)
            if not angles is None:
                [alpha, beta, gamma] = angles
            else:
                return True
            if abs(beta) + abs(gamma) < 1:
                return True
    # facet-top/bottom intersection
    for j in range(1, len(disk2.facets())):
        top = planeLineIntersection(tc1, c1 - tc1, disk2.facets()[j - 1], disk2.facets()[j])
        if top[0] and Vector(tc1, top[1]).length() < POLYGONAL_DISK_RADIUS:
            return True
        bottom = planeLineIntersection(bc1, c1 - bc1, disk2.facets()[j - 1], disk2.facets()[j])
        if bottom[0] and Vector(bc1, bottom[1]).length() < POLYGONAL_DISK_RADIUS:
            return True
    return False

    
def decompose1(axeVector, basisVector1, basisVector2, point):
    x1 = axeVector.x()
    x2 = basisVector1.x()
    x3 = basisVector2.x()
    y1 = axeVector.y()
    y2 = basisVector1.y()
    y3 = basisVector2.y()
    z1 = axeVector.z()
    z2 = basisVector1.z()
    z3 = basisVector2.z()
    a = point.x()
    b = point.y()
    c = point.z()
    determinant = det([[x1, x2, x3], [y1, y2, y3], [z1, z2, z3]])
    if determinant < EPSILON:
        #print('Determinant = 0!')
        return None
    #print(determinant)
    alpha = det([[a, x2, x3], [b, y2, y3], [c, z2, z3]]) / determinant
    beta = det([[x1, a, x3], [y1, b, y3], [z1, c, z3]]) / determinant
    gamma = det([[x1, x2, a], [y1, y2, b], [z1, z2, c]]) / determinant
    return [alpha, beta, gamma]
    

def planeLineIntersection(pointOnPlane, normalOrigin, linePoint1, linePoint2):
    # from english wikipedia
    # (p - p0) * n = 0 - plane
    # p = d * l + l0 - line
    # d = (p0 - l0) * n / (l * n)
    # l * n = 0 -> (p0 - l0) * n = 0 - they are parallel
    #           -> else line lays in the plane
    # else there is one intersection point d * l + l0
    #
    # l = linePoint2 - linePoint1
    # l0 = linePoint1
    # n = facet - diskCenter
    # p0 = facet
    p0 = pointOnPlane
    l0 = linePoint1
    l = linePoint2 - linePoint1
    n = pointOnPlane - normalOrigin
    denominator = l.x() * n.x() + l.y() * n.y() + l.z() * n.z()
    numerator = (p0 - l0).x() * n.x() + (p0 - l0).y() * n.y() + (p0 - l0).z() * n.z()
    if abs(denominator) < EPSILON and abs(numerator) < EPSILON:
        return [True, None]
    elif abs(denominator) < EPSILON and abs(numerator) > EPSILON:
        return [False, None]
    elif abs(denominator) > EPSILON:
        intersectionPoint = l0 + l * numerator / denominator
        return [True, intersectionPoint]
    return True


def orderParameter(cosTheta):
    return (3 * cosTheta**2 - 1) / 2


def mainExfoliation(cubeSize=None, diskRadius=None, diskThickness=None):
    matrixString = 'solid matrix = cell'
    f = open(FNAME, 'w')
    f.write('algebraic3d;\n')
    f.write('solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'.format(CUBE_EDGE_LENGTH))
    #f.write('tlo cell -transparent;\n')
    disks = []
    attempt = 0
    while len(disks) < NUMBER_OF_DISKS:
        attempt += 1
        disk = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS/2), Point(0, 0, POLYGONAL_DISK_THICKNESS/2), POLYGONAL_DISK_RADIUS)
        alpha = random.random() * 2 * math.pi
        beta = random.random() * 2 * math.pi
        gamma = random.random() * 2 * math.pi
        x = random.random() * CUBE_EDGE_LENGTH
        y = random.random() * CUBE_EDGE_LENGTH
        z = random.random() * CUBE_EDGE_LENGTH
        c = math.cos(alpha)
        s = math.sin(alpha)
        Malpha = [[1, 0, 0],
                  [0, c, -s],
                  [0, s, c]]
        disk.rotate(Malpha)
        c = math.cos(beta)
        s = math.sin(beta)
        Mbeta = [[c, 0, s],
                 [0, 1, 0],
                 [-s, 0, c]]
        disk.rotate(Mbeta)
        c = math.cos(gamma)
        s = math.sin(gamma)
        Mgamma = [[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]]
        disk.rotate(Mgamma)
        disk.translate(Vector(Point(0, 0, 0), Point(x, y, z)))
        flag = 0
        for oldDisk in disks:
            if disksCross1(oldDisk, disk):
                flag = 1
                break
        if not boxCross(disk) and flag == 0:
            disks.append(disk)
        print('Try {0}, ready {1} of {2}'.format(attempt, len(disks), NUMBER_OF_DISKS))
        if attempt == MAX_ATTEMPTS:
            break
    for i, disk in enumerate(disks):
        randomnessX = 0
        randomnessY = 0
        randomnessZ = 0
        x = disk.mainAxe().x()
        y = disk.mainAxe().y()
        z = disk.mainAxe().z()
        l = disk.mainAxe().length()
        cosThetaX = x / l
        cosThetaY = y / l
        cosThetaZ = z / l
        randomnessX += orderParameter(cosThetaX)
        randomnessY += orderParameter(cosThetaY)
        randomnessZ += orderParameter(cosThetaZ)
        disk.printToCSG(f, 'Disk' + str(i))
        matrixString += ' and not Disk' + str(i)
    f.write(matrixString + ';\n')
    f.write('tlo matrix -transparent;\n')    
    f = open('matrices.txt', 'w')
    for i in range(len(disks) + 1):
        f.write('1 0 0 0 1 0 0 0 1;\n')
        
        
        
        
    f = open('materials.txt', 'w')
    C = [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]]
    #for i in range(3):
    #    C.append([])
    #    for j in range(3):
    #        C[i].append([])
    #        for k in range(3):
    #            C[i][j].append([])
    #            for l in range(3):
    #                C[i][j][k][l].append(0)
    la = Ef * nu / (1.0 - 2 * nu) / (1 + nu)
    mu = Ef / 2 / (1 + nu)
    for particle in range(len(disks)):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        brackets = delta(i, k) * delta(j, l)
                        brackets += delta(i, l) * delta(j, k)
                        C[i][j][k][l] = (la * delta(i, j) * delta(k, l) + mu * brackets)     
                        f.write(str(C[i][j][k][l]) + ' ')
    la = Em * nu / (1.0 - 2 * nu) / (1 + nu)
    mu = Em / 2 / (1 + nu)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    brackets = delta(i, k) * delta(j, l)
                    brackets += delta(i, l) * delta(j, k)
                    C[i][j][k][l] = (la * delta(i, j) * delta(k, l) + mu * brackets)     
                    f.write(str(C[i][j][k][l]) + ' ')
    print('Randomness along X axe: {}'.format(randomnessX / len(disks)))
    print('Randomness along Y axe: {}'.format(randomnessY / len(disks)))
    print('Randomness along Z axe: {}'.format(randomnessZ / len(disks)))
    diskVolume = math.pi * POLYGONAL_DISK_RADIUS**2 * POLYGONAL_DISK_THICKNESS
    allVolume = CUBE_EDGE_LENGTH**3
    part = len(disks) * diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))
    

def mainIntercalation(cubeSize=10, diskRadius=1, diskThickness=0.1):
    disks = []
    disksUp = []
    disksDown = []
    attempt = 0
    while len(disks) < NUMBER_OF_DISKS:
        attempt += 1
        disk = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS / 2),
                              Point(0, 0, POLYGONAL_DISK_THICKNESS / 2),
                              POLYGONAL_DISK_RADIUS)
        diskUp = DiskMadeOfDots(Point(0, 0, POLYGONAL_DISK_THICKNESS / 2 + INTERLAYER_THICKNESS),
                                Point(0, 0, 3 * POLYGONAL_DISK_THICKNESS / 2 + INTERLAYER_THICKNESS),
                                POLYGONAL_DISK_RADIUS)
        diskDown = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS/2 - INTERLAYER_THICKNESS),
                                  Point(0, 0, -3 * POLYGONAL_DISK_THICKNESS / 2 - INTERLAYER_THICKNESS),
                                  POLYGONAL_DISK_RADIUS)
        alpha = random.random() * 2 * math.pi
        beta = random.random() * 2 * math.pi
        gamma = random.random() * 2 * math.pi
        x = random.random() * CUBE_EDGE_LENGTH
        y = random.random() * CUBE_EDGE_LENGTH
        z = random.random() * CUBE_EDGE_LENGTH
        c = math.cos(alpha)
        s = math.sin(alpha)
        Malpha = [[1, 0, 0],
                  [0, c, -s],
                  [0, s, c]]
        disk.rotate(Malpha)
        diskUp.rotate(Malpha)
        diskDown.rotate(Malpha)
        c = math.cos(beta)
        s = math.sin(beta)
        Mbeta = [[c, 0, s],
                 [0, 1, 0],
                 [-s, 0, c]]
        disk.rotate(Mbeta)
        diskUp.rotate(Mbeta)
        diskDown.rotate(Mbeta)
        c = math.cos(gamma)
        s = math.sin(gamma)
        Mgamma = [[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]]
        disk.rotate(Mgamma)
        diskUp.rotate(Mgamma)
        diskDown.rotate(Mgamma)
        disk.translate(Vector(Point(0, 0, 0), Point(x, y, z)))
        diskUp.translate(Vector(Point(0, 0, 0), Point(x, y, z)))
        diskDown.translate(Vector(Point(0, 0, 0), Point(x, y, z)))
        flag = 0
        for oldDisk in disks:
            if disksCross1(oldDisk, disk) or disksCross1(oldDisk, diskUp) or disksCross1(oldDisk, diskDown):
                flag = 1
                break
        if not (boxCross(disk) or boxCross(diskUp) or boxCross(diskDown)) and flag == 0:
            disks.append(disk)
            disksUp.append(diskUp)
            disksDown.append(diskDown)
        print('Try {0}, ready {1} of {2}'.format(attempt, len(disks), NUMBER_OF_DISKS))
        if attempt == MAX_ATTEMPTS:
            break
    matrixString = 'solid matrix = cell'
    f = open(FNAME, 'w')
    f.write('algebraic3d;\n')
    f.write('solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'.format(CUBE_EDGE_LENGTH))
    #f.write('tlo cell -transparent;\n')
    for i, disk in enumerate(disks):
        matrixString += ' and not Disk' + str(i)
        randomnessX = 0
        randomnessY = 0
        randomnessZ = 0
        x = disk.mainAxe().x()
        y = disk.mainAxe().y()
        z = disk.mainAxe().z()
        l = disk.mainAxe().length()
        cosThetaX = x / l
        cosThetaY = y / l
        cosThetaZ = z / l
        randomnessX += orderParameter(cosThetaX)
        randomnessY += orderParameter(cosThetaY)
        randomnessZ += orderParameter(cosThetaZ)
        disk.printToCSG(f, 'Disk' + str(i))
    for i, disk in enumerate(disksUp):
        disk.printToCSG(f, 'DiskUp' + str(i))
        matrixString += ' and not DiskUp' + str(i)
    for i, disk in enumerate(disksDown):
        disk.printToCSG(f, 'DiskDown' + str(i))
        matrixString += ' and not DiskDown' + str(i)
    f.write(matrixString + ';\n')
    f.write('tlo matrix -transparent -maxh=0.3;\n')
    print('Randomness along X axe: {}'.format(randomnessX / len(disks)))
    print('Randomness along Y axe: {}'.format(randomnessY / len(disks)))
    print('Randomness along Z axe: {}'.format(randomnessZ / len(disks)))
    diskVolume = math.pi * POLYGONAL_DISK_RADIUS**2 * POLYGONAL_DISK_THICKNESS
    allVolume = CUBE_EDGE_LENGTH**3
    part = len(disks) * diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))


def mainIntercalation2(cubeSize=10, diskRadius=1, diskThickness=0.1):
    disks = []
    attempt = 0
    while len(disks) / INTERCALATED_STACK_NUMBER < NUMBER_OF_DISKS:
        newDisks = []
        attempt += 1
        disk = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS / 2),
                              Point(0, 0, POLYGONAL_DISK_THICKNESS / 2),
                              POLYGONAL_DISK_RADIUS)
        for stackI in range(0, int((INTERCALATED_STACK_NUMBER - 1) / 2)):
            diskUp = DiskMadeOfDots(Point(0, 0, POLYGONAL_DISK_THICKNESS * (0.5 + stackI) + INTERCALATED_INTERLAYER_THICKNESS * (1 + stackI)),
                                    Point(0, 0, POLYGONAL_DISK_THICKNESS * (1.5 + stackI) + INTERCALATED_INTERLAYER_THICKNESS * (1 + stackI)),
                                    POLYGONAL_DISK_RADIUS)
            diskDown = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS * (0.5 + stackI) - INTERCALATED_INTERLAYER_THICKNESS * (1 + stackI)),
                                      Point(0, 0, -POLYGONAL_DISK_THICKNESS * (1.5 + stackI) - INTERCALATED_INTERLAYER_THICKNESS * (1 + stackI)),
                                      POLYGONAL_DISK_RADIUS)
            newDisks.append(diskUp)
            newDisks.append(diskDown)
            pass
        newDisks.append(disk)
        alpha = random.random() * 2 * math.pi
        beta = random.random() * 2 * math.pi
        gamma = random.random() * 2 * math.pi
        x = random.random() * CUBE_EDGE_LENGTH
        y = random.random() * CUBE_EDGE_LENGTH
        z = random.random() * CUBE_EDGE_LENGTH
        c = math.cos(alpha)
        s = math.sin(alpha)
        Malpha = [[1, 0, 0],
                  [0, c, -s],
                  [0, s, c]]
        for disk in newDisks:
            disk.rotate(Malpha)
        c = math.cos(beta)
        s = math.sin(beta)
        Mbeta = [[c, 0, s],
                 [0, 1, 0],
                 [-s, 0, c]]
        for disk in newDisks:
            disk.rotate(Mbeta)
        c = math.cos(gamma)
        s = math.sin(gamma)
        Mgamma = [[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]]
        for disk in newDisks:
            disk.rotate(Mgamma)
        for disk in newDisks:
            disk.translate(Vector(Point(0, 0, 0), Point(x, y, z)))
        flag = 0
        for oldDisk in disks:
            for disk in newDisks:
                if disksCross1(oldDisk, disk):
                    flag = 1
                    break
        for disk in newDisks:
            if boxCross(disk):
                flag = 1
                break
        if flag == 0:
            for disk in newDisks:
                disks.append(disk)
        print('Try {0}, ready {1} of {2}'.format(attempt, len(disks) / INTERCALATED_STACK_NUMBER, NUMBER_OF_DISKS))
        if attempt == MAX_ATTEMPTS:
            break
    matrixString = 'solid matrix = cell'
    f = open(FNAME, 'w')
    f.write('algebraic3d;\n')
    f.write('solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'.format(CUBE_EDGE_LENGTH))
    #f.write('tlo cell -transparent;\n')
    for i, disk in enumerate(disks):
        matrixString += ' and not Disk' + str(i)
        randomnessX = 0
        randomnessY = 0
        randomnessZ = 0
        x = disk.mainAxe().x()
        y = disk.mainAxe().y()
        z = disk.mainAxe().z()
        l = POLYGONAL_DISK_THICKNESS#disk.mainAxe().length()
        cosThetaX = x / l
        cosThetaY = y / l
        cosThetaZ = z / l
        randomnessX += orderParameter(cosThetaX)
        randomnessY += orderParameter(cosThetaY)
        randomnessZ += orderParameter(cosThetaZ)
        disk.printToCSG(f, 'Disk' + str(i))
    f.write(matrixString + ';\n')
    f.write('tlo matrix -transparent -maxh=0.3;\n')
    print('Randomness along X axe: {}'.format(randomnessX / len(disks)))
    print('Randomness along Y axe: {}'.format(randomnessY / len(disks)))
    print('Randomness along Z axe: {}'.format(randomnessZ / len(disks)))
    diskVolume = math.pi * POLYGONAL_DISK_RADIUS**2 * POLYGONAL_DISK_THICKNESS
    allVolume = CUBE_EDGE_LENGTH**3
    part = len(disks) * diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))
    

def mainTactoid(cubeSize=None, diskRadius=None, diskThickness=None):
    disks = []
    attempt = 0
    while len(disks) / EXFOLIATED_STACK_NUMBER < NUMBER_OF_DISKS:
        newDisks = []
        attempt += 1
        disk = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS / 2),
                              Point(0, 0, POLYGONAL_DISK_THICKNESS / 2),
                              POLYGONAL_DISK_RADIUS)
        for stackI in range(0, int((EXFOLIATED_STACK_NUMBER - 1) / 2)):
            diskUp = DiskMadeOfDots(Point(0, 0, POLYGONAL_DISK_THICKNESS * (0.5 + stackI) + INTERLAYER_THICKNESS * (1 + stackI)),
                                    Point(0, 0, POLYGONAL_DISK_THICKNESS * (1.5 + stackI) + INTERLAYER_THICKNESS * (1 + stackI)),
                                    POLYGONAL_DISK_RADIUS)
            diskDown = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS * (0.5 + stackI) - INTERLAYER_THICKNESS * (1 + stackI)),
                                      Point(0, 0, -POLYGONAL_DISK_THICKNESS * (1.5 + stackI) - INTERLAYER_THICKNESS * (1 + stackI)),
                                      POLYGONAL_DISK_RADIUS)
            newDisks.append(diskUp)
            newDisks.append(diskDown)
            pass
        newDisks.append(disk)
        alpha = random.random() * 2 * math.pi
        beta = random.random() * 2 * math.pi
        gamma = random.random() * 2 * math.pi
        x = random.random() * CUBE_EDGE_LENGTH
        y = random.random() * CUBE_EDGE_LENGTH
        z = random.random() * CUBE_EDGE_LENGTH
        c = math.cos(alpha)
        s = math.sin(alpha)
        Malpha = [[1, 0, 0],
                  [0, c, -s],
                  [0, s, c]]
        for disk in newDisks:
            disk.rotate(Malpha)
        c = math.cos(beta)
        s = math.sin(beta)
        Mbeta = [[c, 0, s],
                 [0, 1, 0],
                 [-s, 0, c]]
        for disk in newDisks:
            disk.rotate(Mbeta)
        c = math.cos(gamma)
        s = math.sin(gamma)
        Mgamma = [[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]]
        for disk in newDisks:
            disk.rotate(Mgamma)
        for disk in newDisks:
            disk.translate(Vector(Point(0, 0, 0), Point(x, y, z)))
        flag = 0
        for oldDisk in disks:
            for disk in newDisks:
                if disksCross1(oldDisk, disk):
                    flag = 1
                    break
        for disk in newDisks:
            if boxCross(disk):
                flag = 1
                break
        if flag == 0:
            for disk in newDisks:
                disks.append(disk)
        print('Try {0}, ready {1} of {2}'.format(attempt, len(disks) / EXFOLIATED_STACK_NUMBER, NUMBER_OF_DISKS))
        if attempt == MAX_ATTEMPTS:
            break
    matrixString = 'solid matrix = cell'
    f = open(FNAME, 'w')
    f.write('algebraic3d;\n')
    f.write('solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'.format(CUBE_EDGE_LENGTH))
    #f.write('tlo cell -transparent;\n')
    for i, disk in enumerate(disks):
        matrixString += ' and not Disk' + str(i)
        randomnessX = 0
        randomnessY = 0
        randomnessZ = 0
        x = disk.mainAxe().x()
        y = disk.mainAxe().y()
        z = disk.mainAxe().z()
        l = POLYGONAL_DISK_THICKNESS#disk.mainAxe().length()
        cosThetaX = x / l
        cosThetaY = y / l
        cosThetaZ = z / l
        randomnessX += orderParameter(cosThetaX)
        randomnessY += orderParameter(cosThetaY)
        randomnessZ += orderParameter(cosThetaZ)
        disk.printToCSG(f, 'Disk' + str(i))
    f.write(matrixString + ';\n')
    f.write('tlo matrix -transparent -maxh=0.3;\n')
    print('Randomness along X axe: {}'.format(randomnessX / len(disks)))
    print('Randomness along Y axe: {}'.format(randomnessY / len(disks)))
    print('Randomness along Z axe: {}'.format(randomnessZ / len(disks)))
    diskVolume = math.pi * POLYGONAL_DISK_RADIUS**2 * POLYGONAL_DISK_THICKNESS
    diskVolume += len(disks) / EXFOLIATED_STACK_NUMBER * (EXFOLIATED_STACK_NUMBER - 1) * math.pi * POLYGONAL_DISK_RADIUS**2 * INTERLAYER_THICKNESS
    allVolume = CUBE_EDGE_LENGTH**3
    part = len(disks) * diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))
    

def printCSGmain(disks):
    f = open(FNAME, 'w')
    f.write('algebraic3d;\n')
    f.write('solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'.format(CUBE_EDGE_LENGTH))
    #f.write('tlo cell -transparent;\n')
    matrixString = 'solid matrix = cell'
    for i, disk in enumerate(disks):
        matrixString += ' and not Disk' + str(i)
        randomnessX = 0
        randomnessY = 0
        randomnessZ = 0
        x = disk.mainAxe().x()
        y = disk.mainAxe().y()
        z = disk.mainAxe().z()
        l = POLYGONAL_DISK_THICKNESS#disk.mainAxe().length()
        cosThetaX = x / l
        cosThetaY = y / l
        cosThetaZ = z / l
        randomnessX += orderParameter(cosThetaX)
        randomnessY += orderParameter(cosThetaY)
        randomnessZ += orderParameter(cosThetaZ)
        disk.printToCSG(f, 'Disk' + str(i))
    f.write(matrixString + ';\n')
    f.write('tlo matrix -transparent -maxh=0.3;\n')
    print('Randomness along X axe: {}'.format(randomnessX / len(disks)))
    print('Randomness along Y axe: {}'.format(randomnessY / len(disks)))
    print('Randomness along Z axe: {}'.format(randomnessZ / len(disks)))
    diskVolume = len(disks) * math.pi * POLYGONAL_DISK_RADIUS**2 * POLYGONAL_DISK_THICKNESS
    diskVolume += len(disks) / EXFOLIATED_STACK_NUMBER * (EXFOLIATED_STACK_NUMBER - 1) * math.pi * POLYGONAL_DISK_RADIUS**2 * INTERLAYER_THICKNESS
    allVolume = CUBE_EDGE_LENGTH**3
    part = diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))
    
    sys.exit()


def tactoidRecursive(disks=[], depths=DEPTHS, depth=0):
    if NUMBER_OF_DISKS > 99:
        print('Too deep deep recursion is need to make the structure!')
        sys.exit()

    attempt = 0
    timeToBreak = 0

    if len(disks) / EXFOLIATED_STACK_NUMBER == NUMBER_OF_DISKS:
        printCSGmain(disks)

    inititalLength = len(disks)
    DEPTHSTMP = copy.deepcopy(depths)
    for attempt in range(RECURSION_MAX_ATTEMPTS):
        disksTmp = disks
        newDisks = []
        disk = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS / 2),
                              Point(0, 0, POLYGONAL_DISK_THICKNESS / 2),
                              POLYGONAL_DISK_RADIUS)
        for stackI in range(0, int((EXFOLIATED_STACK_NUMBER - 1) / 2)):
            diskUp = DiskMadeOfDots(Point(0, 0, POLYGONAL_DISK_THICKNESS * (0.5 + stackI) + INTERLAYER_THICKNESS * (1 + stackI)),
                                    Point(0, 0, POLYGONAL_DISK_THICKNESS * (1.5 + stackI) + INTERLAYER_THICKNESS * (1 + stackI)),
                                    POLYGONAL_DISK_RADIUS)
            diskDown = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS * (0.5 + stackI) - INTERLAYER_THICKNESS * (1 + stackI)),
                                      Point(0, 0, -POLYGONAL_DISK_THICKNESS * (1.5 + stackI) - INTERLAYER_THICKNESS * (1 + stackI)),
                                      POLYGONAL_DISK_RADIUS)
            newDisks.append(diskUp)
            newDisks.append(diskDown)
        newDisks.append(disk)
    
        alpha = random.random() * 2 * math.pi
        beta = random.random() * 2 * math.pi
        gamma = random.random() * 2 * math.pi
        x = random.random() * CUBE_EDGE_LENGTH
        y = random.random() * CUBE_EDGE_LENGTH
        z = random.random() * CUBE_EDGE_LENGTH
        c = math.cos(alpha)
        s = math.sin(alpha)
        Malpha = [[1, 0, 0],
                  [0, c, -s],
                  [0, s, c]]
        for disk in newDisks:
            disk.rotate(Malpha)
        c = math.cos(beta)
        s = math.sin(beta)
        Mbeta = [[c, 0, s],
                 [0, 1, 0],
                 [-s, 0, c]]
        for disk in newDisks:
            disk.rotate(Mbeta)
        c = math.cos(gamma)
        s = math.sin(gamma)
        Mgamma = [[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]]
        for disk in newDisks:
            disk.rotate(Mgamma)
        for disk in newDisks:
            disk.translate(Vector(Point(0, 0, 0), Point(x, y, z)))
        flag = 0
        for oldDisk in disks:
            if flag == 1:
                break
            for disk in newDisks:
                if disksCross1(oldDisk, disk):
                    flag = 1
                    print('Crossing another disk ', end='')
                    break
        for disk in newDisks:
            if boxCross(disk):
                flag = 1
                print('Crossing the box ', end='')
                break
        if flag == 0:
            for disk in newDisks:
                disksTmp.append(disk)
        DEPTHSTMP[depth] += 1
        print('Depth = {0}, attempt = {3}, ready {1} of {2} '.format(DEPTHSTMP, len(disksTmp) / EXFOLIATED_STACK_NUMBER, NUMBER_OF_DISKS, attempt))
        if inititalLength != len(disksTmp):
            disks = tactoidRecursive(disksTmp, DEPTHSTMP, depth + 1)
    return disks#printCSGmain(disks)
        
        
def mainTactoidRecursive():
    disks = tactoidRecursive()
    if len(disks) > 0:
        printCSGmain(disks)


mainExfoliation()
#mainIntercalation2()
#mainTactoid()
#mainTactoidRecursive()
