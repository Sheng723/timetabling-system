from tkinter import *
from tkinter import ttk
from tkinter_theme import Interface
import sqlite3

# load the page to edit the data in database.
def edit_data_page(dbname,table):
    
    edit_data = Interface()
    edit_data.set_title('Edit data')

    edit_data.set_geometry("1000x1000")

    # create treeview frame.
    tree_frame = edit_data.frame()
    tree_frame.pack(pady=20)

    # create scrollbar.
    tree_scrollbar = Scrollbar(tree_frame)
    tree_scrollbar.pack(side=RIGHT, fill=Y)

    # create treeview.
    one_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set, selectmode="extended")
    
    one_tree.pack()

    # configure the scrollbar.
    tree_scrollbar.config(command=one_tree.yview)

    # create a database connection.
    conn = sqlite3.connect(dbname)
    
    # select column names from respective table.
    sql = '''  SELECT name FROM pragma_table_info(?) '''
    cur = conn.cursor()
    cur.execute(sql,[table])
    column = cur.fetchall()[1:]
    
    conn.commit()

    # define treeview column.
    one_tree['columns'] = column
    
    if table == 'student' or table == 'venue':
        
        one_tree.column("#0", width=0, stretch=NO)
        one_tree.column(column[0], anchor=W, width=120)
        one_tree.column(column[1], anchor=CENTER, width=150)
        one_tree.column(column[2], anchor=W, width=200)
        
        one_tree.heading("#0", text="", anchor=W)
        one_tree.heading(column[0], text=str(column[0]), anchor=W)
        one_tree.heading(column[1], text=str(column[1]), anchor=W)
        one_tree.heading(column[2], text=str(column[2]), anchor=CENTER)
       
    elif table == 'lecturer':
        
        one_tree.column("#0", width=0, stretch=NO)
        one_tree.column(column[0], anchor=CENTER, width=150)
        one_tree.column(column[1], anchor=W, width=200)
       
        one_tree.heading("#0", text="", anchor=W)
        one_tree.heading(column[0], text=str(column[0]), anchor=W)
        one_tree.heading(column[1], text=str(column[1]), anchor=CENTER)
        
    elif table == 'subject':
       
        one_tree.column("#0", width=0, stretch=NO)
        one_tree.column(column[0], anchor=W, width=120)
        one_tree.column(column[1], anchor=CENTER, width=150)
        one_tree.column(column[2], anchor=W, width=200)
        one_tree.column(column[3], anchor=W, width=200)
        
        one_tree.heading("#0", text="", anchor=W)
        one_tree.heading(column[0], text=str(column[0]), anchor=W)
        one_tree.heading(column[1], text=str(column[1]), anchor=W)
        one_tree.heading(column[2], text=str(column[2]), anchor=CENTER)
        one_tree.heading(column[3], text=str(column[3]), anchor=W)
        
    # get data from respective tables.
    data_sql = '''  SELECT * FROM %s'''
    cur = conn.cursor()
    cur.execute(data_sql%table)
    data = cur.fetchall()
    conn.commit()
    # initialize counter variable.
    global count
    count=0
    # insert all values get from database into treeview.
    for row in range(len(data)):
        if table == 'student' or table == 'venue':
            one_tree.insert(parent='', index='end', iid=count, text="", values=(data[row][1], data[row][2], data[row][3]))
            count += 1
        elif table == 'lecturer':
            one_tree.insert(parent='', index='end', iid=count, text="", values=(data[row][1], data[row][2]))
            count += 1
        elif table == 'subject':
            one_tree.insert(parent='', index='end', iid=count, text="", values=(data[row][1], data[row][2], data[row][3], data[row][4]))
            count += 1
            
    add_frame = edit_data.frame()
    add_frame.pack(pady=20)

    # create labels.
    l1 = Label(add_frame, text=str(column[0]))
    l1.grid(row=0, column=0)

    l2 = Label(add_frame, text=str(column[1]))
    l2.grid(row=0, column=1)
    
    if table == 'student' or table == 'venue':
    
        l3 = Label(add_frame, text=str(column[2]))
        l3.grid(row=0, column=2)
        
    elif table == 'subject':
    
        l3 = Label(add_frame, text=str(column[2]))
        l3.grid(row=0, column=2)
        l4 = Label(add_frame, text=str(column[3]))
        l4.grid(row=0, column=3)
        
    # create entry boxes.
    l1_box = Entry(add_frame)
    l1_box.grid(row=1, column=0)

    l2_box = Entry(add_frame)
    l2_box.grid(row=1, column=1)

    if table == 'student' or table == 'venue':
        
        l3_box = Entry(add_frame)
        l3_box.grid(row=1, column=2)
        
    elif table == 'subject':
    
        l3_box = Entry(add_frame)
        l3_box.grid(row=1, column=2)
        l4_box = Entry(add_frame)
        l4_box.grid(row=1, column=3)    
        
    # add record into database.
    def add_record():

        global count
        
        if table == 'student':
            one_tree.insert(parent='', index='end', iid=count, text="", values=(l1_box.get(), l2_box.get(), l3_box.get()))
            sql = ''' INSERT INTO student(total_student,enrollment_sem,subject)
                      VALUES(?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql,(l1_box.get(), l2_box.get(), l3_box.get()))
            conn.commit()
            count += 1
            
        elif table == 'venue':
            one_tree.insert(parent='', index='end', iid=count, text="", values=(l1_box.get(), l2_box.get(), l3_box.get()))
            sql = ''' INSERT INTO venue(name,capacity,vtype)
                      VALUES(?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql,(l1_box.get(), l2_box.get(), l3_box.get()))
            conn.commit()
            count += 1

        elif table == 'lecturer':
            one_tree.insert(parent='', index='end', iid=count, text="", values=(l1_box.get(), l2_box.get()))
            sql = ''' INSERT INTO lecturer(name,subject)
                      VALUES(?,?) '''
            cur = conn.cursor()
            cur.execute(sql,(l1_box.get(), l2_box.get()))
            conn.commit()
            count += 1

        elif table == 'subject':
            one_tree.insert(parent='', index='end', iid=count, text="", values=(l1_box.get(), l2_box.get(), l3_box.get(),l4_box.get()))
            sql = ''' INSERT INTO subject(name,practical_time,lecturer_time,total_student)
                      VALUES(?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql,(l1_box.get(), l2_box.get(), l3_box.get(),l4_box.get()))
            conn.commit()
            count += 1
        

        # clear the boxes.
        l1_box.delete(0, END)
        l2_box.delete(0, END)
        
        if table == 'student' or table == 'venue':
            l3_box.delete(0, END)

        elif table == 'subject':
            l3_box.delete(0, END)
            l4_box.delete(0, END)

    # Remove selected row from database.
    def remove_selected_row():
    
        x = one_tree.selection()[0]
        one_tree.delete(x)
        
        sql = ''' DELETE FROM %s WHERE id = ?; '''
        update_sql = ''' UPDATE %s SET id=id-1 WHERE id >= ?; '''
        cur = conn.cursor()
        cur.execute(sql%table,(x,))
        cur.execute(sql%table,(x,))
        conn.commit()
        
        # clear the boxes.
        l1_box.delete(0, END)
        l2_box.delete(0, END)
        
        if table == 'student' or table == 'venue':
            l3_box.delete(0, END)

        elif table == 'subject':
            l3_box.delete(0, END)
            l4_box.delete(0, END)

    # save updated record.
    def update_record():
        # grab record id.
        selected = one_tree.focus()
        
        if selected == '':
            return
        # save new data into database.
        if table == 'student':
            
            one_tree.item(selected, text="", values=(l1_box.get(), l2_box.get(), l3_box.get()))
            sql = ''' UPDATE %s
                      SET total_student = ?, enrollment_sem = ?, subject = ?
                      WHERE id = ?; '''
            cur = conn.cursor()
            cur.execute(sql%table,(l1_box.get(), l2_box.get(), l3_box.get(),selected))
            conn.commit()
            
        elif table == 'lecturer':
        
            if selected == '':
                return
                    
            row_num = int(selected)+1
            one_tree.item(selected, text="", values=(l1_box.get(), l2_box.get()))
            sql = ''' UPDATE %s
                      SET name = ?, subject = ?
                      WHERE id = ?; '''
            cur = conn.cursor()
            cur.execute(sql%table,(l1_box.get(), l2_box.get(),selected))
            conn.commit()    
            
        elif table == 'subject':
        
            if selected == '':
                return
                
            row_num = int(selected)+1
            one_tree.item(selected, text="", values=(l1_box.get(), l2_box.get(), l3_box.get(),l4_box.get()))
            sql = ''' UPDATE %s
                      SET name = ? ,practical_time = ? ,lecturer_time = ?,total_student = ?
                      WHERE id = ?; '''
            cur = conn.cursor()
            cur.execute(sql%table,(l1_box.get(), l2_box.get(), l3_box.get(),l4_box.get(),selected))
            conn.commit()   
            
        elif table == 'venue':
        
            if selected == '':
                return
                
            row_num = int(selected)+1
            one_tree.item(selected, text="", values=(l1_box.get(), l2_box.get(), l3_box.get()))
            sql = ''' UPDATE %s
                      SET name = ? ,capacity = ? ,vtype = ?
                      WHERE id = ?; '''
            cur = conn.cursor()
            cur.execute(sql%table,(l1_box.get(), l2_box.get(), l3_box.get(),selected))
            conn.commit()
            
        # clear the boxes.
        l1_box.delete(0, END)
        l2_box.delete(0, END)
        
        if table == 'student' or table == 'venue':
            l3_box.delete(0, END)

        elif table == 'subject':
            l3_box.delete(0, END)
            l4_box.delete(0, END)

    update_button = edit_data.button("Update record",update_record,20,('Arial', 15))
    add_button = edit_data.button("Add record",add_record,20,('Arial', 15))
    remove_button = edit_data.button("Remove Record",remove_selected_row,20,('Arial', 15))

    update_button.pack(pady=10)
    add_button.pack(pady=10)
    remove_button.pack(pady=10)

    edit_data.keep_looping()

