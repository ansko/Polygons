import math

from Options import Options
from utils import orderParameter


def printCSGMain(disks, fname):
    o = Options()
    cubeEdgeLength = o.getProperty('cubeEdgeLength')
    polygonalDiskRadius = o.getProperty('polygonalDiskRadius')
    polygonalDiskThickness = o.getProperty('polygonalDiskThickness')
    intercalatedStackNumber = o.getProperty('intercalatedStackNumber')
    intercalatedInterlayerThickness = o.getProperty('intercalatedInterlayerThickness')
    f = open(fname, 'w')
    f.write('algebraic3d;\n')
    string = 'solid cell = orthobrick(0, 0, 0; {0}, {0}, {0});\n'
    f.write(string.format(cubeEdgeLength))
    matrixString = 'solid matrix = cell'
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
    singleDiskVolume = math.pi * polygonalDiskRadius**2 * polygonalDiskThickness
    interlayerVolume = math.pi * polygonalDiskRadius**2 * intercalatedInterlayerThickness
    interlayerVolume *= intercalatedStackNumber - 1
    diskVolume = len(disks) * singleDiskVolume
    diskVolume += len(disks) / intercalatedStackNumber * interlayerVolume
    allVolume = cubeEdgeLength ** 3
    part = diskVolume / allVolume
    print('Volume part of fillers is {}'.format(part))