import random
import numpy as np
from copy import deepcopy
from selection import deterministic_survivor_selection, stochastic_universal_sampling, tournament_selection, roulette_wheel, random_selection
from mutation import scramble_mutation, swap_mutation, inverse_mutation
from population import population
from crossover import uniform_crossover
from fitness import fitness, convert_back, get_all_fitness
from crossover import *
from tabulate import tabulate

easy_sudoku =  np.array([[3,1,5,6,0,0,0,0,4],
                    [0,9,0,0,0,0,2,0,0],
                    [2,0,0,5,9,0,0,1,3],
                    [0,6,0,1,7,5,0,0,0],
                    [1,8,0,3,0,0,7,0,0],
                    [5,3,0,0,4,0,0,9,6],
                    [0,2,9,0,5,1,0,7,8],
                    [0,0,0,0,3,0,0,2,0],
                    [7,4,3,0,0,2,5,0,0]])

medium_sudoku =  np.array([[0,0,8,9,0,0,3,4,5],
                    [0,4,3,8,5,0,7,0,6],
                    [6,0,2,4,0,0,0,0,0],
                    [0,6,0,2,0,0,0,0,0],
                    [0,0,0,0,8,0,0,0,8],
                    [0,0,0,7,0,4,1,0,2],
                    [0,0,0,0,9,0,0,0,0],
                    [5,0,0,0,0,2,0,8,0],
                    [7,0,0,0,6,0,0,1,3]])

hard_sudoku =  np.array([[1,7,8,9,0,0,3,4,6],
                    [0,4,0,1,0,6,0,0,0],
                    [0,0,0,0,0,5,2,0,8],
                    [4,0,0,0,7,8,0,0,0],
                    [0,0,6,0,0,0,0,0,5],
                    [0,0,0,0,0,1,3,0,0],
                    [0,2,0,9,0,4,5,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [8,1,0,0,0,0,6,4,9]])

evil_sudoku =  np.array([[0,4,0,0,0,9,0,0,0],
                    [0,7,0,0,0,0,2,0,0],
                    [0,0,6,3,4,0,0,0,5],
                    [0,0,9,0,0,5,0,0,0],
                    [0,0,0,0,0,8,0,0,1],
                    [0,6,0,1,9,0,0,7,0],
                    [0,0,0,8,0,0,0,0,0],
                    [3,0,0,0,0,0,0,5,0],
                    [0,0,4,6,1,0,0,0,3]])

def dimensionality(sudoku):
    dimension = 0
    for i in sudoku:
        for j in i:
            if j==0:
                dimension+=1
    return dimension

def evolve(sudoku, max_gen, pop_size, num_offspring, cx_rate):
    pop, pos = population(sudoku, pop_size, 0.3)
    best_ind = []
    fitnesses = []
    for gen in range(max_gen):
        mating_pool = random_selection(pop, num_offspring)
        # mating_pool = tournament_selection(pop, num_offspring, 2)
        mating_pool = uniform_crossover(mating_pool, cx_rate)
        # rand = random.randint(1, 3)
        # if rand == 1:
        #     mating_pool = order_crossover(mating_pool, pos)
        # elif rand == 2:
        #     mating_pool = PMX_crossover(mating_pool, pos)
        # else:
        #     mating_pool = cycle_crossover(mating_pool, pos)
        rand = random.randint(1, 2)
        if rand == 1:
            mutants = scramble_mutation(mating_pool, pos)
        elif rand==2:
            mutants = swap_mutation(mating_pool, pos)
#         else:
#             mutants = inverse_mutation(mating_pool, pos)
        rand = random.randint(1, 1)
        if rand == 1:
            survivors = deterministic_survivor_selection(pop, mutants)
        else:
            survivors = tournament_selection(mutants+pop, len(pop), 2)
        average_fitness = sum(get_all_fitness(survivors))/len(survivors)
        best_ind.append(survivors[0])
        fitnesses.append(fitness(survivors[0]))
        if (gen+1)%100==0:
            print('Generation {}'.format(gen+1), survivors[0])
            print('Fitness', fitness(survivors[0]))
            print('Average fitness', average_fitness)
        if fitness(survivors[0])==0:
            print('Generation {}'.format(gen + 1), survivors[0])
            print('Found it!')
            print(convert_back(survivors[0]))
            break
        pop = survivors
    return pop, fitnesses

# best_ind, fitnesses = evolve(easy_sudoku, 3000, 10, 50, 0.5)
# for i in range(len(best_ind)):
#     if (i + 1) % 100 == 0:
#         print('Generation {}'.format(i + 1), best_ind[i])
#         print('Fitness', fitness(best_ind[i]))
#     if fitness(best_ind[i]) == 0:
#         print('Generation {}'.format(i + 1), best_ind[i])
#         print('Found it!')
#         print(convert_back(best_ind[i]))
#         break

def run(num_run):
    best_inds = []
    highest_fit = []
    for i in range(num_run):
        print()
        print('This is {} run'.format(i+1))
        pop, fit = evolve(easy_sudoku, 4000, 50, 50, 0.5)
        best_inds.append(pop[-1])
        highest_fit.append(fit[-1])
    data = [[] for _ in range(num_run)]
    for i in range(num_run):
        data[i].append(best_inds[i])
        data[i].append(highest_fit[i])
    high = pd.Series(highest_fit)
    print(highest_fit, '\n', high.describe())
    header = ['Best Individual of Each Run', "Highest Fitness Value of Each Run"]
    return tabulate(data, header, tablefmt='grid', showindex='always')

print(run(10))
