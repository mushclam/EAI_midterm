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
        self.best = []
        self.mean = []

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
        fmax = max(self.fitness)

        # Max-min scaling
        for i, individual in enumerate(self.population):
            if individual.totalDist != 0:
                individual.totalDist = fmax - individual.totalDist
                self.fitness[i] = individual.totalDist

        fmax = max(self.fitness)
        fmin = min(self.fitness)

        for individual in self.population:
            individual.totalDist = (individual.totalDist - fmin) / (fmax - fmin)
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

    def orderOneCrossover(self):
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
                np1.initialization(tmp1)
                np2.initialization(tmp2)
                self.population[i] = np1
                self.population[i + int(self.populationSize/2)] = np2

    def reorderMutation(self):
        for individual in self.population:
            for i in range(self.geneSize):
                if random.random() < self.mutationProb:
                    idx = random.randint(0, self.geneSize - 1)
                    while idx == i:
                        idx = random.randint(0, self.geneSize - 1)

                    tmp = individual.gene[i]
                    individual.gene[i] = individual.gene[idx]
                    individual.gene[idx] = tmp

    def calculateFitness(self, salesman):
        self.fitness = {}
        for i, gene in enumerate(self.population):
            gene.evaluation(salesman)
            self.fitness[i] = gene.totalDist

        self.best.append(min(self.fitness.values()))
        self.mean.append(sum(self.fitness.values()) / len(self.fitness))

    def printMaxSolution(self):
        print(max(self.fitness.values()))

    def printMinSolution(self):
        print(min(self.fitness.values()))