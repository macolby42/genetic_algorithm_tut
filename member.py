import json
import numpy.random as random

class Member:
    def __init__(self, itemList, maxCap):
        self.maxCap = maxCap
        self.weight = 0
        self.value = 0
        self.knapsack = []
        self.fitness = 0
        self.initChrom(itemList)

    def initChrom(self, itemList):
        while self.weight < self.maxCap:
            r = random.randint(len(itemList))
            item = itemList[r]
            #to make sure we don't go over adding the final item
            weight = self.weight + item['weight']
            if weight > self.maxCap:
                break
            self.weight = self.weight + item['weight']
            self.knapsack.append(item)
            self.filterKnapsack()
        self.getFit()

    def filterKnapsack(self):
        self.knapsack = list({x['item']:x for x in self.knapsack}.values())


    def rebirth(self, ma, pa, maHalf, paHalf):
        self.knapsack[:maHalf] = ma
        self.knapsack[paHalf:] = pa
        self.filterKnapsack()
        self.getFit()

    def mutate(self, itemList):
        while self.weight < self.maxCap:
            r = random.randint(len(itemList))
            item = itemList[r]
            #to make sure we don't go over adding the final item
            weight = self.weight + item['weight']
            if weight > self.maxCap:
                break
            self.weight = self.weight + item['weight']
            self.value = self.value + item['value']
            self.knapsack.append(item)
            self.filterKnapsack()

    #Fitness = Total Value - Any Penilty for Over Capacity
    def getFit(self):
        self.weight = 0
        self.value = 0
        for item in self.knapsack:
            self.weight = self.weight + item['weight']
            self.value = self.value + item['value']

        over = self.weight - self.maxCap
        if over > 0:
            over = self.weight * 100 #the fitness is penalized if over capacity
        else:
            over = 0

        self.fitness = self.value - over
