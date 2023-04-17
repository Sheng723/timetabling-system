from tkinter_theme import Interface
from functools import partial
from ok_message_page import confirm_page
from setting import isSqlite3Db
from genetic_system import ga_system
from timeit import default_timer as timer
import numpy as np
import sqlite3
import xlsxwriter
import webbrowser

# create page to let user to perform genetic algorithm.
def generate_tables(dbname,page):
    # if database exists, then create the related page.
    if isSqlite3Db(dbname):
    
        generate_page = Interface()
        
        generate_page.set_title("Generate table")
        generate_page.set_geometry('1000x550+400+250')

        day_no_label = generate_page.label("Total days: ")
        day_no_text_box = generate_page.entry(30)
        
        slot_no_label = generate_page.label("Slots per day: ")
        slot_no_text_box = generate_page.entry(30)
        
        max_generation_label = generate_page.label("Maximum generations:")
        max_generation_text_box = generate_page.entry(30)
        # show the solution after confirm button is pressed.
        def confirm(day_no_text_box,slot_no_text_box,max_generation_text_box):
            start = timer()
            day_no = int(day_no_text_box.get())
            slot_no = int(slot_no_text_box.get())
            max_generation = int(max_generation_text_box.get())
            solution = ga_system(dbname, day_no,slot_no,max_generation)
            generate_page.destroy()
            page.destroy()
            end_time = round(timer() - start, 2)
            execute_string = "Execution Time: "+str(end_time)+" seconds"
            confirm_page(execute_string, 36)
            show_solution(solution,dbname,day_no,slot_no)
            
        generate_table_button = generate_page.button("Create timetable", partial(confirm,day_no_text_box,
                                    slot_no_text_box,max_generation_text_box),20,('Arial', 15))
        
        generate_page.widget_position(day_no_label, (5, 20), 0, 0)
        generate_page.widget_position(day_no_text_box, (5, 20), 0, 1)
        
        generate_page.widget_position(slot_no_label, (5, 20), 1, 0)
        generate_page.widget_position(slot_no_text_box, (5, 20), 1, 1)
        
        generate_page.widget_position(max_generation_label, (5, 20), 2, 0)
        generate_page.widget_position(max_generation_text_box, (5, 20), 2, 1)
        
        generate_page.widget_position(generate_table_button, (5, 20), 3, 0)
       
        
        generate_page.keep_looping()
    # if databse not exist, prompt user to import files first.
    else:
        confirm_page("No database found. Import files first.", 36)

# show the timetable created in excel file.
def show_solution(solution,dbname,day_no,slot_no):
    # open the excel file.
    def open_file(url):
        webbrowser.open_new(url)
        
    filename = dbname.split(".")[0] + '.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    one_tuple = np.where(solution[:,:,:] == 1)
    
    conn = sqlite3.connect(dbname)
    data_sql = '''  SELECT name FROM venue'''
    cur = conn.cursor()
    cur.execute(data_sql)
    data = cur.fetchall()
    conn.commit()
    #initialize the variables.
    row = 1
    column = 1
    time = 8
    #write headers.
    for i in range(day_no):
        time = 8
        for i in range(slot_no):

            time_slot = str(time) + ':00'
            worksheet.write(0, column,     time_slot)
            time+=1
            column+=1
    #write venue info.
    for i in range(len(data)):
        worksheet.write(row, 0,str(data[i]))
        row +=1
        
    subject_sql = '''  SELECT name FROM subject where id = ?;'''
    cur = conn.cursor()
    subject_no = int(solution.shape[2] / 2)
    #write subject info.
    for r in range(len(one_tuple[0])):
        one_tuple_0,one_tuple_1,one_tuple_2 = one_tuple[0][r],one_tuple[1][r],(one_tuple[2][r]+1)
        if one_tuple_2 > subject_no:
            one_tuple_2 -=subject_no
        cur.execute(subject_sql,(str(one_tuple_2),))
        data = cur.fetchone()[0]
        worksheet.write(one_tuple_0+1, one_tuple_1+1, data)
        
    workbook.close()
    
    open_file(filename)