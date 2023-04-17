from penalty import penalty_function
from load_data import load
import numpy as np
import genetic_algo as ga


# produce the best solution after running genetic algorithm for several times
def ga_system(dbname,day_no,slot_no,ga_max_generation):
    # load data and functions
    venue_slot_subject, lecturer_subject, student_subject, venue_subject_capacity,subject_time,venue_type = load(dbname,day_no,slot_no)

    # initialize variables
    venue_no = venue_slot_subject.shape[0]
    slot_no = venue_slot_subject.shape[1]
    subject_no = venue_slot_subject.shape[2]
    
    population_size = 10
    population = np.empty([population_size, venue_no,slot_no, subject_no], dtype=np.int8)
    penalty_function_points = np.empty(population_size, dtype=int)

    # create initial population
    for i in range(population_size):
        chromosome = ga.generate_chromosome(venue_slot_subject,subject_time,venue_type)
        population[i] = chromosome
        penalty_function_point = \
            penalty_function(venue_slot_subject, lecturer_subject, student_subject, venue_subject_capacity,subject_time,venue_type)
        penalty_function_points[i] = penalty_function_point

    # sort initial population based on penalty_function points
    population = population[penalty_function_points.argsort()]
    penalty_function_points = penalty_function_points[penalty_function_points.argsort()]

   
    best_candidate = ga.reproduction(ga_max_generation, penalty_function_points, population,venue_slot_subject, lecturer_subject, 
                    student_subject, venue_subject_capacity,subject_time,venue_type)
    
    return best_candidate
