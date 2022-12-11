import random
import numpy as np
from copy import deepcopy
from fitness import fitness, get_all_fitness

def tournament_selection(pop, size_mating_pool, num_participants=2):
    mating_pool = []
    evals = get_all_fitness(pop)
    for i in range(size_mating_pool):
        participant_index = random.sample(range(len(pop)), num_participants)
        tournament = []
        for num in participant_index:
            tournament.append(evals[num])
        winner = min(tournament)
        temp = evals.index(winner)
        mate = pop[temp]
        mating_pool.append(mate)
    mating_pool.sort(key=fitness)
    return mating_pool

def deterministic_survivor_selection(old_pop, new_pop):
    # old_pop.sort(key=fitness)
    pop = new_pop + old_pop
    # print(pop)
    pop.sort(key=fitness)
    survivors = pop[:len(old_pop)]
    return survivors

def random_selection(pop, n_select):
    select_list = []
    pop_copy = deepcopy(pop)
    for i in range(n_select):
        index = random.randint(0, len(pop_copy)-1)
        select_list.append(pop_copy[index])
    return select_list

