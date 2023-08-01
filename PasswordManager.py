from tkinter import *
from tkinter import messagebox, OptionMenu, StringVar
from random import choice, randint, shuffle
import pyperclip
import os
import json

DEFAULT_DROPDOWN = "Select An Entry"


def read_pw_file():
    with open("passwords.json", "r") as data_file:
        return json.load(data_file)


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

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please fill in all the fields.")
    else:
        confirmed = messagebox.askokcancel(title=website,
                                           message=f"Do you want to save the following log-in for {website}? \nEmail: {email} \nPassword: {password}")

        if confirmed:
            current_data = {}
            try:
                current_data = read_pw_file()
            except FileNotFoundError:
                pass
            except json.decoder.JSONDecodeError:
                pass
            finally:
                if website in current_data:
                    confirmed_overwrite = messagebox.askokcancel(title=website, message=f"An entry for {website} already exists. Do you want to overwrite it?")
                    if confirmed_overwrite:
                        del current_data[website]
                    else:
                        return

                with open("passwords.json", "w") as data_file:
                    current_data.update(new_entry)
                    json.dump(current_data, data_file, indent=4)
                website_entry.delete(0, END)
                password_entry.delete(0, END)


def find_password():
    dropdown_val = dropdown_option.get()
    search_bar_val = search_bar_entry.get()
    query = dropdown_val if dropdown_val != DEFAULT_DROPDOWN else search_bar_val

    if len(query) == 0:
        messagebox.showinfo(title="Oops", message="Please enter a search query or select an existing entry from the dropdown menu.")
    else:
        try:
            current_data = read_pw_file()
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="No password data found.")
        except json.decoder.JSONDecodeError:
            messagebox.showinfo(title="Oops", message="No password data found.")
        else:
            if query in current_data:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)
                website_entry.insert(0, query)
                email_entry.insert(0, current_data[query]["email"])
                password_entry.insert(0, current_data[query]["password"])
            else:
                messagebox.showinfo(title="Oops", message=f"No log-in details found for {query}.")
    # Reset dropdown menu and search bar
    dropdown_option.set(DEFAULT_DROPDOWN)
    search_bar_entry.delete(0, END)


def copy_email():
    email = email_entry.get()
    pyperclip.copy(email)


def copy_password():
    password = password_entry.get()
    pyperclip.copy(password)


def open_passwords_file():
    try:
        os.startfile('passwords.json')
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="Save a log-in to generate a passwords file.")


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


pw_file_websites = []
try:
    pw_file = read_pw_file()
    pw_file_websites = list(pw_file.keys())
    # Get email from most recent entry
    recent_email = pw_file[pw_file_websites[-1]]["email"]
except FileNotFoundError:
    recent_email = ""
except json.decoder.JSONDecodeError:
    recent_email = ""

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
window.eval('tk::PlaceWindow . center')

# Search
search_label = Label(text="Search")
search_label.grid(row=1, column=0)

dropdown_option = StringVar()
dropdown_option.set(DEFAULT_DROPDOWN)
search_dropdown_entry = OptionMenu(window, dropdown_option, *pw_file_websites)
search_dropdown_entry.grid(row=1, column=1, columnspan=2)
search_dropdown_entry.config(width=28)

search_bar_entry = Entry(width=35)
search_bar_entry.grid(row=2, column=1, columnspan=2)

search_btn = Button(text="Get Log-In Details", width=29, command=find_password)
search_btn.grid(row=3, column=1, pady=(0, 30), columnspan=2)

# Website
website_label = Label(text="Website")
website_label.grid(row=4, column=0, pady=(0, 15))

website_entry = Entry(width=35)
website_entry.grid(row=4, column=1, pady=(0, 15), columnspan=2)
website_entry.focus()

# Email
email_label = Label(text="Email/Username")
email_label.grid(row=5, column=0, pady=(0, 15))

email_entry = Entry(width=27)
email_entry.grid(row=5, column=1, pady=(0, 15))
if recent_email:
    email_entry.insert(0, recent_email)

copy_email_btn = Button(text="Copy", width=5, command=copy_email)
copy_email_btn.grid(row=5, column=2, pady=(0, 15))

# Password
password_label = Label(text="Password")
password_label.grid(row=6, column=0)

password_entry = Entry(width=27)
password_entry.grid(row=6, column=1)

copy_pw_btn = Button(text="Copy", width=5, command=copy_password)
copy_pw_btn.grid(row=6, column=2)

gen_password_btn = Button(text="Generate New Password", width=29, command=generate_password)
gen_password_btn.grid(row=7, column=1, pady=(0, 30), columnspan=2)

# Misc
save_btn = Button(text="Save Details", width=29, command=save)
save_btn.grid(row=8, column=1, columnspan=2)

open_btn = Button(text="Open Passwords File", width=29, command=open_passwords_file)
open_btn.grid(row=9, column=1, columnspan=2)

window.mainloop()
