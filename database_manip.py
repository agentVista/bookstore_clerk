import sqlite3
import os

# Get valid integer input from user
# This function repeatedly prompts the user until a valid integer is entered.
# It can also enforce optional minimum and maximum value constraints.

def get_valid_int_input(prompt, min_val=None, max_val=None):
    """
    # Prompt user 
    # Args:
    #   prompt (str): Message to display to user
    #   min_val (int): Optional minimum acceptable value
    #   max_val (int): Optional maximum acceptable value
    # Returns:
    #   int: Validated integer input from user
    """
    # Start input loop
    while True:
        try:
            value = int(input(prompt))

            # Check for minimum value constraint
            if min_val is not None and value < min_val:
                print(f"Error: Value must be at least {min_val}")
                continue

            # Check for maximum value constraint
            if max_val is not None and value > max_val:
                print(f"Error: Value must be at most {max_val}")
                continue
            return value
        except ValueError:

            # Handle invalid input
            print("Error: Please enter a correct value")

# Get string input with validation
def get_valid_string_input(prompt, min_length=1):
    """
    # Get validation from user
    # Args:
    #   prompt (str): Message to display to user
    #   min_length (int): Minimum required string length
    # Returns:
    #   str: Validated string input from user
    """

    # Get user input
    while True:
        value = input(prompt).strip()
        if len(value) >= min_length:
            return value
        print(f"Error: Input must be at least {min_length} character(s)")

        # Input is invalid, prompt again

# Database connection
def db_connect(db_file):
    """Initialize database connection"""
    try:
        conn = sqlite3.connect(db_file)
        print(f"DB connection established: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Connection error: {e}")
        return None

# Table initialization
def table_init(conn):
    """Initialize database table schema"""
    schema_sql = """
    CREATE TABLE IF NOT EXISTS python_programming (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        grade INTEGER NOT NULL
    );
    """
    # Create the table
    try:
        cursor = conn.cursor()
        cursor.execute(schema_sql)
        conn.commit()
        print("Table schema initialized.")
        return True
    except sqlite3.Error as e:
        print(f"Schema initialization error: {e}")
        return False

#  Student data
def data_insert(conn, students):
    """ insert student data"""
    insert_sql = """
    INSERT INTO python_programming (id, name, grade)
    VALUES (?, ?, ?)
    """
    # Validate and prepare data
    try:
        cursor = conn.cursor()
        cursor.executemany(insert_sql, students)
        conn.commit()
        print(f"Data added: {len(students)} records")
        return True
    except sqlite3.Error as e:
        print(f" operation error: {e}")
        return False

# Range query
def range_query(conn, min_val, max_val):
    """ range-based query"""
    query_sql = """
    SELECT id, name, grade 
    FROM python_programming 
    WHERE grade BETWEEN ? AND ?
    ORDER BY grade DESC
    """
    # Start the query
    try:
        cursor = conn.cursor()
        cursor.execute(query_sql, (min_val, max_val))
        results = cursor.fetchall()
        
        print(f"Records in range {min_val}-{max_val}:")
        for row in results:
            print(f"ID: {row[0]}, Name: {row[1]}, Grade: {row[2]}")
        
        return results
    except sqlite3.Error as e:
        print(f"Query error: {e}")
        return []

def grade_update(conn):
    """Update specific student grade with input validation"""

    # Get student name with validation
    student_name = get_valid_string_input("Enter student name to update: ", 2)
    
    # Get new grade with validation 
    new_grade = get_valid_int_input("Enter new grade (0-100): ", 0, 100)
    
    update_sql = """
    UPDATE python_programming 
    SET grade = ? 
    WHERE name = ?
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(update_sql, (new_grade, student_name))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Grade updated: {student_name} = {new_grade}")
            return True
        
        # error if we can not find the username
        else:
            print(f" {student_name} not found")
            return False
    except sqlite3.Error as e:
        print(f"Update operation error: {e}")
        return False


# Delete a student record
def record_delete(conn):
    """Delete student record with confirmation"""

    # Get student name with validation
    student_name = get_valid_string_input("Enter student name to delete: ", 2)
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete {student_name}? (y/n): ").lower()
    if confirm != 'y':
        print("Deletion cancelled")
        return False
    
    delete_sql = """
    DELETE FROM python_programming 
    WHERE name = ?
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(delete_sql, (student_name,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Record deleted: {student_name}")
            return True
        else:
            print(f"Deletion failed: {student_name} not found")
            return False
    except sqlite3.Error as e:
        print(f"Delete operation error: {e}")
        return False

def bulk_grade_update(conn):
    """Bulk update grades based on ID with input validation"""
    # Get ID threshold with validation
    id_limit = get_valid_int_input("Enter ID threshold: ", 0)
    
    # Get new grade with validation (0-100 range)
    grade_value = get_valid_int_input("Enter new grade value (0-100): ", 0, 100)
    
    update_sql = """
    UPDATE python_programming 
    SET grade = ? 
    WHERE id > ?
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(update_sql, (grade_value, id_limit))
        conn.commit()
        
        print(f"Bulk update complete: {cursor.rowcount} records modified")
        return True
    except sqlite3.Error as e:
        print(f"Bulk update error: {e}")
        return False

# Display all student records
def display_records(conn):
    """Display all database records"""
    query_sql = "SELECT id, name, grade FROM python_programming ORDER BY id"
    
    try:
        cursor = conn.cursor()
        cursor.execute(query_sql)
        records = cursor.fetchall()
        
        print("Database records:")
        for record in records:
            print(f"ID: {record[0]}, Name: {record[1]}, Grade: {record[2]}")
        print(f"Total records found: {len(records)}")
        return records

    # No records found
    except sqlite3.Error as e:
        print(f"Display operation error: {e}")
        return []

# menu for database operations
def interactive_menu(conn):
    """menu for database operations"""
    while True:
        print("\n--- Database Operations Menu ---")
        print("1. Display all records")
        print("2. Search students by grade range")
        print("3. Change a student's grade")
        print("4. Remove a student record")
        print("5. Update grades by ID threshold")
        print("6. Exit")

        # Get user choice
        choice = get_valid_int_input("Select an option (1-6): ", 1, 6)
        

        
        if choice == 1:
            display_records(conn)
        elif choice == 2:
            min_grade = get_valid_int_input("Enter minimum grade: ", 0, 100)
            max_grade = get_valid_int_input("Enter maximum grade: ", 0, 100)
            range_query(conn, min_grade, max_grade)
        elif choice == 3:
            grade_update(conn)
        elif choice == 4:
            record_delete(conn)
        elif choice == 5:
            bulk_grade_update(conn)
        elif choice == 6:
            print("Exiting program")
            break


# Database workflow
def execute_workflow():
    """Execute database workflow"""
    db_file = "student_db.db"

    # Remove existing database file if it exists
    if os.path.exists(db_file):
        os.remove(db_file)
        print("Existing database removed.")

    # Create a new database connection
    conn = db_connect(db_file)
    if conn is None:
        return
    
    try:
        if not table_init(conn):
            return
        
        student_data = [
            (55, 'Carl Davis', 61),
            (66, 'Dennis Fredrickson', 88),
            (77, 'Jane Richards', 78),
            (12, 'Peyton Sawyer', 45),
            (2, 'Lucas Brooke', 99)
        ]

        # Add initial data
        if not data_insert(conn, student_data):
            return

        # Start menu
        interactive_menu(conn)
        
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# Entry point for the program
if __name__ == "__main__":
    execute_workflow()