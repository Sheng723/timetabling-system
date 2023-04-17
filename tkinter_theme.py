from tkinter import *  # standard library
from tkinter import filedialog

# This class is to standardize the theme of all interface and widget created with tkinter package.
class Interface:
    # The constructor of this class is to instantiate the window created with tkinter package.
    def __init__(self):
        self.interface = Tk()
        
    # The function is to set the title of the window created.
    def set_title(self, name):
        self.interface.title(name)

    # The function is to set the size of the window and its position to be shown in the computer screen.
    def set_geometry(self, size='700x500+400+100'):
        self.interface.geometry(size)

    # The function is to destroy the window created.
    def destroy(self):
        self.interface.destroy()

    # The function is to keep the window available even after some operations that has been made in the window.
    def keep_looping(self):
        self.interface.mainloop()
        
    # The function is to create a frame in the window created.
    def frame(self):
        return Frame(self.interface)
        
    # The function is to create a label widget in the window created.
    def label(self, text, width=20, font=('Arial', 15)):
        return Label(self.interface, text=text, width=width, font=font, anchor=W, bg='white', fg='black')
        
    # The function is to create a entry widget in the window created.
    def entry(self, width=25, font=('Arial', 15)):
        return Entry(self.interface, width=width, font=font)
        
    # The function is to create a button widget in the window created.
    def button(self, text, instruction=None, width=10, font=('Arial', 15)):
        return Button(self.interface, text=text, width=width,  font=font, command=instruction)

    # The function is to create a file dialog to let the user select file.  
    def openfile(self):
        filename = filedialog.askopenfilename(parent=self.interface, title = "Select file",filetypes = (("CSV Files","*.csv"),))
        return filename

    # The function is to position the widget that has been created in the window.
    @staticmethod
    def widget_position(widget, pad_list, row, column):
        widget.grid(row=row, column=column, sticky=W, padx=pad_list[0], pady=pad_list[1])
