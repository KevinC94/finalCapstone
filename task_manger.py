import os
from datetime import datetime, date

# Define the date and time format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to load tasks from tasks.txt
def load_tasks():
    # Create tasks.txt file if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as task_file:
            pass

    # Read task data from tasks.txt
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    # Parse task data and create a list of tasks
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        
        # Try to parse the due date, handle errors gracefully
        try:
            curr_t['due_date'] = datetime.strptime(task_components[3].split()[0], DATETIME_STRING_FORMAT)
        except ValueError:
            print(f"Error parsing due date: {task_components[3]}")
            continue
        
        # Try to parse the assigned date, handle errors gracefully
        try:
            curr_t['assigned_date'] = datetime.strptime(task_components[4].split()[0], DATETIME_STRING_FORMAT)
        except ValueError:
            print(f"Error parsing assigned date: {task_components[4]}")
            continue
        
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)
    
    return task_list

# Function to load users from user.txt
def load_users():
    # Create user.txt file if it doesn't exist
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as user_file:
            user_file.write("admin;password")

    # Read user data from user.txt
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    # Parse user data and create a dictionary of usernames and passwords
    for user in user_data:
        user_info = user.split(';')
        if len(user_info) == 2:
            username_password[user_info[0]] = user_info[1]

    return username_password

# Function to register a new user
def reg_user():
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check if passwords match and username doesn't exist, then add new user
    if new_password == confirm_password:
        if new_username not in username_password:
            username_password[new_username] = new_password
            with open("user.txt", "a") as user_file:
                user_file.write(f"\n{new_username};{new_password}")
            print("New user added.")
        else:
            print("Username already exists. Please choose a different username.")
    else:
        print("Passwords do not match.")

# Function to add a new task
def add_task():
    task_username = input("Username of the person assigned to the task: ")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    task_due_date = input("Due date of task (YYYY-MM-DD): ")
    task_assigned_date = datetime.now().strftime(DATETIME_STRING_FORMAT)

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": datetime.strptime(task_due_date, DATETIME_STRING_FORMAT),  # Convert to datetime object
        "assigned_date": task_assigned_date,
        "completed": False
    }

    task_list.append(new_task)
    update_task_file()
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    if not task_list:
        print("No tasks available.")
        return

    print("All Tasks:")
    for index, task in enumerate(task_list):
        print(f"{index + 1}. {task['title']} - Assigned to: {task['username']}")

# Function to view tasks assigned to the current user
def view_mine():
    task_number = 1
    task_indices = []

    print("Your Tasks:")
    for index, task in enumerate(task_list):
        if task['username'] == curr_user:
            task_indices.append(index)
            print(f"{task_number}. {task['title']}")
            task_number += 1

    if not task_indices:
        print("No tasks have been assigned to you.")
        return

    while True:
        choice = input("Enter the task number to select a task, or '-1' to return to exit to the menu: ")
        if choice == '-1':
            return
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(task_indices):
                selected_task_index = task_indices[choice - 1]
                selected_task = task_list[selected_task_index]
                print_task(selected_task)

                edit_or_mark_complete(selected_task_index)
                return
            else:
                print("Invalid task number. Please try again.")
        else:
            print("Please enter a number.")

# Function to display task details
def print_task(task):
    print("Task Details:")
    print(f"Title: {task['title']}")
    print(f"Description: {task['description']}")
    print(f"Assigned Date: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
    print(f"Completed: {'Yes' if task['completed'] else 'No'}")

# Function to edit or mark task as complete
def edit_or_mark_complete(task_index):
    selected_task = task_list[task_index]
    if selected_task['completed']:
        print("The selected task has been markered as completed.")
        return

    action = input("Choose an action for this task:\n1. Mark as Complete\n2. Edit\nEnter choice (1/2): ")

    if action == '1':
        selected_task['completed'] = True
        update_task_file()
        print("Task marked as complete.")
    elif action == '2':
        new_username = input("Enter new username for the task (press Enter to keep current username): ").strip()
        new_due_date = input("Enter new due date for the task (YYYY-MM-DD) (press Enter to keep current due date): ").strip()

        if new_username:
            selected_task['username'] = new_username
        if new_due_date:
            selected_task['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)  # Convert to datetime object

        update_task_file()
        print("Task has been updated.")
    else:
        print("Task has not been updated")

# Function to update tasks in tasks.txt
def update_task_file():
    with open("tasks.txt", "w") as task_file:
        for t in task_list:
            # Convert assigned_date to string if it's not already a string
            if isinstance(t['assigned_date'], str):
                assigned_date_str = t['assigned_date']
            else:
                assigned_date_str = t['assigned_date'].strftime(DATETIME_STRING_FORMAT)
                
            # Write the task information to the file
            task_file.write(f"{t['username']};{t['title']};{t['description']};{t['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                            f"{assigned_date_str};{'Yes' if t['completed'] else 'No'}\n")


# Function to generate task overview report
def generate_task_overview():
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    
    # Convert due_date to date object for comparison
    today_date = date.today()
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'].date() < today_date)
    
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    with open("task_overview.txt", "w") as report_file:
        report_file.write(f"Total Number of Tasks: {total_tasks}\n")
        report_file.write(f"Total Number of Completed Tasks: {completed_tasks}\n")
        report_file.write(f"Total Number of Uncompleted Tasks: {uncompleted_tasks}\n")
        report_file.write(f"Total Number of Overdue Tasks: {overdue_tasks}\n")
        report_file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage}%\n")
        report_file.write(f"Percentage of Overdue Tasks: {overdue_percentage}%\n")


# Function to generate user overview report
def generate_user_overview():
    total_users = len(username_password)
    total_tasks = len(task_list)

    with open("user_overview.txt", "w") as report_file:
        report_file.write(f"Total Number of Users: {total_users}\n")
        report_file.write(f"Total Number of Tasks: {total_tasks}\n")

        for username, password in username_password.items():
                user_tasks = [t for t in task_list if t['username'] == username]
                total_user_tasks = len(user_tasks)
                completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
                uncompleted_user_tasks = total_user_tasks - completed_user_tasks
                overdue_user_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'].date() < date.today())
                user_task_percentage = (total_user_tasks / total_tasks) * 100 if total_tasks > 0 else 0
                completed_percentage = (completed_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0
                uncompleted_percentage = ((total_user_tasks - completed_user_tasks) / total_user_tasks) * 100 if total_user_tasks > 0 else 0
                overdue_percentage = (overdue_user_tasks / total_user_tasks) * 100 if total_user_tasks > 0 else 0

                report_file.write(f"\nUsername: {username}\n")
                report_file.write(f"Total Number of Tasks Assigned: {total_user_tasks}\n")
                report_file.write(f"Percentage of Total Tasks Assigned: {user_task_percentage}%\n")
                report_file.write(f"Percentage of Completed Tasks: {completed_percentage}%\n")
                report_file.write(f"Percentage of Uncompleted Tasks: {uncompleted_percentage}%\n")
                report_file.write(f"Percentage of Overdue Tasks: {overdue_percentage}%\n")

# Start of the program
username_password = load_users()
task_list = load_tasks()

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
    elif username_password[curr_user] != curr_pass:
        print("Invalid password")
    else:
        print("You have been Log in")
        logged_in = True

while True:
    print()
    # if user is admin displays menu options
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
ds - Display Statics
e - Exit
: ''').lower()
    else:
        # if user is not admin, only displays menu options that are available to them
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'ds':
        generate_task_overview()
        generate_user_overview()
        print("Reports generated.")
    elif menu == 'e':
        print('You have successfully logged out')
        break
    else:
        print("invalid entry, Please Try again")


