#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import os

"""毕业设计程序NCV.py"""
__author__ = "Cui,Scott"


class Chromosome(object):
    chromosomeLength = 10
    chromosomeHigh = 3
    inputList = 2 ** chromosomeHigh
    # 2表示CV+，3表示CV，4表示CN，5表示
    gene = [[1, 1, 1, 0], [2, 3, 4, 5]]

    def chooseGene(self):
        randomElement = random.randint(0, len(self.gene[0]) - 1)
        randomPosition1 = random.randint(0, self.chromosomeHigh - 1)
        randomPosition2 = random.randint(0, self.chromosomeHigh - 1)
        while randomPosition1 == randomPosition2:
            randomPosition2 = random.randint(0, self.chromosomeHigh - 1)
        return randomElement, randomPosition1, randomPosition2

    def createChromosome(self):
        tempChromosome = []
        for chromosomeHighIndex in range(0, self.chromosomeHigh):
            tempChromosome.append([])
        for chromosomeLengthIndex in range(0, self.chromosomeLength):
            genIndex, pos1, pos2 = self.chooseGene()
            for chromosomeHighIndex in range(0, self.chromosomeHigh):
                tempChromosome[chromosomeHighIndex].append(0)
                if pos1 == chromosomeHighIndex:
                    tempChromosome[chromosomeHighIndex][chromosomeLengthIndex] = self.gene[0][genIndex]
                elif pos2 == chromosomeHighIndex:
                    tempChromosome[chromosomeHighIndex][chromosomeLengthIndex] = self.gene[1][genIndex]
        return tempChromosome


