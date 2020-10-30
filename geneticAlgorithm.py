import random
import math
from individual import Individual
from kspIndividual import KSPIndividual

class GeneticAlgorithm():
    def __init__(self, geneSize, populationSize, crossoverProb, mutationProb):
        # geneSize: gene size of individual
        # populationSize: total number of genes
        # crossoverProb: the probability of crossover operator
        # mutationProb: the probability of mutation operator
        # population: the list of individuals(geneSize, gene, totalWeight, totalProfit)
        # best: the best profit of population
        # mean: mean value of fitness of population
        self.geneSize = geneSize
        self.populationSize = populationSize
        self.crossoverProb = crossoverProb
        self.mutationProb = mutationProb
        self.population = []
        self.offspring = []
        self.best = 0
        self.mean = 0

    def initialization(self):
        # Generate random sampled genes of a population size
        # gene: bit-string of gene size
        for _ in range(self.populationSize):
            gene = KSPIndividual(self.geneSize)
            gene.initialization()
            self.population.append(gene)
        print(self.populationSize, 'genes are generated!')

    def kspRouletteWheelSelection(self):
        tmp_pop = []
        roulette = 0

        # Roulette wheel selection with raw profit value show bad selection performance,
        # because profits have large and not normalized value.
        # To decrease the unbalanced proportion of roulette,
        # normalization technique, max-min scaling is used.
        # It normalize profit values from 0 to 1.
        # For this, get max and min of fitness set.

        # Max-min scaling
        # for i, individual in enumerate(self.population):
        #     if individual.totalDist != 0:
        #         individual.totalDist = fmax - individual.totalDist
        #         self.fitness[i] = individual.totalDist

        # fmax = max(self.fitness)
        # fmin = min(self.fitness)

        for individual in self.population:
            # individual.totalDist = (individual.totalDist - fmin) / (fmax - fmin)
            roulette += individual.totalDist

        # Roulette Wheel Selection with max-min scaling
        for i in range(self.populationSize):
            pivot = random.random()
            k = 0
            slot = 0
            while k < len(self.population) and pivot > (slot / roulette):
                slot += self.population[k].totalDist
                k += 1

            k -= 1
            tmp_pop.append(self.population[k])

        self.population = tmp_pop

    def kspPairWiseTournamentSelection(self):
        # Pair-wise Tournament Selection
        tmp_pop = []

        for individual in self.population:
            competitive = self.population[random.randint(0, self.populationSize-1)]
            if individual.totalDist < competitive.totalDist:
                tmp_pop.append(individual)
            else:
                tmp_pop.append(competitive)

        self.population = tmp_pop

    def rankingSelection(self, phi):
        tmp_pop = []
        selectionProb = {}
        alpha = (2 * self.populationSize - phi * (self.populationSize + 1)) / (self.populationSize * (self.populationSize - 1))
        beta = (2 * (phi - 1)) / (self.populationSize * (self.populationSize - 1))

        sortedFitness = sorted(self.fitness.items(), key=(lambda x:x[1]), reverse=True)
        for i, item in enumerate(sortedFitness):
            selectionProb[item[0]] = alpha + beta * (i+1)

        for i in range(self.populationSize):
            pivot = random.random()
            sum_prob = 0
            idx = 0
            while pivot > sum_prob:
                sum_prob += selectionProb[sortedFitness[idx][0]]
                idx += 1

            idx -= 1    
            tmp_pop.append(self.population[sortedFitness[idx][0]])

    def sortingSelection(self):
        tmp_pop = []
        count = 0
        for fit in self.sortedFit:
            tmp_pop.append(self.population[fit[0]])
            count += 1
            if count >= self.populationSize:
                break
        self.population = tmp_pop

    def orderOneCrossover(self):
        tmp_pop = []
        random.shuffle(self.population)

        for i in range(int(self.populationSize/2)):
            if random.random() < self.crossoverProb:
                pos = [random.randint(0, self.geneSize-1), random.randint(0, self.geneSize-1)]
                pos.sort()

                p1 = self.population[i].gene
                p2 = self.population[i + int(self.populationSize/2)].gene

                ch1 = p2[pos[0]:pos[1]]
                ch2 = p1[pos[0]:pos[1]]

                tmp1 = []
                tmp2 = []

                for locus in p1:
                    if not locus in ch1:
                        tmp1.append(locus)
                for locus in p2:
                    if not locus in ch2:
                        tmp2.append(locus)

                ch1 = tmp1[:pos[0]] + ch1 + tmp1[pos[0]:]
                ch2 = tmp2[:pos[0]] + ch2 + tmp2[pos[0]:]

                np1 = KSPIndividual(self.geneSize)
                np2 = KSPIndividual(self.geneSize)
                np1.initialization(ch1)
                np2.initialization(ch2)
                tmp_pop.append(np1)
                tmp_pop.append(np2)

        self.offspring = tmp_pop

    def orderTwoCrossover(self):
        tmp_pop = []
        random.shuffle(self.population)

        while len(tmp_pop) < len(self.population):
            if random.random() < self.crossoverProb:
                pos = [random.randint(0, self.geneSize-1), random.randint(0, self.geneSize-1)]
                pos.sort()

                p1 = self.population[random.randint(0, len(self.population)-1)].gene
                p2 = self.population[random.randint(0, len(self.population)-1)].gene

                ch1 = p2[pos[0]:pos[1]]
                ch2 = p1[pos[0]:pos[1]]

                tmp1 = []
                tmp2 = []

                for locus in p1:
                    if not locus in ch1:
                        tmp1.append(locus)
                for locus in p2:
                    if not locus in ch2:
                        tmp2.append(locus)

                ch1 = tmp1[:pos[0]] + ch1 + tmp1[pos[0]:]
                ch2 = tmp2[:pos[0]] + ch2 + tmp2[pos[0]:]

                np1 = KSPIndividual(self.geneSize)
                np2 = KSPIndividual(self.geneSize)
                np1.initialization(ch1)
                np2.initialization(ch2)
                tmp_pop.append(np1)
                tmp_pop.append(np2)

        self.offspring = tmp_pop

    def partialMappedCrossover(self):
        tmp_pop = []
        random.shuffle(self.population)

        while len(tmp_pop) < len(self.population):
            if random.random() < self.crossoverProb:
                pos = [random.randint(0, self.geneSize-1), random.randint(0, self.geneSize-1)]
                pos.sort()

                p1 = self.population[random.randint(0, len(self.population)-1)].gene
                p2 = self.population[random.randint(0, len(self.population)-1)].gene

                ch1 = p2[pos[0]:pos[1]]
                ch2 = p1[pos[0]:pos[1]]

                tmp1 = []
                tmp2 = []

                o1 = []
                o2 = []

                for locus in p1:
                    if locus in ch1:
                        tmp1.append(locus)
                for locus in p2:
                    if locus in ch2:
                        tmp2.append(locus)

                for locus in p1:
                    if not locus in ch1:
                        tmp1.append(locus)
                    else:
                        tmp2.pop(0)
                for locus in p2:
                    if not locus in ch2:
                        tmp2.append(locus)
                    else:
                        tmp1.pop(0)

                o1 = tmp1[:pos[0]] + ch1 + tmp1[pos[0]:]
                o2 = tmp2[:pos[0]] + ch2 + tmp2[pos[0]:]

                np1 = KSPIndividual(self.geneSize)
                np2 = KSPIndividual(self.geneSize)
                np1.initialization(o1)
                np2.initialization(o2)
                tmp_pop.append(np1)
                tmp_pop.append(np2)

        self.offspring = tmp_pop

    def orderCrossover(self):
        pass

    def cycleCrossover(self):
        tmp_pop = []
        random.shuffle(self.population)

        while len(tmp_pop) < len(self.population):
            if random.random() < self.crossoverProb:
                p1 = self.population[random.randint(0, len(self.population)-1)].gene
                p2 = self.population[random.randint(0, len(self.population)-1)].gene
                
                tmp1 = {}
                tmp2 = {}

                o1 = []
                o2 = []

                pick = 0
                while not p2[pick] in tmp1.values():
                    tmp1[pick] = p1[pick]
                    pick = p1.index(p2[pick])
                tmp1[pick] = p1[pick]

                for k, _ in tmp1.items():
                    tmp2[k] = p2[k]

                for i in range(len(p1)):
                    if not i in tmp1:
                        tmp1[i] = p2[i]
                for i in range(len(p2)):
                    if not i in tmp2:
                        tmp2[i] = p1[i]

                for i in range(self.geneSize):
                    o1.append(tmp1[i])
                    o2.append(tmp2[i])

                np1 = KSPIndividual(self.geneSize)
                np2 = KSPIndividual(self.geneSize)
                np1.initialization(o1)
                np2.initialization(o2)
                tmp_pop.append(np1)
                tmp_pop.append(np2)

        self.offspring = tmp_pop

    def reorderMutation(self):
        for individual in self.offspring:
            for i in range(self.geneSize):
                if random.random() < self.mutationProb:
                    idx = random.randint(0, self.geneSize - 1)
                    while idx == i:
                        idx = random.randint(0, self.geneSize - 1)

                    tmp = individual.gene[i]
                    individual.gene[i] = individual.gene[idx]
                    individual.gene[idx] = tmp

    def combination(self):
        self.population = self.population + self.offspring
        self.offspring = []

    def getElite(self):
        self.elite = self.population[self.sortedFit[0][0]]

    def setElite(self):
        if self.elite:
            worst_key = self.sortedFit[len(self.sortedFit)-1][0]
            self.population[worst_key] = self.elite

    def calculateFitness(self, salesman):
        self.fitness = {}
        for i, gene in enumerate(self.population):
            gene.evaluation(salesman)
            self.fitness[i] = gene.totalDist

        self.sortedFit = sorted(self.fitness.items(), key=(lambda x:x[1]), reverse=True)
        self.best = self.sortedFit[0][1]
        self.mean = sum(self.fitness.values()) / len(self.fitness)

        return self.best, self.mean

    def printMaxSolution(self):
        print(max(self.fitness.values()))

    def printMinSolution(self):
        print(min(self.fitness.values()))