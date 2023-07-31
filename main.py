from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import os
import json


def generate_password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    new_password = "".join(password_list)
    password_entry.insert(0, new_password)
    pyperclip.copy(new_password)


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_entry = {
        website: {
            "email": email,
            "password": password
        }
    }
    
    if len(email) > 0:
        with open("recent_email.txt", "w") as email_file:
            email_file.write(email)

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please fill in all the fields.")
    else:
        confirmed = messagebox.askokcancel(title=website,
                                           message=f"Do you want to save the following log-in? \nEmail: {email} \nPassword: {password}")

        if confirmed:
            current_data = {}
            try:
                with open("passwords.json", "r") as data_file:
                    current_data = json.load(data_file)
                    current_data.update(new_entry)
            except FileNotFoundError:
                current_data = new_entry
            except json.decoder.JSONDecodeError:
                current_data = new_entry
            finally:
                with open("passwords.json", "w") as data_file:
                    json.dump(current_data, data_file, indent=4)
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)


def open_passwords_file():
    try:
        os.startfile('passwords.json')
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="Save a log-in to generate a passwords file.")


try:
    with open("recent_email.txt", "r") as email_text_file:
        recent_email = email_text_file.readlines()
except FileNotFoundError:
    recent_email = ""

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
window.eval('tk::PlaceWindow . center')

# Labels
website_label = Label(text="Website")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)
password_label = Label(text="Password")
password_label.grid(row=3, column=0)

# TODO: Make classes for inputs and buttons

# Inputs
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
if recent_email:
    email_entry.insert(0, recent_email)
password_entry = Entry(width=35)
password_entry.grid(row=3, column=1, columnspan=2)

# Buttons
gen_password_btn = Button(text="Generate Password", width=29, command=generate_password)
gen_password_btn.grid(row=4, column=1, columnspan=2, pady=(0, 20))
save_btn = Button(text="Save Details", width=29, command=save)
save_btn.grid(row=5, column=1, columnspan=2)
open_btn = Button(text="Open Passwords File", width=29, command=open_passwords_file)
open_btn.grid(row=6, column=1, columnspan=2)

window.mainloop()
