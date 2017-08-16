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


def mainIntercalation(cubeSize=10, diskRadius=1, diskThickness=0.1):
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
    interlayerThickness = o.getProperty('interlayerThickness')

    disks = []
    disksUp = []
    disksDown = []
    attempt = 0
    while len(disks) < numberOfDisks:
        attempt += 1
        disk = DiskMadeOfDots(Point(0, 0, -polygonalDiskThickness / 2),
                              Point(0, 0, polygonalDiskThickness / 2),
                              polygonalDiskRadius)
        diskUp = DiskMadeOfDots(Point(0, 0, polygonalDiskThickness / 2 + interlayerThickness),
                                Point(0, 0, 3 * polygonalDiskThickness / 2 + interlayerThickness),
                                polygonalDiskRadius)
        diskDown = DiskMadeOfDots(Point(0, 0, -polygonalDiskThickness/2 - interlayerThickness),
                                  Point(0, 0, -3 * polygonalDiskThickness / 2 - interlayerThickness),
                                  polygonalDiskRadius)
        alpha = random.random() * 2 * math.pi
        beta = random.random() * 2 * math.pi
        gamma = random.random() * 2 * math.pi
        x = random.random() * cubeEdgeLength
        y = random.random() * cubeEdgeLength
        z = random.random() * cubeEdgeLength
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
            if disksCross(oldDisk, disk) or disksCross(oldDisk, diskUp) or disksCross(oldDisk, diskDown):
                flag = 1
                break
        if not (boxCross(disk) or boxCross(diskUp) or boxCross(diskDown)) and flag == 0:
            disks.append(disk)
            disksUp.append(diskUp)
            disksDown.append(diskDown)
        print('Try {0}, ready {1} of {2}'.format(attempt, len(disks), numberOfDisks))
        if attempt == maxAttempts:
            break
    matrixString = 'solid matrix = cell'
    f = open(fname, 'w')
    f.write('algebraic3d;\n')
    f.write('solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'.format(cubeEdgeLength))
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
    diskVolume = math.pi * polygonalDiskRadius**2 * polygonalDiskThickness
    allVolume = cubeEdgeLength**3
    part = len(disks) * diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))


mainIntercalation()
