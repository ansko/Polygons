def delta(i, j):
    if i == j:
        return 1
    return 0


def det(M):
    l = len(M)
    if l == 0 or M is None:
        print('Error in determinant calculation!')
        return None
    if l == 1:
        return M[0][0]
    if l > 100:
        print('Too big matrix for the recursive algorithm.')
        return None
    result = 0
    for i in range(l):
        newM = []
        for j in range(1, l):
            newM.append(copy.deepcopy(M[j]))
            newM[j-1].pop(i)
        result += ((-1) ** i) * det(newM) * M[0][i]
    #if result == 0:
    #    pprint(M)
    return result


def decompose(axeVector, basisVector1, basisVector2, point):
    x1 = axeVector.x()
    x2 = basisVector1.x()
    x3 = basisVector2.x()
    y1 = axeVector.y()
    y2 = basisVector1.y()
    y3 = basisVector2.y()
    z1 = axeVector.z()
    z2 = basisVector1.z()
    z3 = basisVector2.z()
    a = point.x()
    b = point.y()
    c = point.z()
    determinant = det([[x1, x2, x3], [y1, y2, y3], [z1, z2, z3]])
    if determinant < EPSILON:
        #print('Determinant = 0!')
        return None
    #print(determinant)
    alpha = det([[a, x2, x3], [b, y2, y3], [c, z2, z3]]) / determinant
    beta = det([[x1, a, x3], [y1, b, y3], [z1, c, z3]]) / determinant
    gamma = det([[x1, x2, a], [y1, y2, b], [z1, z2, c]]) / determinant
    return [alpha, beta, gamma]


def orderParameter(cosTheta):
    return (3 * cosTheta**2 - 1) / 2
