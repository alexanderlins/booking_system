import os
import platform
import getpass
import hashlib
import json
import datetime

__version__ = '1.2'
__desc__ = "A simple implementation of a room-booking system with basic functionality"

script_dir = os.path.dirname(os.path.abspath(__file__))
schedule_file_path = os.path.join(script_dir, 'schedule.json')
reservation_file_path = os.path.join(script_dir, 'reservations.json')


class Reservation:
	def __init__(self, room, usr_id, res_id, start_time, end_time, index):
		self.room = room
		self.usr_id = usr_id
		self.res_id = res_id
		self.start_time = start_time
		self.end_time = end_time
		self.index = index	# value to maintain original index of reservation

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


class ReservationHandler:
	def __init__(self):
		self.__rooms = []
		self.__reservations = []
		self.usr_id = None
		self.index_ctr = 0
	
	def add_room(self, room_id, room_name, is_reservable=True):
		new_room = Room(room_id, room_name, is_reservable)
		self.__rooms.append(new_room)
		print(f"Room added: {new_room}")
		
	def add_reservation(self, res_id, room_id, usr_id, start_time, end_time):
		room = next((r for r in self.__rooms if r.room_id == room_id), None)
		
		if room:
			for reservation in self.__reservations:
				if reservation.room.room_id == room_id and not (end_time <= reservation.start_time or start_time >= reservation.end_time):
					print("Error: Room/Object is already reserved for the specified time interval")
					return
			
			tmp_res = Reservation(room, usr_id, res_id, start_time, end_time, self.index_ctr)
			self.index_ctr += 1
			self.__reservations.append(tmp_res)
			print(f"Reservation succesfully made: {tmp_res}")
		else:
			print(f"Error: Room is not available or is not present in the system")

	def remove_reservation(self, res_id):
		res = next((r for r in self.__reservations if r.res_id == res_id), None)
		if res:
			if self.usr_id == res.usr_id:
				self.__reservations.remove(res)
				save_reservation_to_json(self)
   				# Convert start_time and end_time to datetime objects for comparison
				print(f"\nA reservation under the name \"{res.usr_id}\" for {res.room.room_name} with reservation ID: {res.res_id}")
				print(f"From: {res.start_time}")
				print(f"To: {res.end_time}\nHas successfully been removed.\n")
			else:
				print(f"\nThis reservation was registered under {res.usr_id}, {self.usr_id} may not remove it.")

	def is_reservation_id_unique(self, res_id):
		return not any(res.res_id == res_id for res in self.__reservations)

	def update_reservation(self):
		current_time = datetime.datetime.now()
		__reservations = list((res for res in self.__reservations if res.end_time > current_time))

	def list_rooms(self):
		for room in self.__rooms:
			print(f"Room ID: {room.room_id}, Room Name: {room.room_name}")

	def list_reservations(self):
		for reservation in self.reservations:
			print(f"Reservation ID: {self.__reservation.res_id}, Room ID: {reservation.room.room_id}, "
		 		  f"User ID: {self.__reservation.usr_id}, Start Time: {reservation.start_time}, End Time: {reservation.end_time}")
			
	def get_user_id(self):
		return self.usr_id
	
	def set_user_id(self, username):
		self.usr_id = username

	def get_rooms(self):
		return self.__rooms
	
	def get_reservations(self):
		return self.__reservations

	def sort_reservations(self, key):
		if key == 'res_id':
			self.__reservations.sort(key=lambda x: x.res_id)
		elif key == 'start_time':
			self.__reservations.sort(key=lambda x: x.start_time)
		elif key == 'end_time':
			self.__reservations.sort(key=lambda x: x.end_time)
		elif key == 'room_id':
			self.__reservations.sort(key=lambda x: x.room.room_id)
		elif key == 'usr_id':
			self.__reservations.sort(key=lambda x: x.usr_id)
		elif key == 'index':
			self.__reservations.sort(key=lambda x: x.index)
		else:
			print("Invalid key provided for sorting.")
		print(f"Reservations sorted by {key}.")

	def restore_original_order(self):
		self.sort_reservations('index')

	def is_reservations_empty(self):
		return len(self.__reservations) == 0
	
	def is_rooms_empty(self):
		return len(self.__rooms) == 0
	
	def is_room_present(self, room_id):
		return any(room.room_id == room_id for room in self.__rooms)


# clear/update terminal window during menu-nav
def clear_terminal():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")


# display main menu in terminal window
def display_main_menu():
	clear_terminal()
	print(f"Room Reservation System v{__version__}")
	print("**|| Main Menu ||**")
	print("1. Make Reservation")
	print("2. Print Reservation(s)")
	print("3. Search")
	print("4. Remove Reservation")
	print("5. Exit")


