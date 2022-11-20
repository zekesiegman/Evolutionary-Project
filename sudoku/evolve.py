import random
from population import population, convert_back
from crossover import uniform_crossover, cycle_crossover, PMX_crossover, order_crossover
from selection import roulette_wheel, survivor_selection, tournament_selection, stochastic_universal_sampling
from mutation import scramble_mutation, inverse_mutation, swap_mutation
from fitness import fitness, get_all_fitness
import numpy as np
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

evil_sudoku =  np.array([[0,4,0,0,0,9,0,0,0],
                    [0,7,0,0,0,0,2,0,0],
                    [0,0,6,3,4,0,0,0,5],
                    [0,0,9,0,0,5,0,0,0],
                    [0,0,0,0,0,8,0,0,1],
                    [0,6,0,1,9,0,0,7,0],
                    [0,0,0,8,0,0,0,0,0],
                    [3,0,0,0,0,0,0,5,0],
                    [0,0,4,6,1,0,0,0,3]])

def evolve(sudoku, max_gen, pop_size, num_offspring, mut_rate, cx_rate):
    pop, pos = population(sudoku, pop_size)
    best_ind = []
    fitnesses = []
    num_unchanged = 0
    for gen in range(max_gen):
        mating_pool = tournament_selection(pop, num_offspring, 2)
        mating_pool = uniform_crossover(mating_pool, cx_rate)
        rand = random.randint(1,3)
        if rand==1:
            mating_pool = order_crossover(mating_pool, pos)
        elif rand==2:
            mating_pool = PMX_crossover(mating_pool, pos)
        else:
            mating_pool = cycle_crossover(mating_pool, pos)
        rand = random.randint(1, 2)
        if rand==1:
            mutants = scramble_mutation(mating_pool, pos, mut_rate)
        elif rand == 2:
            mutants = swap_mutation(mating_pool, pos, mut_rate)
        else:
            mutants = inverse_mutation(mating_pool, pos, mut_rate)
        rand = random.randint(1, 1)
        if rand == 1:
            survivors = survivor_selection(pop, mutants)
        else:
            survivors = tournament_selection(mutants+pop, len(pop), 2)
        best_ind.append(survivors[0])
        fitnesses.append(fitness(survivors[0]))
        last_best = fitnesses[gen-1] if gen>=1 else 0
        current_best = fitnesses[gen]
        if current_best==last_best:
            num_unchanged+=1
        else:
            num_unchanged=0
        if num_unchanged>200:
            mut_rate = ((num_unchanged-200)//200)*0.1 + 0.05
        else:
            mut_rate=0.3
        if (gen+1)%100==0:
            print('Generation {}'.format(gen+1), survivors[0])
            print('Fitness', fitness(survivors[0]))
            print('Average fitness', sum(get_all_fitness(survivors)) / len(pop))
        if fitness(survivors[0])==0:
            print('Generation {}'.format(gen + 1), survivors[0])
            print('Found it!')
            print(convert_back(survivors[0]))
            break
        pop = survivors
    return best_ind, fitnesses
    # return pop

# best_ind, fitnesses = evolve(easy_sudoku, 10000, 100, 15, 0.05, 0.5)
# for i in range(len(best_ind)):
#     if (i + 1) % 100 == 0:
#         print('Generation {}'.format(i + 1), best_ind[i])
#         print('Fitness', fitness(best_ind[i]))
#     if fitness(best_ind[i]) == 0:
#         print('Generation {}'.format(i + 1), best_ind[i])
#         print('Found it!')
#         print(convert_back(best_ind[i]))
#         break


def evolve_in_island (num_island, sudoku, max_gen_separate, max_gen_together, pop_size, num_offspring, mut_rate, cx_rate):
    pop_group = []
    pop, pos = population(sudoku, 1)
    for i in range(num_island):
        pop = evolve(sudoku, max_gen_separate, pop_size, num_offspring, mut_rate, cx_rate)
        pop_group.append(pop)
        print('Group {} fitness value: '.format(i+1), fitness(pop[0]))
    total_pop = []
    for i in pop_group:
        total_pop+=i
    pop = total_pop
    best_ind = []
    fitnesses = []
    num_unchanged = 0
    for gen in range(max_gen_together):
        mating_pool = tournament_selection(pop, num_island * num_offspring, 2)
        recombinants = uniform_crossover(mating_pool, cx_rate)
        rand = random.randint(1, 3)
        if rand == 1:
            recombinants = order_crossover(recombinants, pos)
        elif rand == 2:
            recombinants = PMX_crossover(recombinants, pos)
        else:
            recombinants = cycle_crossover(recombinants, pos)
        rand = random.randint(1, 3)
        if rand == 1:
            mutants = scramble_mutation(recombinants, pos, mut_rate)
        elif rand == 2:
            mutants = swap_mutation(recombinants, pos, mut_rate)
        else:
            mutants = inverse_mutation(recombinants, pos, mut_rate)
        rand = random.randint(1, 3)
        if rand == 1:
            survivors = survivor_selection(pop, mutants)
        else:
            survivors = tournament_selection(mutants + pop, len(pop), 2)
        best_ind.append(survivors[0])
        fitnesses.append(fitness(survivors[0]))
        last_best = fitnesses[gen - 1] if gen >= 1 else 0
        current_best = fitnesses[gen]
        if current_best == last_best:
            num_unchanged += 1
        else:
            num_unchanged = 0
        if num_unchanged > 100:
            mut_rate = ((num_unchanged - 200) // 200) * 0.1 + 0.05
        else:
            mut_rate = 0.05
        if (gen+1)%100==0:
            print('Generation {}'.format(gen+1), survivors[0])
            print('Fitness', fitness(survivors[0]))
            print('Average fitness', sum(get_all_fitness(survivors))/len(pop))
        if fitness(survivors[0])==0:
            print('Generation {}'.format(gen + 1), survivors[0])
            print('Found it!')
            print(convert_back(survivors[0]))
            break
        pop = survivors
    return best_ind, fitnesses


# best_ind, fitnesses = evolve_in_island(5, easy_sudoku, 1000, 50, 10, 0.5, 0.5)
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
        print('This is the {} run'.format(i+1))
        pop, fit = evolve(medium_sudoku, 30000, 100, 50, 0.05, 0.5)
        best_inds.append(pop[-1])
        highest_fit.append(fit[-1])
    data = [[] for _ in range(num_run)]
    for i in range(num_run):
        data[i].append(best_inds[i][:])
        data[i].append(highest_fit[i])
    header = ['Best Individual of Each Run', "Highest Fitness Value of Each Run"]
    return tabulate(data, header, tablefmt='grid', showindex='always')

print(run(10))