import sqlite3
import numpy as np

# retrieve data from database
def load(dbname,day_no,slot_no):
    # create database connection
    conn = sqlite3.connect(dbname)
    # get = total number of rows from each tables.
    sql = ''' SELECT COUNT(*) FROM %s '''
    cur = conn.cursor()
    cur.execute(sql%'lecturer')
    lecturer_no = cur.fetchone()[0]
    cur.execute(sql%'student')
    student_group_no = cur.fetchone()[0]
    cur.execute(sql%'subject')
    subject_no = cur.fetchone()[0]
    cur.execute(sql%'venue')
    venue_no = cur.fetchone()[0]
    conn.commit()
    # calculate total slot 
    total_slot_no = slot_no * day_no
    # initialize arrays to represent the data
    lecturer_subject = np.zeros([lecturer_no,subject_no*2], dtype=np.int8)
    student_subject = np.zeros([student_group_no, subject_no*2], dtype=np.int8)
    venue_slot_subject = np.zeros([venue_no,total_slot_no, subject_no*2], dtype=np.int8)
    venue_subject_capacity = np.zeros([venue_no, subject_no*2], dtype=np.int8)
    
    # retrieve data needed from student and lecturer tables, then represent the data in numpy arrays
    sql = ''' SELECT id,subject FROM %s '''
    cur = conn.cursor()
    
    cur.execute(sql%'student')
    student_tuple = cur.fetchall()
    
    for row in range(len(student_tuple)):
        student_id = student_tuple[row][0] - 1
        total_subject = student_tuple[row][1].split(',')
        for subject_id in range(len(total_subject)-1):
            r = int(total_subject[subject_id]) - 1
            student_subject[student_id][r] = 1
            student_subject[student_id][r+subject_no] = 1
            
    cur.execute(sql%'lecturer')
    lecturer_tuple = cur.fetchall()
    
    for row in range(len(lecturer_tuple)):
        lecturer_id = lecturer_tuple[row][0] - 1
        total_subject = lecturer_tuple[row][1].split(',')
        for subject_id in range(len(total_subject)-1):
            r = int(total_subject[subject_id]) - 1
            lecturer_subject[lecturer_id][r] = 1
            
            lecturer_subject[lecturer_id][r+subject_no] = 1
            
    # retrieve data needed from subject table, then represent the data in numpy array
    sql = ''' SELECT practical_time,lecturer_time,total_student FROM subject '''
    cur.execute(sql)
    subject_tuple = cur.fetchall()
    
    subject_practical_time = [row[0] for row in subject_tuple]
    subject_lecturer_time = [row[1] for row in subject_tuple]
    subject_total_student = [row[2] for row in subject_tuple]
    subject_time = list(subject_practical_time + subject_lecturer_time)
    subject_total_student = subject_total_student + subject_total_student
    
    # retrieve data needed from venue table, then represent the data in numpy array
    sql = ''' SELECT capacity,vtype FROM venue '''
    cur.execute(sql)
    venue_tuple = cur.fetchall()
    
    venue_capacity = [row[0] for row in venue_tuple]
    venue_type = list([row[1] for row in venue_tuple])
    for item in range(len(venue_type)):
        if venue_type[item] == 'Lecturer':
            venue_type[item] = 1
        else:
            venue_type[item] = 0

    for subject_id in range(subject_no*2):
        for venue_id in range(venue_no):
            if int(venue_capacity[venue_id]) < int(subject_total_student[subject_id]):
                venue_subject_capacity[venue_id][subject_id] = -2
   
    return venue_slot_subject, lecturer_subject, student_subject, venue_subject_capacity,subject_time,venue_type
