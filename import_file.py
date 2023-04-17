from tkinter import *
from tkinter_theme import Interface
from tkinter import filedialog
import webbrowser
from functools import partial
from ok_message_page import confirm_page
from connect_db import add_rows

# import file to get the data and insert them into database
def import_all_files(dbname):
    # open file to let user check the file format
    def open_file(url):
        webbrowser.open_new(url)
    # let user to select file
    def browsefunc(page, label):
        filename = page.openfile()
        label.configure(text=str(filename))
        
    # insert data into database once confirm button is selected.
    def confirm(lecturer_filename_label,student_filename_label,subject_filename_label,venue_filename_label):
        
        while lecturer_filename_label.cget("text") == '' or student_filename_label.cget("text")=='' or subject_filename_label.cget("text")== '' or venue_filename_label.cget("text") == '':
            confirm_page("Make sure all files are imported. Try again.", 36)
            return
        add_rows(dbname,lecturer_filename_label.cget("text"),
        student_filename_label.cget("text"),subject_filename_label.cget("text"),venue_filename_label.cget("text"))
        import_file.destroy()
        confirm_page("All files have been imported successfully", 36)

    import_file = Interface()

    import_file.set_title("Import file")
    import_file.set_geometry('1000x750+400+100')
    # widgets for lecturer import files option
    lecturer_label = import_file.label("Lecturer: ")
    lecturer_how_to_button = import_file.button("Check format",partial(open_file,"shorturl.at/dnzIL"))
    lecturer_file_label = import_file.label("File name: ")
    lecturer_filename_label = import_file.label("",width=50, font=('Arial', 7))
    lecturer_submit_button = import_file.button("Open file",
                                                partial(browsefunc,import_file,lecturer_filename_label))
    # widgets for student import files option
    student_label = import_file.label("Student: ")
    student_how_to_button = import_file.button("Check format",partial(open_file,"shorturl.at/isvU1"))
    student_file_label = import_file.label("File name: ")
    student_filename_label = import_file.label("",width=50, font=('Arial', 7))
    student_submit_button = import_file.button("Open file",
                                                partial(browsefunc,import_file,student_filename_label))
    # widgets for venue import files option
    venue_label = import_file.label("Venue: ")
    venue_how_to_button = import_file.button("Check format",partial(open_file,"shorturl.at/ruIM5"))
    venue_file_label = import_file.label("File name: ")
    venue_filename_label = import_file.label("",width=50, font=('Arial', 7))
    venue_submit_button = import_file.button("Open file",
                                                partial(browsefunc,import_file,venue_filename_label))
    # widgets for subject import files option
    subject_label = import_file.label("Subject: ")
    subject_how_to_button = import_file.button("Check format",partial(open_file,"shorturl.at/msFHK"))
    subject_file_label = import_file.label("File name: ")
    subject_filename_label = import_file.label("",width=50, font=('Arial', 7))
    subject_submit_button = import_file.button("Open file",
                                                partial(browsefunc,import_file,subject_filename_label))
    # button to let user confirm their choices
    ok_button = import_file.button("Ok",  partial(confirm,lecturer_filename_label,student_filename_label,subject_filename_label,venue_filename_label))
    # location of the widgets
    import_file.widget_position(lecturer_label, (5, 20), 0, 0)
    import_file.widget_position(lecturer_how_to_button, (5, 20), 0, 1)
    import_file.widget_position(lecturer_submit_button, (5, 20), 0, 2)
    import_file.widget_position(lecturer_file_label, (5, 20), 1, 0)
    import_file.widget_position(lecturer_filename_label, (5, 20), 1, 1)
    
    import_file.widget_position(student_label, (5, 20), 2, 0)
    import_file.widget_position(student_how_to_button, (5, 20), 2, 1)
    import_file.widget_position(student_submit_button, (5, 20), 2, 2)
    import_file.widget_position(student_file_label, (5, 20), 3, 0)
    import_file.widget_position(student_filename_label, (5, 20), 3, 1)
    
    import_file.widget_position(subject_label, (5, 20), 4, 0)
    import_file.widget_position(subject_how_to_button, (5, 20), 4, 1)
    import_file.widget_position(subject_submit_button, (5, 20), 4, 2)
    import_file.widget_position(subject_file_label, (5, 20), 5, 0)
    import_file.widget_position(subject_filename_label, (5, 20), 5, 1)
    
    import_file.widget_position(venue_label, (5, 20), 6, 0)
    import_file.widget_position(venue_how_to_button, (5, 20), 6, 1)
    import_file.widget_position(venue_submit_button, (5, 20), 6, 2)
    import_file.widget_position(venue_file_label, (5, 20), 7, 0)
    import_file.widget_position(venue_filename_label, (5, 20), 7, 1)
    
    import_file.widget_position(ok_button, (5, 20), 8, 1)
    import_file.keep_looping()
    