
import SudClasses
from SudFunctions import *
import random

testArray = ['7', '-', '4', '9', '5', '1', '-', '-', '2', '-', '-', '-', '-', '6', '7', '5', '-', '4', '1', '2', '5', '-', '-', '-', '-', '9', '6', '-', '-', '7', '-', '-', '-', '2', '-', '-', '9', '-', '-', '4', '-', '-', '3', '-', '5', '-', '-', '-', '1', '3', '5', '-', '-', '-', '-', '-', '-', '3', '2', '4', '-', '-', '-', '-', '9', '-', '-', '-', '8', '-', '6', '-', '4', '5', '-', '-', '-', '-', '1', '-', '3']
testArray2 = ['-', '11', '9', '-', '-', '16', '13', '4', '-', '-', '14', '-', '10', '6', '15', '-', '4', '12', '15', '-', '3', '6', '-', '11', '-', '5', '-', '1', '16', '7', '14', '2', '1', '-', '6', '-', '15', '2', '-', '-', '11', '9', '10', '-', '-', '-', '8', '-', '-', '13', '-', '-', '-', '1', '-', '-', '4', '6', '-', '15', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '15', '-', '8', '1', '5', '3', '-', '4', '11', '7', '6', '-', '1', '-', '-', '12', '8', '-', '9', '-', '-', '2', '-', '-', '3', '-', '14', '-', '4', '13', '6', '-', '-', '3', '-', '12', '7', '10', '8', '-', '2', '-', '3', '8', '-', '-', '4', '7', '2', '-', '6', '-', '-', '-', '-', '12', '16', '5', '13', '-', '-', '16', '-', '8', '14', '10', '3', '4', '15', '-', '12', '5', '1', '11', '-', '-', '-', '6', '2', '-', '-', '1', '10', '-', '11', '-', '15', '3', '-', '9', '7', '-', '-', '12', '-', '4', '-', '15', '5', '-', '9', '14', '-', '-', '-', '-', '10', '-', '-', '8', '-', '-', '11', '-', '-', '-', '1', '12', '4', '-', '13', '16', '-', '-', '-', '-', '-', '-', '7', '-', '15', '2', '-', '-', '-', '-', '12', '3', '-', '-', '7', '-', '-', '10', '6', '-', '1', '8', '-', '13', '11', '-', '9', '14', '8', '6', '5', '-', '-', '3', '-', '-', '14', '-', '-', '9', '-', '-', '-', '-', '-', '16', '-', '2', '-', '-', '-', '14', '-', '10', '-', '-', '-', '-', '-', '-']


def main(sudSize, sudType, sudText, maxCount):
    preCals = SudClasses.preCalculations(size)
    gBoard = SudClasses.Board(sudSize, sudText, preCals)
    setupBoard(gBoard)
    updateExacts(gBoard)
    updateErrors(gBoard)
    if sudType == "back":
        runBacktrack(gBoard)
    elif sudType == "GA":
        runGA(gBoard)
    elif sudType == "plus":
        print("Not implemented")
    elif sudType == "combo":
        print("Not implemented")
    else:
        print("What is", sudType, "?")
    gBoard.printNice()
    #print(gBoard)
    updateErrors(gBoard)
    if gBoard.checkTerminal():
        print("Passed")
    else:
        print("Non Terminal Board being returned")
    return gBoard.returnString()

def multiBacktrack(gBoard, maxCount):
    #Prime Board update constraints Function
    #Check if maxCount >= number of possible in board[0]
    #Check if maxCount >= #possible board[0] * board[1]
    #For up to maxCount, create a gBoard with board[0..X] filled in with each Y
    #Left over room fill in with board[1] filled in with X
    pass

