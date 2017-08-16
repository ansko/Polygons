class Options():
    def __init__(self):
        self.values = {}
        f = open('options.ini', 'r')
        for line in f:
            if line.startswith('#'):
                continue
            ls = line.split()
            if len(ls) < 2:
                continue
            value = ls[1]
            try:
                value = float(value)
            except:
                pass
            self.values[ls[0]] = value

    def printAll(self):
        for k in self.values.keys():
            print(k, self.values[k])

    def getProperty(self, propertyName):
        try:
            return self.values[propertyName]
        except:
            return None
