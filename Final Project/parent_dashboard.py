import tkinter as tk
from tkinter import ttk, messagebox
from data_operations import load_grades, load_users, load_absences
import matplotlib.pyplot as plt

"""Display the parent dashboard."""
def parent_dashboard(parent_id):
    grades_df = load_grades()
    absences_df = load_absences()
    user_data = load_users()
    '''Gets parent and child details'''
    parent_data = user_data[user_data["User"] == parent_id]
    if parent_data.empty or parent_data["Role"].iloc[0] != "Parent":
        messagebox.showerror("Access Denied", "Only parents can access this dashboard.")
        return

    child_id = parent_data["Child"].iloc[0]
    child_data = user_data[user_data["User"] == child_id]

    if child_data.empty:
        messagebox.showerror("Error", "No child data associated with this parent.")
        return

    child_name = f"{child_data['Name'].iloc[0]} {child_data['Surname'].iloc[0]}"

    def view_grades():
        """View grades for the parent's child."""
        child_grades = grades_df[grades_df["User"] == child_id]
        if child_grades.empty:
            messagebox.showinfo("Grades", f"No grades available for {child_name}.")
        else:
            table_window = tk.Toplevel()
            table_window.title(f"Grades for Student ID {child_name}")
            table_window.geometry("600x400")

            tree = ttk.Treeview(table_window, columns=["Subject", "Grade"], show="headings")
            tree.heading("Subject", text="Subject")
            tree.heading("Grade", text="Grade")

            for _, row in child_grades.iterrows():
                tree.insert("", "end", values=(row["Subject"], row["Grade"]))

            scrollbar = tk.Scrollbar(table_window, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y", padx=5, pady=5)

            tree.pack(expand=True, fill="both", padx=10, pady=10)

    def visualize_grades():
        """Visualize grades of the parent's child across subjects."""
        child_grades = grades_df[grades_df["User"] == child_id]
        if child_grades.empty:
            messagebox.showinfo("Visualization", f"No grades available to visualize for {child_name}.")
        else:
            child_grades.set_index("Subject")["Grade"].plot(kind="bar", title=f"{child_name}'s Grades")
            plt.ylabel("Grade")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    """View the number of absences, the dates of the absences, and the subject with their status in a table."""
    def view_absences():
        '''Filter absences for the child by User ID'''
        child_absences = absences_df[absences_df["User"] == child_id]

        '''A new window to show the absences'''
        absence_window = tk.Toplevel()
        absence_window.title(f"Absences for {child_name}")
        absence_window.geometry("600x400")

        if child_absences.empty:
            messagebox.showinfo("Absences", f"No absences recorded for {child_name}.")
            absence_window.destroy()  # Close the window if no absences
        else:
            tree = ttk.Treeview(absence_window, columns=("Subject", "Date", "Status"), show="headings")
            tree.heading("Subject", text="Subject")
            tree.heading("Date", text="Date")
            tree.heading("Status", text="Status")

            for _, row in child_absences.iterrows():
                tree.insert("", "end", values=(row["Subject"], row["Date"], row["Status"]))

            tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            scrollbar = ttk.Scrollbar(absence_window, orient="vertical", command=tree.yview)
            scrollbar.pack(side="right", fill="y")
            tree.configure(yscrollcommand=scrollbar.set)

    # Parent Dashboard GUI using standard tkinter
    dashboard = tk.Toplevel()
    dashboard.title("Parent Dashboard")
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

    '''Header labels'''
    header_label = tk.Label(content_frame,
                            text=f"Welcome, {parent_data['Name'].iloc[0]} {parent_data['Surname'].iloc[0]}",
                            font=("Arial", 16))
    header_label.grid(row=0, column=0, pady=10)
    child_label = tk.Label(content_frame, text=f"Viewing data for: {child_name}", font=("Arial", 14))
    child_label.grid(row=1, column=0, pady=10)

    '''Buttons'''
    buttons = [
        ("View Grades", view_grades),
        ("Visualize Grades", visualize_grades),
        ("View Absences", view_absences),  # Add the button to view absences
    ]

    for index, (text, command) in enumerate(buttons):
        ttk.Button(content_frame, text=text, command=command).grid(row=index + 2, column=0, pady=10, padx=220,
                                                                   sticky="ew")

    dashboard.mainloop()
