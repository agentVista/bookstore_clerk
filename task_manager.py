# ======importing libraries===========
import time
import os
import datetime

# Check if user.txt exists, create it if not
if not os.path.exists('user.txt'):
    with open('user.txt', 'w') as f:
        f.write("admin, adm1n")

# Check if tasks.txt exists, create it if not
if not os.path.exists('tasks.txt'):
    with open('tasks.txt', 'w') as f:
        f.write("")  # Create empty file

# ====Login Section====
# This function is for the log in process
# Ask for user input
user = {}
with open('user.txt', 'r') as f:
    for line in f:
        segments = line.strip().split(', ')
        user[segments[0]] = segments[1]

# Check if the input is correct
# If the user is not in the file, it will ask for the input again

# When the user has not logged in 
user_logged = False
while not user_logged:
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # If user is logged in
    if username in user and user[username] == password:
        user_logged = True
        present = username
        print(f"Hi, {username} you are logged in successfully")
    else:
        print("Incorrect login details, please try again")

# ====Main Menu Section====
# This function is for the main menu
while True:
    # Display the main menu options for the user
    # This is the admins menu 
    if present == 'admin':
        menu = input('''Select one of the following options:
r - register a user
a - add a task
va - view all tasks
vm - view my tasks
ds - display statistics
e - exit                                                                                        
:   ''').lower()
    else:
        # This is the users menu
        menu = input('''Select one of the following options:
a - add a task
va - view all tasks
vm - view my tasks
e - exit
:   ''').lower()

    # If admin selects the register option
    if menu == 'r':
        if present != 'admin':
            print("Only admins are authorized to register users.")
            continue
        
        # Prompts for the user to register a new user
        new_user = input("Enter the new user's username: ")
        new_password = input("Enter the new user's password: ")
        confirmed_access_code = input("Confirm the new user's password: ")

        # Check if the information is valid
        # If the user already exists
        if new_user in user:
            print("Username already exists. Please try a different username.")
        # Confirm the password
        elif new_password != confirmed_access_code:
            print("Passwords do not match. Please try again.")
        else:
            # If the user is new, add the user to the file
            # Make changes to our dictionary
            with open('user.txt', 'a') as f:
                f.write(f"\n{new_user}, {new_password}")
            user[new_user] = new_password    
            print(f"User {new_user} registered successfully.")

    elif menu == 'a':
        registered_user = input("Enter the username of the user to assign the task to: ")
        # Check if the user is registered
        if registered_user not in user:
            print("User not found.")
            continue
        
        task_type = input("Enter task title: ")
        task_description = input("Enter task description: ")
        
        # Date validation
        while True:
            task_deadline = input("Enter task due date (e.g. 10 Sep 2003): ")
            try:
                # Validate date format
                datetime.datetime.strptime(task_deadline, '%d %b %Y')
                break
            except ValueError:
                print("Invalid date format. Please use format like '10 Sep 2003'")
        
        # Get current date in correct format
        date_today = time.strftime("%d %b %Y")
        
        # Write the task to the file with proper formatting
        task_data = f"{registered_user}, {task_type}, {task_description}, {date_today}, {task_deadline}, No"
        
        # Check if file is empty to determine if we need a newline
        if os.path.getsize('tasks.txt') > 0:
            task_data = "\n" + task_data
            
        with open('tasks.txt', 'a') as f:
            f.write(task_data)

        print(f"Task successfully added for {registered_user}.")

    # If user chooses va 
    elif menu == 'va':
        try:
            with open('tasks.txt', 'r') as f:
                print("\nAll tasks:")
                for line in f:
                    if line.strip():
                        sectors = line.strip().split(', ')
                        # Calculate days remaining for due date
                        try:
                            due_date = datetime.datetime.strptime(sectors[4], '%d %b %Y')
                            today = datetime.datetime.now()
                            days_remaining = (due_date - today).days
                            if days_remaining < 0:
                                status = f"OVERDUE by {abs(days_remaining)} days"
                            else:
                                status = f"{days_remaining} days remaining"
                        except:
                            status = "Invalid date format"
                        
                        # Display all task information in proper format
                        print(f"""
Task:           {sectors[1]}
Assigned to:    {sectors[0]}
Date assigned:  {sectors[3]}
Due date:       {sectors[4]} ({status})
Completed:      {sectors[5]}
Description:    {sectors[2]}
-------------------------""")
        except FileNotFoundError:
            print("No tasks found. Please add tasks first.")

    # If user chooses vm
    elif menu == 'vm':
        try:
            with open('tasks.txt', 'r') as f:
                print(f"\nMy tasks for {present}:")
                for line in f:
                    if line.strip():
                        sectors = line.strip().split(', ')
                        if sectors[0] == present:
                            # Calculate days remaining for due date
                            try:
                                due_date = datetime.datetime.strptime(sectors[4], '%d %b %Y')
                                today = datetime.datetime.now()
                                days_remaining = (due_date - today).days
                                if days_remaining < 0:
                                    status = f"OVERDUE by {abs(days_remaining)} days"
                                else:
                                    status = f"{days_remaining} days remaining"
                            except:
                                status = "Invalid date format"
                            
                            # Display all task information in proper format
                            print(f"""
Task:           {sectors[1]}
Date assigned:  {sectors[3]}
Due date:       {sectors[4]} ({status})
Completed:      {sectors[5]}
Description:    {sectors[2]}
-------------------------""")
        except FileNotFoundError:
            print("No tasks found. Please add tasks first.")

    # If admin chooses ds (display statistics)
    elif menu == 'ds' and present == 'admin':
        try:
            # Count number of users
            with open('user.txt', 'r') as f:
                user_count = sum(1 for line in f)
            
            # Count number of tasks
            with open('tasks.txt', 'r') as f:
                task_count = sum(1 for line in f if line.strip())
                
            print(f"\nStatistics:")
            print(f"Total number of users: {user_count}")
            print(f"Total number of tasks: {task_count}")
        except FileNotFoundError:
            print("Error accessing data files.")

    # If user chooses e
    elif menu == 'e':
        print("Exiting the task manager. Goodbye!")
        exit()

    # Check if option is valid
    else:
        print("Invalid option. Please try again.")