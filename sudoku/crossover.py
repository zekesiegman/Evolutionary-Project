import random
import numpy as np
from copy import deepcopy

def uniform_crossover(pop, cx_rate):
    pop_copy = deepcopy(pop)
    children = []
    for i in range(len(pop_copy)):
        child = deepcopy(pop_copy[i])
        for j in range(len(child)):
            rand = random.random()
            if rand < cx_rate:
                index = random.randint(0, len(pop_copy) - 1)
                child[j] = pop_copy[index][j]
        children.append(child)
    return children

# from population import total
#
# children = uniform_crossover(total, 1)
# for i, j in zip(total, children):
#     print(i)
#     print(j)

def order_crossover(pop, pos):
    pop_copy = deepcopy(pop)
    children = []
    for num in range(int(len(pop)/2)):
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
        children.append(child1)
        children.append(child2)
    return children

# child = order_crossover(total, pos)
# for i, j in zip(total, child):
#     print(i)
#     print(j)

def PMX_crossover(pop, pos):
    pop_copy = deepcopy(pop)
    children = []
    for num in range(int(len(pop)/2)):
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
            crossoverpoint1, crossoverpoint2 = random.sample(range(len(changeable_num1)), 2)
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
        children.append(child1)
        children.append(child2)
    return children

# children = PMX_crossover(total, pos)
# for i in children:
#     print(i)

def cycle_crossover(pop, pos):
    pop_copy = deepcopy(pop)
    children = []
    for num in range(int(len(pop) / 2)):
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
        children.append(child1)
        children.append(child2)
    return children

# child =  cycle_crossover(total, pos)
# print(len(child))
# for i, j in zip(total, child):
#     print(i)
#     print(j)

# def micro_crossovr(pop, pos, cx_rate):
#     pop_copy = deepcopy(pop)
#     children = []
#     for i in range(len(pop)):
#         child = []
#         for j in range(len(pop[i])):
#             index = random.sample(range(len(pop_copy)), 2)
#             subgrid = pop_copy[index][j]
#             rand = random.sample(range(1,4), 3)
#             if rand==1:
#
#
#             if rand==2:
#
#             if rand==3: