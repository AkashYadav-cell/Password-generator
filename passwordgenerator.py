import string
import random
from tkinter import *
from tkinter import messagebox
import re
import sqlite3


# Database setup
with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
cursor.execute("SELECT * FROM users")
db.commit()
db.close()


class GUI():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()

        root.title('Password Generator')
        root.geometry('660x500')
        root.config(bg='#2E4053')
        root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.label = Label(text=":PASSWORD GENERATOR:", anchor=N, fg='#F7DC6F', bg='#2E4053', font='arial 20 bold underline')
        self.label.grid(row=0, column=1)

        self.blank_label1 = Label(text="", bg='#2E4053')
        self.blank_label1.grid(row=1, column=0, columnspan=2)

        self.blank_label2 = Label(text="", bg='#2E4053')
        self.blank_label2.grid(row=2, column=0, columnspan=2)    

        self.blank_label3 = Label(text="", bg='#2E4053')
        self.blank_label3.grid(row=3, column=0, columnspan=2)    

        self.user = Label(text="Enter User Name: ", font='times 15 bold', bg='#2E4053', fg='#F7DC6F')
        self.user.grid(row=4, column=0)

        self.textfield = Entry(textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=4, column=1)
        self.textfield.focus_set()

        self.blank_label4 = Label(text="", bg='#2E4053')
        self.blank_label4.grid(row=5, column=0)

        self.length = Label(text="Enter Password Length: ", font='times 15 bold', bg='#2E4053', fg='#F7DC6F')
        self.length.grid(row=6, column=0)

        self.length_textfield = Entry(textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.length_textfield.grid(row=6, column=1)

        self.blank_label5 = Label(text="", bg='#2E4053')
        self.blank_label5.grid(row=7, column=0)

        self.generated_password = Label(text="Generated Password: ", font='times 15 bold', bg='#2E4053', fg='#F7DC6F')
        self.generated_password.grid(row=8, column=0)

        self.generated_password_textfield = Entry(textvariable=self.n_generatedpassword, font='times 15', bd=6, relief='ridge', fg='#DC143C')
        self.generated_password_textfield.grid(row=8, column=1)

        self.blank_label6 = Label(text="", bg='#2E4053')
        self.blank_label6.grid(row=9, column=0)

        self.blank_label7 = Label(text="", bg='#2E4053')
        self.blank_label7.grid(row=10, column=0)

        self.generate = Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#1ABC9C', bg='#34495E', command=self.generate_pass)
        self.generate.grid(row=11, column=1)

        self.blank_label8 = Label(text="", bg='#2E4053')
        self.blank_label8.grid(row=12, column=0)

        self.accept = Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#8E44AD', bg='#F0E68C', command=self.accept_fields)
        self.accept.grid(row=13, column=1)

        self.blank_label9 = Label(text="", bg='#2E4053')
        self.blank_label9.grid(row=14, column=0)

        self.reset = Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#8E44AD', bg='#F0E68C', command=self.reset_fields)
        self.reset.grid(row=15, column=1)

        self.show_users = Button(text="SHOW USERS", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#C0392B', bg='#F0E68C', command=self.show_users)
        self.show_users.grid(row=16, column=1)

    def generate_pass(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"
        upper = list(upper)
        lower = list(lower)
        chars = list(chars)
        numbers = list(numbers)
        name = self.textfield.get()
        leng = self.length_textfield.get()

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()

        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.textfield.delete(0, 25)
            return

        if not self.validate_length(leng):
            return

        length = int(leng)

        self.generated_password_textfield.delete(0, length)

        u = random.randint(1, length-3)
        l = random.randint(1, length-2-u)
        c = random.randint(1, length-1-u-l)
        n = length-u-l-c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        gen_passwd = "".join(password)
        self.generated_password_textfield.insert(0, gen_passwd)

    def validate_length(self, leng):
        if not leng.isdigit() or int(leng) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long and a valid number")
            self.length_textfield.delete(0, 25)
            return False
        return True

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM users WHERE Username = ?")
            cursor.execute(find_user, [(self.n_username.get())])

            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username")
            else:
                insert = "INSERT INTO users(Username, GeneratedPassword) VALUES(?, ?)"
                cursor.execute(insert, (self.n_username.get(), self.n_generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success", "Password generated successfully")

    def reset_fields(self):
        self.textfield.delete(0, 25)
        self.length_textfield.delete(0, 25)
        self.generated_password_textfield.delete(0, 25)

    def show_users(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            user_info = "\n".join([f"Username: {user[0]}, Password: {user[1]}" for user in users])
            messagebox.showinfo("User List", user_info)


if __name__ == '__main__':
    root = Tk()
    pass_gen = GUI(root)
    root.mainloop()
