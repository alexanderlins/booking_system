"""	
	Initial menu design - frst1301 
"""
import os
import platform

reservations = []	# array to store reservations during runtime

class Reservations:
	def __init__(self, room_id, start_time, end_time):
		self.room_id = room_id
		self.start_time = start_time
		self.end_time = end_time

		def __repr__(self): # for debugging purposes - prints string of object
			return(f"Reservation(room_id='{self.room_id}', "
		  		   f"start_time='{self.start_time}', end_time='{self.end_time}')")

# clear/update terminal window during menu-nav
def clear_terminal():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

# display main menu in terminal window
def display_main_menu():
	clear_terminal()
	print("Main Menu")
	print("1. Make/Change Reservations")
	print("2. Print Reservations")
	print("3. Option 3")
	print("4. Exit")

# 
def handle_main_menu_selection(selection):
	if selection == "1":
		handle_option_1()
	elif selection == "2":
		handle_option_2()
	elif selection == "3":
		handle_option_3()
	elif selection == "4":
		print("Exiting the program. Goodbye!")
		exit()
	else:
		input("Invalid selection. Please try again by pressing Enter")

def handle_option_1():
	print("Make/Change Reservations")
	display_sub_menu_1()

def handle_option_2():
	print("Print Reservations")
	display_sub_menu_2()

def handle_option_3():
	print("You selected Option 3")
	display_sub_menu_3()

def display_sub_menu_1():
	clear_terminal()
	print("Make/Change Reservations")
	# add logic to this menu-selection here!
	input("Press Enter to return to the main menu.")

def display_sub_menu_2():
	clear_terminal()
	print("Print Reservations")
	input("Press Enter to return to the main menu.")

def display_sub_menu_3():
	clear_terminal()
	print("Sub-Menu 3")
	input("Press Enter to return to the main menu.")

def add_reservation(room_name, start_time, end_time):
	# TODO: implement logic for adding a reservation
	pass

def remove_reservation():
	# TODO: implement logic for removing a reservation
	pass

def print_reservations():
	# TODO: implement logic for printing reservations
	pass

def main():
	while True:
		display_main_menu()
		selection = input("Please enter your selection: ")
		handle_main_menu_selection(selection)

if __name__ == "__main__":
	main()