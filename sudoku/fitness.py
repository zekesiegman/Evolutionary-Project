import numpy

import sudoku
import numpy as np

# pop = sudoku.total

def convert_back(flatsudoku):
    filled_sudoku = np.zeros([len(flatsudoku), len(flatsudoku)])
    for i in range(len(flatsudoku)):
        index1 = i//int((len(flatsudoku)**0.5))
        index2 = i%int((len(flatsudoku)**0.5))
        for j in range(int(len(flatsudoku)**0.5)):
            filled_sudoku[index1*3+j][3*index2:3*(index2+1)]= flatsudoku[i][3*j:3*(j+1)]
    return filled_sudoku

def fitness(flat_sudoku):
    sudoku = convert_back(flat_sudoku)
    row_fitness = 0
    col_fitness = 0
    for i in sudoku:
        sudoku_set = set(i)
        row_fitness += len(i) - len(sudoku_set)
        # row_fitness+=1 if len(sudoku_set)<9 else row_fitness
    sudoku_transpose = sudoku.transpose()
    for j in sudoku_transpose:
        sudoku_set = set(j)
        col_fitness += len(j) - len(sudoku_set)
        # col_fitness+=1 if len(sudoku_set)<9 else col_fitness
    fitness_value = row_fitness + col_fitness
    return fitness_value

# def fitness(flat_sudoku):
#     sudoku=convert_back(flat_sudoku)
#     row_repetition = 0
#     row_sum = 0
#     row_product = 0
#     col_repetition = 0
#     col_sum = 0
#     col_product = 0
#     for i in sudoku:
#         sudoku_set = set(i)
#         row_repetition += len(i) - len(sudoku_set)
#         temp_sum = 0
#         temp_product = 1
#         for j in i:
#             temp_sum += j
#             temp_product *= j
#         row_sum += 45 - temp_sum
#         row_product += np.math.factorial(9) - temp_product
#     sudoku_transpose = sudoku.transpose()
#     for i in sudoku_transpose:
#         sudoku_set = set(i)
#         col_repetition += len(i) - len(sudoku_set)
#         temp_sum = 0
#         temp_product = 1
#         for j in i:
#             temp_sum += j
#             temp_product *= j
#         col_sum += 45 - temp_sum
#         col_product += np.math.factorial(9) - temp_product
#     return 50*(row_repetition+col_repetition) + np.sqrt(row_product) + np.sqrt(col_product) + 10*(row_sum+col_sum)

def get_all_fitness(pop):
    fit_list = []
    for i in pop:
        fit = fitness(i)
        fit_list.append(fit)
    return fit_list

# fitnesses = get_all_fitness(pop)
# print(fitnesses)