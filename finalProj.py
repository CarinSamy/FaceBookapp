import tkinter as tk
from PIL import Image, ImageTk
import json
import re
from datetime import datetime

def load_data(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

users = load_data('users.json')

def register_user():
    name = reg_entry_name.get()
    phone = reg_entry_phone.get()
    email = reg_entry_username.get()
    password = reg_entry_password.get()
    gender = reg_entry_gender.get()
    day = reg_entry_day.get()
    month = reg_entry_month.get()
    year = reg_entry_year.get()

    if not all([name, phone, email, password, gender, day, month, year]):
        reg_result_label.config(text="All fields are required!", fg="red")
        return

    if not (phone.isdigit()):
        reg_result_label.config(text="Phone number must be numeric!", fg="red")
        return

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        reg_result_label.config(text="Invalid email format!", fg="red")
        return

    try:
        birth_date = datetime(int(year), int(month), int(day))
        age = (datetime.now() - birth_date).days // 365
        if age < 16:
            reg_result_label.config(text="You must be at least 16 years old to register.", fg="red")
            return
    except ValueError:
        reg_result_label.config(text="Invalid birth date!", fg="red")
        return

    if email in users:
        reg_result_label.config(text="User already exists!", fg="red")
        return

    new_user = {
        'name': name,
        'phone': phone,
        'email': email,
        'password': password,
        'gender': gender,
        'birth_date': birth_date.strftime("%Y-%m-%d"),
    }

    users[email] = new_user
    save_data(users, 'users.json')
    reg_result_label.config(text="Registration successful!", fg="green")

def open_register_window():
    window.withdraw()
    register_window = tk.Toplevel(window)
    register_window.title("Sign up")
    register_window.geometry("400x600")
    register_window.configure(bg='#f0f2f5')

    logo_label = tk.Label(register_window, image=resized_logo, bg='#f0f2f5')
    logo_label.place(x=10, y=10)

    tk.Label(register_window, text="Sign Up", font=('Arial', 20), bg='#f0f2f5').pack(pady=10)

    tk.Label(register_window, text="Name:", font=('Arial', 12), bg='#f0f2f5').pack(pady=5)
    global reg_entry_name
    reg_entry_name = tk.Entry(register_window)
    reg_entry_name.pack(pady=5)

    tk.Label(register_window, text="Phone:", font=('Arial', 12), bg='#f0f2f5').pack(pady=5)
    global reg_entry_phone
    reg_entry_phone = tk.Entry(register_window)
    reg_entry_phone.pack(pady=5)

    tk.Label(register_window, text="Email:", font=('Arial', 12), bg='#f0f2f5').pack(pady=5)
    global reg_entry_username
    reg_entry_username = tk.Entry(register_window)
    reg_entry_username.pack(pady=5)

    tk.Label(register_window, text="Password:", font=('Arial', 12), bg='#f0f2f5').pack(pady=5)
    global reg_entry_password
    reg_entry_password = tk.Entry(register_window, show="*")
    reg_entry_password.pack(pady=5)

    tk.Label(register_window, text="Birth-Date:", font=('Arial', 12), bg='#f0f2f5').pack(pady=5)

    frame_date = tk.Frame(register_window, bg='#f0f2f5')
    frame_date.pack(pady=5)

    global reg_entry_day, reg_entry_month, reg_entry_year
    reg_entry_day = tk.Entry(frame_date, width=5)
    reg_entry_month = tk.Entry(frame_date, width=5)
    reg_entry_year = tk.Entry(frame_date, width=7)

    reg_entry_day.pack(side=tk.LEFT, padx=5)
    tk.Label(frame_date, text="Day", bg='#f0f2f5').pack(side=tk.LEFT)
    reg_entry_month.pack(side=tk.LEFT, padx=5)
    tk.Label(frame_date, text="Month", bg='#f0f2f5').pack(side=tk.LEFT)
    reg_entry_year.pack(side=tk.LEFT, padx=5)
    tk.Label(frame_date, text="Year", bg='#f0f2f5').pack(side=tk.LEFT)


    tk.Label(register_window, text="Gender:", font=('Arial', 12), bg='#f0f2f5').pack(pady=10)
    global reg_entry_gender
    reg_entry_gender = tk.StringVar(value="Male")
    gender_frame = tk.Frame(register_window, bg='#f0f2f5')
    gender_frame.pack()

    tk.Radiobutton(gender_frame, text="Male", variable=reg_entry_gender, value="Male", bg='#f0f2f5').pack(side=tk.LEFT, padx=20)
    tk.Radiobutton(gender_frame, text="Female", variable=reg_entry_gender, value="Female", bg='#f0f2f5').pack(side=tk.LEFT, padx=20)

    tk.Button(register_window, text="Sign up", command=register_user, bg='green', fg='white').pack(pady=10)
    tk.Button(register_window, text="Back", command=lambda: back_to_login(register_window), bg='#4267B2', fg='white').pack(pady=10)

    global reg_result_label
    reg_result_label = tk.Label(register_window, text="", font=('Arial', 12), bg='#f0f2f5')
    reg_result_label.pack(pady=10)

def back_to_login(register_window):
    register_window.destroy()
    window.deiconify()

def login():
    email = entry.get()
    password = entry2.get()

    if email in users and users[email]['password'] == password:
        open_user_dashboard(users[email]['name'])
        window.withdraw()
    else:
        result_label.config(text="Login Failed. Invalid Username or Password.", fg="red")


def confirm_logout(current_window):
    confirm_window = tk.Toplevel(window)
    confirm_window.title("Confirm Logout")
    confirm_window.geometry("300x150")
    confirm_window.configure(bg='#f0f2f5')

    message_label = tk.Label(confirm_window, text="Logout of your account?", bg='#f0f2f5', font=('Arial', 14))
    message_label.pack(pady=20)
    logout_button = tk.Button(confirm_window, text="Logout",
                              command=lambda: logout_and_close(current_window, confirm_window), bg='red', fg='white')
    logout_button.pack(side=tk.LEFT, padx=20, pady=10)

    cancel_button = tk.Button(confirm_window, text="Cancel", command=confirm_window.destroy, bg='black', fg='white')
    cancel_button.pack(side=tk.RIGHT, padx=20, pady=10)


def logout_and_close(current_window, confirm_window):
    entry.delete(0, tk.END)
    entry2.delete(0, tk.END)

    current_window.destroy()
    confirm_window.destroy()
    window.deiconify()


def open_user_dashboard(name):
    user_window = tk.Toplevel(window)
    user_window.title("User Dashboard")
    user_window.geometry("400x400")
    user_window.configure(bg='#f0f2f5')

    tk.Label(user_window, text=f"Welcome {name}!", font=("Arial", 18), bg='#f0f2f5').pack(pady=10)
    tk.Button(user_window, text="Logout", command=lambda: confirm_logout(user_window), bg='#4267B2', fg='white').pack(
        pady=10)


def on_button_click(event):
    event.widget.config(bg='#3b5998')

def on_button_release(event):
    event.widget.config(bg='#4267B2')

window = tk.Tk()
window.title("FaceBook Application")
window.geometry("400x400")
window.configure(bg='#f0f2f5')

original_logo = Image.open("facebook-logo-icon.png")
resized_logo = ImageTk.PhotoImage(original_logo.resize((50, 50), Image.LANCZOS))

logo_label = tk.Label(window, image=resized_logo, bg='#f0f2f5')
logo_label.place(x=10, y=10)

tk.Label(window, text="Login", font=('Arial', 20), bg='#f0f2f5').pack(pady=10)
tk.Label(window, text="Email:", font=('Arial', 14), bg='#f0f2f5').pack(pady=5)
entry = tk.Entry(window)
entry.pack(pady=5)

tk.Label(window, text="Password:", font=('Arial', 14), bg='#f0f2f5').pack(pady=5)
entry2 = tk.Entry(window, show="*")
entry2.pack(pady=5)

result_label = tk.Label(window, text="", font=('Arial', 12), bg='#f0f2f5')
result_label.pack(pady=10)

login_button = tk.Button(window, text="Login", command=login, bg='#4267B2', fg='white')
login_button.pack(pady=10)
login_button.bind("<ButtonPress>", on_button_click)
login_button.bind("<ButtonRelease>", on_button_release)

register_button = tk.Button(window, text="Create new account", command=open_register_window, bg='green', fg='white')
register_button.pack(pady=10)
register_button.bind("<ButtonPress>", on_button_click)
register_button.bind("<ButtonRelease>", on_button_release)

window.mainloop()
