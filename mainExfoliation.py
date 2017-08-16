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
            if disksCross(oldDisk, disk):
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


mainExfoliation()
