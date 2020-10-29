import argparse
import datetime
import json
import os
import random
import sys

from matplotlib import pyplot as plt

from geneticAlgorithm import GeneticAlgorithm
from individual import Individual
from knapsack import Knapsack
from salesman import Salesman

if __name__ == '__main__':
    # Set work directory
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    os.chdir(path)
    # Argument parsing
    parser = argparse.ArgumentParser(description='Basic Genetic Algorithm Sample')
    parser.add_argument('-p', '--problem', dest='problem', action='store',
                        default='TSP', type=str, help='Choose the problem(KP/TSP).')
    parser.add_argument('-cprob', '--crossoverProbability', dest='crossover_prob', action='store', 
                        default=0.9, type=float, help='Set the probability of crossover operator.')
    parser.add_argument('-mprob', '--mutationProbability', dest='mutation_prob', action='store',
                        default=0.01, type=float, help='Set the probability of mutation operator.')
    parser.add_argument('-psize', '--populationSize', dest='population_size', action='store',
                        default=300, type=int, help='Set the size of population.')
    parser.add_argument('-gen', '--generation', dest='generation', action='store',
                        default=500, type=int, help='Set the maximum generation.')
    parser.add_argument('-in', '--input', dest='filename', action='store',
                        default='tsp_data.txt', type=str, help='Set the input filename.')
    parser.add_argument('-out', '--output', dest='output', action='store',
                        default='result.json', type=str, help='Set the output filename(json).')
    args = parser.parse_args()
    # Check argument by standard output
    print(args)

    # Set arguments to variables
    problem = args.problem
    filename = args.filename
    crossover_prob = args.crossover_prob
    mutation_prob = args.mutation_prob
    popSize = args.population_size
    generation = args.generation

     # Traveling Salesman Problem Dataset
    dataset = Salesman(filename)
    dataset.read()
    gene_size = len(dataset.location)

    # Generate each GA instance
    # roulette = GeneticAlgorithm(gene_size, popSize, crossover_prob, mutation_prob)
    # tournament = GeneticAlgorithm(gene_size, popSize, crossover_prob, mutation_prob)
    ranking = GeneticAlgorithm(gene_size, popSize, crossover_prob, mutation_prob)

    # # Roulette Wheel selection GA Initialization
    # print('Roulette', end=' ')
    # roulette.initialization()
    # roulette.calculateFitness(dataset)
    # # Tournament selection GA Initialization
    # print('Tournament', end=' ')
    # tournament.initialization()
    # tournament.calculateFitness(dataset)
    print('Ranking', end=' ')
    ranking.initialization()
    ranking.calculateFitness(dataset)

    # Training
    for i in range(generation):
        # roulette.kspRouletteWheelSelection()
        # roulette.orderOneCrossover()
        # roulette.reorderMutation()
        # roulette.calculateFitness(dataset)
        
        # tournament.kspPairWiseTournamentSelection()
        # tournament.orderOneCrossover()
        # tournament.reorderMutation()
        # tournament.calculateFitness(dataset)

        ranking.rankingSelection(2)
        ranking.orderOneCrossover()
        ranking.reorderMutation()
        ranking.calculateFitness(dataset)

    # Print total best results.
    # print('Roulette Wheel Selection best profit:', max(roulette.best))
    # print('Roulette Wheel Selection mean of profit:', max(roulette.mean))
    # print('Pairwise Tournament Selection best profit:', max(tournament.best))
    # print('Pairwise Tournament Selection mean of profit:', max(tournament.mean))
    print('Ranking Selection best profit:', max(ranking.best))
    print('Ranking Selection mean of profit:', max(ranking.mean))

    # # Save result to json format
    # result_file = args.output
    # if os.path.isfile(result_file):
    #     with open(result_file, 'r') as f:
    #         jsonDict = json.load(f)
    #     for i in range(generation+1):
    #         jsonDict[i]['roulette'].append(roulette.best[i])
    #         jsonDict[i]['tournament'].append(tournament.best[i])
    #     jsonString = json.dumps(jsonDict, indent=4)
    #     with open(result_file, 'w') as f:
    #         f.write(jsonString)
        
    # else:
    #     tmp_list = []
    #     for i in range(generation+1):
    #         tmp_dict = {
    #             'generation' : i,
    #             'roulette' : [roulette.best[i]],
    #             'tournament' : [tournament.best[i]]
    #         }
    #         tmp_list.append(tmp_dict)
    #     jsonString = json.dumps(tmp_list, indent=4)
    #     with open(result_file, 'w') as f:
    #         f.write(jsonString)

    # Draw plot of results.
    # plt.plot(range(generation+1), roulette.best, color='blue')
    # plt.plot(range(generation+1), roulette.mean, color='blue', linestyle='--')
    # plt.plot(range(generation+1), tournament.best, color='orange')
    # plt.plot(range(generation+1), tournament.mean, color='orange', linestyle='--')
    plt.plot(range(generation+1), ranking.best, color='green')
    plt.plot(range(generation+1), ranking.mean, color='green', linestyle='--')
    plt.xlabel('generation')
    plt.ylabel('total profit')
    # plt.legend(['roulette best', 'roulette mean', 'tournament best', 'tournament mean', 'ranking best', 'ranking mean'])
    plt.legend(['ranking best', 'ranking mean'])
    now = datetime.datetime.now()
    plt.savefig('result/' + now.strftime('%Y-%m-%d_%H:%M:%S') + '.png')
