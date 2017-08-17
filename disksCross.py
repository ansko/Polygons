import sys
import math

from Options import Options
from Point import Point
from Vector import Vector

from planeLineIntersection import planeLineIntersection
from utils import decompose, det


def disksCross(disk1, disk2):
    o = Options()
    verticesNumber = o.getProperty('verticesNumber')
    polygonalDiskRadius = o.getProperty('polygonalDiskRadius')
    polygonalDiskThickness = o.getProperty('polygonalDiskThickness')
    bigDistance = 2 * (polygonalDiskRadius**2 + polygonalDiskThickness**2)**0.5
    smallDistance = polygonalDiskThickness * 2
    # check if centers are very far from each other
    c1 = disk1.center()
    c2 = disk2.center()
    tc1 = disk1.topCenter()
    tc2 = disk2.topCenter()
    bc1 = disk1.bottomCenter()
    bc2 = disk2.bottomCenter()
    vector = Vector(c1, c2)
    if vector.length() > bigDistance:
        return False
    if vector.length() < smallDistance:
        return True
    # more accurate checking
    # facet-facet intersection
    axeVector = tc1 - bc1
    for i in range(1, len(disk1.facets()) - 1):
        basisVector1 = disk1.facets()[i - 1] / 2 + disk1.facets()[i] / 2
        basisVector2 = disk1.facets()[i + 1] / 2 + disk1.facets()[i] / 2
        for facet2 in disk2.facets():
            angles = decompose(axeVector, basisVector1, basisVector2, facet2)
            if not angles is None:
                [alpha, beta, gamma] = angles
            else:
                return True
            if abs(beta) + abs(gamma) < 1:
                return True

    axeVector = Vector(bc1, tc1)
    nt1 = tc1 - c1
    dt1 = -(nt1.x() * tc1.x() + nt1.y() * tc1.y() + nt1.z() * tc1.z())
    nb1 = bc1 - c1
    db1 = -(nb1.x() * bc1.x() + nb1.y() * bc1.y() + nb1.z() * bc1.z())
    for j in range(1, len(disk2.facets())):
        pt1 = disk2.facets()[j - 1]
        pt2 = disk2.facets()[j]
        v12 = Vector(pt1, pt2)
        vectorToVertex = Vector(Point(0, 0, 0), Point(v12.y() * axeVector.z() - v12.z() * axeVector.y(),
                                                      v12.z() * axeVector.x() - v12.x() * axeVector.z(),
                                                      v12.x() * axeVector.y() - v12.y() * axeVector.x()))
        vectorToVertex /= axeVector.length()
        angle = math.pi / verticesNumber
        vectorToVertex *= math.tan(angle)
        vertex1 = pt2 + vectorToVertex + axeVector / 2
        vertex2 = pt2 - vectorToVertex + axeVector / 2
        vertex3 = pt2 + vectorToVertex - axeVector / 2
        vertex4 = pt2 - vectorToVertex - axeVector / 2
        for v12 in [Vector(vertex1, vertex4), Vector(vertex2, vertex3)]:
            alpha = -(dt1 + nt1.x() * pt1.x() + nt1.y() * pt1.y() + nt1.z() * pt1.x()) / (nt1.x() * v12.x() + nt1.y() * v12.y() + nt1.z() * v12.z())
            beta = -(db1 + nb1.x() * pt1.x() + nb1.y() * pt1.y() + nb1.z() * pt1.x()) / (nb1.x() * v12.x() + nb1.y() * v12.y() + nb1.z() * v12.z())
            if abs(alpha) > 2 and abs(beta) > 2:
                pass
                #return False
            else:
                it = pt1 + v12 * alpha
                ib = pt1 + v12 * beta
                vt = Vector(tc1, it)
                vb = Vector(bc1, ib)
                if vt.length() < polygonalDiskRadius and vb.length() < polygonalDiskRadius:
                    pass
                else:
                    return True
    return False
