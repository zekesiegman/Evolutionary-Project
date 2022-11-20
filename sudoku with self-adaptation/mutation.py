import random
import numpy as np
from copy import deepcopy


def inverse_mutation(pop, pos):
    pop_copy = deepcopy(pop)
    mutants = []
    for i in range(len(pop_copy)):
        mutant = []
        mut_rates = []
        for j in range(int(len(pop_copy[i])/2), len(pop_copy[i])):
            pop_copy[i][j] *= np.exp(random.normalvariate(0, 1)*1/np.sqrt(40))
            mut_rates.append(pop_copy[i][j])
        for j in range(int(len(pop_copy[i])/2)):
            subgrid = pop_copy[i][j]
            changeable_num = []
            rand = random.random()
            if rand<pop_copy[i][j+int(len(pop_copy[i])/2)]:
                for k in range(len(subgrid)):
                    if pos[j][k] == 0:
                        changeable_num.append(subgrid[k])
                        subgrid[k] = 0
                changeable_num.reverse()
                for k in range(len(subgrid)):
                    if subgrid[k] == 0:
                        subgrid[k] = changeable_num[0]
                        changeable_num.pop(0)
            mutant.append(subgrid)
        mutant += mut_rates
        mutants.append(mutant)
    return mutants

# print(pos)
# for i, j in zip(total, mutants):
#     print(i)
#     print(j)

def swap_mutation(pop, pos):
    pop_copy = deepcopy(pop)
    mutants = []
    for i in range(len(pop_copy)):
        mutant = []
        mut_rates = []
        for j in range(int(len(pop_copy[i]) / 2), len(pop_copy[i])):
            pop_copy[i][j] *= np.exp(random.normalvariate(0, 1) * 1/ np.sqrt(80) )
            mut_rates.append(pop_copy[i][j])
        # print(mut_rates)
        for j in range(int(len(pop_copy[i]) / 2)):
            subgrid = pop_copy[i][j]
            changeable_num = []
            rand = random.random()
            if rand < pop_copy[i][j + int(len(pop_copy[i]) / 2)]:
                for k in range(len(subgrid)):
                    if pos[j][k] == 0:
                        changeable_num.append(subgrid[k])
                        subgrid[k] = 0
                index1, index2 = random.sample(range(len(changeable_num)-1), 2)
                changeable_num[index1], changeable_num[index2] = changeable_num[index2], changeable_num[index1]
                for k in range(len(subgrid)):
                    if subgrid[k] == 0:
                        subgrid[k] = changeable_num[0]
                        changeable_num.pop(0)
            mutant.append(subgrid)
        mutant += mut_rates
        mutants.append(mutant)
    return mutants
# from population import total, pos
# swap_mutation(total, pos)

# mutants = swap_mutation(total, pos, 1)
# print(pos)
# for i, j in zip(total, mutants):
#     print(i)
#     print(j)

def scramble_mutation(pop, pos):
    pop_copy = deepcopy(pop)
    mutants = []
    for i in range(len(pop_copy)):
        mutant = []
        mut_rates = []
        for j in range(int(len(pop_copy[i]) / 2), len(pop_copy[i])):
            pop_copy[i][j] *= np.exp(random.normalvariate(0, 1) * 1/ np.sqrt(80) )
            mut_rates.append(pop_copy[i][j])
        for j in range(int(len(pop_copy[i]) / 2)):
            subgrid = pop_copy[i][j]
            changeable_num = []
            rand = random.random()
            if rand < pop_copy[i][j + int(len(pop_copy[i]) / 2)]:
                for k in range(len(subgrid)):
                    if pos[j][k] == 0:
                        changeable_num.append(subgrid[k])
                        subgrid[k] = 0
                random.shuffle(changeable_num)
                for k in range(len(subgrid)):
                    if subgrid[k] == 0:
                        subgrid[k] = changeable_num[0]
                        changeable_num.pop(0)
            mutant.append(subgrid)
        mutant += mut_rates
        mutants.append(mutant)
    return mutants

# mutants = scramble_mutation(total, pos, 1)
# print(pos)
# for i, j in zip(total, mutants):
#     print(i)
#     print(j)