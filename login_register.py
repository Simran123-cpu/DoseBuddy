# Import required libraries
from tkinter import *
from tkinter import messagebox
import database
from main import pro_med_win

logged_in_user = None
# creatiing register window
def register_window():
    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()




        # check if the username already exists in the database
        cursor = database.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username COLLATE NOCASE = ?", (username,))
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            register_window.destroy()
        elif password == confirm_password:
            database.register_user(username, password)
            logged_in_user = username
            register_window.destroy()
            win.destroy()
            pro_med_win(logged_in_user)


        else:
            messagebox.showerror("Error", "Passwords do not match")
            register_window.destroy()

    register_window = Tk()
    register_window.title("DoseBuddy - Register")
    register_window.geometry("440x240+1080+200")

    reg_frame = Frame(register_window, bg="aquamarine4", width=480, height=240)
    reg_frame.pack()

    username_label = Label(reg_frame, text="Username:", font="Nexa 12 bold", fg="aliceblue", bg="aquamarine4")
    username_label.place(x=35, y=50)
    username_entry = Entry(register_window, font="Nexa 12 bold", fg="aquamarine4")
    username_entry.place(x=240, y=50)

    password_label = Label(register_window, text="Password:", font="Nexa 12 bold", fg="aliceblue", bg="aquamarine4")
    password_label.place(x=35, y=90)
    password_entry = Entry(register_window, font="Nexa 12 bold", fg="aquamarine4", show = "*")
    password_entry.place(x=240, y=90)

    confirm_password_label = Label(register_window, text="Confirm Password:", font="Nexa 12 bold", fg="aliceblue",
                                   bg="aquamarine4")
    confirm_password_label.place(x=35, y=130)
    confirm_password_entry = Entry(register_window, font="Nexa 12 bold", fg="aquamarine4", show = "*")
    confirm_password_entry.place(x=240, y=130)

    register_button = Button(register_window, text="Register", font="Nexa 12 bold", command=register_user,
                             fg="aliceblue", bg="aquamarine4")
    register_button.place(x=180, y=170)

    register_window.mainloop()


# creating login window
def login_window():
    def login_user():
        global logged_in_user
        username = username_entry.get()
        password = password_entry.get()

        # Check if the username exists
        user = database.login_user(username, password)
        if user:
            logged_in_user = username
            login_window.destroy()
            win.destroy()
            pro_med_win(logged_in_user)

        else:
            cursor = database.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            cursor.close()
            if existing_user:
                messagebox.showerror("Error", "Invalid passowrd.")
                login_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid username")
                login_window.destroy()

    login_window = Tk()
    login_window.title("DoseBuddy - Login")
    login_window.geometry("400x200+1100+200")

    reg_frame = Frame(login_window, bg="aquamarine4", width=480, height=240)
    reg_frame.pack()

    username_label = Label(reg_frame, text="Username:", font="Nexa 12 bold", fg="aliceblue", bg="aquamarine4")
    username_label.place(x=65, y=60)
    username_entry = Entry(login_window, font="Nexa 12 bold", fg="aquamarine4")
    username_entry.place(x=160, y=60)

    password_label = Label(login_window, text="Password:", font="Nexa 12 bold", fg="aliceblue", bg="aquamarine4")
    password_label.place(x=65, y=100)
    password_entry = Entry(login_window, font="Nexa 12 bold", fg="aquamarine4", show = "*")
    password_entry.place(x=160, y=100)

    login_button = Button(login_window, text="Login", font="Nexa 12 bold", command=login_user, fg="aliceblue",
                             bg="aquamarine4")
    login_button.place(x=200, y=160)

    login_window.mainloop()

 
# creating main window
win = Tk()

screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
# Define the geometry of the window
win.geometry(f"{screen_width}x{screen_height}")

win.title("DoseBuddy")
win.minsize(720, 480)

frame = Frame(win, background="aquamarine4", pady=50)
frame.pack(side="top", fill="x")

label = Label(frame, text="Join Us!", bg="aquamarine4", font="Nexa 24 bold ", fg="aliceblue")
label.pack()

label2 = Label(frame, text="Already a user?", bg="aquamarine4", font="nexa 12 bold italic ", fg="aliceblue", pady=5)
label2.place(x=1355, y=15)

log_button = Button(frame, text="Login", bg="aquamarine4", font="nexa 12 bold ", fg="aliceblue", command=login_window)
log_button.place(x=1395, y=48)

reg_button = Button(frame, text="Create Account", bg="aquamarine4", font="nexa 12 bold", fg="aliceblue",
                    command=register_window)
reg_button.place(x=1350, y=-30)

img = PhotoImage(file="DoseBuddy.png")
img_label = Label(win, image=img)
img_label.pack()

win.mainloop()

