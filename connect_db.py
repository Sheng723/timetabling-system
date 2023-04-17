import sqlite3
import csv 

# create table in database.
def create_table(conn, create_table_sql):
    
    c = conn.cursor()
    c.execute(create_table_sql)
    
# insert related data into lecturer table.        
def add_lecturer(conn, lecturer):
    sql = ''' INSERT INTO lecturer(name,subject)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, lecturer)
    conn.commit()
    
# insert related data into student table.     
def add_student(conn, student):
    sql = ''' INSERT INTO student(total_student,enrollment_sem,subject)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    
# insert related data into venue table.     
def add_venue(conn, venue):
    sql = ''' INSERT INTO venue(name,capacity,vtype)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, venue)
    conn.commit()
    
# insert related data into subject table.     
def add_subject(conn, subject):
    sql = ''' INSERT INTO subject(name,practical_time,lecturer_time,total_student)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, subject)
    conn.commit()
    
# insert number of total students enrolled in the corresponding subjects into subject table.     
def add_total_students(conn,subject_id):
    
    sql = ''' SELECT SUM(total_student) FROM student WHERE subject LIKE ?'''
    cur = conn.cursor()
    cur.execute(sql,[subject_id])
    total_student = cur.fetchone()[0]
    conn.commit()
    return total_student

# add all data from imported files into corresponding tables.
def add_rows(dbname,lecturer_filename,student_filename,
            subject_filename,venue_filename):
    database = dbname
    sql_create_lecturer_table = """ CREATE TABLE IF NOT EXISTS lecturer (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        subject text
                                    ); """

    sql_create_student_table = """CREATE TABLE IF NOT EXISTS student (
                                    id integer PRIMARY KEY,
                                    total_student integer,
                                    enrollment_sem text,
                                    subject text
                                );"""
                                
    sql_create_venue_table = """CREATE TABLE IF NOT EXISTS venue (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    capacity integer,
                                    vtype text
                                );"""
                                
    sql_create_subject_table = """CREATE TABLE IF NOT EXISTS subject (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    practical_time integer,
                                    lecturer_time integer,
                                    total_student integer
                                );"""
    # create a database connection.
    conn = sqlite3.connect(dbname)
    # create related tables.
    create_table(conn, sql_create_lecturer_table)

    create_table(conn, sql_create_student_table)
    
    create_table(conn, sql_create_venue_table)
    
    create_table(conn, sql_create_subject_table)
    
    with conn:
        
        with open(lecturer_filename, encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=',')
            
            # read header and count columns.     
            ncol = len(next(csv_reader)) 
            
            for row in csv_reader:
            
                name = str(row[0])
                lecturer_subject = ''
                
                for r in range(1,ncol):
                
                    if row[r] == '':
                        next
                        continue
                        
                    lecturer_subject += str(row[r]) + ','
                    
                lecturer = (name, lecturer_subject);
                
                lecturer_id = add_lecturer(conn, lecturer)
        
        with open(student_filename, encoding='utf-8') as file:
        
            csv_reader = csv.reader(file, delimiter=',')
                  
            ncol = len(next(csv_reader)) 
            
            for row in csv_reader:
            
                total_student = str(row[0])
                enrollment_sem = str(row[1])
                student_subject = ''
                
                for r in range(2,ncol):
                
                    if row[r] == '':
                    
                        next
                        continue
                        
                    student_subject += str(row[r]) + ','
                    
                student = (total_student, enrollment_sem, student_subject);
                student_id = add_student(conn, student)
                
        with open(venue_filename, encoding='utf-8') as file:
        
            csv_reader = csv.reader(file, delimiter=',')
            
            next(csv_reader)       
            
            for row in csv_reader:
            
                name = str(row[0])
                capacity = str(row[1])
                vtype = str(row[2])
                venue = (name,capacity,vtype);
                venue_id = add_venue(conn, venue)
                
        counter = 0
        
        with open(subject_filename, encoding='utf-8') as file:
        
            csv_reader = csv.reader(file, delimiter=',')
            
            next(csv_reader)       
            
            for row in csv_reader:
            
                name = str(row[0])
                practical_time = str(row[1])
                lecturer_time = str(row[2])
                
                counter += 1
                
                subject_id = "%," + str(counter) + ",%"
                total_student = add_total_students(conn,subject_id)
                subject = (name,practical_time,lecturer_time,total_student);
                subject_id = add_subject(conn, subject)
                