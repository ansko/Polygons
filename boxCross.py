from Options import Options


def boxCross(disk):
    o = Options()
    cubeEdgeLength = o.getProperty('cubeEdgeLength')
    verticesNumber = disk.verticesNumber()
    vectorUp = disk.topCenter() - disk.bottomCenter()
    vectorUp /= 2
    for i, dot in enumerate(disk.facets()):
        vectorSide = disk.facets()[i - int(verticesNumber * 3 / 4)] - disk.facets()[i - int(verticesNumber / 4) ]
        vectorSide /= 2
        if ((dot + vectorUp + vectorSide).x() < 0 or 
            (dot + vectorUp + vectorSide).y() < 0 or
            (dot + vectorUp + vectorSide).z() < 0 or
            (dot + vectorUp + vectorSide).x() > cubeEdgeLength or
            (dot + vectorUp + vectorSide).y() > cubeEdgeLength or
            (dot + vectorUp + vectorSide).z() > cubeEdgeLength):
            return True
        if ((dot - vectorUp + vectorSide).x() < 0 or 
            (dot - vectorUp + vectorSide).y() < 0 or
            (dot - vectorUp + vectorSide).z() < 0 or
            (dot - vectorUp + vectorSide).x() > cubeEdgeLength or
            (dot - vectorUp + vectorSide).y() > cubeEdgeLength or
            (dot - vectorUp + vectorSide).z() > cubeEdgeLength):
            return True
        if ((dot + vectorUp - vectorSide).x() < 0 or 
            (dot + vectorUp - vectorSide).y() < 0 or
            (dot + vectorUp - vectorSide).z() < 0 or
            (dot + vectorUp - vectorSide).x() > cubeEdgeLength or
            (dot + vectorUp - vectorSide).y() > cubeEdgeLength or
            (dot + vectorUp - vectorSide).z() > cubeEdgeLength):
            return True
        if ((dot - vectorUp - vectorSide).x() < 0 or 
            (dot - vectorUp - vectorSide).y() < 0 or
            (dot - vectorUp - vectorSide).z() < 0 or
            (dot - vectorUp - vectorSide).x() > cubeEdgeLength or
            (dot - vectorUp - vectorSide).y() > cubeEdgeLength or
            (dot - vectorUp - vectorSide).z() > cubeEdgeLength):
            return True
    return False
