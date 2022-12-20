import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import main

root = tk.Tk()
root.geometry("300x300")
root.resizable(False,False)
root.title('Gradebook Maker')

name = tk.StringVar()
roster_url = tk.StringVar()
u_temp_url = tk.StringVar()

## TODO: Make a function to check validity of the URLs
def url_check(url_list):
    return True

## Calls the main function if valid urls are given
def submit_clicker():
    urls = [roster_url.get(),u_temp_url.get()]

    valid = url_check(urls)
    
    if valid == True:
        msg = f'Generating gradebooks for {name.get()}'
        showinfo(
            title = 'Information',
            message = msg
        )
        root.destroy()
        main.main(name.get(),roster_url.get(),u_temp_url.get())

        showinfo(
            title = 'Information',
            message = 'Done.'
        )
    else:
        showinfo(
            title = 'Error',
            message = 'One or more URLs is not valid'
        )

initializer = ttk.Frame(root)
initializer.pack(padx=10,pady=10, fill='x', expand=True)

name_label = ttk.Label(initializer, text='Name: ')
name_label.pack(fill='x',expand=True)

name_entry = ttk.Entry(initializer, textvariable=name)
name_entry.pack(fill='x', expand=True)
name_entry.focus

roster_label = ttk.Label(initializer, text='Roster URL:')
roster_label.pack(fill='x', expand=True)

roster_entry = ttk.Entry(initializer, textvariable=roster_url)
roster_entry.pack(fill='x', expand=True)
roster_entry.focus()

gb_temp_label = ttk.Label(initializer, text='Template URL:')
gb_temp_label.pack(fill='x', expand=True)

gb_temp_entry = ttk.Entry(initializer, textvariable=u_temp_url)
gb_temp_entry.pack(fill='x', expand=True)
gb_temp_entry.focus()

submit_button = ttk.Button(initializer, text='Submit', command=submit_clicker)
submit_button.pack()

root.mainloop()
