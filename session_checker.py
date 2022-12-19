import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

def session_checker(classlist):
    
    classdict = {}

    for section in classlist:
        classdict[section] = ''
    
    def accept(class_dictionary, key):
        meetings_output = class_entry.get()
        if meetings_output == '1' or meetings_output == '2':
            class_dictionary[key] = meetings_output
            root.destroy()
        else:
            showinfo(
                title = 'Error',
                message = 'Class can only meet once or twice per week.\nPlease enter 1 or 2.'
            )

    for class_section in classdict:
        root = tk.Tk()
        root.geometry = ("300x300")
        root.resizable(False, False)
        root.title = 'Gradebook Maker'
        
        meetings = tk.StringVar()
        
        initializer = ttk.Frame(root)
        initializer.pack(padx=10,pady=10, fill='x', expand=True)
        
        class_label = ttk.Label(initializer, text=f'How many times per week does {class_section} meet? (1 or 2)')
        class_label.pack(fill='x',expand=True)
        
        class_entry = ttk.Entry(initializer, textvariable=meetings)
        class_entry.pack(fill='x', expand=True)
        class_entry.focus
        
        accept_button = tk.Button(initializer, text='Accept', command = lambda: accept(classdict, class_section))
        accept_button.pack(fill='x',expand=False)

        root.mainloop()
    return classdict