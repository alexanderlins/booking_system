"""	
	Initial template design and basic menu layout - frst1301 
"""
"""
	Added functionality(actually working) of: adding reservation, removal of and search op.
	
	Converted menu functionality of earlier "intermediary" functions to actual methods of action when making a
		selection in the menu and commented out the previous implementation of selection-definitions.
"""
import os
import platform

from datetime import datetime

rooms = []	# array to hold rooms available during runtime
reservations = []	# array to store reservations during runtime

class Reservation:
	def __init__(self, room, usr_id, res_id, start_time, end_time):
		self.room = room
		self.usr_id = usr_id
		self.res_id = res_id
		self.start_time = start_time
		self.end_time = end_time

	def __repr__(self): # for debugging purposes - prints string of object
			return(f"Reservation(usr_id='{self.usr_id}', res_id='{self.res_id}', room={self.room}, "
		  		   f"start_time='{self.start_time}', end_time='{self.end_time}')")

class Room:
	def __init__(self, room_id, room_name, is_reservable=True):
		self.room_id = room_id
		self.room_name = room_name
		self.is_reservable = is_reservable

	def __repr__(self):
		return f"Room(room_id='{self.room_id}', room_name='{self.room_name}', is_reservable={self.is_reservable})"

# clear/update terminal window during menu-nav
def clear_terminal():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

# display main menu in terminal window
def display_main_menu():
	clear_terminal()
	print("Reservation system v.1.0.1")
	print("**|| Main Menu ||**")
	print("1. Make Reservation")
	print("2. Change Reservation")
	print("3. Print Reservation(s)")
	print("4. Search")
	print("5. Remove Reservation")
	print("6. Store to file")
	print("7. Exit")

# 
def handle_main_menu_selection(selection):
	if selection == "1":
		handle_option_1()
	elif selection == "2":
		handle_option_2()
	elif selection == "3":
		handle_option_3()
	elif selection == "4":
		handle_option_4()
	elif selection == "5":
		handle_option_5()
	elif selection == "6":
		handle_option_6()
	elif selection == "7":
		print("Exiting the program. Goodbye!")
		exit()
	else:
		input("Invalid selection. Please try again by pressing Enter")

def handle_option_1():
	clear_terminal()
	print("Make Reservation")

	cnf = input("Do you want to proceed making a reservation?(y/n): ")
	if cnf.lower() != 'y':
		print("Aborting reservation. Returning to the main menu.")
		input("Press Enter to return to the main menu.")
		return

	print("Available Rooms:")
	for room in rooms:
		if room.is_reservable:
			print(f"Room ID: {room.room_id}, Room Name: {room.room_name}")
		
	room_id = input("Enter Room ID: ")
	usr_id = input("Enter User ID: ")
	res_id = input("Enter Reservation ID: ")

	while True:
		try:
			start_time = input("Enter Start Time (YYYY-MM-DD HH:MM): ")
			start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
			break
		except ValueError:
			print("Invalid format for start time.")

	while True:
		try:
			end_time = input("Enter End Time (YYYY-MM-DD HH:MM): ")
			end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
			break
		except ValueError:
			print("Invalid format for end time.")

	add_reservation(res_id, usr_id, room_id, start_time, end_time)
	input("Press Enter to return to the main menu.")
	#display_sub_menu_1()

def handle_option_2():
	clear_terminal()
	print("Change Reservation")
	#display_sub_menu_2()

def handle_option_3():
	clear_terminal()
	print("Print Reservation(s)")
	#display_sub_menu_3()

def handle_option_4():
	clear_terminal()
	print("Search")

	reservations.sort(key=lambda x: x.res_id)
	search_id = input("Enter Reservation ID to search: ")

	found_res = search_reservation(search_id)
	if found_res:
		print(f"Reservation found: {found_res}")
	else:
		print("Reservation not found")

	input("Press Enter to return to the main menu.")
	#display_sub_menu_4()

