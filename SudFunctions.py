import random
import SudClasses

def setupBoard(gBoard):
    size = gBoard.size
    for x in range(size**2 * size**2):
        value = gBoard.elements[x].currentValue
        if value != 0:
            row = gBoard.getRow(x)
            for y in row:
                if value in gBoard.elements[y].potentials:
                    gBoard.elements[y].potentials.remove(value)
            col = gBoard.getCol(x)
            for y in col:
                if value in gBoard.elements[y].potentials:
                    gBoard.elements[y].potentials.remove(value)
            squ = gBoard.getSquare(x)
            for y in squ:
                if value in gBoard.elements[y].potentials:
                    gBoard.elements[y].potentials.remove(value)

def updateExacts(gBoard):
    size = gBoard.size
    for x in range(size**2 * size**2):
        if gBoard.elements[x].currentValue == 0 and len(gBoard.elements[x].potentials) == 1:
            gBoard.elements[x].currentValue = gBoard.elements[x].potentials[0]
            gBoard.elements[x].errors = 0
            value = gBoard.elements[x].currentValue
            row = gBoard.getRow(x)
            for y in row:
                if value in gBoard.elements[y].potentials:
                    gBoard.elements[y].potentials.remove(value)
            col = gBoard.getCol(x)
            for y in col:
                if value in gBoard.elements[y].potentials:
                    gBoard.elements[y].potentials.remove(value)
            squ = gBoard.getSquare(x)
            for y in squ:
                if value in gBoard.elements[y].potentials:
                    gBoard.elements[y].potentials.remove(value)
        if len(gBoard.elements[x].potentials) <= 0:
            print("Error: ", x)
            print(gBoard.elements[x])
            exit -1

def updateErrors(gBoard, pBoard = 0):
    if pBoard == 0:
        size = gBoard.size
        for x in range(size**2 * size**2):
            totalErrors = 0
            value = gBoard.elements[x].currentValue
            if len(gBoard.elements[x].potentials) != 1:
                row = gBoard.getRow(x)
                for y in row:
                    if value == gBoard.elements[y].currentValue:
                        totalErrors += 1
                col = gBoard.getCol(x)
                for y in col:
                    if value == gBoard.elements[y].currentValue:
                        totalErrors += 1
                squ = gBoard.getSquare(x)
                for y in squ:
                    if value == gBoard.elements[y].currentValue:
                        totalErrors += 1
            gBoard.elements[x].errors = totalErrors
    else:
        size = gBoard.size
        for x in range(size**2 * size**2):
            totalErrors = 0
            value = pBoard[x].currentValue
            if len(pBoard[x].potentials) != 1:
                row = gBoard.getRow(x)
                for y in row:
                    if value == pBoard[y].currentValue:
                        totalErrors += 1
                col = gBoard.getCol(x)
                for y in col:
                    if value == pBoard[y].currentValue:
                        totalErrors += 1
                squ = gBoard.getSquare(x)
                for y in squ:
                    if value == pBoard[y].currentValue:
                        totalErrors += 1
            pBoard[x].errors = totalErrors

def primeBoard(gBoard):
    for x in range(4):
        updateExacts(gBoard)
        updateErrors(gBoard)

def singleError(gBoard, index):
    size = gBoard.size
    value = gBoard.elements[index].currentValue
    row = gBoard.getRow(index)
    for y in row:
        if value == gBoard.elements[y].currentValue:
            return True
    col = gBoard.getCol(index)
    for y in col:
        if value == gBoard.elements[y].currentValue:
            return True
    squ = gBoard.getSquare(index)
    for y in squ:
        if value == gBoard.elements[y].currentValue:
            return True
    return False

def createChildRan(gBoard):
    temp = []
    for element in gBoard.elements:
        newBox = SudClasses.Box(gBoard.size)
        newBox.currentValue = element.currentValue
        newBox.errors = element.errors
        newBox.potentials = element.potentials[:]
        temp.append(newBox)
    for x in range(len(temp)):
        length = len(temp[x].potentials)
        temp[x].currentValue = temp[x].potentials[random.randint(0, length - 1)]
    updateErrors(gBoard, temp)
    temp = SudClasses.partBoard(temp)
    return temp