# 
def handle_main_menu_selection(selection, handler):
	if selection == "1":
		handle_option_1(handler)
	elif selection == "2":
		handle_option_2(handler)
	elif selection == "3":
		handle_option_3(handler)
	elif selection == "4":
		handle_option_4(handler)
	elif selection == "5":
		print("Saving session state...")
		save_reservation_to_json(handler)		
		print("Exiting the program. Goodbye!")
		exit()
	else:
		input("Invalid selection. Please try again by pressing Enter")


def handle_option_1(handler):
	clear_terminal()
	print("Make Reservation")	

	print("Available Rooms:")
	handler.list_rooms()
			
	cnf = input("Do you want to proceed making a reservation?(y/n): ")
	if cnf.lower() != 'y':
		print("Aborting reservation. Returning to the main menu.")
		input("Press Enter to return to the main menu.")
		return

	while True:
		room_id = input("Enter Room ID: ")
		if handler.is_room_present(room_id):
			break
		else:
			print("Error: Room does not exist. Please enter a valid Room ID.")
	
	while True:
		res_id = input("Enter Reservation ID: ").strip()
		if res_id and handler.is_reservation_id_unique(res_id):
			break
		else:
			print("Error: Reservation ID already exists or invalid input. Please enter a unique Reservation ID.")

	while True:
		try:
			month_day = input("Enter Start Date (MM-DD): ")
			year = datetime.datetime.now().year
			start_date = datetime.datetime(year, int(month_day[:2]), int(month_day[3:]))
			if start_date < datetime.datetime.now():
				raise ValueError("Date must be today or a future date.")
			break
		except ValueError as e:
			print(f"Invalid input: {e}. Please use 'MM-DD' for date.")

	while True:
		try:
			start_hour = input("Enter Start Time (HH): ")
			start_hour = int(start_hour)
			if not (0 <= start_hour <= 23):
				raise ValueError("Hour must be between 0 and 23.")
			year = datetime.datetime.now().year
			start_datetime = datetime.datetime(year, int(month_day[:2]), int(month_day[3:]), start_hour)
			break
		except ValueError:
			print("Invalid format for start date or time. Please use 'MM-DD' and 'HH'.")

	while True:
		try:
			duration_hours = float(input("How many hours do you wish to reserv the room for? "))
			end_datetime = start_datetime + datetime.timedelta(hours=duration_hours)
			break
		except ValueError:
			print("Invalid format for duration. Please enter a number.")

	handler.add_reservation(res_id, room_id, handler.get_user_id(), start_datetime, end_datetime)
	input("Press Enter to return to the main menu.")


def handle_option_2(handler):
	clear_terminal()
	print("Print Reservation(s)")
	print_room_reservations(handler)
	input("Press Enter to return to the main menu.")


def handle_option_3(handler):
	clear_terminal()
	print("Search")
	id = input("Enter Reservation ID to search: ")

	found_res = search_reservation(handler, id)
	if found_res:
		print(f"  - Reservation ID: {found_res.res_id}")
		print(f"  - User ID: {found_res.usr_id}")
		print(f"  - Room: {found_res.room.room_id}")
		print(f"  - Start Time: {found_res.start_time}")
		print(f"  - End Time: {found_res.end_time}")
	else:
		print("Reservation not found")

	input("Press Enter to return to the main menu.")


def handle_option_4(handler):
	clear_terminal()
	print("Remove Reservation")

	if handler.is_reservations_empty():
		print("No reservations to be removed.")
		input("Press Enter to return to main menu.")
		return
	
	print("Removable Reservations:")
	for res in handler.get_reservations():
		print(f"Reservation ID: {res.res_id}, User ID: {res.usr_id}, Room ID: {res.room.room_id}, Start Time: {res.start_time}, End Time: {res.end_time}")

	cnf = input("Do you want to proceed removing a reservation?(y/n): ")
	if cnf.lower() != 'y':
		print("Aborting removal process. Returning to the main menu.")
		input("Press Enter to return to the main menu.")
		return

	remove_id = input("Enter Reservation ID to be removed: ")

	handler.remove_reservation(remove_id)
	input("Press Enter to return to the main menu.")


def search_reservation(handler, id):
	handler.sort_reservations("res_id")
	left, right = 0, len(handler.get_reservations()) - 1

	while left <= right:
		mid = (left + right) // 2
		if handler.get_reservations()[mid].res_id == id:
			return handler.get_reservations()[mid]
		elif handler.get_reservations()[mid].res_id < id:
			left = mid + 1
		else:
			right = mid - 1
	return None


