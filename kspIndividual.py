from simpleError import DatasetError
import random
import math

class KSPIndividual():
    def __init__(self, geneSize):
        # geneSize: length of chromosome. In this problem, gene size is 500.
        # gene: List of locus. allele of locus is 1 or 0.
        # totalWeight: Sum of item weight. It can't jump over capacity of Knapsack.
        # totalProfit: Sum of item profit. It is fitness value of individual.
        # If totalWeight > capacity, totalProfit = 0.
        self.geneSize = geneSize
        self.gene = []
        self.totalDist = 0

    def initialization(self, gene=[]):
        # If input gene is not exist, gene is randomly generated by bit 0, 1
        if not gene:
            for i in range(self.geneSize):
                self.gene.append(i)
            random.shuffle(self.gene)
        else:
            s = set(gene)
            if len(s) < self.geneSize:
                raise DatasetError()
            self.gene = gene

    def evaluation(self, salesman):
        # Evaluate individual.
        # Sum all weight and profit of items individual have.
        # If totalWeight is bigger than capacity, totalProfit is 0.
        location = salesman.location
        for i, _ in enumerate(self.gene):
            cur = self.gene[i]
            nxt = self.gene[(i+1)%self.geneSize]
            x = location[nxt][0] - location[cur][0]
            y = location[nxt][1] - location[cur][1]
            self.totalDist += math.sqrt(x**2 + y**2)
        self.totalDist = 1/self.totalDist