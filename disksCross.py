import sys

from Options import Options
from Vector import Vector

from planeLineIntersection import planeLineIntersection
from utils import decompose, det


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
    #axeVector = tc1 - bc1
    #for i in range(1, len(disk1.facets()) - 1):
    #    basisVector1 = disk1.facets()[i - 1] / 2 + disk1.facets()[i] / 2
    #    basisVector2 = disk1.facets()[i + 1] / 2 + disk1.facets()[i] / 2
    #    for facet2 in disk2.facets():
    #        angles = decompose(axeVector, basisVector1, basisVector2, facet2)
    #        if not angles is None:
    #            [alpha, beta, gamma] = angles
    #        else:
    #            return True
    #        if abs(beta) + abs(gamma) < 1:
    #            return True
    # facet-top/bottom intersection
    #for j in range(1, len(disk2.facets())):
    #    top = planeLineIntersection(tc1, c1 - tc1, disk2.facets()[j - 1], disk2.facets()[j])
    #    if top[0]:
    #        if top[1] is None or Vector(tc1, top[1]).length() < polygonalDiskRadius:
    #            return True
    #        #else:
    #        #    return False
    #    bottom = planeLineIntersection(bc1, c1 - bc1, disk2.facets()[j - 1], disk2.facets()[j])
    #    if bottom[0]:
    #        if bottom[1] is None or Vector(bc1, bottom[1]).length() < polygonalDiskRadius:
    #            return True
    #        #else:
    #        #    return False
    nt1 = tc1 - c1
    dt1 = -(nt1.x() * tc1.x() + nt1.y() * tc1.y() + nt1.z() * tc1.z())
    nb1 = bc1 - c1
    db1 = -(nb1.x() * bc1.x() + nb1.y() * bc1.y() + nb1.z() * bc1.z())
    for j in range(1, len(disk2.facets())):
        pt1 = disk2.facets()[j - 1]
        pt2 = disk2.facets()[j]
        # top plane equation: nt1.x() * (x - tc1.x()) + nt1.y() * (y - tc1.y()) + nt1.z() * (z - tc1.z()) = 0
        # nt1.x() * x + nt1.y() * y + nt1.z() * z - nt1.x() * tc1.x() - nt1.y() * tc1.y() - nt1.z() * tc1.z() = 0
        v12 = Vector(pt1, pt2)
        # intersection: pt1 + alpha * v12 belongs to top plane:
        # nt1.x() * (pt1.x() + alpha * v12.x()) + nt1.y() * (pt1.y() + alpha * v12.y()) + nt1.z() * (pt1.x() + alpha * v12.z()) + dt1 = 0
        # nt1.x() * pt1.x() + nt1.y() * pt1.y() + nt1.z() * pt1.x() + dt1 + alpha * (nt1.x() * v12.x() + nt1.y() * v12.y() + nt1.z() * v12.z()) = 0
        alpha = -(dt1 + nt1.x() * pt1.x() + nt1.y() * pt1.y() + nt1.z() * pt1.x()) / (nt1.x() * v12.x() + nt1.y() * v12.y() + nt1.z() * v12.z())
        beta = -(db1 + nb1.x() * pt1.x() + nb1.y() * pt1.y() + nb1.z() * pt1.x()) / (nb1.x() * v12.x() + nb1.y() * v12.y() + nb1.z() * v12.z())
        it = pt1 + v12 * alpha
        ib = pt1 + v12 * beta
        vt = Vector(tc1, it)
        vb = Vector(bc1, ib)
        if abs(alpha) > 2 and abs(beta) > 2:
            pass
            #return False
        else:
            if vt.length() < polygonalDiskRadius and vb.length() < polygonalDiskRadius:
                pass
            else:
                return True
    return False
