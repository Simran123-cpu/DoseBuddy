import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date, timedelta
import database

# Global variables to store the current user's ID and active profile ID
current_username = None
active_profile_id = None

def pro_med_win(username):
    win = tk.Tk()
    win.title("DoseBuddy - Medication")

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Define the geometry of the window
    win.geometry(f"{screen_width}x{screen_height}")

    frame = tk.Frame(win, background="aquamarine4", height=screen_height, width=screen_width)
    frame.pack()

    label1 = tk.Label(frame, text="Stay on Track, Stay on Top of Health!", font="Nexa 28 bold", bg="aquamarine4",
                      fg="aliceblue")
    label1.place(x=680, y=70)
    frame2 = tk.Frame(frame, background="black", height=screen_height, width=200)
    frame2.place(x=0, y=0)

    horizontal_line = tk.Frame(frame2, height=2, width=300, bg="white")
    horizontal_line.place(y=200)

    history_button = tk.Button(frame2, text="History", bg="aquamarine4", font="Nexa 12", fg="aliceblue", width=10)
    history_button.place(x=49, y=400)

    def show_profile():
        profile_listbox = tk.Listbox(frame, bg="white", font="Nexa 12", width=80, height=35, relief="flat")
        profile_listbox.place(x=650, y=200)


        # fetch all profiles and desplay
        current_username = username
        cursor = database.conn.cursor()
        cursor.execute("SELECT name, id FROM user_profiles WHERE username = ?", (current_username,))
        profiles = cursor.fetchall()
        cursor.close()
        for profile in profiles:
            profile_listbox.insert(tk.END, profile[0])

        def profile_win():
            def add_profile():
                name = name_entry.get()
                age = age_entry.get()

                users_id = database.get_user_id(username)
                if not name or not age:
                    messagebox.showerror("Error", "Please fill in all the fields")
                else:
                    database.add_profile(users_id, username, name, age)
                    messagebox.showinfo("Success", "Profile Added")
                    name_win.destroy()
                    show_profile()

            global name_win
            name_win = tk.Tk()
            name_win.title("Add Profile")
            name_win.configure(bg="aquamarine4", height=240, width=480)

            name_label = tk.Label(name_win, text="Name:", font="Nexa 12 bold", fg="aliceblue", bg="aquamarine4")
            name_label.place(x=85, y=70)
            name_entry = tk.Entry(name_win, font="Nexa 12 bold", fg="aquamarine4")
            name_entry.place(x=200, y=70)

            age_label = tk.Label(name_win, text="Age:", font="Nexa 12 bold", fg="aliceblue", bg="aquamarine4")
            age_label.place(x=85, y=110)
            age_entry = tk.Entry(name_win, font="Nexa 12 bold", fg="aquamarine4", show="*")
            age_entry.place(x=200, y=110)

            profile_button = tk.Button(name_win, text="Add", font="Nexa 12 bold", command=add_profile,fg="aliceblue", bg="aquamarine4")
            profile_button.place(x=200, y=160)
            name_win.mainloop()


        def activate_profile():
            global active_profile_id
            global name
            selected_index = profile_listbox.curselection()
            if selected_index:
                name = profile_listbox.get(selected_index[0])

                cursor = database.conn.cursor()
                cursor.execute('SELECT id FROM user_profiles WHERE name = ?', (name,))
                profile_id = cursor.fetchone()
                cursor.close()
                if profile_id:
                    active_profile_id = profile_id[0]
                    messagebox.showinfo("Success", f"{name} is now the active profile.")
                else:
                    active_profile_id = None
                    messagebox.showerror("Error", "Profile not found.")
            else:
                active_profile_id = None
                messagebox.showerror("Error", "No profile selected.")

        profile_add_button = tk.Button(frame, text="Add", bg="aquamarine4", font="Nexa 12", fg="aliceblue", width=10,command=profile_win)
        profile_add_button.place(x=1240, y=810)

        activate_button = tk.Button(frame, text="Activate", command=activate_profile, bg="aquamarine4", font="Nexa 12", fg="aliceblue", width=10)
        activate_button.place(x=1040, y=810)


    profiles_button = tk.Button(frame2, text="Profiles", bg="aquamarine4", font="Nexa 12", fg="aliceblue", width=10,command=show_profile)
    profiles_button.place(x=49, y=280)

    # Medications window
    def show_medication():
        medication_listbox = tk.Listbox(frame, bg="white", font="Nexa 12", width=80, height=35, relief="flat")
        medication_listbox.place(x=650, y=200)
        frame3 = tk.Frame(frame, bg="azure3", height=53, width=724, relief="flat")
        frame3.place(x=650, y=816)

        medication_add_button1 = tk.Button(frame, text="Medication", bg="aquamarine4", font="Nexa 12", fg="aliceblue",width=10)
        medication_add_button1.place(x=1240, y=826)

        medication_add_button3 = tk.Button(frame, text="Today", bg="aquamarine4", font="Nexa 12", fg="aliceblue", width=10)
        medication_add_button3.place(x=690, y=826)

        # Fetch and display the medication details specific to the active profile
        if active_profile_id:
            cursor = database.conn.cursor()
            cursor.execute('SELECT * FROM medication WHERE username = ? AND profile_id = ?',(current_username, active_profile_id))
            user_medications = cursor.fetchall()
            for medication in user_medications:
                medication_listbox.insert(tk.END, f"{medication[4]}({medication[1]})       {medication[7]}"),

        # Add Medication
        def med_win():
            def add_medication():
                if not active_profile_id:
                    messagebox.showerror("Error", "No active profile selected.")
                    return

                medicine_name = medicine_entry.get()
                medication_cause = medication_cause_entry.get()  # New field
                description = dosage_entry.get()  # New field
                repeat_interval = repeat_var.get()
                custom_schedule = ','.join([day_var.get() for day_var in days_vars])  # Combine selected days

                reminder_times_option = times_var.get()
                if reminder_times_option == "x times a day":
                    reminder_times = times_entry.get()
                elif reminder_times_option == "after x hours":
                    try:
                        hours_interval = float(hours_entry.get())
                    except ValueError:
                        messagebox.showerror("Error", "Invalid input for hours interval (must be a number)")
                        return
                    reminder_times = generate_times_every_x_hours(hours_interval)
                else:
                    messagebox.showerror("Error", "Please select a reminder times option")
                    return
                if not medicine_name or not reminder_times or not medication_cause or not repeat_interval:
                    messagebox.showerror("Error", "Please fill in all fields")
                else:
                    database.add_medication(username, active_profile_id,name, medication_cause, medicine_name, description,
                                            reminder_times, repeat_interval, custom_schedule)
                    medication_listbox.insert(tk.END,f"{medicine_name}({medication_cause}),{reminder_times}")
                    med_win.destroy()

                # Check for valid time format (HH:MM)
                reminder_times = [time.strip() for time in reminder_times.split(",")]  # Split times by comma
                for time_str in reminder_times:
                    try:
                        datetime.strptime(time_str, '%H:%M')
                    except ValueError:
                        messagebox.showerror("Error", "Invalid time format. Use HH:MM (24-hour format)")
                        return

            def generate_times_every_x_hours(hours_interval):
                now = datetime.now()
                reminder_times = []

                for i in range(int(24 / hours_interval)):
                    reminder_time = now + timedelta(hours=i * hours_interval)
                    reminder_times.append(reminder_time.strftime('%H:%M'))

                return ','.join(reminder_times)

            def back_frame():
                med_win.destroy()
                show_medication()

            med_win = tk.Frame()
            med_win.configure(bg="aquamarine4", height=670, width=724, borderwidth=2, highlightcolor="black",
                              highlightthickness=2, highlightbackground="black")
            med_win.place(x=650, y=200)

            medicine_label = tk.Label(med_win, text="Medicine Name", font="Nexa 16 ", bg="aquamarine4", fg="aliceblue")
            medicine_label.place(x=478, y=85)

            medicine_entry = tk.Entry(med_win, font="Nexa 16 ", fg="aquamarine4", bg="aliceblue")
            medicine_entry.place(x=440, y=120)

            medication_cause_label = tk.Label(med_win, text=" Medication Cause", font="Nexa 16 ", bg="aquamarine4",
                                              fg="aliceblue")
            medication_cause_label.place(x=60, y=85)
            medication_cause_entry = tk.Entry(med_win, font="Nexa 16 ", fg="aquamarine4", bg="aliceblue")
            medication_cause_entry.place(x=30, y=120)

            dosage_label = tk.Label(med_win, text="Description", font="Nexa 16", bg="aquamarine4",
                                    fg="aliceblue")  # New field
            dosage_label.place(x=95, y=185)

            dosage_entry = tk.Entry(med_win, font="Nexa 16 ", fg="aquamarine4", bg="aliceblue")  # New field
            dosage_entry.place(x=30, y=220)

            times_var = tk.StringVar()
            times_var.set("Reminder Times")
            times_dropdown = tk.OptionMenu(med_win, times_var, "Reminder Times", "x times a day", "after x hours")
            times_dropdown.configure(bg="aquamarine4", fg="aliceblue", font="Nexa 12")
            times_dropdown.place(x=70, y=285)

            times_label = tk.Label(med_win, text="Enter Times", font="Nexa 16 ", bg="aquamarine4", fg="aliceblue")
            times_entry = tk.Entry(med_win, font="Nexa 16 ", fg="aquamarine4", bg="aliceblue")

            hours_label = tk.Label(med_win, text="Enter Hours", font="Nexa 16 ", bg="aquamarine4", fg="aliceblue")
            hours_entry = tk.Entry(med_win, font="Nexa 16 ", fg="aquamarine4", bg="aliceblue")

            def toggle_times(*args):
                selected_option = times_var.get()
                if selected_option == "x times a day":
                    times_label.place(x=85, y=325)
                    times_entry.place(x=30, y=360)
                    hours_label.place_forget()
                    hours_entry.place_forget()
                elif selected_option == "after x hours":
                    hours_label.place(x=85, y=325)
                    hours_entry.place(x=30, y=360)
                    times_label.place_forget()
                    times_entry.place_forget()
                else:
                    times_label.place_forget()
                    times_entry.place_forget()
                    hours_label.place_forget()
                    hours_entry.place_forget()

            toggle_times()  # Hide the custom day checkboxes initially

            # Trace variable changes to call the toggle_custom_days function when the repeat_var changes
            times_var.trace("w", toggle_times)

            repeat_label = tk.Label(med_win, text="Repeat Interval:", font="Nexa 16 ", bg="aquamarine4", fg="aliceblue")
            repeat_label.place(x=470, y=185)

            repeat_var = tk.StringVar()
            repeat_var.set("None")

            repeat_dropdown = tk.OptionMenu(med_win, repeat_var, "None", "Daily", "Weekly", "Custom")
            repeat_dropdown.configure(bg="aquamarine4", fg="aliceblue", font="Nexa 12")
            repeat_dropdown.place(x=508, y=220)

            days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            days_vars = []
            days_checkboxes = []  # Keep references to checkboxes

            frame2 = tk.Frame(med_win, bg="aquamarine4", height=100, width=50)
            frame2.place(x=508, y=260)

            for day in days_of_week:
                day_var = tk.StringVar()
                day_var.set(day)
                day_checkbox = tk.Checkbutton(frame2, text=day, variable=day_var, bg="aquamarine4", font="Nexa 12")
                days_vars.append(day_var)
                days_checkboxes.append(day_checkbox)

            # Function to toggle custom day checkboxes based on the selected repeat option

            def toggle_custom_days(*args):
                if repeat_var.get() == "Custom":
                    for day_checkbox in days_checkboxes:
                        day_checkbox.pack(anchor="w")
                else:
                    for day_checkbox in days_checkboxes:
                        day_checkbox.pack(anchor="w")
                        day_checkbox.forget()

            # Hide the custom day checkboxes initially
            toggle_custom_days()

            # Trace variable changes to call the toggle_custom_days function when the repeat_var changes
            repeat_var.trace("w", toggle_custom_days)

            add_button = tk.Button(med_win, text="Add Reminder", command=add_medication, font="Nexa 12 ",bg="aquamarine4",fg="aliceblue")
            add_button.place(x=310, y=450)

            back_button = tk.Button(med_win, text="Back", font="Nexa 12", command=back_frame)
            back_button.place(x=40, y=600)

            med_win.mainloop()

        medication_add_button2 = tk.Button(frame, text="Add", bg="aquamarine4", font="Nexa 12", fg="aliceblue", command=med_win)
        medication_add_button2.place(x=965, y=802)

    medications_button = tk.Button(frame2, text="Medications", bg="aquamarine4", font="Nexa 12", fg="aliceblue",width=10, command=show_medication)
    medications_button.place(x=49, y=340)

    win.mainloop()