def print_room_reservations(handler, room_filter=None):
	# Ensure there are reservations in the global list
	if handler.is_reservations_empty():
		print("No reservations found.")
		return

	if room_filter:
		print(f"\n=== {room_filter}'s Reservations List ===\n")
	else:
		print("\n=== Entire Reservations List ===\n")

	found = False

	# Loop through and print each reservation
	for i, reservation in enumerate(handler.get_reservations(), start=1):
		if room_filter is None or reservation.room.room_id == room_filter:
			found = True
			print(f"Reservation {i}:")
			# Ensure the room object is valid
			if isinstance(reservation.room, Room):
				print(f"  - Room Name: {reservation.room.room_name} (ID: {reservation.room.room_id})")
			else:
				print("  - Room: N/A (Invalid Room Data)")
			print(f"  - Reservation ID: {reservation.res_id}") # Not shown? Private key variable for removing reservation?
			print(f"  - User ID: {reservation.usr_id}")
			print(f"  - Start Time: {reservation.start_time}")
			print(f"  - End Time: {reservation.end_time}")
			print("-" * 40)  # Separator line

	if not found:
		print("No reservations match the given filter.")
	else:
		print("\n=== Reservations List End ===\n")


def save_reservation_to_json(handler):
	#Saves by overwriting the old file.
	try:
		# Serialize the reservations list
		reservations_data = [
			{
				"room": {
					"room_id": res.room.room_id,
					"room_name": res.room.room_name,
					"is_reservable": res.room.is_reservable
				},
				"usr_id": res.usr_id,
				"res_id": res.res_id,
				"start_time": res.start_time.strftime('%Y-%m-%d %H:%M'),
				"end_time": res.end_time.strftime('%Y-%m-%d %H:%M')
			} for res in handler.get_reservations()
		]
		# Write to file
		with open(reservation_file_path, "w") as file:
			json.dump({"reservations": reservations_data}, file, indent=4)
		print("Reservations saved successfully.")
	except Exception as e:
		print(f"An error occurred while saving reservations: {e}")


def load_reservations_from_json(handler):
	# Load reservations from json file.
	if not os.path.exists(reservation_file_path) or os.path.getsize(reservation_file_path) == 0:
		return #Return if the file doesn't exist or is empty.
	try:
		with open(reservation_file_path, "r") as file:
			data = json.load(file)
		
		for res in data["reservations"]:
			# Recreate the Room object
			if not handler.is_room_present(res["room"]["room_id"]):
				handler.add_room(res["room"]["room_id"], res["room"]["room_name"])

			start_time = datetime.datetime.strptime(res["start_time"], '%Y-%m-%d %H:%M')
			end_time = datetime.datetime.strptime(res["end_time"], '%Y-%m-%d %H:%M')
			if end_time >= datetime.datetime.now():
				handler.add_reservation(res["res_id"], res["room"]["room_id"], res["usr_id"], start_time, end_time)

	except Exception as e:
		print(f"An error occurred while loading reservations: {e}")


def hash_password(pwd, salt):
    return hashlib.sha256((salt + pwd).encode()).hexdigest()


def login(handler):
	valid_users = {
		"anwa2301": {"salt": "bc998cdbf30b03db581244bf75394dec", "hashed_password": "d72cc55563ba330722af5d880386b7c77336191d7b6b72689da0c9cf58693e32"},
		"frst1301": {"salt": "596360727e1c668231c4fc73791bf7a3", "hashed_password": "942e704242a0c283363459fc13d9e34ad7e8c257ea1eb18ee8c217311782f3f9"},
		"igli2400": {"salt": "c53bc1d98d5bdb7adf52ca1db4790995", "hashed_password": "03dfef70dc27636d8866ae0a49f7347a7ecc30eeeeb439b0c00b86965ceb5ebc"},
		"anov2400": {"salt": "d1ce2657667364d4947c27a45ebfa479", "hashed_password": "4ff4a209abcf96dc7966fc710b237393e760c69c21030e14851614881db6e68d"},
		"a": {"salt": "61ba3e9ba93fc41cbc09b49342725cd1", "hashed_password": "9688bdbed4f151292968e9d7c99e4132af81b7486157fe320c33cce318454dc7"}
    }

	while True:
		username = input("Enter your username: ")
		password = getpass.getpass("Enter your password: ")  # Use getpass to hide the input
		clear_terminal()

		# Check if stored hash = generated hash
		if username in valid_users and valid_users[username]["hashed_password"] == hash_password(password, valid_users[username]["salt"]):
			handler.set_user_id(username)
			print(f"Welcome, {username}!")
			input("Press Enter to continue.")
			break
		else:
			print("Invalid username or password. Please try again.")


def main():

	handler = ReservationHandler()	
	#
	# uncomment below calls to add rooms if json-load file is empty
	handler.add_room("R001", "Room1", True)
	handler.add_room("R002", "Room2", True)
	handler.add_room("R003", "Room3", True)
	handler.add_room("R004", "Room4", True)
	handler.add_room("S006", "Storage6", True)

	login(handler)
	load_reservations_from_json(handler)
	while True:
		handler.update_reservation()
		display_main_menu()
		selection = input("Please enter your selection: ")
		handle_main_menu_selection(selection, handler)


if __name__ == "__main__":
	main()