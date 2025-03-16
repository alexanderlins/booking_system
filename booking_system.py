import os
import platform
import getpass
import hashlib
import json
import datetime
import database as db
import textwrap

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

	def __repr__(self): # for debugging purposes - prints string of object
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
		#print(f"Room added: {new_room}")	# print-out of rooms added Uncomment for debug purposes
		
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
			print(f"Error: {room_id} is not available or is not present in the system")

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
		self.__reservations = list((res for res in self.__reservations if res.end_time > current_time))

	def list_rooms(self):
		for room in self.__rooms:
			print(f"Room ID: {room.room_id}, Room Name: {room.room_name}")

	def list_reservations(self):
		for reservation in self.__reservations:
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
	print("2. Display Reservations")
	print("3. Display 7-day Schedule (Terminal-size may break structure.)")
	print("4. Search")
	print("5. Remove Reservation")
	print("X. Exit")

# Main Menu
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
		handle_option_5(handler)
	elif selection.lower() == "x":
		print("Saving session state...")
		save_reservation_to_json(handler)		
		print("Exiting the program. Goodbye!")
		exit()
	else:
		input("Invalid selection. Please try again by pressing Enter")

# Make Reservation
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
			now = datetime.datetime.now()
			if start_date < now.replace(hour=0, minute=0, second=0, microsecond=0):
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
			duration_hours = int(input("How many hours do you wish to reserve the room for? Maximum is 4: "))
			if not (0 < duration_hours <= 4):
				raise ValueError("You can only book for a maximum of 4 hours")
			end_datetime = start_datetime + datetime.timedelta(hours=duration_hours)
			break
		except ValueError:
			print("Invalid format for duration. Please enter a number between 1 to 4.")

	# Check for conflicting reservations in other rooms by user
		for reservation in handler.get_reservations():
			# Skip current room. It's handled in add_reservation
			if room_id == reservation.room.room_id:
				continue
			# Skip other user's reservations
			if handler.get_user_id() != reservation.usr_id:
				continue

			# Check for conflicting reservations in other rooms
			if not (end_datetime <= reservation.start_time or start_datetime >= reservation.end_time):
				print(f"You have already reserved {reservation.room.room_id} during this time. Please select a different time or remove your other reservation")
				input("Press Enter to return ")
				return
	
	handler.add_reservation(res_id, room_id, handler.get_user_id(), start_datetime, end_datetime)
	input("Press Enter to return to the main menu.")

# Display Reservations
def handle_option_2(handler):
    clear_terminal()
    print("If you want to see ALL rooms, press enter.")
    selected_room = choose_room(handler)
    try:
        if selected_room is None: # User gave faulty input.
            pass
        elif not selected_room: # User gave empty string input.
            # Sort the reservations by time first, then by room-ID
            handler.sort_reservations("end_time")
            handler.sort_reservations("room_id")
            
            list_or_table = input("\nWould you like to see it in a table format? (Press enter for 'Yes', input any character for list format.)\n").lower()
            clear_terminal()
            if not list_or_table:
                print_reservations_table(handler)
            else:
                print_reservations_list(handler)
                print("The above shows all future reservations.")
        else: # User gave correct input.
            # Sort the reservations by time.
            handler.sort_reservations("end_time")
            
            list_or_table = input("\nWould you like to see it in a table format? (Press enter for 'Yes', input any character for list format.)\n").lower()
            clear_terminal()
            print(f"Below are all the reservations for: {selected_room.room_name} ({selected_room.room_id})")
            if not list_or_table: #If no input, assume they wanted table.
                print_reservations_table(handler, selected_room.room_id)
            else:
                print_reservations_list(handler, selected_room.room_id)
                print(f"The above are the reservations for: {selected_room.room_name} ({selected_room.room_id})")
    except Exception as e:
        print(f"An error occurred while printing room schedule: {e}")
    input("\nPress Enter to return to the main menu.")

