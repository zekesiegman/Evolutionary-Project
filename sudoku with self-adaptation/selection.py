import random
import numpy as np
from copy import deepcopy
from fitness import fitness, get_all_fitness

def selection_prob(pop):
    prob_list = []
    bound = 0
    evals = get_all_fitness(pop)
    for i in range(len(pop)):
        lower_bound = bound
        upper_bound = lower_bound + (evals[i]/sum(evals))
        bound = upper_bound
        prob_list.append([lower_bound, upper_bound])
    return prob_list

def stochastic_universal_sampling(pop, n_select):
    select_list = []
    new_pop = deepcopy(pop)
    prob_range = selection_prob(new_pop)
    prob_list = []
    increment = 1/n_select
    rand = random.random()
    for i in range(n_select):
        prob = rand + i * increment
        if prob >= 1:
            prob_list.append(prob-1)
        else:
            prob_list.append(prob)
    for i in range(len(prob_list)):
        prob = prob_list[i]
        for j in range(len(prob_range)):
            if prob_range[j][0] <= prob < prob_range[j][1]:
                select_list.append(pop[j])
                break
    return select_list

def roulette_wheel(pop, n_select):
    select_list = []
    new_pop = deepcopy(pop)
    prob_range = selection_prob(new_pop)
    for i in range(n_select):
        rand = random.random()
        for j in range(len(prob_range)):
            if prob_range[j][0]<=rand<prob_range[j][1]:
                select_list.append(pop[j])
                break
    select_list.sort(key=fitness)
    return select_list

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

# from population import total
# select = random_selection(total, 2)
# for i in select:
#     print(i)
#     print(len(i))