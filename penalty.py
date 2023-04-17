from load_data import load
import numpy as np

# calculate penalty points for the chromosome generated
def penalty_function(venue_slot_subject, lecturer_subject, student_subject, venue_subject_capacity,subject_time,venue_type):
    # initialize variables
    penalty_point = 0
    
    hc1_count = 0
    hc1_count_list = np.zeros([1,lecturer_subject.shape[0]], dtype=np.int8)
    
    hc2_count = 0
    hc2_count_list = np.zeros([1,student_subject.shape[0]], dtype=np.int8)
    
    hc3_count = 0
    hc3_count_list = np.zeros([1,venue_slot_subject.shape[1]], dtype=np.int8)
    
    hc_total_count = 0
    
    subject_no = venue_slot_subject.shape[2]
    
    venue_slot_subject = np.copy(venue_slot_subject)
    
    venue_slot_subject_merged = np.sum(venue_slot_subject, axis=0)
    
    venue_slot_subject_merged[venue_slot_subject_merged>=1] = 1
    # calculate penalty points for the constraint: no lecturer cannot attend two subjects at same time
    for row in range(lecturer_subject.shape[0]):

        lecturer_subject_1 =  venue_slot_subject_merged+lecturer_subject[row]
        hc1_count_list = np.count_nonzero(lecturer_subject_1 == 2, axis=1)
       
        for r in hc1_count_list:
            if r > 1:
                hc1_count += 1
                penalty_point += 1000
        
        lecturer_subject_1.fill(0)
       
    
    # calculate penalty points for the constraint: no student cannot attend two subjects at same time
    for row in range(student_subject.shape[0]):
        
        student_subject_1 = venue_slot_subject_merged + student_subject[row]
        
        hc2_count_list = np.count_nonzero(student_subject_1 == 2, axis=1)
        
        for r in hc2_count_list:
            if r > 1:
                hc2_count += 1
                penalty_point += 1000
                
        student_subject_1.fill(0) 
    
    
    # calculate penalty points for the constraint: no venue capacity can small than student size
    for row in range(venue_subject_capacity.shape[0]):
        
        venue_subject_capacity_1 = venue_slot_subject[row] + venue_subject_capacity[row]
        
        hc3_count_list = np.count_nonzero(venue_subject_capacity_1 == -1, axis=1)
        
        for r in hc3_count_list:
            if r == 1:
                hc3_count += 1
                penalty_point += 1000
                
        venue_subject_capacity_1.fill(0) 
    
 
    return penalty_point
    