# Display 7-day Schedule
def handle_option_3(handler):
    selected_room = choose_room(handler)
    try:
        if selected_room: #If there's content, i.e., not None nor empty!
            print(f"Below is the 7-day schedule for: {selected_room.room_name} ({selected_room.room_id})")
            print_schedule_table_with_reservations(handler, selected_room.room_id)
            print("The schedule is split into Early Morning, Morning, Afternoon, and Evening for terminal-formatting purposes.")
            print(f"Above is the 7-day schedule for: {selected_room.room_name} ({selected_room.room_id})")
        else:
            input("The Schedule-viewing functionality is room-specific and limited to 7 days, otherwise it'd be too spammy!\nPlease try again.\n")

    except Exception as e:
        print(f"An error occurred while printing room schedule: {e}")
    
    input("\nPress Enter to return to the main menu.")


# Search
def handle_option_4(handler):
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

# Remove Reservation
def handle_option_5(handler):
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

def choose_room(handler):
    # List all rooms
    handler.list_rooms()
    
    # Ask the user which room schedule they want to see
    room_filter = input("Which room would you like to see?\n").lower()
    
    if not room_filter:
        # Just pressing enter could've been by mistake, but let's treat it like a choice! >:D)-<
        return "" 

    # Check for matching rooms
    for selected_room in handler.get_rooms():
        if (selected_room.room_id.lower() == room_filter) or \
           (selected_room.room_name.lower() == room_filter):
            return selected_room # If user has selected a valid room, return the room.         

    # Handle case where no match is found
    print("No matching room found. Please check the room ID or name and try again.")
    return None



def print_reservations_list(handler, room_filter=None):
    # Ensure there are reservations in the list
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
            print(f"  - Reservation ID: {reservation.res_id}")
            print(f"  - User ID: {reservation.usr_id}")
            print(f"  - Start Time: {reservation.start_time}")
            print(f"  - End Time: {reservation.end_time}")
            print("-" * 40)  # Separator line

    if not found:
        print("No reservations match the given filter.")
    else:
        print("\n=== Reservations List End ===\n")


def save_reservation_to_json(handler):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reservation_file_path = os.path.join(script_dir, 'reservations.json')
    
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reservation_file_path = os.path.join(script_dir, 'reservations.json')
    
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
            if end_time.date() >= datetime.datetime.now().date(): ### NEW! Edited to only care about today's date and not time.
                handler.add_reservation(res["res_id"], res["room"]["room_id"], res["usr_id"], start_time, end_time)

    except Exception as e:
        print(f"An error occurred while loading reservations: {e}")


def hash_password(pwd, salt):
    return hashlib.sha256((salt + pwd).encode()).hexdigest()


def login(handler):
	print("")
	print(f"Room Reservation System v{__version__}")
	print("1. Login")
	print("2. Create new user")
	selection = input("Please enter your selection: ")

	if selection == "1":
		username = input("Enter username: ")
		password = getpass.getpass("Enter password: ")
		if db.login(username, password):
			print(f"Welcome, {username}!")
			handler.set_user_id(username)
		else:
			print("Invalid credentials.")

	elif selection == "2":
		username = input("Choose username: ")
		handler.set_user_id(username)
		password = getpass.getpass("Choose password: ")
		if db.create_new_user(username, password):
			print("User created successfully.")
		else:
			print("User creation failed.")

	else:
		print("Invalid selection.")

