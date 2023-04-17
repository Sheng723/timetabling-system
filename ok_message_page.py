from tkinter_theme import Interface  # local source


# This function is to create a window that show the operations made is successful.
def confirm_page(text, size):
    # confirm variable is assigned to create a window.
    confirm = Interface()
    # Set the title, size and position of the window.
    confirm.set_title("")
    confirm.set_geometry('500x120+600+350')
    # Create a label showing the successful message in the window.
    confirm.widget_position(confirm.label(text, size), (5, 0), 0, 0)
    # Create an ok button that when it is clicked, destroy the window created.
    ok_button = confirm.button('Ok', lambda: confirm.destroy())
    confirm.widget_position(ok_button, (5, 20), 1, 0)
    # Keep the window available.
    confirm.keep_looping()
