class PlaneMadeOfDots():
    def __init__(self, dot1, dot2, dot3):
        vector1 = dot2 - dot1
        vector2 = dot3 - dot1
        normal = (vector1.y() * vector2.x() - vector2.y() * vector1.z(),
                  vector2.x() * vector1.z() - vector1.x() * vector2.z(),
                  vector1.x() * vector2.y() - vector2.x() * vector1.y())
        self.values = {}
        self.values['normal'] = normal
        self.values['origin'] = dot1
        
    def printToCSG(self, f):
        f.write('plane(')
        self.origin().printToCSG(f)
        f.write('; ')
        self.normal().printToCSG(f)
        f.write(')')
