#!/usr/bin/env python3
# coding utf-8

import math
import random
import copy
import sys

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from DiskMadeOfDots import DiskMadeOfDots
from Options import Options
from PlaneMadeOfDots import PlaneMadeOfDots
from Point import Point
from Vector import Vector

from boxCross import boxCross
from disksCross import disksCross
from planeLineIntersection import planeLineIntersection
from printCSGMain import printCSGMain
from utils import delta, det, decompose, orderParameter


def mainExfoliation(cubeSize=None, diskRadius=None, diskThickness=None):
    o = Options()
    cubeEdgeLength = o.getProperty('cubeEdgeLength')
    numberOfDisks = o.getProperty('numberOfDisks')
    polygonalDiskThickness = o.getProperty('polygonalDiskThickness')
    polygonalDiskRadius = o.getProperty('polygonalDiskRadius')
    numberOfDisks = o.getProperty('numberOfDisks')
    maxAttempts = o.getProperty('maxAttempts')
    E_m = o.getProperty('E_m')
    nu_m = o.getProperty('nu_m')
    E_f = o.getProperty('E_f')
    nu_f = o.getProperty('nu_f')
    fname = o.getProperty('fname')

    matrixString = 'solid matrix = cell'
    f = open(fname, 'w')
    f.write('algebraic3d;\n')
    f.write('solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'.format(cubeEdgeLength))
    #f.write('tlo cell -transparent;\n')
    disks = []
    attempt = 0
    while len(disks) < numberOfDisks:
        attempt += 1
        z = polygonalDiskThickness / 2
        disk = DiskMadeOfDots(Point(0, 0, -z), Point(0, 0, z), polygonalDiskRadius)
        coef = 2
        alpha = random.random() * coef * math.pi
        beta = random.random() * coef * math.pi
        gamma = random.random() * coef * math.pi
        x = random.random() * cubeEdgeLength
        y = random.random() * cubeEdgeLength
        z = random.random() * cubeEdgeLength
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
            if disksCross(oldDisk, disk):
                flag = 1
                break
        if not boxCross(disk) and flag == 0:
            disks.append(disk)
        print('Try {0}, ready {1} of {2}'.format(attempt, len(disks), numberOfDisks))
        if attempt == maxAttempts:
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
        f.write('1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0\n')
    f = open('materials.txt', 'w')
    C = [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
          [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
          [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
         [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
          [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
          [[0, 0, 0], [0, 0, 0], [0, 0, 0]]],
         [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
          [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
          [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]]
    la = E_f * nu_f / (1.0 - 2 * nu_f) / (1 + nu_f)
    mu = E_f / 2 / (1 + nu_f)
    for particle in range(len(disks)):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        brackets = delta(i, k) * delta(j, l)
                        brackets += delta(i, l) * delta(j, k)
                        C[i][j][k][l] = (la * delta(i, j) * delta(k, l) + mu * brackets)     
                        f.write(str(C[i][j][k][l]) + ' ')
    la = E_m * nu_m / (1.0 - 2 * nu_m) / (1 + nu_m)
    mu = E_m / 2 / (1 + nu_m)
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
    diskVolume = math.pi * polygonalDiskRadius**2 * polygonalDiskThickness
    allVolume = cubeEdgeLength**3
    part = len(disks) * diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))


mainExfoliation()
