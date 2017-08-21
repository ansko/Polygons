import numpy as np

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint

from Options import Options
from Point import Point
from Vector import Vector

from planeLineIntersection import planeLineIntersection
from utils import decompose, det


def disksCross(disk1, disk2):
    o = Options()
    polygonalDiskRadius = o.getProperty('polygonalDiskRadius')
    polygonalDiskThickness = o.getProperty('polygonalDiskThickness')
    bigDistance = 2 * (polygonalDiskRadius**2 + polygonalDiskThickness**2 / 4)**0.5
    smallDistance = polygonalDiskThickness
    epsilon = o.getProperty('epsilon')
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
    # http://mathworld.wolfram.com/Line-PlaneIntersection.html
    for i in range(len(disk1.facets())):
        x1 = disk1.facets()[i]
        x2 = disk1.facets()[i - 1]
        x3 = c1
        for j in range(len(disk2.facets())):
            x4 = disk2.facets()[j]
            x5 = disk2.facets()[j - 1]
            numerator = det([
                             [1, 1, 1, 1],
                             [x1.x(), x2.x(), x3.x(), x4.x()],
                             [x1.y(), x2.y(), x3.y(), x4.y()],
                             [x1.z(), x2.z(), x3.z(), x4.z()]
                            ])
            denominator = det([
                               [1, 1, 1, 0],
                               [x1.x(), x2.x(), x3.x(), (x5 - x4).x()],
                               [x1.y(), x2.y(), x3.y(), (x5 - x4).y()],
                               [x1.z(), x2.z(), x3.z(), (x5 - x4).z()]
                              ])
            if abs(denominator) < epsilon:
                pass
            else:
                t = numerator / denominator
                if -1 <= t <= 1: # why -1 but not 0?
                    return True
                              
    return False
