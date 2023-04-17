import csv 
from tkinter_theme import Interface
from functools import partial
from ok_message_page import confirm_page
import setting
from menu_page import menu

# create the first page when run the program
def main_page():
    
    login = Interface()
    # create the widgets 
    login.set_title("User login")
    login.set_geometry('1000x550+400+250')
    
    username_label = login.label("Username: ")
    username_text_box = login.entry(30)
    
    password_label = login.label("Password: ")
    password_text_box = login.entry(30)
    
   
    warning_label = login.label("Welcome!",width=35, font=('Arial', 15))
    
    login_button = login.button("Login", partial(verification,login,username_text_box,
                                password_text_box,warning_label))
    register_button = login.button("Register", register)
    
    # set the location of the widgets in this window
    login.widget_position(username_label, (20, 20), 0, 0)
    login.widget_position(username_text_box, (20, 20), 0, 1)

    login.widget_position(password_label, (20, 20), 1, 0)
    login.widget_position(password_text_box, (20, 20), 1, 1)
    
    login.widget_position(warning_label, (20, 20), 2, 1)
    login.widget_position(login_button, (20, 20), 3, 1)
    login.widget_position(register_button, (20, 20), 4, 1)

    login.keep_looping()

# verify if the user enter the correct username and password
def verification(page,username_text_box,password_text_box,label):

    with open('login_list.csv', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)
        while True:
            for row in csv_reader:
                if row[0] == username_text_box.get():
                    if row[1] == password_text_box.get():
                        setting.dbname = username_text_box.get() + '.db'
                        page.destroy()
                        confirm_page("Successful login!", 36)
                        menu(setting.dbname)
                        return
            if True:
                label.configure(text = "Wrong username or password. Try again. ")
                break
        file.close()

# create a window to let the user register their account                    
def register():
    # save the login details into csv file
    def save_login_info(username_text_box, password_text_box,label):
    
        with open('login_list.csv', encoding='utf-8') as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                if row[0] == username_text_box.get() or username_text_box.get() == '' or password_text_box.get() == '':
                    label.configure(text = "Duplicate username or null values detected. Try again. ")
                    return
            file.close()
            
        row = [str(username_text_box.get()),str(password_text_box.get())]
        with open('login_list.csv', 'a', newline='') as file:
            write = csv.writer(file)
            write.writerow(row)
            file.close()
        registration.destroy()
        confirm_page("Your account has been successfully created.", 36)
        
    registration = Interface()
   
    registration.set_title("Register New Account")
    registration.set_geometry('800x600+450+10')
    # create the widgets 
    username_label = registration.label("Username: ")
    username_text_box = registration.entry(25)
    
    password_label = registration.label("Password: ")
    password_text_box = registration.entry(25) 
    
    warning_label = registration.label("",width=50, font=('Arial', 10))
    # set the location of the widgets in this window
    registration.widget_position(username_label, (5, 20), 0, 0)
    registration.widget_position(username_text_box, (5, 20), 0, 1)
    
    registration.widget_position(warning_label, (5, 20), 1, 1)
    
    registration.widget_position(password_label, (5, 20), 2, 0)
    registration.widget_position(password_text_box, (5, 20), 2, 1)
    
    confirm_button = registration.button("Confirm", partial(save_login_info,username_text_box,
                        password_text_box,warning_label))
    registration.widget_position(confirm_button, (5, 20), 3, 1)
    
    registration.keep_looping()
    

            
main_page()