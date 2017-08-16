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
