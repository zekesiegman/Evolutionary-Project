import sudoku
import numpy as np

# pop = sudoku.total

def convert_back(flatsudoku):
    filled_sudoku = np.zeros([int(len(flatsudoku)/2), int(len(flatsudoku)/2)])
    for i in range(9):
        index1 = i//int(np.sqrt(len(flatsudoku)/2))
        index2 = i%int(np.sqrt(len(flatsudoku)/2))
        for j in range(int(np.sqrt(len(flatsudoku)/2))):
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

def get_all_fitness(pop):
    fit_list = []
    for i in pop:
        fit = fitness(i)
        fit_list.append(fit)
    return fit_list

# fitnesses = get_all_fitness(pop)
# print(fitnesses)