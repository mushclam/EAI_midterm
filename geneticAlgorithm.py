import random
from individual import Individual

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
            gene = Individual(self.geneSize)
            gene.initialization()
            self.population.append(gene)
        print(self.populationSize, 'genes are generated!')

    def rouletteWheelSelection(self):
        tmp_pop = []
        roulette = 0

        # Remove 0 profit individuals in population and fitness
        n_pop = []
        self.fitness = []
        for individual in self.population:
            if individual.totalProfit > 0:
                self.fitness.append(individual.totalProfit)
                n_pop.append(individual)
        self.population = n_pop

        # Roulette wheel selection with raw profit value show bad selection performance,
        # because profits have large and not normalized value.
        # To decrease the unbalanced proportion of roulette,
        # normalization technique, max-min scaling is used.
        # It normalize profit values from 0 to 1.
        # For this, get max and min of fitness set.
        fmax = max(self.fitness)
        fmin = min(self.fitness)

        # Max-min scaling
        for individual in self.population:
            if individual.totalProfit != 0:
                individual.totalProfit = (individual.totalProfit - fmin) / (fmax - fmin)
                roulette += individual.totalProfit

        # Roulette Wheel Selection with max-min scaling
        for i in range(self.populationSize):
            pivot = random.random()
            k = 0

            slot = self.population[k].totalProfit
            while k < len(self.population) and pivot > (slot / roulette):
                k += 1
                slot += self.population[k].totalProfit

            tmp_pop.append(self.population[k])

        self.population = tmp_pop

    def pairwiseTournamentSelection(self):
        # Pair-wise Tournament Selection
        tmp_pop = []

        for individual in self.population:
            competitive = self.population[random.randint(0, self.populationSize-1)]
            if individual.totalProfit < competitive.totalProfit:
                tmp_pop.append(competitive)
            else:
                tmp_pop.append(individual)

        self.population = tmp_pop

    def threePointCrossover(self):
        # To remove positional bias of selection,
        # Shuffle elements of population.
        random.shuffle(self.population)

        # 3-point crossover
        for i in range(int(self.populationSize / 2)):
            if random.random() < self.crossoverProb:
                # Get 3-point randomly and sort positions.
                pos = [random.randint(1, self.geneSize - 1),
                        random.randint(1, self.geneSize - 1),
                        random.randint(1, self.geneSize - 1)]
                pos.sort()

                # Take gene of parents.
                p1 = self.population[i].gene
                p2 = self.population[i + int(self.populationSize/2)].gene
                # crossover based on sorted positions.
                tmp1 = p1[:pos[0]] + p2[pos[0]:pos[1]] + p1[pos[1]:pos[2]] + p2[pos[2]:]
                tmp2 = p2[:pos[0]] + p1[pos[0]:pos[1]] + p2[pos[1]:pos[2]] + p1[pos[2]:]
                # Generate children.
                np1 = Individual(self.geneSize)
                np2 = Individual(self.geneSize)
                np1.initialization(tmp1)
                np2.initialization(tmp2)
                # Put into population.
                self.population[i] = np1
                self.population[i + int(self.populationSize/2)] = np2

    def bitwiseMutation(self):
        # 0 to 1, 1 to 0 if locus is mutated
        for individual in self.population:
            for i in range(self.geneSize):
                if random.random() < self.mutationProb:
                    if individual.gene[i] == 0:
                        individual.gene[i] = 1
                    else:
                        individual.gene[i] = 0

    def calculateFitness(self, problem, dataset):
        if problem == 'KP':
            self.KPFitness(dataset)
        elif problem == 'TSP':
            self.TSPFitness(dataset)

    def KPFitness(self, knapsack):
        # capacity: total weight capacity = knapsack.capacity
        # If chromosome in gene is 1, sum weight and profit of dataset[chromosome index]
        # If total weight of gene is larger than total weight capacity, Total profit of gene is 0.
        self.fitness = []
        for gene in self.population:
            gene.evaluation(knapsack)
            self.fitness.append(gene.totalProfit)

        self.best.append(max(self.fitness))
        self.mean.append(sum(self.fitness) / len(self.fitness))

    def TSPFitness(self, salesman):
        self.fitness = []
        for gene in self.population:
            return

    def printBestSolution(self):
        print(max(self.fitness))