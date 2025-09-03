# Import necessary libraries
import sqlite3
import os

# Define the BookstoreDB class
class BookstoreDB:
    def __init__(self, db_name='ebookstore.db'):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    # Connect to the database
    def connect(self):
        """ connection to the SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return True

        # If the database file does not exist, it will be created
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    # Disconnect from the database
    def disconnect(self):
        """Close the connection"""
        if self.connection:
            self.connection.close()

    # Initialize the database with the book table and default data
    # Create the book table and populate it with initial data
    def initialize_database(self):
        """Create the book table and populate it with initial data"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            qty INTEGER NOT NULL
        )
        """
        
        # Initial book data
        initial_books = [
            (3001, "A Tale of Two Cities", "Charles Dickens", 30),
            (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
            (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
            (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
            (3005, "Alice in Wonderland", "Lewis Carroll", 12)
        ]
        
        
        try:
            self.cursor.execute(create_table_sql)
            
            # Check if table is empty before inserting initial data
            self.cursor.execute("SELECT COUNT(*) FROM book")
            count = self.cursor.fetchone()[0]

            # If the table is empty, add the  data
            if count == 0:
                self.cursor.executemany(
                    "INSERT INTO book (id, title, author, qty) VALUES (?, ?, ?, ?)",
                    initial_books
                )
                # Print a message indicating successful initialization
                print("Database created with default books.")

            self.connection.commit()
            return True

        # If an error occurs during initialization
        except sqlite3.Error as e:
            print(f"Failure to initialize database: {e}")
            return False

    # Add a new book to the data
    def add_book(self):
        """Add a new book to the database"""
        print("\n--- Add New Books ---")

        # Get book details from user
        try:
            book_id = int(input("Enter book ID: "))
            # Input validation for title
            while True:
                title = input("Enter the book title: ").strip()
                if title:
                    break
                print("Error: Title cannot be empty. Please enter a title.")
            
            # Input validation for author
            while True:
                author = input("Enter author name: ").strip()
                if author:
                    break
                print("Error: Author name cannot be empty. Please enter an author name.")
                
            qty = int(input("Enter quantity: "))
            
            # Check if ID already exists
            self.cursor.execute("SELECT id FROM book WHERE id = ?", (book_id,))
            if self.cursor.fetchone():
                print("Error: Please note that a book with this ID already exists.")
                return False
                
            # Insert the new book
            self.cursor.execute(
                "INSERT INTO book (id, title, author, qty) VALUES (?, ?, ?, ?)",
                (book_id, title, author, qty)
            )
            self.connection.commit()
            print("Book added successfully!")
            return True
        
        # Handle invalid input    
        except ValueError:
            print("Error: Please enter valid numeric values for ID and quantity.")
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    # Update an existing book's information
    def update_book(self):
        """Update an existing book's information"""
        print("\n-- Update Book --")

        # Get book ID from user
        try:
            book_id = int(input("Enter the ID of the book to update: "))
            
            # Check if book exists
            self.cursor.execute("SELECT * FROM book WHERE id = ?", (book_id,))
            book = self.cursor.fetchone()
            
        
            if not book:
                print("Error: No book found with that ID  .")
                return False
                
            print(f"\nCurrent details for book ID {book_id}:")
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Quantity: {book[3]}")
            
            # Get updated information
            print("\nEnter new details (press Enter to keep current value):")
            
            # Input validation for title
            while True:
                new_title = input(f"New title [{book[1]}]: ").strip()
                if not new_title:  # If user pressed Enter
                    new_title = book[1]
                    break
                if new_title:  # If user entered something
                    break
                print("Error: Title cannot be empty. Please enter a title or press Enter to keep current.")
            
            # Input validation for author
            while True:
                new_author = input(f"New author [{book[2]}]: ").strip()
                if not new_author:  # If user pressed Enter
                    new_author = book[2]
                    break
                if new_author:  # If user entered something
                    break
                print("Error: Author name cannot be empty. Please enter an author name or press Enter to keep current.")
            
            new_qty_input = input(f"New quantity [{book[3]}]: ")
            new_qty = int(new_qty_input) if new_qty_input else book[3]
            
            # Update the book
            self.cursor.execute(
                "UPDATE book SET title = ?, author = ?, qty = ? WHERE id = ?",
                (new_title, new_author, new_qty, book_id)
            )
            # If the update is successful
            self.connection.commit()
            print("Book updated successfully!")
            return True

        # Handle invalid input
        except ValueError:
            print("Error: Please enter a valid numeric value for quantity.")
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    # Delete a book from the database
    def delete_book(self):
        """Delete a book from the database"""
        print("\n--- Delete Book ---")
        
        try:
            book_id = int(input("Enter the ID of the book to delete: "))
            
            # Check if book exists
            self.cursor.execute("SELECT title, author FROM book WHERE id = ?", (book_id,))
            book = self.cursor.fetchone()
            
            if not book:
                print("Error: No book found with that ID.")
                return False
                
            # Enhanced "Are you sure?" prompt
            confirm = input(f"Are you sure you want to delete '{book[0]}' by {book[1]}? This cannot be undone. (y/n): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return False
                
            # Delete the book
            self.cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
            self.connection.commit()
            print("Book deleted successfully!")
            return True
            
        except ValueError:
            print("Error: Please enter a valid numeric value for book ID.")
            return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    # Search for books with advanced filters
    def search_books(self):
        """Search for books with advanced filters"""
        print("\n--- Search Books ---")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by Title or Author")
        print("4. Search by ID")
        print("5. Search by Quantity Range")
        print("6. Search for Low Stock (Qty < 5)")
        
        try:

            # Get search option from user
            search_option = input("\nSelect search option (1-6): ").strip()
            
            if search_option == '1':
                search_term = input("Enter title to search for: ").strip()
                if not search_term:
                    print("Please enter a search term.")
                    return False
                self.cursor.execute(
                    "SELECT * FROM book WHERE title LIKE ?",
                    (f'%{search_term}%',)
                )
                
            elif search_option == '2':
                search_term = input("Enter author to search for: ").strip()
                if not search_term:
                    print("Please enter a search term.")
                    return False
                self.cursor.execute(
                    "SELECT * FROM book WHERE author LIKE ?",
                    (f'%{search_term}%',)
                )
                
            elif search_option == '3':
                search_term = input("Enter title or author to search for: ").strip()
                if not search_term:
                    print("Please enter a search term.")
                    return False
                self.cursor.execute(
                    "SELECT * FROM book WHERE title LIKE ? OR author LIKE ?",
                    (f'%{search_term}%', f'%{search_term}%')
                )
                
            elif search_option == '4':
                # Search by ID
                try:
                    search_id = int(input("Enter book ID to search for: "))
                    self.cursor.execute(
                        "SELECT * FROM book WHERE id = ?",
                        (search_id,)
                    )
                except ValueError:
                    print("Error: Please enter a valid numeric ID.")
                    return False
                
            elif search_option == '5':
                # Search by Quantity Range
                try:
                    min_qty = int(input("Enter minimum quantity: "))
                    max_qty = int(input("Enter maximum quantity: "))
                    self.cursor.execute(
                        "SELECT * FROM book WHERE qty BETWEEN ? AND ? ORDER BY qty ASC",
                        (min_qty, max_qty)
                    )
                except ValueError:
                    print("Error: Please enter valid numeric values for quantity range.")
                    return False
                
            elif search_option == '6':
                # Search for low stock (quantity less than 5)
                self.cursor.execute(
                    "SELECT * FROM book WHERE qty < 5 ORDER BY qty ASC"
                )
                print("Searching for low stock items (qty < 5)...")
                
            else:
                print("Invalid search option.")
                return False
                
            results = self.cursor.fetchall()
            
            if not results:
                print("No books found matching your search.")
                return False
                
            print(f"\nFound {len(results)} matching book(s):")
            print("-" * 70)
            print(f"{'ID':<6} {'Title':<35} {'Author':<20} {'Qty':<5}")
            print("-" * 70)

            # Display search results
            for book in results:
                # Truncate long titles for better display
                title = book[1] if len(book[1]) <= 35 else book[1][:32] + "..."
                # Add low stock warning for items with quantity less than 5
                qty_display = f"{book[3]} ***" if book[3] < 5 else f"{book[3]}"
                print(f"{book[0]:<6} {title:<35} {book[2]:<20} {qty_display:<5}")
                
            return True
            
        except sqlite3.Error as e:
            print(f"Database error during search: {e}")
            return False
            
    def display_all_books(self):
        """Display all books in the database with low stock alerts"""
        try:
            self.cursor.execute("SELECT * FROM book ORDER BY id")
            books = self.cursor.fetchall()
            
            if not books:
                print("No books in the database.")
                return False
                
            print(f"\n{'All Books in Database':^70}")
            print("-" * 70)
            print(f"{'ID':<6} {'Title':<35} {'Author':<20} {'Qty':<5}")
            print("-" * 70)

            # Count low stock items
            low_stock_count = 0
            for book in books:

                # Truncate long titles for better display
                title = book[1] if len(book[1]) <= 35 else book[1][:32] + "..."

                # Add low stock warning for items with quantity less than 5
                qty_display = f"{book[3]} ***" if book[3] < 5 else f"{book[3]}"
                if book[3] < 5:
                    low_stock_count += 1
                print(f"{book[0]:<6} {title:<35} {book[2]:<20} {qty_display:<5}")
            
            # Display low stock summary
            if low_stock_count > 0:
                print("\n*** LOW STOCK ALERT ***")
                print(f"There are {low_stock_count} book(s) with less than 5 copies in stock.")
                print("Please consider restocking these items soon.")
                
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

def display_menu():
    """Display the main menu options"""
    print("\n" + "=" * 42)
    print("       TSHWANELO'S BOOKSTORE  MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. Display all books")
    print("0. Exit")
    print("=" * 50)

def main():
    """Main function to run the bookstore application"""
    print("Initializing Bookstore Database System...")
    
    # Create database instance
    bookstore = BookstoreDB()
    
    # Connect to database
    if not bookstore.connect():
        print("Failed to connect to database. Exiting.")
        return
        
    # Initialize database with tables and default data
    if not bookstore.initialize_database():
        print("Failed to initialize database. Exiting.")
        bookstore.disconnect()
        return
        
    # Main program loop
    while True:
        display_menu()
        choice = input("Please enter your choice (0-5): ").strip()
        
        if choice == '0':
            # Add exit confirmation
            confirm = input("Are you sure you want to exit? (y/n): ")
            if confirm.lower() == 'y':
                print("Thank you for using the Bookstore Database System. Goodbye!")
                break
            else:
                print("Returning to main menu...")
                continue
            
        elif choice == '1':
            bookstore.add_book()
            
        elif choice == '2':
            bookstore.update_book()
            
        elif choice == '3':
            bookstore.delete_book()
            
        elif choice == '4':
            bookstore.search_books()
            
        elif choice == '5':
            bookstore.display_all_books()
            
        else:
            print("Wrong choice. Please enter a number between 0 and 5.")


        # Wait for user input before continuing
        input("\nPress Enter to continue...")
    
    # Clean up
    bookstore.disconnect()

if __name__ == "__main__":
    main()