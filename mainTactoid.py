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


def mainTactoid(cubeSize=None, diskRadius=None, diskThickness=None):
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
    interlayerThickness = o.getProperty('tactoidInterlayerThickness')
    tactoidStackNumber = o.getProperty('tactoidStackNumber')

    disks = []
    attempt = 0
    while len(disks) / tactoidStackNumber < numberOfDisks:
        newDisks = []
        attempt += 1
        disk = DiskMadeOfDots(Point(0, 0, -polygonalDiskThickness / 2),
                              Point(0, 0, polygonalDiskThickness / 2),
                              polygonalDiskRadius)
        for stackI in range(0, int((tactoidStackNumber - 1) / 2)):
            z1 = (polygonalDiskThickness * (0.5 + stackI) +
                  interlayerThickness * (1 + stackI))
            z2 = (polygonalDiskThickness * (1.5 + stackI) +
                  interlayerThickness * (1 + stackI))
            diskUp = DiskMadeOfDots(Point(0, 0, z1),
                                    Point(0, 0, z2),
                                    polygonalDiskRadius)
            diskDown = DiskMadeOfDots(Point(0, 0, -z1),
                                      Point(0, 0, -z2),
                                      polygonalDiskRadius)
            newDisks.append(diskUp)
            newDisks.append(diskDown)
            pass
        newDisks.append(disk)
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
                if disksCross(oldDisk, disk):
                    flag = 1
                    break
        for disk in newDisks:
            if boxCross(disk):
                flag = 1
                break
        if flag == 0:
            for disk in newDisks:
                disks.append(disk)
        string = 'Try {0}, ready {1} of {2}'
        overall = int(len(disks) / tactoidStackNumber)
        print(string.format(attempt, overall, numberOfDisks))
        if attempt == maxAttempts:
            break
    matrixString = 'solid matrix = cell'
    f = open(fname, 'w')
    f.write('algebraic3d;\n')
    string = 'solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'
    f.write(string.format(cubeEdgeLength))
    #f.write('tlo cell -transparent;\n')
    for i, disk in enumerate(disks):
        matrixString += ' and not Disk' + str(i)
        randomnessX = 0
        randomnessY = 0
        randomnessZ = 0
        x = disk.mainAxe().x()
        y = disk.mainAxe().y()
        z = disk.mainAxe().z()
        l = polygonalDiskThickness
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
    diskVolume = math.pi * polygonalDiskRadius**2 * polygonalDiskThickness
    tactoidsNum = len(disks) / tactoidStackNumber
    interlayerVolume = math.pi * polygonalDiskRadius**2 * interlayerThickness
    diskVolume += tactoidsNum * (tactoidStackNumber - 1) * interlayerVolume
    allVolume = cubeEdgeLength**3
    part = len(disks) * diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))


mainTactoid()
