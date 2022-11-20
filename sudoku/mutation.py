import random
import numpy as np
from copy import deepcopy


def inverse_mutation(pop, pos, mut_rate):
    pop_copy = deepcopy(pop)
    mutants = []
    for i in range(len(pop_copy)):
        mutant = []
        for j in range(len(pop_copy[i])):
            subgrid = pop_copy[i][j]
            changeable_num = []
            rand = random.random()
            if rand<mut_rate:
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
        mutants.append(mutant)
    return mutants

# mutants = inverse_mutation(total, pos, 1)
# print(pos)
# for i, j in zip(total, mutants):
#     print(i)
#     print(j)


def swap_mutation(pop, pos, mut_rate):
    pop_copy = deepcopy(pop)
    mutants = []
    for i in range(len(pop_copy)):
        mutant = []
        for j in range(len(pop_copy[i])):
            subgrid = pop_copy[i][j]
            changeable_num = []
            rand = random.random()
            if rand < mut_rate:
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
        mutants.append(mutant)
    return mutants

# mutants = swap_mutation(total, pos, 1)
# print(pos)
# for i, j in zip(total, mutants):
#     print(i)
#     print(j)

def scramble_mutation(pop, pos, mut_rate):
    pop_copy = deepcopy(pop)
    mutants = []
    for i in range(len(pop_copy)):
        mutant = []
        for j in range(len(pop_copy[i])):
            subgrid = pop_copy[i][j]
            changeable_num = []
            rand = random.random()
            if rand < mut_rate:
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
        mutants.append(mutant)
    return mutants

# mutants = scramble_mutation(total, pos, 1)
# print(pos)
# for i, j in zip(total, mutants):
#     print(i)
#     print(j)