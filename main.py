from tkinter import messagebox
from password_generator import generate_password
import pyperclip
from tkinter import *
import json
file = "passwords.json"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def get_password():
    password_Entry.delete(0, END)
    password = generate_password()
    password_Entry.insert(END, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = websiteEntry.get()
    email = email_username_Entry.get().lower()
    password = password_Entry.get()
    record_dict = {
        website: {
            "Email/Username": email,
            "Password": password
        }
    }
    if "" in [website, record_dict[website]["Email/Username"], record_dict[website]["Password"]]:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty")
    else:
        is_ok = messagebox.askokcancel(title="Info Confirmation", message=f"These are the details entered:"
                                                                          f" \nEmail: {email}\nPassword: {password}"
                                                                          f"\nIs ok to save?")
        if is_ok:
            try:
                with open(file, mode="r") as f:
                    data = json.load(f)
                    data.update(record_dict)
                with open(file, mode="w") as f:
                    json.dump(data, f, indent=4)
            except FileNotFoundError:
                with open(file, mode="w") as f:
                    json.dump(record_dict, f, indent=4)
            except json.decoder.JSONDecodeError:
                with open(file, mode="w") as f:
                    json.dump(record_dict, f, indent=4)
            finally:
                messagebox.showinfo(title="SUCCESS", message=f"Password for {website} has been saved Successfully.")
                clear()


# -----------------------------------------------FIND PASSWORDS------------------------------------------------------- #


def find_password():
    website = websiteEntry.get()
    try:
        with open(file, mode="r") as f:
            data = json.load(f)
        if website in data:
            search_button.config(bg="blue")
            messagebox.showinfo(title="Info Confirmation", message=f"These are the details entered:\nEmail: {data[website]['Email/Username']}\nPassword: {data[website]['Password']}")
            pyperclip.copy(data[website]['Password'])
        else:
            print("No such Website Added.")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data file Found.\nTry adding a password First.")
    finally:
        search_button.config(bg="white")

def clear():
    websiteEntry.delete(0, END)
    email_username_Entry.delete(0, END)
    email_username_Entry.insert(0, "mahaleviraj@gmail.com")
    password_Entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("PASSWORD MANAGER")
window.config(padx=50, pady=50, bg="light blue")


canvas = Canvas(height=200, width=200, bg="light blue", highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(row=0, column=1)

websiteLabel = Label(text="Website:", bg="light blue")
websiteLabel.grid(row=1, column=0)

websiteEntry = Entry(width=39)
websiteEntry.grid(row=1, column=1, )
websiteEntry.focus()

search_button = Button(text="Search", bg="white", width=20, font=("Arial", 8, "normal"), command=find_password)
search_button.grid(row=1, column=2)

email_username_Label = Label(text="email/username:".title(), bg="light blue", highlightthickness=0)
email_username_Label.grid(row=2, column=0)

email_username_Entry = Entry(width=61)
email_username_Entry.grid(row=2, column=1, columnspan=2)
email_username_Entry.insert(0, "user-x@gmail.com")

password_Label = Label(text="Password:", bg="light blue")
password_Label.grid(row=3, column=0)

password_Entry = Entry(width=39)
password_Entry.grid(row=3, column=1)

generate_pass = Button(text="Generate Password", bg="white", command=get_password, width=20, font=("Arial", 8, "normal"))
generate_pass.grid(row=3, column=2)

add_password = Button(text="ADD", width=15, font=("Arial", 8, "normal"), command=save)
add_password.grid(row=4, column=1)

window.mainloop()
