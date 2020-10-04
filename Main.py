
import SudClasses
from SudFunctions import *
import random
import multiprocessing
import time

testArray = ['7', '-', '4', '9', '5', '1', '-', '-', '2', '-', '-', '-', '-', '6', '7', '5', '-', '4', '1', '2', '5', '-', '-', '-', '-', '9', '6', '-', '-', '7', '-', '-', '-', '2', '-', '-', '9', '-', '-', '4', '-', '-', '3', '-', '5', '-', '-', '-', '1', '3', '5', '-', '-', '-', '-', '-', '-', '3', '2', '4', '-', '-', '-', '-', '9', '-', '-', '-', '8', '-', '6', '-', '4', '5', '-', '-', '-', '-', '1', '-', '3']
testArray2 = ['-', '11', '9', '-', '-', '16', '13', '4', '-', '-', '14', '-', '10', '6', '15', '-', '4', '12', '15', '-', '3', '6', '-', '11', '-', '5', '-', '1', '16', '7', '14', '2', '1', '-', '6', '-', '15', '2', '-', '-', '11', '9', '10', '-', '-', '-', '8', '-', '-', '13', '-', '-', '-', '1', '-', '-', '4', '6', '-', '15', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '15', '-', '8', '1', '5', '3', '-', '4', '11', '7', '6', '-', '1', '-', '-', '12', '8', '-', '9', '-', '-', '2', '-', '-', '3', '-', '14', '-', '4', '13', '6', '-', '-', '3', '-', '12', '7', '10', '8', '-', '2', '-', '3', '8', '-', '-', '4', '7', '2', '-', '6', '-', '-', '-', '-', '12', '16', '5', '13', '-', '-', '16', '-', '8', '14', '10', '3', '4', '15', '-', '12', '5', '1', '11', '-', '-', '-', '6', '2', '-', '-', '1', '10', '-', '11', '-', '15', '3', '-', '9', '7', '-', '-', '12', '-', '4', '-', '15', '5', '-', '9', '14', '-', '-', '-', '-', '10', '-', '-', '8', '-', '-', '11', '-', '-', '-', '1', '12', '4', '-', '13', '16', '-', '-', '-', '-', '-', '-', '7', '-', '15', '2', '-', '-', '-', '-', '12', '3', '-', '-', '7', '-', '-', '10', '6', '-', '1', '8', '-', '13', '11', '-', '9', '14', '8', '6', '5', '-', '-', '3', '-', '-', '14', '-', '-', '9', '-', '-', '-', '-', '-', '16', '-', '2', '-', '-', '-', '14', '-', '10', '-', '-', '-', '-', '-', '-']
testArray3 = ['-', '-', '4', '9', '5', '1', '-', '-', '2', '-', '-', '-', '-', '-', '7', '5', '-', '4', '1', '2', '-', '-', '-', '-', '-', '9', '-', '-', '-', '7', '-', '-', '-', '2', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '1', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '9', '-', '-', '-', '8', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '3']


def main(sudSize, sudType, sudText, maxCount):
    preCals = SudClasses.preCalculations(sudSize)
    gBoard = SudClasses.Board(sudSize, sudText, preCals)
    setupBoard(gBoard)
    updateExacts(gBoard)
    #gBoard.elements[79].currentValue = 3
    #gBoard.elements[79].potentials = [3]
    updateErrors(gBoard)
    #gBoard.printNice()
    if sudType == "back":
        #print("")
        soln = runBacktrack(gBoard)
        #print(soln[0])
        #soln[1].printNice()
    elif sudType == "GA":
        solut = runGA(gBoard)
        #solut.printNice2(gBoard)
        gBoard.elements = solut.elements
    elif sudType == "plus":
        gBoard = multiBacktrack(gBoard, maxCount)
        #gBoard = soln
    elif sudType == "combo":
        solut = runGACombo(gBoard, maxCount)
        gBoard.elements = solut.elements
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

def spinWheel( ):
    count = 0
    while count < 99999999:
        x = 999 * 999
        count += 1
    print(count)

def getPermuts(gBoard, count):
    if count == 0:
        tempL = gBoard.elements[0].potentials[:]
        for x in range(len(tempL)):
            tempL[x] = tempL[x] if isinstance(tempL[x], list) else [tempL[x]]
        return tempL
    else:
        leftValues = getPermuts(gBoard, count - 1)
        tempL = []
        for x in leftValues:
            for y in gBoard.elements[count].potentials:
                tEle = x[:]
                tEle.append(y)
                tempL.append( tEle )
        return tempL

