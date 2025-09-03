### --- OOP Email Simulator --- ###

# --- Email Class --- #
class Email:
    # Class variable to track if email has been read
    has_been_read = False

    # Constructor method
    def __init__(self, email_address, subject_line, email_content):
        self.email_address = email_address
        self.subject_line = subject_line
        self.email_content = email_content

    # Method to mark email as read
    def mark_as_read(self):
        self.has_been_read = True

# --- Lists --- #
# Initialize empty list to store email objects
inbox = []

# --- Functions --- #
def populate_inbox():
    # Create 3 sample emails 
    email1 = Email("Thabo@hyperiondev.com", "Welcome to HyperionDev!", "Thank you for joining us.")
    email2 = Email("Marcus@hyperiondev.com", "Great work on the bootcamp!", "You are doing fantastic.")
    email3 = Email("Steven@hyperiondev.com", "Your excellent marks!", "You beat your highest mark of 76%.")
    
    inbox.extend([email1, email2, email3])

def list_emails():
    # subject lines 
    print("\nInbox:")
    for index, email in enumerate(inbox):
        print(f"{index} {email.subject_line}")

def read_email(index):
    # show selected email and mark as read
    if 0 <= index < len(inbox):
        email = inbox[index]
        print(f"\nFrom: {email.email_address}")
        print(f"Subject: {email.subject_line}")
        print(f"Content: {email.email_content}")
        email.mark_as_read()
        print(f"\nEmail from {email.email_address} marked as read.\n")
    else:
        print("Invalid email index.")

# --- Email Program --- #
# add sample emails to inbox
populate_inbox()

# Main loop
while True:
    try:
        user_choice = int(input('''\nWould you like to:
1. Read an email
2. View unread emails
3. Quit application

Enter selection: '''))
           
        if user_choice == 1:
            # all emails
            list_emails()
            try:
                email_index = int(input("\nEnter the number of the email you want to read: "))
                read_email(email_index)
            except ValueError:
                print("Please enter a valid number.")
            
        elif user_choice == 2:
            # View unread emails
            print("\nUnread Emails:")
            unread_count = 0
            for email in inbox:
                if not email.has_been_read:
                    print(f"- {email.subject_line}")
                    unread_count += 1
            if unread_count == 0:
                print("No unread emails.")
                
        elif user_choice == 3:
            # Quit application
            print("Goodbye!")
            break
            
        else:
            print("Incorrect input. Please enter 1, 2, or 3.")
            
    except ValueError:
        print("Please enter a valid number.")