#!/usr/bin/env python3
# coding utf-8

import math
import random
import copy
import sys

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from DiskMadeOfDots import DiskMadeOfDots
from PlaneMadeOfDots import PlaneMadeOfDots
from Point import Point
from Vector import Vector

from boxCross import boxCross
from disksCross import disksCross
from planeLineIntersection import planeLineIntersection
from printCSGMain import printCSGMain
from utils import delta, det, decompose, orderParameter

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

def tactoidRecursive(disks=[], depths=DEPTHS, depth=0):
    if NUMBER_OF_DISKS > 99:
        print('Too deep deep recursion is need to make the structure!')
        sys.exit()
    timeToBreak = 0
    if len(disks) / EXFOLIATED_STACK_NUMBER == NUMBER_OF_DISKS:
        printCSGMain(disks, FNAME)
        sys.exit()
    inititalLength = len(disks)
    DEPTHSTMP = copy.deepcopy(depths)
    for attempt in range(RECURSION_MAX_ATTEMPTS):
        disksTmp = disks
        newDisks = []
        disk = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS / 2),
                              Point(0, 0, POLYGONAL_DISK_THICKNESS / 2),
                              POLYGONAL_DISK_RADIUS,
                              VERTICES_NUMBER)
        for stackI in range(0, int((EXFOLIATED_STACK_NUMBER - 1) / 2)):
            diskUp = DiskMadeOfDots(Point(0, 0, POLYGONAL_DISK_THICKNESS * (0.5 + stackI) + INTERLAYER_THICKNESS * (1 + stackI)),
                                    Point(0, 0, POLYGONAL_DISK_THICKNESS * (1.5 + stackI) + INTERLAYER_THICKNESS * (1 + stackI)),
                                    POLYGONAL_DISK_RADIUS,
                                    VERTICES_NUMBER)
            diskDown = DiskMadeOfDots(Point(0, 0, -POLYGONAL_DISK_THICKNESS * (0.5 + stackI) - INTERLAYER_THICKNESS * (1 + stackI)),
                                      Point(0, 0, -POLYGONAL_DISK_THICKNESS * (1.5 + stackI) - INTERLAYER_THICKNESS * (1 + stackI)),
                                      POLYGONAL_DISK_RADIUS,
                                      VERTICES_NUMBER)
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
        print('Depth = {0}, ready {1} of {2} '.format(DEPTHSTMP, len(disksTmp) / EXFOLIATED_STACK_NUMBER, NUMBER_OF_DISKS))
        if inititalLength != len(disksTmp):
            disks = tactoidRecursive(disksTmp, DEPTHSTMP, depth + 1)
    return disks
        
        
def mainTactoidRecursive():
    disks = tactoidRecursive()
    if len(disks) > 0:
        printCSGMain(disks, FNAME)
        sys.exit()


mainTactoidRecursive()
