import random
import numpy as np
from copy import deepcopy
import time


sudoku1 =  np.array([[5,0,2,1,0,0,0,0,0],
                    [3,0,9,0,7,2,5,6,1],
                    [6,0,4,5,3,8,0,7,9],
                    [0,5,0,0,0,0,0,0,4],
                    [9,0,0,0,4,7,0,0,0],
                    [0,0,0,9,8,0,7,1,0],
                    [0,9,0,0,0,3,4,5,0],
                    [7,0,0,8,0,0,0,0,0],
                    [1,3,0,0,0,0,0,2,7] ])
# for i in sudoku1:
#     for j in i:
#         print(j, ' ', end='')
#     print()

def valid_solution(individual):
    for i in individual:
        set_i = set(i)
        if len(i) != len(set_i):
            print('Invalid')
            break
    print('valid')

def convert_sudoku(sudoku):
    flat_sudoku = [[] for _ in range(len(sudoku))]
    row = 0
    col = 0
    counter = 0
    step = int((len(sudoku)**0.5))
    for a in range(step):
        col = 0
        for b in range(step):
            for i in range(row, row+step):
                for j in range(col, col+step):
                    flat_sudoku[counter].append(sudoku[i][j])
            counter+=1
            col+=3
        row+=3
    pos = deepcopy(flat_sudoku)
    for i in range(len(pos)):
        for j in range(len(pos[i])):
            if pos[i][j]!=0:
                pos[i][j]=1
    return flat_sudoku, pos
flatsudoku, pos = convert_sudoku(sudoku1)
# print(flatsudoku)
# print(pos)

# sudoku = [[] for i in range(9)]
# print(sudoku)

def population(flatsudoku, pos, pop_num):
    total_pop = []
    for _ in range(pop_num):
        flat = deepcopy(flatsudoku)
        for i in range(len(flat)):
            rand_list = []
            rand = random.sample(range(1, len(flatsudoku)+1), len(flatsudoku))
            for j in rand:
                if j not in flat[i]:
                    rand_list.append(j)
            while 0 in flat[i]:
                for k in rand_list:
                    flat[i][flat[i].index(0)]=k
        total_pop.append(flat)
    return total_pop

total1 = population(flatsudoku, pos, 5)
total2 = population(flatsudoku, pos, 4)

def convert_back(flatsudoku):
    filled_sudoku = np.zeros([len(flatsudoku), len(flatsudoku)])
    for i in range(len(flatsudoku)):
        index1 = i//int((len(flatsudoku)**0.5))
        index2 = i%int((len(flatsudoku)**0.5))
        for j in range(int(len(flatsudoku)**0.5)):
            filled_sudoku[index1*3+j][3*index2:3*(index2+1)]= flatsudoku[i][3*j:3*(j+1)]
    return filled_sudoku

converted_sudoku =convert_back(total1[0])

def fitness(sudoku):
    row_fitness = 0
    col_fitness = 0
    for i in sudoku:
        sudoku_set = set(i)
        row_fitness += len(i) - len(sudoku_set)
    sudoku_transpose = sudoku.transpose()
    for j in sudoku_transpose:
        sudoku_set = set(j)
        col_fitness += len(j) - len(sudoku_set)
    fitness_value = row_fitness + col_fitness
    return fitness_value

# sudoku2 = np.array([[5,3,4,6,7,8,9,1,2],
#                     [6,7,2,1,9,5,3,4,8],
#                     [1,9,8,3,4,2,5,6,7],
#                     [8,5,9,7,6,1,4,2,3],
#                     [4,2,6,8,5,3,7,9,1],
#                     [7,1,3,9,2,4,8,5,6],
#                     [9,6,1,5,3,7,2,8,4],
#                     [2,8,7,4,1,9,6,3,5],
#                     [3,4,5,2,8,6,1,7,9] ])

# fit = fitness(converted_sudoku)
# print(fit)



def n_point_crossover(pop, pos, cx_rate):
    pop_copy = deepcopy(pop)
    index = random.sample(range(len(pop_copy)), 2)
    child1 = pop_copy[index[0]]
    child2 = pop_copy[index[1]]
    for i in range(len(child1[0])):
        rand = random.random()
        if rand<cx_rate:
            child1[i], child2[i] = child2[i], child1[i]
    return child1, child2

def order_crossover(pop, pos):
    pop_copy = deepcopy(pop)
    index = random.sample(range(len(pop_copy)), 2)
    parent1, parent2 = pop_copy[0], pop_copy[1]
    child1 = []
    child2 = []
    for i in range(len(parent1)):
        crossoverpoints = [random.randint(0, 8), random.randint(0, 8)]
        crossoverpoints.sort()
    # create the subgrids for the first child
        reorder_pos = pos[i][crossoverpoints[0]:] + pos[i][:crossoverpoints[0]]
        reorder1 = parent1[i][crossoverpoints[0]:] + parent1[i][:crossoverpoints[0]]
        reorder2 = parent2[i][crossoverpoints[1]:] + parent2[i][:crossoverpoints[1]]
        for j in range(int((crossoverpoints[1] - crossoverpoints[0])), len(parent1[i])):
            if reorder_pos[j] == 0:
                reorder1[j] = 0
        temp = []
        for j in reorder2:
            if j not in reorder1:
                temp.append(j)
        for j in range(len(reorder1)):
            if reorder1[j] == 0:
                reorder1[j] = temp[0]
                temp.pop(0)
        subgrid1 = reorder1[-crossoverpoints[0]:] + reorder1[:-crossoverpoints[0]]
        child1.append(subgrid1)
        # create subgrids for the second child
        reorder2 = parent2[i][crossoverpoints[0]:] + parent2[i][:crossoverpoints[0]]
        reorder1 = parent1[i][crossoverpoints[1]:] + parent1[i][:crossoverpoints[1]]
        for j in range(int((crossoverpoints[1] - crossoverpoints[0])), len(parent2[i])):
            if reorder_pos[j] == 0:
                reorder2[j] = 0
        temp = []
        for j in reorder1:
            if j not in reorder2:
                temp.append(j)
        for j in range(len(reorder2)):
            if reorder2[j] == 0:
                reorder2[j] = temp[0]
                temp.pop(0)
        subgrid2 = reorder2[-crossoverpoints[0]:] + reorder2[:-crossoverpoints[0]]
        child2.append(subgrid2)
    return child1, child2

