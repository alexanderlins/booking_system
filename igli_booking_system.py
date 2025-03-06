import database as db
import getpass
import os
import platform
import hashlib
from datetime import datetime

# clear/update terminal window during menu-nav
def clear_terminal():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")
	
def handle_selections(selection: int):
    if selection == 1:
        print("TODO")
    elif selection == 2:
        print("TODO")
    elif selection == 3:
        print("TODO")
    elif selection == 4:
        db.check_bookings()
    elif selection == 5:
        db.check_customers()
        next = input("Go back? Yes or No: ")
        if next == "Yes" or next == "Y" or next == "YES" or next == "y" or next == "yes":
            display_main_menu()
        else:
            print("Application closes")

    elif selection == 6:
        print("TODO")
    elif selection == 7:
        print("Application closes")

    else:
        print("Invalid selection.")
        display_main_menu()
	
def display_login():
    print("Welcome to Booking System!")
    print("1. Login")
    print("2. Create Account")

    choice = int(input(""))
    
    if choice == 1:
        print("Enter your username and password")
        username = input("Username: ")
        print(f"Ok, the inserted username is: {username}")
        print("Now insert your password")
        password = input("Password: ")
        print("Logging in...")
        return db.login(username, password)
    
    elif choice == 2:
        username = input("Pick a username: ")
        password = input("Pick a password: ")

        db.create_new_user(username, password)
        db.check_specific_customers(username)

# display main menu in terminal window
def display_main_menu():
    clear_terminal()
    print("Reservation system v.1.0.1")
    print("**|| Main Menu ||**")
    print("1. Make Reservation")
    print("2. Change Reservation")
    print("3. Print Reservation(s)")
    print("4. Search")
    print("5. Check User Database")
    print("6. Store to file")
    print("7. Exit")
    choice = int(input(""))
    handle_selections(choice)

if __name__ == "__main__":
    db.initial_setup()
    result = display_login()
    if result:
        display_main_menu()
    else:
        print("Login failed")