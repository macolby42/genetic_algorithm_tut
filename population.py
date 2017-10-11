from member import Member
import random
import json
from math import sqrt

class Population:
    def __init__(self, popSize, file, maxCap, goal, gensUntil):
        self.pop = []
        self.popSize = popSize
        self.gensUntil = gensUntil
        self.goal = goal
        self.currGen = 0
        self.initializeMembers(file, maxCap)
        self.bestAvg = 0
        self.bestFit = self.pop[0].fitness
        self.staleCount = 0
        self.gensUntil = gensUntil
        self.bestGen = 0
        self.bestMember = None

    def initializeMembers(self, file, maxCap):
        data = json.load(file)
        self.itemList = data["items"]
        for x in range(self.popSize):
            m = Member(self.itemList, maxCap)
            self.pop.append(m)
        self.pop.sort(key=lambda x: x.fitness)
        self.bestMember = self.pop[-1]
        self.bestFit = self.bestMember.fitness

    def run(self):
        finished = False
        while not finished: #1.0 is what we find acceptable
            self.currGen = self.currGen + 1
            self.repopulate()
            if self.pop[-1].fitness > self.bestFit:
                self.bestMember = self.pop[-1]
                self.bestFit = self.pop[-1].fitness
                self.bestGen = self.currGen
                print("New Best!")
                self.printResults(self.bestMember)
                self.staleCount = 0 #reset because we're doing better

            if self.avg > self.bestAvg:
                self.bestAvg = self.avg
                print("Better Average: {0} in Generation {1}".format(self.bestAvg, self.currGen))

            if self.currGen % 1000 == 0 and self.currGen > 1:
                print("Gen {0}".format(self.currGen))

            self.staleCount = self.staleCount + 1
            if self.bestFit > self.goal:
                finished = True
            elif self.gensUntil < self.staleCount:
                finished = True

        self.printResults(self.bestMember, knapPrint=True)

    def printResults(self, member, knapPrint=False):
        if knapPrint:
            for item in member.knapsack:
                print(item['item'])
        print("Items: {0}".format(len(member.knapsack)))
        print("Fitness: {0}".format(member.fitness))
        print("Value: {0}".format(member.value))
        print("Weight: {0}".format(member.weight))
        print("Generation: {0}".format(self.bestGen))

    def repopulate(self):
        self.pop.sort(key=lambda x: x.fitness)
        #print("Low: {0} High: {1}".format(self.pop[0].fitness, self.pop[-1].fitness))
        breed = self.popSize // 2
        toCross = self.pop[breed:]
        toKill = self.pop[:breed]
        newBorn = []
        for m in range(len(toCross)):
            p1 = toCross[m]
            p2 = toCross[m-1]
            baby = self.cross(p1, p2, toKill[m])
            newBorn.append(baby)

        #replace all the poor performers with the offspring of the better performers
        self.pop[:breed] = newBorn

        #get the average and along the way see if anyone will mutate!
        s = 0
        for m in range(len(self.pop)):
            r = random.randint(0,100)
            #the top 4 can't be mutated
            if r > 80 or m > len(self.pop)-4:
                self.pop[m].mutate(self.itemList)
            s = s + self.pop[m].fitness
        self.avg = s / self.popSize

    def cross(self, p1, p2, dead):
        maHalf = len(p1.knapsack) // 2
        paHalf = len(p2.knapsack) // 2
        ma = p1.knapsack[:]
        pa = p2.knapsack[1::2]
        dead.rebirth(ma, pa, maHalf, paHalf)
        return dead
