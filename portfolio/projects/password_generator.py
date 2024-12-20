from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random

window = Tk()
window.title("Password Generator")
window.geometry("400x450")


length_var = StringVar(value="12")
use_upper = BooleanVar(value=True)
use_lower = BooleanVar(value=True)
use_nums = BooleanVar(value=True)
use_symbols = BooleanVar(value=True)
password_var = StringVar()

def check_length(text):
    if text == "":
        return True
    if text.isdigit():
        num = int(text)
        if num > 0 and num <= 100:
            return True
    return False


title = Label(window, text="Make a Password!", font=('Arial', 16))
title.pack(pady=20)


length_box = LabelFrame(window, text="How long?", padx=10, pady=10)
length_box.pack(padx=20, pady=10)

length_label = Label(length_box, text="Type length (max 100):")
length_label.pack(side='left')

check = (window.register(check_length), '%P')
length_entry = Entry(length_box, textvariable=length_var, width=5, validate='key', validatecommand=check)
length_entry.pack(side='left', padx=5)


options = LabelFrame(window, text="What to include?", padx=10, pady=10)
options.pack(padx=20, pady=10)

Checkbutton(options, text="ABC", variable=use_upper).pack()
Checkbutton(options, text="abc", variable=use_lower).pack()
Checkbutton(options, text="123", variable=use_nums).pack()
Checkbutton(options, text="!@


pass_box = LabelFrame(window, text="Your Password", padx=10, pady=10)
pass_box.pack(padx=20, pady=10)

pass_entry = Entry(pass_box, textvariable=password_var, font=('Courier', 12), justify='center')
pass_entry.pack(pady=5)

def make_password():
    try:
        length = int(length_var.get())
        if length < 1 or length > 100:
            messagebox.showerror("Error", "Length must be 1-100!")
            return
    except:
        messagebox.showerror("Error", "Type a proper number!")
        return
    
    chars = ""
    if use_upper.get():
        chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_lower.get():
        chars += "abcdefghijklmnopqrstuvwxyz"
    if use_nums.get():
        chars += "0123456789"
    if use_symbols.get():
        chars += "!@
    
    if not chars:
        password_var.set("Pick something to include!")
        return
    
    password = ""
    for i in range(length):
        password += random.choice(chars)
    
    password_var.set(password)

def copy_pass():
    password = password_var.get()
    if password and password != "Pick something to include!":
        window.clipboard_clear()
        window.clipboard_append(password)


Button(window, text="Make Password!", command=make_password).pack(pady=5)
Button(window, text="Copy", command=copy_pass).pack(pady=5)

window.mainloop()
