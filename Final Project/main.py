import tkinter as tk
from tkinter import messagebox
from data_operations import load_users
from authentication import authenticate_user
from teacher_dashboard import teacher_dashboard
from student_dashboard import student_dashboard
from parent_dashboard import parent_dashboard

'''Login function'''
def login():
    username = entry_username.get()
    password = entry_password.get()

    role, subject = authenticate_user(username, password, user_data)
    if role == "Teacher":
        teacher_dashboard(subject)
    elif role == "Student":
        student_dashboard(username)
    elif role == "Parent":
        parent_dashboard(username)
    else:
        messagebox.showerror("Access Denied", "Invalid username or password.")

'''Load user data'''
user_data = load_users()

'''Create the main GUI window'''
root = tk.Tk()
root.title("LMS Login System")
root.geometry("500x200")

'''Username label and entry'''
tk.Label(root, text="Username:").grid(row=0, column=0, padx=20, pady=10)
entry_username = tk.Entry(root, width=30)
entry_username.grid(row=0, column=1, padx=20, pady=10)

'''Password label and entry'''
tk.Label(root, text="Password:").grid(row=1, column=0, padx=20, pady=10)
entry_password = tk.Entry(root, show="*", width=30)
entry_password.grid(row=1, column=1, padx=20, pady=10)

'''Login button'''
tk.Button(root, text="Login", command=login, width=30).grid(row=2, column=0, columnspan=2, pady=20)

'''Run the application'''
root.mainloop()