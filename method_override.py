
# Request user input for personal details
user_name = input("Please enter name: ")
user_age = int(input("Please enter age: "))
hair_color = input("Please enter hair color: ")
eye_color = input("Please enter the eye color: ")

# Adult class
class Adult:
    def __init__(self, name, age, hair_color, eye_color):
        self.name = name
        self.age = age
        self.hair_color = hair_color
        self.eye_color = eye_color
    
    def can_drive(self):
        print(f"{self.name} is old enough to drive.")

# Child subclass
class Child(Adult):
    def can_drive(self):
        print(f"{self.name} is too young to drive.")

# determine if user is Adult or Child
if user_age >= 18:
    user = Adult(user_name, user_age, hair_color, eye_color)
else:
    user = Child(user_name, user_age, hair_color, eye_color)


user.can_drive()