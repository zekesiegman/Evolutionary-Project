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

def survivor_selection(old_pop, new_pop):
    pop = old_pop + new_pop
    pop.sort(key=fitness)
    survivors = pop[:len(old_pop)]
    return survivors