class Population(Chromosome):
    scalePopulation = 600
    crossProbability = 0.9
    mutationProbability = 0.1
    populationList = []
    populationOutputList = []
    populationFitnessList = []
    maxFitnessList = {"Fitness": None, "chromosome1": None, "chromosome2": None}
    minFitnessList = {"Index": None, "Fitness": None}
    nextPopulation = []
    input = []

    def chromosomeInput(self):
        tempInput = []
        for chromosomeHighIndex in range(0, self.chromosomeHigh):
            tempInput.append([])
        for inputListIndex in range(0, self.inputList):
            temp = inputListIndex
            for chromosomeHighIndex in range(0, self.chromosomeHigh):
                tempInput[self.chromosomeHigh - chromosomeHighIndex - 1].append(temp % 2)
                temp //= 2
        self.input = tempInput
        return self.input

    def createPopulation(self):
        tempPopulation = []
        for scalePopulationIndex in range(0, self.scalePopulation):
            tempPopulation.append(self.createChromosome())
        self.populationList = tempPopulation
        return self.populationList

    def calculateOutput(self, populationIndex):
        output = []
        mid = []
        for chromosomeHighIndex in range(0, self.chromosomeHigh):
            output.append([])
            mid.append([])
        for inputListIndex in range(0, self.inputList):
            for chromosomeHighIndex in range(0, self.chromosomeHigh):
                output[chromosomeHighIndex].append(0)
                mid.append(0)
        for inputIndex in range(0, len(self.input[0])):
            for chromosomeHighIndex in range(0, self.chromosomeHigh):
                mid[chromosomeHighIndex] = self.input[chromosomeHighIndex][inputIndex]
            chromosomeLengthIndex = -1
            while chromosomeLengthIndex < self.chromosomeLength - 1:
                chromosomeLengthIndex += 1
                control = -100
                ncv = -100
                direct = []
                for chromosomeHighIndex1 in range(0, self.chromosomeHigh):
                    if self.populationList[populationIndex][chromosomeHighIndex1][chromosomeLengthIndex] == 1:
                        control = chromosomeHighIndex1
                    elif self.populationList[populationIndex][chromosomeHighIndex1][chromosomeLengthIndex] == 0:
                        direct.append(chromosomeHighIndex1)
                    else:
                        ncv = chromosomeHighIndex1
                for directContent in direct:
                    output[directContent][inputIndex] = mid[directContent]
                if control == -100:
                    if self.populationList[populationIndex][ncv][chromosomeLengthIndex] == 5:
                        # 2表示V0，3表示V1
                        if mid[ncv] == 0:
                            output[ncv][inputIndex] = 1
                        elif mid[ncv] == 1:
                            output[ncv][inputIndex] = 0
                        elif mid[ncv] == 2:
                            output[ncv][inputIndex] = 3
                        elif mid[ncv] == 3:
                            output[ncv][inputIndex] = 2
                        mid[ncv] = output[ncv][inputIndex]
                    else:
                        print u"非门错误：控制位 = -100，受控位 =", self.populationList[populationIndex][ncv][
                            chromosomeLengthIndex]
                elif -1 < control < self.chromosomeHigh:
                    output[control][inputIndex] = mid[control]
                    if mid[control] == 0:
                        output[ncv][inputIndex] = mid[ncv]
                    elif mid[control] == 1:
                        if self.populationList[populationIndex][ncv][chromosomeLengthIndex] == 2:
                            if mid[ncv] == 0:
                                output[ncv][inputIndex] = 3
                            elif mid[ncv] == 1:
                                output[ncv][inputIndex] = 2
                            elif mid[ncv] == 2:
                                output[ncv][inputIndex] = 0
                            elif mid[ncv] == 3:
                                output[ncv][inputIndex] = 1
                            mid[ncv] = output[ncv][inputIndex]
                        elif self.populationList[populationIndex][ncv][chromosomeLengthIndex] == 3:
                            if mid[ncv] == 0:
                                output[ncv][inputIndex] = 2
                            elif mid[ncv] == 1:
                                output[ncv][inputIndex] = 3
                            elif mid[ncv] == 2:
                                output[ncv][inputIndex] = 1
                            elif mid[ncv] == 3:
                                output[ncv][inputIndex] = 0
                            mid[ncv] = output[ncv][inputIndex]
                        elif self.populationList[populationIndex][ncv][chromosomeLengthIndex] == 4:
                            if mid[ncv] == 0:
                                output[ncv][inputIndex] = 1
                            elif mid[ncv] == 1:
                                output[ncv][inputIndex] = 0
                            elif mid[ncv] == 2:
                                output[ncv][inputIndex] = 3
                            elif mid[ncv] == 3:
                                output[ncv][inputIndex] = 2
                            mid[ncv] = output[ncv][inputIndex]
                        else:
                            print u"受控位错误：控制位 =", self.populationList[populationIndex][control][
                                chromosomeLengthIndex], u"受控位 =", self.populationList[populationIndex][ncv][
                                chromosomeLengthIndex]
                    elif 1 < mid[control] < 4:
                        position1 = random.randint(0, self.chromosomeHigh - 1)
                        position2 = random.randint(0, self.chromosomeHigh - 1)
                        while position1 == position2:
                            position2 = random.randint(0, self.chromosomeHigh - 1)
                        newControl = self.populationList[populationIndex][control][chromosomeLengthIndex]
                        newNcv = self.populationList[populationIndex][ncv][chromosomeLengthIndex]
                        self.populationList[populationIndex][control][chromosomeLengthIndex] = 0
                        self.populationList[populationIndex][ncv][chromosomeLengthIndex] = 0
                        self.populationList[populationIndex][position1][chromosomeLengthIndex] = newControl
                        self.populationList[populationIndex][position2][chromosomeLengthIndex] = newNcv
                        chromosomeLengthIndex = -1
                        for chromosomeHighIndex2 in range(0, self.chromosomeHigh):
                            mid[chromosomeHighIndex2] = self.input[chromosomeHighIndex2][inputIndex]
        self.populationOutputList.append(output)
        return self.populationList, self.populationOutputList

    def calculateFitness(self):
        """2位Toffoli"""
        # target = [[0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1, 1, 0]]
        """(A+B)^C"""
        # target = [[0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0, 1, 1], [0, 1, 1, 0, 1, 0, 1, 0]]
        """控制交换门"""
        # target = [[0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 0, 1, 1]]
        """3-17"""
        target = [[1, 0, 0, 0, 1, 0, 1, 1], [1, 0, 0, 1, 0, 1, 1, 0], [1, 0, 1, 1, 0, 0, 0, 1]]
        """4位Toffoli"""
        # target = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        #           [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0]]
        # print "self.", self.populationList
        for scaleIndex in range(0, self.scalePopulation):
            fit = 0
            for targetHighIndex in range(0, len(target)):
                for targetLengthIndex in range(0, len(target[0])):
                    if target[targetHighIndex][targetLengthIndex] == \
                            self.populationOutputList[scaleIndex][targetHighIndex][targetLengthIndex]:
                        fit += 1
                    if max(self.populationList[scaleIndex][targetHighIndex]) == min(
                            self.populationList[scaleIndex][targetHighIndex]):
                        fit -= self.inputList
            self.populationFitnessList.append(fit)
        # print "fitness", self.populationFitnessList
        return self.populationFitnessList

    def findMaxFitness(self):
        self.maxFitnessList["Fitness"] = max(self.populationFitnessList)
        print self.populationFitnessList
        print '初代', self.populationList
        self.maxFitnessList["Index"] = self.populationFitnessList.index(self.maxFitnessList["Fitness"])
        self.maxFitnessList["chromosome1"] = self.populationList[self.maxFitnessList["Index"]]
        return self.maxFitnessList

    def distanceChromosome(self):
        listChromosome = []
        self.maxFitnessList["Fitness"] = max(self.populationFitnessList)
        for fitnessIndex in range(0, len(self.populationFitnessList)):
            if self.populationFitnessList[fitnessIndex] == self.maxFitnessList["Fitness"]:
                listChromosome.append(self.populationList[fitnessIndex])
        if len(listChromosome) > 1:
            maxDistance = 0
            for content1 in listChromosome:
                for content2 in listChromosome[listChromosome.index(content1) + 1: len(listChromosome)]:
                    distance = 0
                    for contentLengthIndex in range(0, len(content1[0])):
                        for contentHighIndex in range(0, len(content1)):
                            distance += (content1[contentHighIndex][contentLengthIndex] - content2[contentHighIndex][
                                contentLengthIndex]) ** 2
                    if distance >= maxDistance:
                        # print ":", content1
                        # print content2
                        self.maxFitnessList["chromosome1"] = content1
                        self.maxFitnessList["chromosome2"] = content2
                        maxDistance = distance
                        # print "mmmmmm", maxDistance
        else:
            self.maxFitnessList["chromosome1"] = listChromosome[0]
            self.maxFitnessList["chromosome2"] = listChromosome[0]
        return self.maxFitnessList

    def cross(self):
        # self.nextPopulation = self.populationList
        for populationIndex in range(0, len(self.populationList), 2):
            individual1 = random.randint(0, len(self.populationList) - 1)
            individual2 = random.randint(0, len(self.populationList) - 1)
            while individual1 == individual2:
                individual2 = random.randint(0, len(self.populationList) - 1)
            if random.random() < self.crossProbability:
                tempLine1 = []
                tempLine2 = []
                tempChromosome1 = []
                tempChromosome2 = []
                crossPosition = random.randint(0, self.chromosomeLength - 1)
                for highIndex in range(0, self.chromosomeHigh):
                    tempLine1.extend(self.populationList[individual1][highIndex][0: crossPosition])
                    tempLine1.extend(self.populationList[individual2][highIndex][crossPosition: self.chromosomeLength])
                    tempLine2.extend(self.populationList[individual2][highIndex][0: crossPosition])
                    tempLine2.extend(self.populationList[individual1][highIndex][crossPosition: self.chromosomeLength])
                    tempChromosome1.append(tempLine1)
                    tempChromosome2.append(tempLine2)
                    tempLine1 = []
                    tempLine2 = []
                self.nextPopulation.append(tempChromosome1)
                self.nextPopulation.append(tempChromosome2)
            else:
                self.nextPopulation.append(self.populationList[individual1])
                self.nextPopulation.append(self.populationList[individual2])
        return self.nextPopulation

    def mutation(self):
        for scaleIndex in range(0, self.scalePopulation):
            if random.random() < self.mutationProbability:
                if random.random() < 0.5:
                    self.nextPopulation[scaleIndex] = self.createChromosome()
                else:
                    position = random.randint(0, self.chromosomeLength - 1)
                    genIndex, pos1, pos2 = self.chooseGene()
                    for highIndex in range(0, self.chromosomeHigh):
                        self.nextPopulation[scaleIndex][highIndex][position] = 0
                    self.nextPopulation[scaleIndex][pos1][position] = self.gene[0][genIndex]
                    self.nextPopulation[scaleIndex][pos2][position] = self.gene[1][genIndex]
        return self.nextPopulation

    def optimalReserve(self):
        individual = random.randint(0, self.scalePopulation - 1)
        individual2 = random.randint(0, self.scalePopulation - 1)
        while individual == individual2:
            individual2 = random.randint(0, self.scalePopulation - 1)
        self.nextPopulation[0] = self.maxFitnessList["chromosome1"]
        if self.maxFitnessList["chromosome1"] != self.maxFitnessList["chromosome2"]:
            # print 'oooooooooooo', self.maxFitnessList["chromosome1"]
            # print 'oooooooooooo', self.maxFitnessList["chromosome2"]
            self.nextPopulation[1] = self.maxFitnessList["chromosome2"]
        self.populationList = self.nextPopulation
        self.nextPopulation = []
        self.populationOutputList = []
        self.populationFitnessList = []
        return self.populationList, self.nextPopulation, self.populationOutputList, self.populationFitnessList


