from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(4, 7))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 3))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 3))]

    password = password_letters + password_numbers + password_symbols
    shuffle(password)
    password = "".join(password)

    password_entry.delete(0, END)
    password_entry.insert(0, password)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def copy_password():
    password = password_entry.get()

    if len(password) > 0:
        pyperclip.copy(password)
        messagebox.showinfo(title="Copy Password", message="Password successfully copied to clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        email: {
            website: password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                              f"\nPassword: {password} \nIs it ok to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # read old data
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                if email in data:
                    data[email][website] = password
                else:
                    data.update(new_data)

                with open("data.json", "w") as data_file:
                    # write data to json file
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().title()
    email = email_entry.get()

    if len(website) == 0 and len(email):
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left website and email field empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="You have not entered data yet.")

        else:
            if email in data:
                if website in data[email]:
                    messagebox.showinfo(title=f"{website}",
                                        message=f"Email: {email}\nPassword: {data[email][website]}")
                else:
                    messagebox.showinfo(title="Oops", message=f"There is no data for website or app {website} with email: {email}.")

            else:
                messagebox.showinfo(title="Oops", message=f"There is no data for website or app {website} with email: {email}.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=70, pady=70)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", pady=4)
website_label.grid(column=0, row=1, sticky="W")

email_label = Label(text="Email/Username:", pady=4)
email_label.grid(column=0, row=2, sticky="W")

password_label = Label(text="Password:", pady=4)
password_label.grid(column=0, row=3, sticky="W")

# Entries
website_entry = Entry(width=24, font=("Arial", 11))
website_entry.grid(column=1, row=1, columnspan=2, sticky="W")
website_entry.focus()

email_entry = Entry(width=24, font=("Arial", 11))
email_entry.grid(column=1, row=2, columnspan=2, sticky="W")
email_entry.insert(END, "example@gmail.com")

password_entry = Entry(font=("Arial", 11), width=35)
password_entry.grid(column=1, row=3, columnspan=2, sticky="EW")

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW", rowspan=2, ipady=12)

password_button = Button(text="Generate Password", width=27, command=generate_password)
password_button.grid(column=1, row=4, sticky="W", pady=4)

copy_button = Button(text="Copy Password", command=copy_password)
copy_button.grid(column=2, row=4, sticky="EW")

add_button = Button(text="Add", width=35, command=save)
add_button.grid(column=1, row=5, columnspan=2, sticky="EW")

window.mainloop()
