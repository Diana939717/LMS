# LMS

## Functions

### `load_users()`
Loads user data from a CSV file into a pandas DataFrame.
The loaded DataFrame containing user information.

### `save_users(users_df)`
Saves a given DataFrame (`users_df`) to the CSV file. 
The `index=False` parameter prevents saving the row index as a separate column.

### `load_grades()`
Tries to load grade data from a CSV file. 
An empty DataFrame with columns "User", "Subject", and "Grade" if the file doesn't exist.

### `save_grades(grades_df)`
Saves the `grades_df` DataFrame to a CSV file.

### `load_homework()`
Tries to load homework data from a CSV file.
An empty DataFrame with columns "Subject", "Homework", and "DueDate" if the file doesn't exist.

### save_homework(homework_df)
 Saves the `homework_df` DataFrame to a CSV file.

### load_absences()
Tries to load attendance data from a CSV file. 
An empty DataFrame with columns "User", "Subject", "Date", and "Status" if the file doesn't exist.

### save_absences(absence_df)
Saves the `absence_df` DataFrame to a CSV file.

### authenticate_user(username, password, user_data)
Verifies if a user’s username and password are correct. 
If authentication is successful, it determines and returns the user's role and subject. 
If authentication fails, it returns `None, None`.

### Main Function: teacher_dashboard(subject)
This serves as the central hub for teacher-specific operations in a school management system. 
It takes a subject as input and allows the teacher to perform various tasks related to grades, absences, and homework for that subject.
### add_student()
Adds a new student to the system.
Steps
Collects details such as student ID, password, first name, and last name.
Validates the input to ensure the student ID is unique.
Updates the users' database with the new student's details.
### delete_student()
Removes a student from the system.
Steps
Prompts the teacher for a student ID.
Confirms the deletion action.
Removes the student from the users' database.
### add_grade()
Records a grade for a specific student in the subject.
Steps:
Prompts for the student ID and the grade.
Validates the grade to ensure it's between 0 and 10.
Updates the grades database with the new entry.
### view_class_average()
Displays the class average for the subject.
Steps:
Filters grades for the subject.
Calculates and displays the average grade.
### view_low_performers()
Identifies students performing below a certain grade threshold in the subject.
Steps:
Filters grades for the subject.
Asks for a grade threshold.
Displays students with an average grade below the threshold in a table.
### visualize_subject_data()
Creates a bar chart showing the average grades of students in the subject.
Steps:
Groups grades by student.
Plots a bar chart for visual analysis.
### add_absence()
Records a student's attendance status for a specific date.
Steps:
Prompts for student ID, date, and attendance status (Present/Absent).
Updates the absences database.
### analyze_student_grades_and_attendance()
Examines the relationship between grades and attendance.
Steps:
Merges average grades with total absences for each student.
Plots a scatter plot to visualize the correlation.
### view_absences()
Displays attendance records for the subject.
Steps:
Creates a pivot table with student IDs and their attendance status.
Displays the table in a new window.
### view_student_grades()
Displays all grades for a specific student in the subject.
Steps:
Filters grades by student ID and subject.
Displays the grades in a table format.
### visualize_student_performance()
Visualizes the grade trend of a specific student in the subject.
Steps:
Filters grades for the student and subject.
Plots a bar chart showing the student's performance over time.
### add_homework()
Allows the teacher to assign homework for the subject.
Steps:
Prompts for homework details and a due date.
Updates the homework database with the new assignment.
### view_homework()
Displays all assigned homework for the subject.
Steps:
Filters homework for the subject.
Displays it in a table format.
### delete_homework()
Enables the teacher to remove an assigned homework.
Steps:
Lists all homework for the subject.
Prompts for the homework to delete based on its index.
Removes the selected homework from the database

### Main Function: def student_dashboard(username):
This function initializes the student dashboard for a specific user, identified by their username. 
It loads necessary data files, validates the user's role, and provides options for the student to view grades, visualize grades, and view homework.
### view_grades()
Allows the logged-in student to view their grades for all subjects.
Filters the grades dataset for entries matching the student's username.
If no grades are found, it displays a message.
Otherwise, opens a new window displaying grades in a table format with subjects and corresponding grades.
### visualize_grades()
Provides a visual representation of the student's grades across subjects.
Filters the grades dataset for the logged-in student.
If no grades are available, it displays a message.
Otherwise, creates a bar chart showing grades for each subject, labeled and styled for readability.
### view_homework()
Displays all homework assignments relevant to the student's enrolled subjects.
Identifies the subjects the student is enrolled in from the grades dataset.
Filters the homework dataset to find assignments matching these subjects.
If no homework is found, it displays a message.
Otherwise, opens a new window with a table of homework assignments, showing subject, due date, and homework details.

### Main Function: parent_dashboard(parent_id):
This is the main function that generates the parent dashboard. 
It first loads the data for grades, absences, and users from external sources. 
It then checks if the given parent_id corresponds to a valid parent. 
If valid, it fetches the child’s details linked to the parent and provides access to several options for viewing the child’s data (grades, absences).
### view_grades():
This function allows parents to view their child’s grades. 
It retrieves the child’s grades from the grades_df data frame and displays them in a pop-up window using a table format (using Treeview from Tkinter). 
If no grades are found, it shows a message indicating that no grades are available for that child.
### visualize_grades():
This function visualizes the child’s grades across different subjects in a bar chart. 
It uses the matplotlib library to plot the grades and displays the chart in a new window. 
If no grades are available, a message is shown indicating that.
### view_absences():
This function displays the child’s absences in a separate pop-up window. 
It retrieves data about absences from the absences_df data frame and presents it in a table format, showing subjects, dates, and statuses of absences. 
If no absences are found, a message is shown, and the window is closed.
### Dashboard GUI:
The main GUI for the parent dashboard is created with Tkinter. 
A new window (dashboard) is opened, containing a header with the parent’s name and the child’s name. 
Below the header, there are buttons for each of the functions: "View Grades," "Visualize Grades," and "View Absences." 
These buttons allow parents to interact with the dashboard and view their child’s academic data in different ways.

### Debugging Example

In `main.py`, the `load_users()` function is called to load user data from the file `user.csv` into a pandas DataFrame:

```python
user_data = load_users()
if user_data.empty:
    print("User data is empty or could not be loaded. Check the CSV path.")
else:
    print(user_data.head())
```