def main():
    localtime = time.asctime(time.localtime(time.time()))
    print "********", "Local current time :", localtime, "********"
    print u"程序开始运行，请等待结果..."
    number = 0
    f = open("text.txt", 'wt')
    fileNumber = 0
    print >> f, "********", "Local current time :", localtime, "********"
    a = Population()
    a.createPopulation()
    a.chromosomeInput()
    while a.maxFitnessList["Fitness"] < a.chromosomeHigh * a.inputList:
        number += 1
        for scaleIndex in range(0, a.scalePopulation):
            a.calculateOutput(scaleIndex)
        a.calculateFitness()
        # print a.findMaxFitness()
        a.distanceChromosome()
        a.cross()
        a.mutation()
        a.optimalReserve()
        print >> f, "_____________第%d代________________" % (number)
        print >> f, "Fitness =", a.maxFitnessList["Fitness"]
        print >> f, "   ##########maxFitnessList[chromosome1]########"
        for highIndex in range(a.chromosomeHigh):
            print >> f, a.maxFitnessList["chromosome1"][highIndex]
        if a.maxFitnessList["chromosome1"] != a.maxFitnessList["chromosome2"]:
            print >> f, "   ##########maxFitnessList[chromosome2]########"
            for highIndex in range(a.chromosomeHigh):
                print >> f, a.maxFitnessList["chromosome2"][highIndex]
        size = os.path.getsize("text.txt")
        if size > 50000000:
            print size
            f.close()
            name = "text" + str(fileNumber) + ".txt"
            os.rename("text.txt", name)
            fileNumber += 1
            f = open("text.txt", 'wt')
            localtime = time.asctime(time.localtime(time.time()))
            print >> f, "********", "Local current time :", localtime, "********"
    for scaleIndex in range(0, a.scalePopulation):
        print >> f, "****第%d个体****" % (scaleIndex)
        for highIndex in range(0, a.chromosomeHigh):
            print >> f, a.populationList[scaleIndex][highIndex]
    print >> f, "______****_______最优结果_______****_________"
    for highIndex in range(a.chromosomeHigh):
        print >> f, a.maxFitnessList["chromosome1"][highIndex]
    print u"程序运行结束，详情请查看：text.txt"
    localtime = time.asctime(time.localtime(time.time()))
    print "********", "Local current time :", localtime, "********"
    print >> f, "********", "Local current time :", localtime, "********"
    f.close()


main()