def survivalWave(pop, gBoard):
    tempPop = []
    nonEdit = pop[0:len(pop)]
    nonEdit.sort(key=lambda x: x.fitness, reverse=False)
    x = int(len(pop)*.1 + 1)
    if x %2 != 0:
        x += 1
    for y in range(x):
        tempPop.append(nonEdit[y])
    x = int(len(pop)*.05 + 1)
    if x %2 != 0:
        x += 1
    for y in range(x):
        tempPop.append(nonEdit[0])
        
    while len(tempPop) != len(pop):
        chosen = []
        for x in range(4):
            chosen.append(pop[random.randint(0, len(pop) - 1)])
        chosen.sort(key=lambda x: x.fitness, reverse=False)
        tempPop.append(chosen[0])
        tempPop.append(chosen[1])
    return tempPop

def createChild(parent1, parent2, gBoard):
    aPath = random.randint(0, 2)
    if aPath == 0:
        x = int(len(parent1.elements) * .5 + 1)
        if random.randint(0, 1) == 0:
            x = random.randint(0, len(parent1.elements)//2 + 1) + x
            if x > len(parent1.elements):
                x = len(parent1.elements)
        else:
            x = x - random.randint(0, len(parent1.elements)//2 + 1)
            if x < 0:
                x = 0
        if parent1.fitness < parent2.fitness:
            c1 = parent1.elements[0:x] + parent2.elements[x:len(parent2.elements)]
            c2 = parent2.elements[0:x] + parent1.elements[x:len(parent1.elements)]
        else:
            c1 = parent2.elements[0:x] + parent1.elements[x:len(parent1.elements)]
            c2 = parent1.elements[0:x] + parent2.elements[x:len(parent2.elements)]
        updateErrors(gBoard, c1)
        updateErrors(gBoard, c2)
        c1 = SudClasses.partBoard(c1)
        c2 = SudClasses.partBoard(c2)
        return c1, c2
    else:
        x = int(len(parent1.elements) * .1 + 1)
        c1 = parent1.elements[:]
        c2 = parent2.elements[:]
        for y in range(x):
            y = random.randint(0, len(parent1.elements) - 1)
            c1[y], c2[y] = c2[y], c1[y]
        updateErrors(gBoard, c1)
        updateErrors(gBoard, c2)
        c1 = SudClasses.partBoard(c1)
        c2 = SudClasses.partBoard(c2)
        return c1, c2

def childWave(population, gBoard):
    x = 0
    tempPo = []
    while x < len(population):
        #75% chance of recombination
        y = random.randint(1, 4)
        if y != 4:
            c1, c2 = createChild(population[x], population[x+1], gBoard)
            if int(c1.fitness / ( c1.fitness + population[x].fitness + 1) * 100) < 55:
                tempPo.append(c1)
            else:
                tempPo.append(population[x])
            if int(c2.fitness / ( c2.fitness + population[x + 1].fitness + 1) * 100) < 55:
                tempPo.append(c2)
            else:
                tempPo.append(population[x + 1])
        else:
            tempPo.append(population[x])
            tempPo.append(population[x+1])
        x += 2
    return tempPo

def createMutation(indiv):
    x = .02 * len(indiv.elements) + 1
    for y in range(int(x)):
        y = random.randint(0, len(indiv.elements) - 1)
        length = len(indiv.elements[y].potentials)
        z = 1
        if indiv.elements[y].errors == 0:
            z = random.randint(1, 4)
        if z != 4:
            indiv.elements[y].currentValue = indiv.elements[y].potentials[random.randint(0, length - 1)]


def mutateWave(population, gBoard):
    #Give % of the population mutations
    mutants = int(len(population) * .01 + 1)
    for g in range(mutants):
        a = random.randint(0, len(population) - 1)
        createMutation(population[a])
        updateErrors(gBoard, population[a].elements)
        population[a].calcFinalError()

def shakeUpConverge(pop, fitn, number, gBoard):
    percen = number/len(pop)*100
    if percen > 80:
        toChange = int(number * .5)
    else:
        toChange = int(number * .25)
    for x in range(len(pop)):
        if toChange == 0:
            break
        if pop[x].fitness == fitn:
            temp = createChildRan(gBoard)
            pop[x] = temp
            toChange -= 1

def forSort(e):
    return e.fitness

def partition(pop, low, high):
    i = (low - 1)
    pivot = pop[high].fitness
    for j in range(low, high):
        if pop[j].fitness < pivot:
            i = i+1
            pop[i], pop[j] = pop[j], pop[i]
    pop[i+1], pop[high] = pop[high], pop[i+1]
    return (i + 1)

def orderSort(pop, low, high):
    if low < high:
        pi = partition(pop, low, high)
        orderSort(pop, low, pi-1)
        orderSort(pop, pi+1, high)
