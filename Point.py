class Point():
    def __init__(self, x, y, z):
        self.values = {}
        self.values['x'] = x
        self.values['y'] = y
        self.values['z'] = z
        
    def __add__(self, otherPoint):
        return Point(self.x() + otherPoint.x(),
                     self.y() + otherPoint.y(),
                     self.z() + otherPoint.z())
    
    def __sub__(self, otherPoint):
        return Point(self.x() - otherPoint.x(),
                     self.y() - otherPoint.y(),
                     self.z() - otherPoint.z())
                     
    def __mul__(self, coefficient):
        return Point(self.x() * coefficient,
                     self.y() * coefficient,
                     self.z() * coefficient)
                     
    def __truediv__(self, coefficient):
        return Point(self.x() / coefficient,
                     self.y() / coefficient,
                     self.z() / coefficient)
                     
    def __str__(self):
        return '{}, {}, {}'.format(self.x(), self.y(), self.z())
        
    def x(self):
        return self.values['x']
        
    def y(self):
        return self.values['y']
    
    def z(self):
        return self.values['z']
    
    def setX(self, newX):
        self.values['x'] = newX
   
    def setY(self, newY):
        self.values['y'] = newY
        
    def setZ(self, newZ):
        self.values['z'] = newZ
        
    def printToCSG(self, f):
        f.write(self.__str__())
