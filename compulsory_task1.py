"""

1. Add another method in the Course class that prints the head office location: Cape Town
2. Create a subclass of the Course class named OOPCourse
3. Create a constructor that initialises the following attributes and assigns these values:
    --- "description" with a value "OOP Fundamentals"
    --- "trainer" with a value "Mr Anon A. Mouse"
4. Create a method in the subclass named "trainer_details" that prints what the 
   course is about and the name of the trainer by using the description and trainer attributes.
5. Create a method in the subclass named "show_course_id" that prints the ID number of the course: #12345
6. Create an object of the subclass called course_1 and call the following methods
   contact_details
   trainer_details
   show_course_id
   These methods should all print out the correct information to the terminal

Note: this task covers single inheritance. Multiple inheritance is also possible in Python and 
we encourage you to do some research on multiple inheritance when you have finished this course.
"""

class Course:
    name = "Fundamentals of Computer Science"
    contact_website = "www.hyperiondev.com"

    def contact_details(self):
        print("Please contact us by visiting", self.contact_website)
    
    # method to print head office location
    def office_location(self):
        print("Head office location: Cape Town")

# Create subclass of Course1
class OOPCourse(Course):
    # Constructor with initialized attributes
    def __init__(self):
        self.description = "OOP Fundamentals"
        self.trainer = "Mr Anon A. Mouse"
    
    # print trainer details
    def trainer_details(self):
        print(f"This course is about: {self.description}")
        print(f"Trainer: {self.trainer}")
    
    # show course ID
    def show_course_id(self):
        print("Course ID: #12345")

# Create object of subclass
course_1 = OOPCourse()

# Call methods
course_1.contact_details()
course_1.trainer_details()
course_1.show_course_id()
course_1.office_location()