from Point import Point


class Vector():
    def __init__(self, dot1, dot2):
        self.values = {}
        self.values['beginX'] = dot1.x()
        self.values['beginY'] = dot1.y()
        self.values['beginZ'] = dot1.z()
        self.values['endX'] = dot2.x()
        self.values['endY'] = dot2.y()
        self.values['endZ'] = dot2.z()
        
    def __add__(self, otherVector):
        self.values['endX'] += (otherVector.end() - otherVector.begin()).x
        self.values['endY'] += (otherVector.end() - otherVector.begin()).y
        self.values['endZ'] += (otherVector.end() - otherVector.begin()).z
        return Vector(Point(0, 0, 0), Point(self.x(), self.y(), self.z()))
        
    def __sub__(self, otherVector):
        self.values['endX'] -= (otherVector.end() - otherVector.begin()).x
        self.values['endY'] -= (otherVector.end() - otherVector.begin()).y
        self.values['endZ'] -= (otherVector.end() - otherVector.begin()).z
        return Vector(Point(0, 0, 0), Point(self.x(), self.y(), self.z()))
        
    def __mul__(self, coefficient):
        x = self.values['endX'] - self.values['beginX']
        y = self.values['endY'] - self.values['beginY']
        z = self.values['endZ'] - self.values['beginZ']
        self.values['endX'] = self.values['beginX'] + x * coefficient
        self.values['endX'] = self.values['beginY'] + y * coefficient
        self.values['endX'] = self.values['beginZ'] + z * coefficient
        return Vector(Point(0, 0, 0), Point(self.x(), self.y(), self.z()))
        
    def __truediv__(self, coefficient):
        x = self.values['endX'] - self.values['beginX']
        y = self.values['endY'] - self.values['beginY']
        z = self.values['endZ'] - self.values['beginZ']
        self.values['endX'] = self.values['beginX'] + x / coefficient
        self.values['endX'] = self.values['beginY'] + y / coefficient
        self.values['endX'] = self.values['beginZ'] + z / coefficient
        return Vector(Point(0, 0, 0), Point(self.x(), self.y(), self.z()))

    def __str__(self):
        return str(self.x()) + ' ' + str(self.y()) + ' ' + str(self.z())
        
    def begin(self):
        return Point(self.values['beginX'],
                     self.values['beginY'],
                     self.values['beginZ'])
                     
    def end(self):
        return Point(self.values['endX'],
                     self.values['endY'],
                     self.values['endZ'])
                     
    def x(self):
        return self.values['endX'] - self.values['beginX']

    def y(self):
        return self.values['endY'] - self.values['beginY']
        
    def z(self):
        return self.values['endZ'] - self.values['beginZ']
                     
    def length(self):
        x = self.values['endX'] - self.values['beginX']
        y = self.values['endY'] - self.values['beginY']
        z = self.values['endZ'] - self.values['beginZ']
        return (x**2 + y**2 + z**2)**0.5
