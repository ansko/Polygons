from Options import Options
from Vector import Vector

from planeLineIntersection import planeLineIntersection
from utils import decompose


def disksCross(disk1, disk2):
    o = Options()
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
    # facet-top/bottom intersection
    for j in range(1, len(disk2.facets())):
        top = planeLineIntersection(tc1, c1 - tc1, disk2.facets()[j - 1], disk2.facets()[j])
        if top[0] and Vector(tc1, top[1]).length() < polygonalDiskRadius:
            return True
        bottom = planeLineIntersection(bc1, c1 - bc1, disk2.facets()[j - 1], disk2.facets()[j])
        if bottom[0] and Vector(bc1, bottom[1]).length() < polygonalDiskRadius:
            return True
    return False
