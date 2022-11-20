import random
import numpy as np
from copy import deepcopy
from fitness import get_all_fitness, fitness
from sudoku import total1, total2

def survivor_selection(old_pop, new_pop):
    pop = old_pop + new_pop
    pop.sort(key=fitness)
    survivors = pop[:len(old_pop)]
    return survivors