def print_schedule_table_with_reservations(handler, room_filter):
    # Function prints the schedule of the next 7 days starting from the current day.

    # Get today's date
    today = datetime.datetime.today()

    # Generate a list of the next 7 dates
    next_7_days = [(today + datetime.timedelta(days=i)) for i in range(7)]

    # List times of day in order
    time_of_day = ["Early Morning", "Morning", "Afternoon", "Evening"]

    # Process reservations to map reservations by date and hour
    reservation_map = {day.strftime("%d-%m-%Y, %A"): [" "] * 24 for day in next_7_days}  # Initialize all slots, replace [" "] if you want the boxes free to say something.
    for reservation in handler.get_reservations():
        if reservation.room.room_id == room_filter:
            # Calculate all days covered by the reservation
            current_time = reservation.start_time
            while current_time <= reservation.end_time:
                reservation_day = current_time.strftime("%d-%m-%Y, %A")
                if reservation_day in reservation_map:  # Only process if the reservation is within these 7 days
                    start_hour = max(reservation.start_time.hour, current_time.hour) if current_time.date() == reservation.start_time.date() else 0
                    end_hour = min(reservation.end_time.hour, 23) if current_time.date() == reservation.end_time.date() else 23
                    for hour in range(start_hour, end_hour):
                        # Mark as reserved with user and reservation details
                        reservation_map[reservation_day][hour] = reservation.usr_id + " (ID: " + reservation.res_id + ")"
                # Move to the next day
                current_time = (current_time + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Generate and print tables for 4 chunks (24 hours total)
    for chunk in range(4):  # 4 chunks (6 hours each)
        current_time_word = time_of_day[chunk]

        # Define headers
        headers = [current_time_word] + [
            f"{(datetime.datetime.strptime('00:00', '%H:%M') + datetime.timedelta(hours=i + chunk * 6)).strftime('%H:%M')}"
            for i in range(6)
        ]

        # Fixed column widths
        fixed_col_widths = [25] + [12] * 6

        def wrap_text(text, width):
            """Wraps text into multiple lines to fit column width."""
            return textwrap.fill(str(text), width=width)

        # Print headers
        print("~" * (sum(fixed_col_widths) + len(fixed_col_widths) * 3 + 1))  # Top border
        print("| " + " | ".join(f"{headers[i]:<{fixed_col_widths[i]}}" for i in range(len(headers))) + " |")
        print("~" * (sum(fixed_col_widths) + len(fixed_col_widths) * 3 + 1))  # Header separator

        # Generate rows with wrapped text
        rows = [[day] + [
            reservation_map[day][i + chunk * 6]
            for i in range(6)
        ] for day in reservation_map.keys()]

        for row in rows:
            wrapped_cells = [wrap_text(str(cell), fixed_col_widths[i]) for i, cell in enumerate(row)]
            # Split wrapped text into lines
            max_lines = max(cell.count("\n") + 1 for cell in wrapped_cells)
            for line_num in range(max_lines):
                print("| " + " | ".join(
                    wrapped_cells[i].split("\n")[line_num].ljust(fixed_col_widths[i])
                    if line_num < len(wrapped_cells[i].split("\n")) else " " * fixed_col_widths[i]
                    for i in range(len(wrapped_cells))
                ) + " |")
            print("-" * (sum(fixed_col_widths) + len(fixed_col_widths) * 3 + 1)) # bottom row border
        # Put bottom border here if you remove bottom row borders, otherwise it'd look odd.


def print_reservations_table(handler, room_filter=None):
    if handler.is_reservations_empty():
        print("No reservations found.")
        return

    if room_filter:
        print(f"\n=== {room_filter}'s Reservations List ===\n")
    else:
        print("\n=== Entire Reservations List ===\n")

    found = False
    
    # Define table headers and rows
    headers = ["Room ID", "Room Name", "User ID", "Reservation ID", "Start Time", "End Time"]
    rows = []
 
    # Add reservations to rows
    for reservation in handler.get_reservations():
        if room_filter is None or reservation.room.room_id == room_filter:
            found = True
            rows += [[
                reservation.room.room_id,
                reservation.room.room_name,
                reservation.usr_id,
                reservation.res_id,
                reservation.start_time.strftime("%Y-%m-%d %H:%M"),
                reservation.end_time.strftime("%Y-%m-%d %H:%M")
            ]]

    # Calculate column widths
    col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *rows)]

    # Print the table
    print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))  # Top border
    print("| " + " | ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers))) + " |")
    print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))  # Header separator
    for row in rows:
        print("| " + " | ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row))) + " |")
    print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))  # Bottom border
 
    if not found:
        print("No reservations match the given filter.")
		


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
