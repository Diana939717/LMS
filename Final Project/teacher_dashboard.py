import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from data_operations import load_grades, save_grades, load_homework, save_homework, load_absences, save_absences, load_users, save_users

'''Defines the main function teacher_dashboard that takes subject as an argument.
grades_df - DataFrame containing student grades
absence_df - DataFrame containing student absence
homework_df - DataFrame containing homework'''
def teacher_dashboard(subject):
    grades_df = load_grades()
    absence_df = load_absences()
    homework_df = load_homework()
    '''Add a new student to the system.'''
    def add_student():
        '''DataFrame containing user data'''
        users_df = load_users()

        student_id = simpledialog.askstring("Input", "Enter Student ID:")
        if not student_id or student_id in users_df["User"].values:
            messagebox.showerror("Error", "Invalid or duplicate Student ID.")
            return

        password = simpledialog.askstring("Input", "Enter Password for Student:")
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        '''Prompts the user to input the student's details'''
        name = simpledialog.askstring("Input", "Enter Student First Name:")
        surname = simpledialog.askstring("Input", "Enter Student Last Name:")

        '''dictionary with the new student's details'''
        new_student = {
            "User": student_id,
            "Password": password,
            "Role": "Student",
            "Name": name,
            "Surname": surname,
        }

        '''Adds the new student's data to the existing users_df DataFrame'''
        users_df = pd.concat([users_df, pd.DataFrame([new_student])])
        save_users(users_df)
        messagebox.showinfo("Success", f"Student {student_id} added successfully.")

    def delete_student():
        '''Handles the removal of a student from the system'''
        users_df = load_users()

        student_id = simpledialog.askstring("Input", "Enter Student ID to Delete:")
        if not student_id or student_id not in users_df["User"].values:
            messagebox.showerror("Error", "Student ID not found.")
            return

        if messagebox.askyesno("Confirm", f"Are you sure you want to delete Student {student_id}?"):
            users_df = users_df[users_df["User"] != student_id]
            save_users(users_df)
            messagebox.showinfo("Success", f"Student {student_id} deleted successfully.")

    '''Add a grade for a student'''
    def add_grade():
        student_name = simpledialog.askstring("Input", "Enter Student ID:")
        if not student_name:
            return

        try:
            grade = float(simpledialog.askstring("Input", f"Enter Grade for {subject} (0-10):"))
            if grade < 0 or grade > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid grade. Please enter a number between 0 and 10.")
            return

        nonlocal grades_df
        grades_df = pd.concat([grades_df, pd.DataFrame({"User": [student_name], "Subject": [subject], "Grade": [grade]})])
        save_grades(grades_df)
        messagebox.showinfo("Success", f"Grade for {student_name} in {subject} added successfully.")

    '''Displays the class average in a dialog box, formatted to 2 decimal places.'''
    def view_class_average():
        subject_grades = grades_df[grades_df["Subject"] == subject]
        if subject_grades.empty:
            messagebox.showinfo("Class Average", f"No data available for {subject}.")
            return
        avg = subject_grades["Grade"].mean()
        messagebox.showinfo("Class Average", f"The class average for {subject} is {avg:.2f}.")

    def view_low_performers():
        '''Shows students who are behind'''
        subject_grades = grades_df[grades_df["Subject"] == subject]
        if subject_grades.empty:
            messagebox.showinfo("Low Performers", f"No data available for {subject}.")
            return

        '''Get the grade threshold'''
        threshold = simpledialog.askfloat("Input", "Enter Grade Threshold:")
        if threshold is None:
            return

        '''Calculate mean grade for each student in the subject'''
        student_mean_grades = (
            subject_grades.groupby("User", as_index=False)
            .agg({"Grade": "mean"})
        )

        '''Filter for low performers (mean grade below threshold)'''
        low_performers = student_mean_grades[student_mean_grades["Grade"] < threshold]

        if low_performers.empty:
            messagebox.showinfo("Low Performers", f"No students scored below {threshold} in {subject}.")
            return

        '''A new window to display the table'''
        table_window = tk.Toplevel()
        table_window.title(f"Low Performers for {subject}")
        table_window.geometry("600x400")

        '''A Treeview widget'''
        tree = ttk.Treeview(table_window, columns=["Student ID", "Mean Grade"], show="headings")
        tree.heading("Student ID", text="Student ID")
        tree.heading("Mean Grade", text="Mean Grade")

        '''Populate the Treeview with data'''
        for _, row in low_performers.iterrows():
            tree.insert("", "end", values=(row["User"], row["Grade"]))

        '''A scrollbar to the Treeview'''
        scrollbar = tk.Scrollbar(table_window, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=5, pady=5)

        '''Pack the Treeview'''
        tree.pack(expand=True, fill="both", padx=10, pady=10)

    '''Creates a visualization of student grades for the given subject'''
    def visualize_subject_data():
        subject_grades = grades_df[grades_df["Subject"] == subject]
        if subject_grades.empty:
            messagebox.showinfo("Visualization", f"No data available for {subject}.")
            return
        subject_grades.groupby("User")["Grade"].mean().plot(kind="bar", title=f"Grades in {subject}")
        plt.ylabel("Grade")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    '''Track Attendance'''
    def add_absence():
        absence_df = load_absences()
        student_id = simpledialog.askstring("Input", "Enter Student ID:")
        if not student_id:
            return

        date = simpledialog.askstring("Input", "Enter Date (e.g., YYYY-MM-DD):")
        if not date:
            return

        status = simpledialog.askstring("Input", "Enter Status (Present/Absent):")
        if status not in ["Present", "Absent"]:
            messagebox.showerror("Error", "Status must be 'Present' or 'Absent'.")
            return

        new_entry = {"User": student_id, "Subject": subject, "Date": date, "Status": status}
        absence_df = pd.concat([absence_df, pd.DataFrame([new_entry])], ignore_index=True)
        save_absences(absence_df)
        messagebox.showinfo("Success", f"Attendance record for {student_id} added successfully.")

    '''Shows correlation between attendance and grades'''
    def analyze_student_grades_and_attendance():
        if grades_df.empty or absence_df.empty:
            messagebox.showinfo("Analysis", "Grades or absences data is not available.")
            return

        mean_grades = grades_df.groupby("User")["Grade"].mean().reset_index(name="Mean Grade")

        # Calculate the total absences for each student
        absences_summary = (
            absence_df[absence_df["Status"] == "Absent"]
            .groupby("User")
            .size()
            .reset_index(name="Total Absences")
        )

        merged_data = pd.merge(mean_grades, absences_summary, on="User", how="left")
        merged_data["Total Absences"] = merged_data["Total Absences"].fillna(0)  # Handle students with no absences

        plt.scatter(merged_data["Mean Grade"], merged_data["Total Absences"], alpha=0.6, edgecolor="k")
        plt.title("Correlation Between Mean Grades and Total Absences")
        plt.xlabel("Mean Grade")
        plt.ylabel("Total Absences")
        plt.show()

    '''View attendance for the subject'''
    def view_absences():
        absence_df = load_absences()
        subject_absences = absence_df[absence_df["Subject"] == subject]

        if subject_absences.empty:
            messagebox.showinfo("Attendance Records", f"No attendance records for {subject}.")
            return

        '''Create a pivot table with Student IDs as rows and Dates as columns'''
        table = subject_absences.pivot_table(index="User", columns="Date", values="Status", aggfunc=lambda x: x.iloc[0])

        table_window = tk.Toplevel()
        table_window.title(f"Attendance Records for {subject}")

        tree = ttk.Treeview(table_window, columns=["Student ID"] + list(table.columns), show="headings")

        tree.heading("Student ID", text="Student ID")
        for col in table.columns:
            tree.heading(col, text=col)

        for student_id, row in table.iterrows():
            values = [student_id] + row.tolist()
            tree.insert("", "end", values=values)

        scrollbar = tk.Scrollbar(table_window, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=5, pady=5)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

    def view_student_grades():
        """View all grades for a specific student in the teacher's subject in a table."""
        student_id = simpledialog.askstring("Input", "Enter Student ID:")
        if not student_id:
            return

        '''Filter grades for the specified student and subject'''
        student_grades = grades_df[(grades_df["User"] == student_id) & (grades_df["Subject"] == subject)]

        if student_grades.empty:
            messagebox.showinfo(
                "Student Grades",
                f"No grades found for student ID {student_id} in the subject '{subject}'."
            )
        else:
            '''Create a new window to display the table'''
            table_window = tk.Toplevel()
            table_window.title(f"Grades for Student ID {student_id} in {subject}")
            table_window.geometry("600x400")

            tree = ttk.Treeview(table_window, columns=["Grade"], show="headings")
            tree.heading("Grade", text="Grade")

            for _, row in student_grades.iterrows():
                tree.insert("", "end", values=(row["Grade"],))

            scrollbar = tk.Scrollbar(table_window, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y", padx=5, pady=5)

            tree.pack(expand=True, fill="both", padx=10, pady=10)

    def visualize_student_performance():
        '''Visualize the grades of a specific student in the teacher's subject'''
        student_id = simpledialog.askstring("Input", "Enter Student ID:")
        if not student_id:
            return

        '''Filter grades for the specific student and subject'''
        student_grades = grades_df[(grades_df["User"] == student_id) & (grades_df["Subject"] == subject)]

        if student_grades.empty:
            messagebox.showinfo("Visualization",f"No grades found for student ID {student_id} in the subject '{subject}'.")
        else:
            student_grades["Index"] = range(1, len(student_grades) + 1)
            student_grades.set_index("Index")["Grade"].plot(kind="bar",
                                                            title=f"Performance of {student_id} in {subject}")
            plt.ylabel("Grade")
            plt.xlabel("Assessment Number")
            plt.xticks(rotation=0)
            plt.tight_layout()
            plt.show()

    def add_homework():
        '''Allow teachers to add homework for their subject.'''
        homework_df = load_homework()
        homework_text = simpledialog.askstring("Input", "Enter Homework Details:")
        if not homework_text:
            return

        due_date = simpledialog.askstring("Input", "Enter Due Date (e.g., DD-MM-YYYY):")
        if not due_date:
            return

        homework_df = pd.concat(
            [homework_df, pd.DataFrame({"Subject": [subject], "Homework": [homework_text], "DueDate": [due_date]})])
        save_homework(homework_df)
        messagebox.showinfo("Success", "Homework added successfully.")

    def view_homework():
        '''Filter homework for the specified subject'''
        subject_homework = homework_df[homework_df["Subject"] == subject]
        if subject_homework.empty:
            messagebox.showinfo("Homework", f"No homework assigned for {subject}.")
            return

        table_window = tk.Toplevel()
        table_window.title(f"Homework for {subject}")
        table_window.geometry("600x400")

        tree = ttk.Treeview(table_window, columns=["Due Date", "Homework"], show="headings")
        tree.heading("Due Date", text="Due Date")
        tree.heading("Homework", text="Homework")

        for _, row in subject_homework.iterrows():
            tree.insert("", "end", values=(row["DueDate"], row["Homework"]))

        scrollbar = tk.Scrollbar(table_window, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=5, pady=5)

        tree.pack(expand=True, fill="both", padx=10, pady=10)

    def delete_homework():
        '''Allow teachers to delete homework for their subject.'''
        homework_df = load_homework()
        subject_homework = homework_df[homework_df["Subject"] == subject]
        if subject_homework.empty:
            messagebox.showinfo("Delete Homework", f"No homework assigned for {subject}.")
            return

        homework_list = [f"{i}: Due {row['DueDate']} - {row['Homework']}" for i, row in subject_homework.iterrows()]
        homework_str = "\n".join(homework_list)

        try:
            to_delete = simpledialog.askinteger(
                "Delete Homework",
                f"Select homework to delete (Enter the index):\n\n{homework_str}"
            )
            if to_delete is None:
                return

            if to_delete < 0 or to_delete >= len(subject_homework):
                raise ValueError

        except ValueError:
            messagebox.showerror("Error", "Invalid selection.")
            return

        homework_df = homework_df.drop(subject_homework.index[to_delete])
        save_homework(homework_df)
        messagebox.showinfo("Success", "Homework deleted successfully.")


    '''Teacher Dashboard GUI'''
    dashboard = tk.Tk()
    dashboard.title(f"{subject} - Teacher Dashboard")
    dashboard.geometry("600x400")

    '''Apply consistent styling'''
    style = ttk.Style()
    style.configure("TButton", font=("Adobe Caslon Pro Bold", 20), padding=10)

    '''Frame with Scrollbar'''
    main_frame = tk.Frame(dashboard)
    main_frame.pack(fill=tk.BOTH, expand=True)

    '''Allows scrolling and drawing complex layouts'''
    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    '''Creates a vertical scrollbar. Vertical view'''
    scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    '''Connects the canvas's scrolling behavior to the scrollbar, ensuring the scrollbar updates as the canvas scrolls.'''
    canvas.configure(yscrollcommand=scrollbar.set)
    '''Adjusts the scrollable region of the canvas dynamically'''
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    '''Secondary frame that will hold all the widgets and content'''
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    '''Buttons'''
    buttons = [
        ("Add Grade", add_grade),
        ("View Class Average", view_class_average),
        ("View Low Performers", view_low_performers),
        ("Visualize Grades", visualize_subject_data),
        ("View Student Grades", view_student_grades),
        ("Visualize Student Performance", visualize_student_performance),
        ("Attendance", add_absence),
        ("View Attendance", view_absences),
        ("Add Homework", add_homework),
        ("View Homework", view_homework),
        ("Delete Homework", delete_homework),
        ("Visualize Correlation", analyze_student_grades_and_attendance),
        ("Add Student", add_student),
        ("Delete Student", delete_student),
    ]

    for index, (text, command) in enumerate(buttons):
        ttk.Button(content_frame, text=text, command=command).grid(row=index, column=0, pady=10, padx=170, sticky="ew")

    dashboard.mainloop()