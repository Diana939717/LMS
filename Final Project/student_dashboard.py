import tkinter as tk
from tkinter import ttk, messagebox
from data_operations import load_grades, load_homework, load_users
import matplotlib.pyplot as plt

'''Display Student Dashboard'''
def student_dashboard(username):
    grades_df = load_grades()
    homework_df = load_homework()
    user_data = load_users()
    student_data = user_data[user_data["User"] == username]

    if student_data.empty or student_data["Role"].iloc[0] != "Student":
        messagebox.showerror("Access Denied", "Only students can access this dashboard.")
        return

    student_name = f"{student_data['Name'].iloc[0]} {student_data['Surname'].iloc[0]}"

    def view_grades():
        '''View all grades for the logged-in student.'''
        student_grades = grades_df[grades_df["User"] == username]

        if student_grades.empty:
            messagebox.showinfo("Grades", "No grades available for you.")
            return

        grades_window = tk.Toplevel()
        grades_window.title("Your Grades")
        grades_window.geometry("600x400")

        tree = ttk.Treeview(grades_window, columns=("Subject", "Grade"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        tree.heading("Subject", text="Subject")
        tree.heading("Grade", text="Grade")

        tree.column("Subject", width=150)
        tree.column("Grade", width=100)

        for _, row in student_grades.iterrows():
            tree.insert("", "end", values=(row["Subject"], row["Grade"]))

        scrollbar = ttk.Scrollbar(grades_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    def visualize_grades():
        '''Visualize the student's grades across all subjects.'''
        student_grades = grades_df[grades_df["User"] == username]
        if student_grades.empty:
            messagebox.showinfo("Visualization", "No grades available to visualize.")
        else:
            student_grades.set_index("Subject")["Grade"].plot(kind="bar", title="Your Grades")
            plt.ylabel("Grade")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    def view_homework():
        '''View homework based on the student's enrolled subjects.'''
        student_subjects = grades_df[grades_df["User"] == username]["Subject"].unique()
        subject_homework = homework_df[homework_df["Subject"].isin(student_subjects)]

        if subject_homework.empty:
            messagebox.showinfo("Homework", "No homework assigned for your subjects.")
            return

        homework_window = tk.Toplevel()
        homework_window.title("Homework Assigned")
        homework_window.geometry("600x400")

        tree = ttk.Treeview(homework_window, columns=("Subject", "Due Date", "Homework"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        tree.heading("Subject", text="Subject")
        tree.heading("Due Date", text="Due Date")
        tree.heading("Homework", text="Homework")

        tree.column("Subject", width=150)
        tree.column("Due Date", width=120)
        tree.column("Homework", width=250)

        for _, row in subject_homework.iterrows():
            tree.insert("", "end", values=(row["Subject"], row["DueDate"], row["Homework"]))

        scrollbar = ttk.Scrollbar(homework_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

    '''Student Dashboard GUI'''
    dashboard = tk.Tk()
    dashboard.title(f"{student_name} - Student Dashboard")
    dashboard.geometry("600x400")

    '''Apply consistent styling'''
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 14), padding=10)

    '''Frame with Scrollbar'''
    main_frame = tk.Frame(dashboard)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    '''Buttons'''
    buttons = [
        ("View Grades", view_grades),
        ("Visualize Grades", visualize_grades),
        ("View Homework", view_homework),
    ]

    for index, (text, command) in enumerate(buttons):
        ttk.Button(content_frame, text=text, command=command).grid(row=index, column=0, pady=10, padx=220, sticky="ew")

    dashboard.mainloop()