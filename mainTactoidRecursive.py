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


def tactoidRecursive(disks=[], depths=None, depth=0):
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
    verticesNumber = o.getProperty('verticesNumber')
    recursionMaxAttempts = o.getProperty('recursionMaxAttempts')

    if numberOfDisks > 99:
        print('Too deep deep recursion is need to make the structure!')
        sys.exit()
    timeToBreak = 0
    if len(disks) / tactoidStackNumber == numberOfDisks:
        printCSGMain(disks, fname)
        sys.exit()
    inititalLength = len(disks)
    DEPTHSTMP = copy.deepcopy(depths)
    for attempt in range(int(recursionMaxAttempts)):
        disksTmp = disks
        newDisks = []
        disk = DiskMadeOfDots(Point(0, 0, -polygonalDiskThickness / 2),
                              Point(0, 0, polygonalDiskThickness / 2),
                              polygonalDiskRadius,
                              verticesNumber)
        for stackI in range(0, int((tactoidStackNumber - 1) / 2)):
            diskUp = DiskMadeOfDots(Point(0, 0, polygonalDiskThickness * (0.5 + stackI) + interlayerThickness * (1 + stackI)),
                                    Point(0, 0, polygonalDiskThickness * (1.5 + stackI) + interlayerThickness * (1 + stackI)),
                                    polygonalDiskRadius,
                                    verticesNumber)
            diskDown = DiskMadeOfDots(Point(0, 0, -polygonalDiskThickness * (0.5 + stackI) - interlayerThickness * (1 + stackI)),
                                      Point(0, 0, -polygonalDiskThickness * (1.5 + stackI) - interlayerThickness * (1 + stackI)),
                                      polygonalDiskRadius,
                                      verticesNumber)
            newDisks.append(diskUp)
            newDisks.append(diskDown)
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
            if flag == 1:
                break
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
                disksTmp.append(disk)
        DEPTHSTMP[depth] += 1
        print('Depth = {0}, ready {1} of {2} '.format(DEPTHSTMP, len(disksTmp) / tactoidStackNumber, numberOfDisks))
        if inititalLength != len(disksTmp):
            disks = tactoidRecursive(disksTmp, DEPTHSTMP, depth + 1)
    return disks
        
        
def mainTactoidRecursive():
    o = Options() 
    depths=[0 for i in range(int(o.getProperty('numberOfDisks')))]
    disks = tactoidRecursive(disks=[], depths=depths)
    fname = o.getProperty('fname')
    if len(disks) > 0:
        printCSGMain(disks, fname)
        sys.exit()


mainTactoidRecursive()
