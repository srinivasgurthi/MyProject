print("Hello World")
print("Srinivas", "Aparna", "Lakshmi", sep="*", end="\t")
print("Venkat")

# # How to take a User Input
# name = input("Enter your Name")
# print(name)

# print(self, *args, sep=' ', end='\n', file=None)
# *args - multiple number of arguments you can enter
# sep - seperator =  space
# end = How you want to print the after end

# Task 4th Oct 2023:
# 1. Print the Name of the user by taking it from the input command.
# 2. Take first name and last name of user and print with sep. = "-" and end with /t
# 3. Take a user input as name and say with message

# 1. Print the Name of the user by taking it from the input command.
name = input("Enter User name:")
print(name)

# 2. Take first name and last name of user and print with sep. = "-" and end with /t
print("Srinivas", "Aparna", sep="-", end="/t")

# 3. Take a user input as name and say with message
user_name = input("Please enter your name: ")
print(f"Hello, {user_name}! Welcome to my python world!!.")
