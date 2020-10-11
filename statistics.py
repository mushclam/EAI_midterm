import json
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    json_file = 'result.json'
    with open(json_file, 'r') as f:
        jsonDict = json.load(f)

    generations = []
    roulette_means = []
    roulette_stds = []
    tournament_means = []
    tournament_stds = []
    for element in jsonDict:
        generations.append(element['generation'])

        roulette = np.array(element['roulette'])
        roulette_means.append(roulette.mean())
        roulette_stds.append(roulette.std())

        tournament = np.array(element['tournament'])
        tournament_means.append(tournament.mean())
        tournament_stds.append(tournament.std())

    plt.errorbar(generations, roulette_means, roulette_stds, color='orange')
    plt.errorbar(generations, tournament_means, tournament_stds, color='blue')
    plt.xlabel('generation')
    plt.ylabel('total profit')
    plt.legend(['roulette', 'tournament'])
    plt.show()