def runBacktrack(gBoard):
    #print(gBoard)
    currentPos = 0
    moveTree = []
    size = gBoard.size
    size = size**2 * size**2
    gBoard.elements[0].currentValue = gBoard.elements[0].potentials[0]
    moveTree.append([0, 0])
    while currentPos < size:
        length = len(moveTree)
        if moveTree[length - 1][1] == len(gBoard.elements[moveTree[length - 1][0]].potentials):
            if len(gBoard.elements[moveTree[length - 1][0]].potentials) != 1:
                gBoard.elements[moveTree[length - 1][0]].currentValue = 0
            del moveTree[length - 1]
            length = len(moveTree)
            moveTree[length - 1][1] += 1
            currentPos = moveTree[length - 1][0]
            if moveTree[length - 1][1] != len(gBoard.elements[moveTree[length - 1][0]].potentials):
                curPos = moveTree[length - 1][0]
                gBoard.elements[curPos].currentValue = gBoard.elements[curPos].potentials[moveTree[length - 1][1]]
            continue
            
        if singleError(gBoard, moveTree[length - 1][0]):
            moveTree[length - 1][1] += 1
            if moveTree[length - 1][1] != len(gBoard.elements[moveTree[length - 1][0]].potentials):
                curPos = moveTree[length - 1][0]
                gBoard.elements[curPos].currentValue = gBoard.elements[curPos].potentials[moveTree[length - 1][1]]
            continue

        currentPos += 1
        if currentPos < size:
            moveTree.append([currentPos, 0])
            gBoard.elements[currentPos].currentValue = gBoard.elements[currentPos].potentials[0]
            

def runGA(gBoard):
    populationSize = 100
    population = []
    tempFitness = 0
    for x in range(populationSize):
        population.append(createChildRan(gBoard))
        tempFitness += population[x].fitness
    print("Avg starting fitness: ", format(tempFitness/populationSize, ".2f"))
    print("-----\n")
    #Begin generation loop
    for y in range(150):
        #Print out a small update to make sure progress is being made
        if y % 10 == 0:
            print("Generation", y)
            minFit = population[0].fitness
            modeDetect = {}
            for apop in population:
                if apop.fitness < minFit:
                    minFit = apop.fitness
                if apop.fitness in modeDetect:
                    modeDetect[apop.fitness] = modeDetect[apop.fitness] + 1
                else:
                    modeDetect[apop.fitness] = 1
            print("Best Fitness:", minFit)
            for apop in population:
                if apop.fitness == minFit:
                    apop.printNice2(gBoard)
                    break
            else:
                print("No match")
            if False:
                nonEdit = population[0:len(population)]
                nonEdit.sort(key=lambda x: x.fitness, reverse=False)
                print(nonEdit[0].fitness, nonEdit[0].calcBoxError())
                nonEdit[0].printNice2(gBoard)
            modeFit = 0
            modeNum = 0
            for key in modeDetect.keys():
                if modeDetect[key] > modeNum:
                    modeNum = modeDetect[key]
                    modeFit = key
            converge = float(format(modeNum/len(population)*100, ".2f"))
            print("Fitness", modeFit, "has a convergence of", converge, "%\n")
            if converge > 50:
                shakeUpConverge(population, modeFit, modeNum, gBoard)

        #Actual generation loop logic
        population = survivalWave(population, gBoard) #Selection
        random.shuffle(population)
        population = childWave(population, gBoard) #Recombination
        random.shuffle(population) 
        mutateWave(population, gBoard) #Mutation

    #Print out final output
    population.sort(key=lambda x: x.fitness, reverse=False)
    print("Best:")
    print(population[0].fitness, population[0].calcBoxError())
    population[0].printNice2(gBoard)
    print("")
    gBoard.elements = population[0].elements
    '''
    toPrint = 0
    if len(population) < 15:
        toPrint = len(population)
    else:
        toPrint = 15
    for x in range(toPrint):
        print(x, ":\n", population[x].fitness)
        population[x].printNice(gBoard)
    print("Last :\n", population[len(population)-1].fitness)
    population[len(population)-1].printNice(gBoard)
    '''


main(3, "back", testArray, 1)
main(3, "GA", testArray, 1)
