# Exercise 1: Personal Information

# Get user's input
name = input("Enter your name: ")
age = int(input("Enter your age: "))
college = input("Enter your college: ")
branch = input("Enter your branch: ")
cgpa = float(input("Enter your CGPA: "))

# Display the information using an f-string
print(f"My name is {name}. I am {age} studying {branch} at {college} with {cgpa} CGPA")