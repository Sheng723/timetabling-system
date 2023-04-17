import numpy as np
from penalty import penalty_function
from load_data import load

# generate chromosome in the population
def generate_chromosome(venue_slot_subject,subject_time,venue_type):
    
    chromosome = np.copy(venue_slot_subject)
    venue_no = chromosome.shape[0]
    slot_no = chromosome.shape[1]
    subject_no = chromosome.shape[2]
    subject_time_copy = np.copy(subject_time)
    counter = 0
    for subject in range(subject_no):
        while subject_time_copy[subject]!=0:  
            random_slot = np.random.randint(slot_no)
            while True:
                random_venue = np.random.randint(venue_no)
                if subject > (subject_no /2) and venue_type[random_venue] == 1:
                    break
                elif subject <= (subject_no /2) and venue_type[random_venue] == 0:
                    break
            # if the slot is available and empty    
            if chromosome[random_venue][random_slot][subject] == 0 and np.count_nonzero(chromosome[random_venue][random_slot] == 1) == 0 \
            and np.count_nonzero(chromosome[:,random_slot,subject] == 1) == 0\
            and np.count_nonzero(chromosome[random_venue,random_slot,:] == 1) == 0:
                counter = random_slot
                for r in range(subject_time_copy[subject]):
                    difference = int(slot_no-random_slot)
                    
                    if  difference >= int(subject_time_copy[subject]) or difference ==0:
                        if chromosome[random_venue][counter][subject] == 0 and np.count_nonzero(chromosome[random_venue][counter] == 1) == 0:
                            chromosome[random_venue][counter][subject] = 1  
                            counter += 1
                            subject_time_copy[subject] -= 1
                    else:
                        if chromosome[random_venue][counter][subject] == 0 and np.count_nonzero(chromosome[random_venue][counter] == 1) == 0:
                            chromosome[random_venue][counter][subject] = 1  
                            counter -=1
                            subject_time_copy[subject] -= 1
                
               
                
    return chromosome

# select best chromosome with lowest penalty point in the population
def select(population, penalty_function):
    tournament_size = 2

    # select 1st chromosome based on 1st tournament selection
    p1, p2 = np.random.choice(range(population.shape[0]), tournament_size)
    first = p1 if penalty_function[p1] <= penalty_function[p2] else p2

    # ensure 2 chromosomes selected are not identical
    while True:
        # select 2nd chromosome based on 2nd tournament selection
        p1, t2 = np.random.choice(range(population.shape[0]), tournament_size)
        second = p1 if penalty_function[p1] <= penalty_function[p2] else p2

        if second != first:
            break

    return population[first], population[second]

# perform crossover operator
def crossover(parent_one, parent_two):
    child_one = np.copy(parent_one)
    child_two = np.copy(parent_two)
    venue_no = parent_one.shape[0]
    subject_no = parent_one.shape[2]
    cutpoint1, cutpoint2 = np.random.choice(range(subject_no), 2)
    cutpoint3, cutpoint4 = np.random.choice(range(venue_no), 2)
    
    if cutpoint1 > cutpoint2:
        cutpoint1, cutpoint2 = cutpoint2, cutpoint1
    if cutpoint3 > cutpoint4:
        cutpoint3, cutpoint4 = cutpoint4, cutpoint3
    
    # swap presentations from cutpoint1 to cutpoint2 and from cutpoint3 to cutpoint4 between 2 parents
    child_one[:, cutpoint1:cutpoint2, cutpoint3:cutpoint4], child_two[:, cutpoint1:cutpoint2, cutpoint3:cutpoint4] = \
        child_two[:, cutpoint1:cutpoint2, cutpoint3:cutpoint4], np.copy(child_one[:, cutpoint1:cutpoint2, cutpoint3:cutpoint4])
   
    return child_one, child_two
    
# replace 2 chromosomes in population
def replacement(population, penalty_function, first_child, second_child, first_penalty_point, second_penalty_point):
    # replace 2 chromosomes of highest penalty points with 2 new chromosomes
    population_size = len(population)
    population[population_size - 1], population[population_size - 2] = first_child, second_child
    penalty_function[population_size - 1], penalty_function[population_size - 2] = first_penalty_point, second_penalty_point

    # sort population based on penalty points
    population = population[penalty_function.argsort()]
    penalty_function = penalty_function[penalty_function.argsort()]

    return population, penalty_function

# produce the best solution
def reproduction(max_generations, penalty_functions, population,venue_slot_subject, lecturer_subject, 
student_subject, venue_subject_capacity,subject_time,venue_type):
    
    
    for generation in range(max_generations):
        first_parent, second_parent = select(population, penalty_functions)
        first_child, second_child = crossover(first_parent, second_parent)
        first_penalty_point = \
            penalty_function(venue_slot_subject, lecturer_subject, student_subject, venue_subject_capacity,subject_time,venue_type)
        second_penalty_point = \
            penalty_function(venue_slot_subject, lecturer_subject, student_subject, venue_subject_capacity,subject_time,venue_type)
        population, penalty_functions = \
            replacement(population, penalty_functions, first_child, second_child,
                        first_penalty_point, second_penalty_point)
       
    return population[0]
    
    