def multiBacktrack(gBoard, maxCount):
    #Additional helpful step eliminate permutations that have copies of same element and in same row
    #For size 3: [1, 2, 3, 4] good permut -> [1, 2, 3, 1] bad permut, it will fail, should just toss it
    #for each permut create a new gBoard with first X filled in (set current value and potentials == 1)
    #hand off each new gBoard to a new process running backtrack algorithm
    #Keep track when they return, if return solved cancel all others and return solved gBoard
    #Else create new process in same spot for next gBoard
    permuts = []
    count = 0
    while len(permuts) < maxCount:
            permuts = getPermuts(gBoard, count)
            #print("Count: " + str(count))
            #for x in permuts:
                #print(x)
            count += 1
    #print("Final: ")
    #for x in permuts:
        #print(x)
    '''
    if __name__ == '__main__':
        processes = []
        manager = multiprocessing.Manager()
        sharedData = manager.list([[False, False, None] for _ in range(maxCount)])
        answer = -1
        for y in range(maxCount):
            tempBoard = gBoard.getCopy()
            for x in range(len(permuts[0]) ):
                tempBoard.elements[x].currentValue = permuts[0][x]
                tempBoard.elements[x].potentials = [permuts[0][x]]
            permuts = permuts[1:]
            p = multiprocessing.Process(target=runBacktrack, args=[tempBoard, sharedData, y])
            processes.append(p)
        for p in processes:
            p.start()
        endValue = True
        while endValue:
            for y in range(len(sharedData)):
                if sharedData[y][0]:
                    if sharedData[y][1]:
                        for p in processes:
                            p.terminate()
                        answer = sharedData[y][2].getCopy()
                        endValue = False
                        break
                    else:
                        if len(permuts) > 0:
                            tempBoard = gBoard.getCopy()
                            for x in range(len(permuts[0]) ):
                                tempBoard.elements[x].currentValue = permuts[0][x]
                                tempBoard.elements[x].potentials = [permuts[0][x]]
                            permuts = permuts[1:]
                            p = multiprocessing.Process(target=runBacktrack, args=[tempBoard, sharedData, y])
                            processes.append(p)
                            p.start()
            time.sleep(.001)


        for process in processes:
            process.join()
        print("All done")
        if answer == -1:
            return gBoard
        else:
            return answer
    '''
    processes = []
    manager = multiprocessing.Manager()
    sharedData = manager.list([[False, False, None] for _ in range(maxCount)])
    answer = -1
    for y in range(maxCount):
        tempBoard = gBoard.getCopy()
        for x in range(len(permuts[0]) ):
            tempBoard.elements[x].currentValue = permuts[0][x]
            tempBoard.elements[x].potentials = [permuts[0][x]]
        permuts = permuts[1:]
        p = multiprocessing.Process(target=runBacktrack, args=[tempBoard, sharedData, y])
        processes.append(p)
    for p in processes:
        p.start()
    endValue = True
    while endValue:
        for y in range(len(sharedData)):
            if sharedData[y][0]:
                if sharedData[y][1]:
                    for p in processes:
                        p.terminate()
                    answer = sharedData[y][2].getCopy()
                    endValue = False
                    break
                else:
                    if len(permuts) > 0:
                        tempBoard = gBoard.getCopy()
                        for x in range(len(permuts[0]) ):
                            tempBoard.elements[x].currentValue = permuts[0][x]
                            tempBoard.elements[x].potentials = [permuts[0][x]]
                        permuts = permuts[1:]
                        p = multiprocessing.Process(target=runBacktrack, args=[tempBoard, sharedData, y])
                        processes.append(p)
                        p.start()
        time.sleep(.001)


    for process in processes:
        process.join()
    print("All done")
    if answer == -1:
        return gBoard
    else:
        return answer
    


def runBacktrack(gBoard, sharedData = None, processNumber = None):
    currentPos = 0
    moveTree = [] # [board element number, potentials number]
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
            if length == 0:
                if sharedData == None:
                    return [False, gBoard]
                else:
                    sharedData[processNumber] = [True, False, gBoard]
                    return
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
    if sharedData == None:
        return [True, gBoard]
    else:
        sharedData[processNumber] = [True, True, gBoard]
        return
            

def runGA(gBoard):
    populationSize = 1000
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
                break
                if apop.fitness == minFit:
                    apop.printNice2(gBoard)
                    print(apop.calcSpecial(gBoard))
                    updateErrors(gBoard, apop.elements);
                    print(apop.calcBoxError())
                    print(apop.calcSpecial(gBoard))
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
            if converge > 70:
                shakeUpConverge(population, modeFit, modeNum, gBoard)

        #Actual generation loop logic
        population = survivalWave(population, gBoard) #Selection
        random.shuffle(population)
        population = childWave(population, gBoard) #Recombination
        random.shuffle(population) 
        mutateWave(population, gBoard) #Mutation
        for apop in population:
            updateErrors(gBoard, apop.elements)
            apop.fitness = apop.calcBoxError()
            if apop.fitness == 0:
                return apop

    #Print out final output
    population.sort(key=lambda x: x.fitness, reverse=False)
    #print("Best:")
    #print(population[0].fitness, population[0].calcBoxError())
    #population[0].printNice2(gBoard)
    #print("")
    return population[0]
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

def runGACombo(gBoard, maxCount):
    populationSize = 1000
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
                break
                if apop.fitness == minFit:
                    apop.printNice2(gBoard)
                    print(apop.calcSpecial(gBoard))
                    updateErrors(gBoard, apop.elements);
                    print(apop.calcBoxError())
                    print(apop.calcSpecial(gBoard))
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
            if converge > 70:
                shakeUpConverge(population, modeFit, modeNum, gBoard)

        #Actual generation loop logic
        population.sort(key=lambda x: x.fitness, reverse=False)
        if population[0].fitness < gBoard.size * 5:
            temp = gBoard.getCopy()
            temp.elements = population[0].getCopy()
            answ = runBacktrack(temp)
            if answ[0]:
                print("Back worked")
                return answ[1]
        random.shuffle(population)
        population = survivalWave(population, gBoard) #Selection
        random.shuffle(population)
        population = childWave(population, gBoard) #Recombination
        random.shuffle(population) 
        mutateWave(population, gBoard) #Mutation
        for apop in population:
            updateErrors(gBoard, apop.elements)
            apop.fitness = apop.calcBoxError()
            if apop.fitness == 0:
                return apop

    population.sort(key=lambda x: x.fitness, reverse=False)
    return population[0]


if __name__ == '__main__':
    
    main(3, "combo", testArray1, 1)
    '''
    startTime = time.process_time()
    main(3, "back", testArray2, 1)
    endTime = time.process_time()
    print("Time:  " + str(endTime - startTime) + "s")
    #main(3, "GA", testArray, 1)
    startTime = time.process_time()
    main(3, "plus", testArray3, 8)
    endTime = time.process_time()
    print("Time:  " + str(endTime - startTime) + "s")
    '''
