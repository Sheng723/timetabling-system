from tkinter import *
from tkinter_theme import Interface
from import_file import import_all_files
from functools import partial
from edit_data import edit_data_page
from setting import isSqlite3Db
from ok_message_page import confirm_page
from generate_table import generate_tables

# create page to let the user select whether want to import files, edit database or generate timetable
def menu(dbname):
    menu = Interface()
    menu.set_title("User menu")
    menu.set_geometry('400x300+500+250')
    
    import_button = menu.button("Import files",partial(import_all_files,dbname),20,('Arial', 15))
    modify_button = menu.button("Add / Delete records",partial(edit_selected_data,dbname),20,('Arial', 15))
    create_button = menu.button("Create timetable ",partial(generate_tables,dbname,menu),20,('Arial', 15))
    
    menu.widget_position(import_button, (20, 20), 0, 0)
    menu.widget_position(modify_button, (20, 20), 1, 0)
    menu.widget_position(create_button, (20, 20), 2, 0)
   
    menu.keep_looping()

# create page to edit data in database only if the database is available
def edit_selected_data(dbname):
    
    if isSqlite3Db(dbname):
        
        choose_table = Interface()
        choose_table.set_title('Choose which one to edit data')

        choose_table.set_geometry("200x400")
        lecturer_button = choose_table.button("Lecturer", partial(edit_data_page,dbname,'lecturer'))
        student_button = choose_table.button("Student", partial(edit_data_page,dbname,'student'))
        subject_button = choose_table.button("Subject", partial(edit_data_page,dbname,'subject'))
        venue_button = choose_table.button("Venue", partial(edit_data_page,dbname,'venue'))
        
        choose_table.widget_position(lecturer_button, (5, 20), 0, 0)
        choose_table.widget_position(student_button, (5, 20), 1, 0)
        choose_table.widget_position(subject_button, (5, 20), 2, 0)
        choose_table.widget_position(venue_button, (5, 20), 3, 0)
        
        
        choose_table.keep_looping()
    # prompt user to import files first if database is not found
    else:
        confirm_page("No database found. Import files first.", 36)