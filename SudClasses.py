

class Box:
    def __init__(self, size, currentValue = 0, errors = 0):
        self.currentValue = currentValue
        self.errors = errors
        if self.currentValue == 0:
            self.potentials = list(range(1, size**2 + 1))
        else:
            self.potentials = [self.currentValue]
    def __str__(self):
        rString = "Current Value: " + str(self.currentValue)
        rString += "  Errors: " + str(self.errors) + "\n"
        rString += "Potentials: ["
        for x in self.potentials:
            rString += str(x) + ", "
        rString = rString[0:-2]
        rString += "]\n"
        return rString

class Board:
    def __init__(self, size, inputList, preCal):
        self.prCalcs = preCal
        self.elements = []
        self.size = size
        count = 0
        for x in range(size**2 * size**2):
            y = Box(size) if inputList[count] == "-" else Box(size, int(inputList[count]))
            self.elements.append(y)
            count += 1
            
    def getRow(self, elementNum):
        for row in self.prCalcs.rows:
            if elementNum in row:
                temp = row[:]
                temp.remove(elementNum)
                return temp
        print("Error! No row found for element", elementNum)
    def getCol(self, elementNum):
        for col in self.prCalcs.cols:
            if elementNum in col:
                temp = col[:]
                temp.remove(elementNum)
                return temp
        print("Error! No col found for element", elementNum)
    def getSquare(self, elementNum):
        for squ in self.prCalcs.squs:
            if elementNum in squ:
                temp = squ[:]
                temp.remove(elementNum)
                return temp
        print("Error! No squ found for element", elementNum)
    def calcTotalError(self):
        count = 0
        for x in self.elements:
            count += x.errors
        return count
    def calcBoxError(self):
        count = 0
        for x in self.elements:
            count += 0 if x.errors == 0 else 1
        return count
    def checkTerminal(self):
        for x in self.elements:
            if x.errors != 0:
                return False
        return True
    def printNice(self):
        for row in self.prCalcs.rows:
            for x in row:
                print(format(self.elements[x].currentValue, "<3"), end = "")
            print("")
    def returnString(self):
        rString = ""
        for row in self.prCalcs.rows:
            for x in row:
                value = self.elements[x].currentValue
                errors = self.elements[x].errors
                rString += format(value, "<2") if value != 0 and errors == 0 else format("-", "<2")
                rString += " "
            rString += "\n"
        return rString
    def __str__(self):
        rString = ""
        count = 0
        for x in self.elements:
            rString += "Element #: " + str(count) + "\n"
            rString += str(x)
            count += 1
        return rString

class preCalculations:
    def __init__(self, size):
        self.rows = self.setupRows(size)
        self.cols = self.setupCols(size)
        self.squs = self.setupSqus(size)
    def setupCols(self, size):
        size = size**2
        cols = []
        for x in range(size):
            cols.append([])
        count = 0
        for x in range(size):
            for y in range(size):
                cols[y].append(count)
                count += 1
        return cols
    def setupRows(self, size):
        size = size**2
        rows = []
        for x in range(size):
            rows.append([])
        count = 0
        for x in range(size):
            for y in range(size):
                rows[x].append(count)
                count += 1
        return rows
    def setupSqus(self, size):
        size2 = size**2
        squs = []
        for x in range(size2):
            squs.append([])
        count = 0
        for x in range(size2):
            for y in range(x//size * size, x//size * size + size):
                for z in range(size):
                    squs[y].append(count)
                    count += 1
        return squs
                
class partBoard:
    def __init__(self, elements):
        self.elements = elements
        self.fitness = self.calcBoxError()
    def calcFinalError(self):
        self.fitness = self.calcBoxError()
    def calcTotalError(self):
        count = 0
        for x in self.elements:
            count += x.errors
        return count
    def calcBoxError(self):
        count = 0
        for x in self.elements:
            count += 0 if x.errors == 0 else 1
        return count
    def checkTerminal(self):
        for x in self.elements:
            if x.errors != 0:
                return False
        return True
    def printNice(self, gBoard):
        for row in gBoard.prCalcs.rows:
            for x in row:
                print(format(self.elements[x].currentValue, "<3"), end = "")
            print("")
    def printNice2(self, gBoard):
        for row in gBoard.prCalcs.rows:
            for x in row:
                if self.elements[x].errors != 0:
                    print(format("-", "<3"), end = "")
                else:
                    print(format(self.elements[x].currentValue, "<3"), end = "")
            print("")