# child = order_crossover(total, pos)
# for i, j in zip(total, child):
#     print(i)
#     print(j)

def PMX_crossover(pop, pos):
    pop_copy = deepcopy(pop)
    index = random.sample(range(len(pop_copy)), 2)
    parent1, parent2 = pop_copy[0], pop_copy[1]
    child1 = []
    child2 = []
    for i in range(len(parent1)):
        subgrid1 = parent1[i]
        subgrid2 = parent2[i]
        changeable_num1 = []
        changeable_num2 = []
        for j in range(len(subgrid1)):
            if pos[i][j] == 0:
                changeable_num1.append(subgrid1[j])
                changeable_num2.append(subgrid2[j])
                subgrid1[j] = 0
                subgrid2[j] = 0
        crossoverpoint1, crossoverpoint2 = random.sample(range(len(changeable_num1)-1), 2)
        sub_child1 = []
        sub_child2 = []
        #create child 1
        count = 0
        for j in changeable_num2:
            if count == crossoverpoint1:
                break
            if j not in changeable_num1[crossoverpoint1: crossoverpoint2]:
                sub_child1.append(j)
                count += 1
        sub_child1.extend(changeable_num1[crossoverpoint1:crossoverpoint2])
        sub_child1.extend([x for x in changeable_num2 if x not in sub_child1])
        #create child 2
        count = 0
        for j in changeable_num1:
            if count == crossoverpoint1:
                break
            if j not in changeable_num2[crossoverpoint1: crossoverpoint2]:
                sub_child2.append(j)
                count += 1
        sub_child2.extend(changeable_num2[crossoverpoint1:crossoverpoint2])
        sub_child2.extend([x for x in changeable_num1 if x not in sub_child2])
        for j in range(len(subgrid1)):
            if subgrid1[j] == 0:
                subgrid1[j] = sub_child1[0]
                subgrid2[j] = sub_child2[0]
                sub_child1.pop(0)
                sub_child2.pop(0)
        child1.append(subgrid1)
        child2.append(subgrid2)
    return child1, child2

# children = PMX_crossover(total, pos)

def cycle_crossover(pop, pos):
    pop_copy = deepcopy(pop)
    index = random.sample(range(len(pop_copy)), 2)
    parent1, parent2 = pop_copy[0], pop_copy[1]
    child1 = []
    child2 = []
    for i in range(len(parent1)):
        subgrid1 = parent1[i]
        subgrid2 = parent2[i]
        changeable_num1 = []
        changeable_num2 = []
        for j in range(len(subgrid1)):
            if pos[i][j] == 0:
                changeable_num1.append(subgrid1[j])
                changeable_num2.append(subgrid2[j])
                subgrid1[j] = 0
                subgrid2[j] = 0
        cycles = []
        in_cycle_index = []
        for j in range(len(changeable_num1)):
            if j not in in_cycle_index:
                cycle = []
                initial = changeable_num1[j]
                current = changeable_num1[j]
                cycle.append(changeable_num1.index(initial))
                # print(current==P2[P1.index(current)])
                while changeable_num2[changeable_num1.index(current)] != initial:
                    current = changeable_num2[changeable_num1.index(current)]
                    # print('current index', P2.index(current))
                    # input("")
                    # cycle.append(P2.index(current))
                    next_index = changeable_num1.index(current)
                    # print('next index', next_index)
                    cycle.append(next_index)
                    in_cycle_index.append(next_index)
                    current = changeable_num1[next_index]
                    # print(current)
                cycle.sort()
                cycles.append(cycle)
                # print('cycle:', cycle)
        # print('cycles', cycles)
        # print('in cycle index:', in_cycle_index)
        C1 = [-1] * len(changeable_num1)
        C2 = [-1] * len(changeable_num2)
        for j in range(len(cycles)):
            if j % 2 == 0:
                for k in cycles[j]:
                    C1[k] = changeable_num1[k]
                    C2[k] = changeable_num2[k]
            else:
                for k in cycles[j]:
                    C1[k] = changeable_num2[k]
                    C2[k] = changeable_num1[k]
        for j in range(len(subgrid1)):
            if subgrid1[j] == 0:
                subgrid1[j] = C1[0]
                C1.pop(0)
        for j in range(len(subgrid2)):
            if subgrid2[j] == 0:
                subgrid2[j] = C2[0]
                C2.pop(0)
        child1.append(subgrid1)
        child2.append(subgrid2)
    return child1, child2

# child =  cycle_crossover(total, pos)
# for i, j in zip(total, child):
#     print(i)
#     print(j)

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

mutants = scramble_mutation(total1, pos, 1)
# print(pos)
# for i, j in zip(total, mutants):
#     print(i)
#     print(j)