def handle_option_5():
	clear_terminal()
	print("Remove Reservation")

	if not reservations:
		print("No reservations to be removed.")
		input("Press Enter to return to main menu.")
		return
	
	print("Removable Reservations:")
	for res in reservations:
		print(f"Reservation ID: {res.res_id}, User ID: {res.usr_id}, Room ID: {res.room.room_id}, Start Time: {res.start_time}, End Time: {res.end_time}")


	s_id = input("Enter Reservation ID to be removed: ")

	remove_reservation(s_id)
	input("Press Enter to return to the main menu.")
	#display_sub_menu_5()

def handle_option_6():
	clear_terminal()
	print("Store to file")
	#display_sub_menu_6()
"""
def display_sub_menu_1():
	#clear_terminal()
	#print("Make/Change Reservations")
	# add logic to this menu-selection here!
	ro = Room("01", "Room01", True)	# debug instance of room-obj
	r = Reservation(ro, "frst", "001", 1000, 1350) # debug instance of reservation-obj
	print(r)	# printing __repr__ string of r, ro respectively (ro) is actually a chained print invokation?
	input("Press Enter to return to the main menu.")

def display_sub_menu_2():
	#clear_terminal()
	#print("Print Reservations")
	input("Press Enter to return to the main menu.")

def display_sub_menu_3():
	#clear_terminal()
	#print("Search")
	input("Press Enter to return to the main menu.")

def display_sub_menu_4():
	#clear_terminal()
	#print("Remove")
	input("Press Enter to return to the main menu.")

def display_sub_menu_5():
	#clear_terminal()
	#print("")
	input("Press Enter to return to the main menu.")

def display_sub_menu_6():
	input("Press Enter to return to the main menu.")
"""
def add_reservation(res_id, usr_id, room_id, start_time, end_time):
	# TODO: implement logic for adding a reservation

	# Pseudo: perform CHECK/COMPARISON of stored reservations-
	#		  attributes with parameters entered with call to function-
	#		  IF conflict exsists -> return otherwise CREATE-
	#		  Reservations-object and pass parameters to object initiation-
	#		  and APPEND object to global ARRAY end with PRINT-message-
	#		  using suitable informative content

	# example of how implementation could look like follow below: --
	room = next((r for r in rooms if r.room_id == room_id), None)
	if room and room.is_reservable:
		for reservation in reservations:
			if reservation.room.room_id == room_id and not (end_time <= reservation.start_time or start_time >= reservation.end_time):
				print("Error: Room/Object is already reserved for the specified time interval")
				return
			
		tmp_res = Reservation(room, usr_id, res_id, start_time, end_time)
		reservations.append(tmp_res)
		room.is_reservable = False
		print(f"Reservation succesfully made: {tmp_res}")
	else:
		print(f"Error: Room is not available or is not present in the system")

def search_reservation(target_res_id):

	#sorted_res = sorted(reservations, key=lambda x: x.res_id)
	left, right = 0, len(reservations) - 1

	while left <= right:
		mid = (left + right) // 2
		if reservations[mid].res_id == target_res_id:
			return reservations[mid]
		elif reservations[mid].res_id < target_res_id:
			left = mid + 1
		else:
			right = mid - 1
	return None

def remove_reservation(res_id):
	# TODO: implement logic for removing a reservation
	res = next((r for r in reservations if r.res_id == res_id), None)
	if res:
		reservations.remove(res)
		res.room.is_reservable = True
		print(f"Reservation successfully removed: {res}")
	else:
		print(f"Error: Reservation not found.")

def print_reservations():
	# TODO: implement logic for printing reservations
	pass

def store_to_file():
	# TODO: implement logic for store-to-file functionality
	pass

def main():
	# TODO: create dummy room/reservable-objects and push to designated array..
	r1 = Room("R001", "Room1", True)
	r2 = Room("R002", "Room2", True)
	r3 = Room("R003", "Room3", True)
	r4 = Room("R004", "Room4", True)
	r5 = Room("S006", "Storage6", True)
	rooms.append(r1)
	rooms.append(r2)
	rooms.append(r3)
	rooms.append(r4)
	rooms.append(r5)


	while True:
		display_main_menu()
		selection = input("Please enter your selection: ")
		handle_main_menu_selection(selection)

if __name__ == "__main__":
	main()