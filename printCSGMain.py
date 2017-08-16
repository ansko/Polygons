import math

from utils import orderParameter

CUBE_EDGE_LENGTH = 300
POLYGONAL_DISK_THICKNESS = 0.7
POLYGONAL_DISK_RADIUS = 50
EXFOLIATED_STACK_NUMBER = 15  # /
INTERLAYER_THICKNESS = 0.3


def printCSGMain(disks, fname):
    f = open(fname, 'w')
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
    
  #  sys.exit()
