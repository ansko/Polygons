from Options import Options


def planeLineIntersection(pointOnPlane, normalOrigin, linePoint1, linePoint2):
    # from english wikipedia
    # (p - p0) * n = 0 - plane
    # p = d * l + l0 - line
    # d = (p0 - l0) * n / (l * n)
    # l * n = 0 -> (p0 - l0) * n = 0 - they are parallel
    #           -> else line lays in the plane
    # else there is one intersection point d * l + l0
    #
    # l = linePoint2 - linePoint1
    # l0 = linePoint1
    # n = facet - diskCenter
    # p0 = facet
    o = Options()
    epsilon = o.getProperty('epsilon')
    p0 = pointOnPlane
    l0 = linePoint1
    l = linePoint2 - linePoint1
    n = pointOnPlane - normalOrigin
    denominator = l.x() * n.x() + l.y() * n.y() + l.z() * n.z()
    numerator = (p0 - l0).x() * n.x() + (p0 - l0).y() * n.y() + (p0 - l0).z() * n.z()
    #if abs(denominator) < epsilon and abs(numerator) < epsilon:
    #    return [False, None]
    #elif abs(denominator) < epsilon and abs(numerator) > epsilon:
    #    return [True, None]
    #elif abs(denominator) > epsilon:
    #    intersectionPoint = l0 + l * numerator / denominator
    #    return [True, intersectionPoint]
    #return [True, None]
    if abs(denominator) < epsilon:
        if abs(numerator) < epsilon:
            return [False, None]
        else:
            return [True, None]
    else:
        return [True, l0 + l * numerator / denominator]
