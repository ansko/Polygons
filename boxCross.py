CUBE_EDGE_LENGTH = 300


def boxCross(disk):
    verticesNumber = disk.verticesNumber()
    vectorUp = disk.topCenter() - disk.bottomCenter()
    vectorUp /= 2
    for i, dot in enumerate(disk.facets()):
        vectorSide = disk.facets()[i - int(verticesNumber * 3 / 4)] - disk.facets()[i - int(verticesNumber / 4) ]
        vectorSide /= 2
        if ((dot + vectorUp + vectorSide).x() < 0 or 
            (dot + vectorUp + vectorSide).y() < 0 or
            (dot + vectorUp + vectorSide).z() < 0 or
            (dot + vectorUp + vectorSide).x() > CUBE_EDGE_LENGTH or
            (dot + vectorUp + vectorSide).y() > CUBE_EDGE_LENGTH or
            (dot + vectorUp + vectorSide).z() > CUBE_EDGE_LENGTH):
            return True
        if ((dot - vectorUp + vectorSide).x() < 0 or 
            (dot - vectorUp + vectorSide).y() < 0 or
            (dot - vectorUp + vectorSide).z() < 0 or
            (dot - vectorUp + vectorSide).x() > CUBE_EDGE_LENGTH or
            (dot - vectorUp + vectorSide).y() > CUBE_EDGE_LENGTH or
            (dot - vectorUp + vectorSide).z() > CUBE_EDGE_LENGTH):
            return True
        if ((dot + vectorUp - vectorSide).x() < 0 or 
            (dot + vectorUp - vectorSide).y() < 0 or
            (dot + vectorUp - vectorSide).z() < 0 or
            (dot + vectorUp - vectorSide).x() > CUBE_EDGE_LENGTH or
            (dot + vectorUp - vectorSide).y() > CUBE_EDGE_LENGTH or
            (dot + vectorUp - vectorSide).z() > CUBE_EDGE_LENGTH):
            return True
        if ((dot - vectorUp - vectorSide).x() < 0 or 
            (dot - vectorUp - vectorSide).y() < 0 or
            (dot - vectorUp - vectorSide).z() < 0 or
            (dot - vectorUp - vectorSide).x() > CUBE_EDGE_LENGTH or
            (dot - vectorUp - vectorSide).y() > CUBE_EDGE_LENGTH or
            (dot - vectorUp - vectorSide).z() > CUBE_EDGE_LENGTH):
            return True
    return False
