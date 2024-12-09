import pandas as pd

'''Loads user data from a CSV file into a pandas DataFrame. Returns the loaded DataFrame'''
def load_users():
    return pd.read_csv("/Users/dianayan/PycharmProjects/Final Project/Datasets for LMS/user.csv")

'''Saves a given DataFrame (users_df) to the CSV file. index=False prevents saving the row index as a separate column'''
def save_users(users_df):
    """Save user data to CSV file."""
    users_df.to_csv("/Users/dianayan/PycharmProjects/Final Project/Datasets for LMS/user.csv", index=False)

'''Tries to load grade data from a CSV file. If the file doesn't exist, returns an empty DataFrame.'''
def load_grades():
    try:
        return pd.read_csv("/Users/dianayan/PycharmProjects/Final Project/Datasets for LMS/grades.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["User", "Subject", "Grade"])

'''Saves the grades_df DataFrame to a CSV file.'''
def save_grades(grades_df):
    grades_df.to_csv("/Users/dianayan/PycharmProjects/Final Project/Datasets for LMS/grades.csv", index=False)

'''Tries to load homework data from a CSV file'''
def load_homework():
    try:
        return pd.read_csv("/Users/dianayan/PycharmProjects/Final Project/Datasets for LMS/homework.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Subject", "Homework", "DueDate"])


'''Saves the homework_df DataFrame to a CSV file.'''
def save_homework(homework_df):
    homework_df.to_csv("/Users/dianayan/PycharmProjects/Final Project/Datasets for LMS/homework.csv", index=False)

'''Tries to load attendance data from a CSV file.'''
def load_absences():
    try:
        return pd.read_csv("/Users/dianayan/PycharmProjects/Final Project/Datasets for LMS/absences.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["User", "Subject", "Date", "Status"])

'''Saves the absence_df DataFrame to a CSV file.'''
def save_absences(absence_df):
    absence_df.to_csv("/Users/dianayan/PycharmProjects/Final Project/Datasets for LMS/absence.csv", index=False)

'''Debugging in main.py. 
Calls the load_users() function to load user data from the file user.csv into a pandas DataFrame'''
user_data = load_users()
if user_data.empty:
    print("User data is empty or could not be loaded. Check the CSV path.")
else:
    print(user_data.head())
